import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import adfuller
import yfinance as yf
import matplotlib.pyplot as plt
from visualizations import plot_results

def calculate_spread(df):
    """
    Calculate the spread between Gold and Silver prices.
    """
    df['Gold_Return'] = df['Price_gold'].pct_change()
    df['Silver_Return'] = df['Price_silver'].pct_change()
    df['Spread'] = df['Gold_Return'] - df['Silver_Return']

    return df


def calculate_zscore(df):
    """
    Calculate the Z-score of the spread using a rolling mean and std dev.
    """
    df['Spread_Mean'] = df['Spread'].rolling(window=30).mean()
    df['Spread_Std'] = df['Spread'].rolling(window=30).std()
    df['Z_Score'] = (df['Spread'] - df['Spread_Mean']) / df['Spread_Std']
    
    return df


def engle_granger_test(df):
    """
    Perform the Engle-Granger test to check for cointegration.
    """
    # Run the Augmented Dickey-Fuller test on the spread
    result = adfuller(df['Spread'].dropna())  # Drop NaN values before testing, "result" is a tuple btw

    # Extract results
    test_statistic = result[0]
    p_value = result[1]
    critical_values = result[4]

    print("Engle-Granger Test (ADF on Spread):")
    print(f"Test Statistic: {test_statistic:.4f}")
    print(f"P-Value: {p_value:.4f}")
    print("Critical Values:")
    for key, value in critical_values.items():
        print(f"   {key}: {value:.4f}")

    # Interpretation
    if p_value < 0.05:
        print("Result: The spread is stationary (cointegrated), indicating a valid pairs trading relationship.")
    else:
        print("Result: The spread is not stationary, indicating the pairs may not be cointegrated.")


def backtest_strategy(df, z_entry=2.25, z_exit=0.15): #z=1.5 is ~93% and z=0.1 is ~50%
    """
    Backtest the mean reversion strategy based on Z-score thresholds.
    """
    # Generate signals based on Z-score
    df.loc[df['Z_Score'] > z_entry, 'Position'] = 1 # Long spread, buy gold sell silver
    df.loc[df['Z_Score'] < -z_entry, 'Position'] = -1 # Short spread, sell gold buy silver
    df.loc[(df['Z_Score'] >= -z_exit) & (df['Z_Score'] <= z_exit), 'Position'] = 0

    # Calculate strategy returns
    df['Strategy_Return'] = df['Position'].shift(1) * df['Spread']
    df['Growth_Factor'] = 1 + df['Strategy_Return']
    df['Cumulative_Growth_Factor'] = df['Growth_Factor'] * df['Growth_Factor'].shift(1)
    df['Cumulative_Return'] = (1 + df['Strategy_Return']).cumprod() - 1

    return df


def calculate_performance_metrics(df):
    """
    Calculate performance metrics for the strategy.
    """
    cumulative_return = df['Cumulative_Return'].iloc[-1]
    days_held = df['Strategy_Return'].count()
    annualized_return = (1 + cumulative_return) ** (252 / days_held) - 1
    annualized_volatility = df['Strategy_Return'].std() * np.sqrt(252)
    max_drawdown = (((1 + df['Strategy_Return']).cumprod() - (1 + df['Strategy_Return']).cumprod().cummax()) /
                (1 + df['Strategy_Return']).cumprod().cummax()).min()

    """
    Get the latest 10-year US Treasury yield (risk free rate) from Yahoo Finance to calculate Sharpe.
    """
    ticker = "^TNX"  # Yahoo Finance ticker for 10-Year Treasury Yield
    data = yf.download(ticker, period="1d", interval="1d")
    # Convert yield from percentage to decimal
    risk_free_rate = (data['Close'] / 100).values[0].item()
    sharpe_ratio = (annualized_return - risk_free_rate) / annualized_volatility

    print("Performance Metrics:")
    print(f"Cumulative Return: {cumulative_return:.4%}")
    print(f"Annualized Return: {annualized_return:.4%}")
    print(f"Annualized Volatility: {annualized_volatility:.2%}")
    print(f"Max Drawdown: {max_drawdown:.2%}")
    print(f"Sharpe Ratio: {sharpe_ratio:.4f}")


if __name__ == "__main__":
    # Load the cleaned and combined data
    df = pd.read_csv("data/processed_data.csv", index_col="Date", parse_dates=True)

    # Calculate spread and Z-score
    df = calculate_spread(df)
    df = calculate_zscore(df)

    # Perform Engle-Granger test on the spread
    engle_granger_test(df)

    # Backtest strategy
    df = backtest_strategy(df, z_entry=2.25, z_exit=0.15)

    # Calculate performance metrics
    calculate_performance_metrics(df)

    # Plot the results
    plot_results(df) #for visualizations.py script, that's where the function is

