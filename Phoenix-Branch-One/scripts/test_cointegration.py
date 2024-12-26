from statsmodels.tsa.stattools import coint
import pandas as pd

# Load the processed data
df = pd.read_csv("data/processed_data.csv", index_col="Date", parse_dates=True)

# Extract Gold and Silver prices
gold = df['Price_gold']
silver = df['Price_silver']

# Perform the Engle-Granger cointegration test
score, p_value, critical_values = coint(gold, silver)

# Print results
print("Engle-Granger Cointegration Test:")
print(f"Test Statistic: {score:.4f}")
print(f"P-Value: {p_value:.4f}")
print(f"Critical Values: {critical_values}")

# Interpretation
if p_value < 0.05:
    print("Result: The time series are cointegrated (reject null hypothesis).")
else:
    print("Result: The time series are not cointegrated (fail to reject null hypothesis).")
