import pandas as pd

df = pd.read_csv("data\sample_commutes.csv")
print("Raw dtypes:\n", df.dtypes)

# Convert date to datetime
df['date'] = pd.to_datetime(df['date'])

# Quick checks
print("Null counts:\n", df.isnull().sum())
print(df.head())

# Save cleaned
df.to_csv("data/clean_commutes.csv", index=False)
print("Saved cleaned file")