import yfinance as yf
import pandas as pd
import sqlite3
from scipy import stats
# Define the stock ticker and the period for which we want the data
ticker = 'AAPL'
start_date = '2020-01-01'
end_date = '2023-01-01'

# Fetch the data
data = yf.download(ticker, start=start_date, end=end_date)

# Check for missing values
data.fillna(method='ffill', inplace=True)

# Calculate daily returns
data['Daily Return'] = data['Adj Close'].pct_change()

# Save the cleaned data to a CSV file
data.to_csv(f'{ticker}_cleaned_data.csv')

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('financial_data.db')

# Store the cleaned data in a SQL table
data.to_sql(f'{ticker}_data', conn, if_exists='replace', index=True)

# Verify the data has been saved correctly
query = f"SELECT * FROM {ticker}_data LIMIT 5"
result = pd.read_sql(query, conn)
print(result)

# Full Script for Step 2
# Load the cleaned data from the CSV file
data = pd.read_csv('AAPL_cleaned_data.csv', index_col='Date', parse_dates=True)

# Calculate daily returns
data['Daily Return'] = data['Adj Close'].pct_change()

# Save the data with returns to a new CSV file
data.to_csv('AAPL_returns_data.csv')

# Resample data to weekly frequency and calculate the mean for each week
weekly_data = data.resample('W').mean()

# Save the weekly data to a new CSV file
weekly_data.to_csv('AAPL_weekly_data.csv')

# Calculate Z-scores
data['Z-Score'] = stats.zscore(data['Daily Return'].dropna())

# Identify outliers (e.g., Z-score > 3 or < -3)
outliers = data[(data['Z-Score'] > 3) | (data['Z-Score'] < -3)]
print(outliers)

# Remove outliers from the data
clean_data = data[(data['Z-Score'] <= 3) & (data['Z-Score'] >= -3)]

# Drop the Z-Score column as it's no longer needed
clean_data = clean_data.drop(columns=['Z-Score'])

# Save the cleaned data without outliers to a new CSV file
clean_data.to_csv('AAPL_cleaned_no_outliers_data.csv')