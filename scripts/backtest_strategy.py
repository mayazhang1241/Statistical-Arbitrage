import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def calculate_spread(df, scaling_factor=1):
    """
    Calculate the spread between Gold and Silver prices.
    """
    df['Spread'] = df['Price_gold'] - scaling_factor * df['Price_silver']
    return df

def calculate_zscore(df, window=30):
    """
    Calculate the Z-score of the spread using a rolling mean and std dev.
    """
    df['Spread_Mean'] = df['Spread'].rolling(window=window).mean()
    df['Spread_Std'] = df['Spread'].rolling(window=window).std()
    df['Z_Score'] = (df['Spread'] - df['Spread_Mean']) / df['Spread_Std']
    return df

def backtest_strategy(df, z_entry=2, z_exit=0.5):
    """
    Backtest the mean reversion strategy based on Z-score thresholds.
    """
    df['Position'] = 0  # Initialize position: 1 for Long, -1 for Short
    
    # Generate signals based on Z-score
    df.loc[df['Z_Score'] > z_entry, 'Position'] = -1  # Short spread
    df.loc[df['Z_Score'] < -z_entry, 'Position'] = 1  # Long spread
    df.loc[abs(df['Z_Score']) < z_exit, 'Position'] = 0  # Exit position

    # Calculate strategy returns
    df['Strategy_Return'] = df['Position'].shift(1) * df['Spread'].pct_change()

    return df

def plot_results(df):
    """
    Plot the Spread and Z-Score with signals.
    """
    fig, axes = plt.subplots(2, 1, figsize=(12, 8))

    # Plot the Spread
    axes[0].plot(df.index, df['Spread'], label='Spread', color='blue')
    axes[0].plot(df.index, df['Spread_Mean'], label='Rolling Mean', color='red', linestyle='--')
    axes[0].fill_between(df.index, df['Spread_Mean'] + 2*df['Spread_Std'], 
                         df['Spread_Mean'] - 2*df['Spread_Std'], color='gray', alpha=0.2)
    axes[0].set_title("Spread Between Gold and Silver Prices")
    axes[0].legend()

    # Plot the Z-Score
    axes[1].plot(df.index, df['Z_Score'], label='Z-Score', color='orange')
    axes[1].axhline(2, color='red', linestyle='--', label='Z-Score = 2')
    axes[1].axhline(-2, color='green', linestyle='--', label='Z-Score = -2')
    axes[1].axhline(0, color='black', linestyle='-')
    axes[1].set_title("Z-Score of Spread")
    axes[1].legend()

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Load the cleaned and combined data
    df = pd.read_csv("data/processed_data.csv", index_col="Date", parse_dates=True)

    # Calculate spread and Z-score
    df = calculate_spread(df, scaling_factor=1)
    df = calculate_zscore(df, window=30)

    # Backtest strategy
    df = backtest_strategy(df, z_entry=2, z_exit=0.5)

    # Plot the results
    plot_results(df)
