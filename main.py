import os

def run_cointegration_test():
    """
    Run the Engle-Granger cointegration test script.
    """
    print("Running cointegration test...")
    os.system("python scripts/test_cointegration.py")

def run_backtest():
    """
    Run the mean reversion backtest strategy script.
    """
    print("\nRunning backtest strategy...")
    os.system("python scripts/backtest_strategy.py")

if __name__ == "__main__":
    print("=== Statistical Arbitrage Project ===\n")

    # Step 1: Cointegration Test
    run_cointegration_test()

    # Step 2: Ask if the user wants to proceed with backtesting
    proceed = input("\nProceed to backtest strategy? (yes/no): ").strip().lower()

    if proceed in ["yes", "y"]:
        run_backtest()
    else:
        print("Exiting... You can rerun this later to backtest your strategy.")

