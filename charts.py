import pandas as pd
import plotly.graph_objects as go

# Function to create a candlestick chart
def create_candlestick_chart(data, ticker):
    fig = go.Figure(data=[go.Candlestick(x=data.index,
                                         open=data['Open'],
                                         high=data['High'],
                                         low=data['Low'],
                                         close=data['Close'])])
    fig.update_layout(title=f'Candlestick Chart for {ticker}',
                      xaxis_title='Date',
                      yaxis_title='Price')
    fig.show()

# Function to add moving averages
def add_moving_averages(data, window=20):
    data[f'SMA_{window}'] = data['Close'].rolling(window=window).mean()
    data[f'EMA_{window}'] = data['Close'].ewm(span=window, adjust=False).mean()

# Function to plot moving averages
def plot_moving_averages(data, ticker):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Close'))
    fig.add_trace(go.Scatter(x=data.index, y=data[f'SMA_{window}'], mode='lines', name=f'SMA {window}'))
    fig.add_trace(go.Scatter(x=data.index, y=data[f'EMA_{window}'], mode='lines', name=f'EMA {window}'))
    fig.update_layout(title=f'Moving Averages for {ticker}', xaxis_title='Date', yaxis_title='Price')
    fig.show()

# Function to add Bollinger Bands
def add_bollinger_bands(data, window=20):
    data['SMA'] = data['Close'].rolling(window=window).mean()
    data['BB_upper'] = data['SMA'] + 2*data['Close'].rolling(window=window).std()
    data['BB_lower'] = data['SMA'] - 2*data['Close'].rolling(window=window).std()

# Function to plot Bollinger Bands
def plot_bollinger_bands(data, ticker):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Close'))
    fig.add_trace(go.Scatter(x=data.index, y=data['SMA'], mode='lines', name='SMA'))
    fig.add_trace(go.Scatter(x=data.index, y=data['BB_upper'], mode='lines', name='Upper Band'))
    fig.add_trace(go.Scatter(x=data.index, y=data['BB_lower'], mode='lines', name='Lower Band'))
    fig.update_layout(title=f'Bollinger Bands for {ticker}', xaxis_title='Date', yaxis_title='Price')
    fig.show()

# Function to add RSI
def add_rsi(data, window=14):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    data['RSI'] = 100 - (100 / (1 + rs))

# Function to plot RSI
def plot_rsi(data, ticker):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data['RSI'], mode='lines', name='RSI'))
    fig.update_layout(title=f'RSI for {ticker}', xaxis_title='Date', yaxis_title='RSI')
    fig.show()

# Load the data
data = pd.read_csv('AAPL_cleaned_data.csv', index_col='Date', parse_dates=True)

# Create candlestick chart
create_candlestick_chart(data, 'AAPL')

# Add and plot moving averages
add_moving_averages(data)
plot_moving_averages(data, 'AAPL')

# Add and plot Bollinger Bands
add_bollinger_bands(data)
plot_bollinger_bands(data, 'AAPL')

# Add and plot RSI
add_rsi(data)
plot_rsi(data, 'AAPL')
