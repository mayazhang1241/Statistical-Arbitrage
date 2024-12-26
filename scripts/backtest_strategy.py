import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def calculate_spread(df, scaling_factor=1):
    """
    Calculate the spread between Gold and Silver prices.
    """
    df['Spread'] = df['Price_gold'] - scaling_factor * df['Price_silver']
    print("Inside calculate_spread:")
    print(df.head())
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
    df['Cumulative_Return'] = (1 + df['Strategy_Return']).cumprod() - 1
    return df

def calculate_performance_metrics(df):
    """
    Calculate performance metrics for the strategy.
    """
    cumulative_return = df['Cumulative_Return'].iloc[-1]
    annualized_return = df['Strategy_Return'].mean() * 252
    annualized_volatility = df['Strategy_Return'].std() * np.sqrt(252)
    sharpe_ratio = annualized_return / annualized_volatility
    max_drawdown = (df['Cumulative_Return'].cummax() - df['Cumulative_Return']).max()

    print("Performance Metrics:")
    print(f"Cumulative Return: {cumulative_return:.2%}")
    print(f"Annualized Return: {annualized_return:.2%}")
    print(f"Annualized Volatility: {annualized_volatility:.2%}")
    print(f"Sharpe Ratio: {sharpe_ratio:.2f}")
    print(f"Max Drawdown: {max_drawdown:.2%}")

'''
def plot_results(df):
    """
    Plot the Spread and Z-Score with signals.
    """
    fig, axes = plt.subplots(3, 1, figsize=(12, 10))  # 3 rows, 1 column

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

    # Plot Cumulative Returns
    if 'Cumulative_Return' in df.columns:
        axes[2].plot(df.index, df['Cumulative_Return'], label='Cumulative Return', color='purple')
    else:
        print("Warning: 'Cumulative_Return' column is missing.")

    axes[2].plot(df.index, df['Cumulative_Return'], label='Cumulative Return', color='purple')
    axes[2].set_title("Cumulative Returns of Mean Reversion Strategy")
    axes[2].legend()

    plt.tight_layout()
    plt.show()
'''

if __name__ == "__main__":
    # Load the cleaned and combined data
    df = pd.read_csv("data/processed_data.csv", index_col="Date", parse_dates=True)

    # Calculate spread and Z-score
    df = calculate_spread(df, scaling_factor=1)
    df = calculate_zscore(df, window=30)

    # Backtest strategy
    df = backtest_strategy(df, z_entry=2, z_exit=0.5)

    # Calculate performance metrics
    calculate_performance_metrics(df)

'''
    # Plot the results
    plot_results(df)
'''

