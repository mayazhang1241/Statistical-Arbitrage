import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def load_and_clean_data(file_path):
    """
    Load the data from a CSV file, clean it, and return the cleaned dataframe.
    """

    # Skip the first two rows and set the correct column names
    column_names = ["Date", "Price", "Adj Close", "Close", "High", "Low", "Open", "Volume"]
    df = pd.read_csv(
        file_path, 
        skiprows=2, 
        names=column_names, 
        parse_dates=["Date"], 
        date_parser=lambda x: pd.to_datetime(x, format='%Y-%m-%d', errors='coerce')
    )

    df = df.dropna(subset=["Date"])

    print(f"Loaded data from {file_path}")

    # Drop rows where Date or Price are missing
    df = df.dropna(subset=["Date", "Price"])

    # Set Date as the index
    df.set_index("Date", inplace=True)

    # Select only the 'Close' column
    df = df[['Close']].rename(columns={"Close": "Price"})

    print(f"Cleaned data: {len(df)} rows remaining")
    return df

def analyze_data():
    """
    Load, clean, and visualize the gold and silver price data.
    """

    # Load and clean data
    gold_data = load_and_clean_data("data/GC.csv")
    silver_data = load_and_clean_data("data/SI.csv")

    # Combine the two datasets based on Date
    combined_data = gold_data.join(silver_data, how='inner', lsuffix="_gold", rsuffix="_silver")
    print("Combined data:")
    print(combined_data.head())

    # Calculate daily returns for both assets
    combined_data['Gold Returns'] = combined_data['Price_gold'].pct_change()
    combined_data['Silver Returns'] = combined_data['Price_silver'].pct_change()

    # Drop rows with NaN values caused by pct_change()
    combined_data = combined_data.dropna()

    # Save cleaned and processed data to new CSV
    combined_data.to_csv("data/processed_data.csv")
    print("Processed data saved to data/processed_data.csv")

    # Visualize the price trends with a secondary y-axis
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Primary y-axis (Gold Price)
    ax1.plot(combined_data.index, combined_data['Price_gold'], label='Gold Price (GC)', color='tab:blue')
    ax1.set_xlabel("Date")
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))  # Format as Year-Month
    ax1.xaxis.set_major_locator(mdates.MonthLocator(interval=6))  # Show every 6 months
    plt.xticks(rotation=45)  # Rotate dates for better readability

    ax1.set_ylabel("Gold Price", color='tab:blue')
    ax1.tick_params(axis='y', labelcolor='tab:blue')

    # Secondary y-axis (Silver Price)
    ax2 = ax1.twinx()  # Create a secondary y-axis
    ax2.plot(combined_data.index, combined_data['Price_silver'], label='Silver Price (SI)', color='tab:orange')
    ax2.set_ylabel("Silver Price", color='tab:orange')
    ax2.tick_params(axis='y', labelcolor='tab:orange')

    # Title and legend
    fig.suptitle("Gold vs Silver Prices")
    fig.tight_layout()
    plt.show()


if __name__ == "__main__":
    analyze_data()