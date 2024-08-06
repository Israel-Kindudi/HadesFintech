from flask import Flask, render_template, request, jsonify
import pandas as pd
import backtrader as bt
#from strategies.complex_strategy import ComplexStrategy
import numpy as np
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chart', methods=['POST'])
def chart():
    # Process the request and generate chart data
    data = request.json
    stock_symbol = data['symbol']
    start_date = data['start_date']
    end_date = data['end_date']
    indicators = data['indicators']

    # Load historical data
    df = pd.read_csv(f'data/{stock_symbol}.csv', parse_dates=['Date'])
    df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
    df.set_index('Date', inplace=True)

    # Calculate indicators based on user input
    if 'ma' in indicators:
        df['MA50'] = df['Close'].rolling(window=50).mean()
    if 'ema' in indicators:
        df['EMA50'] = df['Close'].ewm(span=50, adjust=False).mean()
    if 'bb' in indicators:
        df['BB_Middle'] = df['Close'].rolling(window=20).mean()
        df['BB_Upper'] = df['BB_Middle'] + 2 * df['Close'].rolling(window=20).std()
        df['BB_Lower'] = df['BB_Middle'] - 2 * df['Close'].rolling(window=20).std()
    if 'rsi' in indicators:
        df['RSI'] = calculate_rsi(df['Close'], 14)
    # Ensure date is included in the response
    df.reset_index(inplace=True)
    # Replace NaN values with None
    df = df.replace({np.nan: None})
    return jsonify(df.to_dict(orient='records'))

@app.route('/backtest', methods=['POST'])
def backtest():
    # Process the request and run backtest
    data = request.json
    stock_symbol = data['symbol']
    start_date = data['start_date']
    end_date = data['end_date']
    cash = data['cash']

    # Load historical data
    df = pd.read_csv(f'data/{stock_symbol}.csv', parse_dates=['Date'])
    df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
    df.set_index('Date', inplace=True)

    # Run backtest
    cerebro = bt.Cerebro()
    cerebro.addstrategy(ComplexStrategy)

    class PandasData(bt.feeds.PandasData):
        params = (
            ('datetime', None),
            ('Open', -1),
            ('high', -1),
            ('low', -1),
            ('close', -1),
            ('volume', -1),
            ('openinterest', -1),
        )

    data_feed = PandasData(dataname=df)
    cerebro.adddata(data_feed)
    cerebro.broker.set_cash(cash)
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe_ratio')
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
    cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='trade_analyzer')

    results = cerebro.run()
    sharpe_ratio = results[0].analyzers.sharpe_ratio.get_analysis()
    drawdown = results[0].analyzers.drawdown.get_analysis()
    trade_analyzer = results[0].analyzers.trade_analyzer.get_analysis()

    return jsonify({
        'final_value': cerebro.broker.getvalue(),
        'sharpe_ratio': sharpe_ratio,
        'drawdown': drawdown,
        'trade_analyzer': trade_analyzer
    })

def calculate_rsi(data, window):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

if __name__ == '__main__':
    app.run(debug=True)
