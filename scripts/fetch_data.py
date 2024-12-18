import yfinance as yf
import os
import glob
import sys
import datetime

def fetch_stock_data(ticker_a, ticker_b, save_dir="data"):
    print("DEBUG: This is the correct fetch_data.py!")

    # Fetch stocks from Yahoo Finance
    print("Fetching stock data for commodities...")
    print(f"Tickers being used: {ticker_a}, {ticker_b}")

    # Stop script execution if tickers are incorrect
    if ticker_a != "GC=F" or ticker_b != "SI=F":
        print("Error: Incorrect tickers provided!")
        sys.exit(1)  # Stop script immediately

    # Clear existing CSV files
    for file in glob.glob(os.path.join(save_dir, "*.csv")):
        os.remove(file)
        print(f"Deleted old file: {file}")

    # Dynamically calculate the date range for the past 3 years
    end_date = datetime.datetime.today().strftime('%Y-%m-%d')  # Today's date
    start_date = (datetime.datetime.today() - datetime.timedelta(days=3*365)).strftime('%Y-%m-%d')  # Past 3 years

    print(f"Fetching data from {start_date} to {end_date}")

    # Fetch stock data
    stock_a = yf.download(ticker_a, start=start_date, end=end_date)
    print(f"Fetched data for {ticker_a}")

    stock_b = yf.download(ticker_b, start=start_date, end=end_date)
    print(f"Fetched data for {ticker_b}")

    # Check if data was fetched
    print("Gold Data (first 5 rows):")
    print(stock_a.head())
    print("Silver Data (first 5 rows):")
    print(stock_b.head())

    # Save to CSV files
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
        print(f"Created directory: {save_dir}")

    stock_a.to_csv(os.path.join(save_dir, f"{ticker_a.replace('=F', '')}.csv"))
    stock_b.to_csv(os.path.join(save_dir, f"{ticker_b.replace('=F', '')}.csv"))

    print(f"Data saved for {ticker_a} and {ticker_b} in {save_dir}")

if __name__ == "__main__":
    fetch_stock_data("GC=F", "SI=F")
