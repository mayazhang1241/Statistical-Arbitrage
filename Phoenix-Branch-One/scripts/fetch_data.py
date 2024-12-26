import yfinance as yf
import os
import glob
import sys
import datetime

def fetch_stock_data(gold_ticker, silver_ticker, save_dir="data"):
    print("DEBUG: This is the correct fetch_data.py!")

    # Fetch stocks from Yahoo Finance
    print(f"Fetching stock data for {gold_ticker} and {silver_ticker}")

    # Stop script execution if tickers are incorrect
    if gold_ticker != "GC=F" or silver_ticker != "SI=F":
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
    gold_stock = yf.download(gold_ticker, start=start_date, end=end_date)
    print(f"Fetched data for {gold_ticker}")

    silver_stock = yf.download(silver_ticker, start=start_date, end=end_date)
    print(f"Fetched data for {silver_ticker}")

    # Check if data was fetched
    print("Gold Data (first 5 rows):")
    print(gold_stock.head())
    print("Silver Data (first 5 rows):")
    print(silver_stock.head())

    # Save to CSV files
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
        print(f"Created directory: {save_dir}")

    gold_stock.to_csv(os.path.join(save_dir, f"{gold_ticker.replace('=F', '')}.csv"))
    silver_stock.to_csv(os.path.join(save_dir, f"{silver_ticker.replace('=F', '')}.csv"))

    print(f"Data saved for {gold_ticker} and {silver_ticker} in {save_dir}")

if __name__ == "__main__":
    fetch_stock_data("GC=F", "SI=F")

