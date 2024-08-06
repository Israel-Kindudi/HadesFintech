import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Function to detect fair value gaps
def detect_fair_value_gaps(data, threshold=0.02):
    gaps = []
    for i in range(1, len(data)):
        prev_close = data['Close'].iloc[i-1]
        curr_open = data['Open'].iloc[i]
        gap = abs(curr_open - prev_close) / prev_close
        if gap > threshold:
            gaps.append((data.index[i], prev_close, curr_open))
    return gaps

# Function to plot fair value gaps
def plot_fair_value_gaps(data, gaps, ticker):
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Plot candlestick chart
    for idx, row in data.iterrows():
        color = 'green' if row['Close'] >= row['Open'] else 'red'
        ax.plot([idx, idx], [row['Low'], row['High']], color='black')
        ax.plot([idx, idx], [row['Open'], row['Close']], color=color, linewidth=5)
    
    # Highlight fair value gaps
    for gap in gaps:
        ax.axvspan(gap[0] - pd.Timedelta(days=0.5), gap[0] + pd.Timedelta(days=0.5), 
                   ymin=(min(gap[1], gap[2]) - data['Low'].min()) / (data['High'].max() - data['Low'].min()), 
                   ymax=(max(gap[1], gap[2]) - data['Low'].min()) / (data['High'].max() - data['Low'].min()), 
                   facecolor='blue', alpha=0.3)
    
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.title(f'Fair Value Gaps for {ticker}')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.grid()
    plt.show()

# Load the data
data = pd.read_csv('GBPJPY.csv', index_col='Date', parse_dates=True)

# Detect fair value gaps
fvg = detect_fair_value_gaps(data)

# Plot fair value gaps
plot_fair_value_gaps(data, fvg, 'AAPL')
