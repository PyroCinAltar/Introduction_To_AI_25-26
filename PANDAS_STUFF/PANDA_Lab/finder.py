import pandas as pd

# Starter Code
df = pd.read_csv("PANDA_Lab/sample_dataset_big.csv")

# print(df.head())
# print(df.shape)
# print(df.columns)
# print(df.info())
# print(df.isnull().sum())
print(df.describe())