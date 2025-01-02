import matplotlib.pyplot as plt


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
    axes[1].plot(df.index, df['Z_Score'], label='Spread', color='orange')
    axes[1].axhline(1.7, color='red', linestyle='--', label='Z-Score = 1.70')
    axes[1].axhline(-1.7, color='red', linestyle='--', label='Z-Score = -1.70')
    axes[1].axhline(0.04, color='green', linestyle='--', label='Z-Score = 0.04')
    axes[1].axhline(-0.04, color='green', linestyle='--', label='Z-Score = -0.04')
    axes[1].axhline(0, color='black', linestyle='-')
    axes[1].set_title("Z-Score of Spread")
    axes[1].legend()

    # Plot Cumulative Returns
    axes[2].plot(df.index, df['Cumulative_Return'], label='Cumulative Return', color='purple')
    axes[2].set_title("Cumulative Returns of Mean Reversion Strategy")
    axes[2].legend()

    plt.tight_layout()
    plt.show()
