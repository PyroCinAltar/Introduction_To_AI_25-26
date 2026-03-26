import pandas as pd

df = pd.read_csv("PANDAS/sample_dataset.csv")

print(df.head())
print()
print()
print(df.shape)
print()
print()
print(df.columns)
print()
print()
print(df.info())
print()
print()
print(df.isnull().sum())

# Questions
'''
Missing data points:
S005 Internet_Access_Home
S008 Final_Project_Score
S011 Study_Hours_Per_Week
S019 Homework_Completion_Rate
S025 Quiz_Average
S028 Final_Course_Result
'''