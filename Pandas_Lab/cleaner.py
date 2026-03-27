import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("Pandas_Lab/Nicholas Liu - student_app_usage.csv")
# print(df.head()) # Default 5 rows

# print(df.shape) # Rows x columns
# print(df.columns) # Column Names
# print(df.info()) # Column Data(values, datatype)
# print(df.isnull().sum()) # Counts missing values.

# print(df.head(10)) # first 10 rows
# print(df.sample(10)) # get random number of rows

print("Before:", df.shape)
df = df.drop_duplicates() # removes duplucates, its a set.
print("After:", df.shape)

text_cols = ["Favorite_App_Category", "AI_Tool_Used", "Club", "Gender"]
num_cols = ["Study_Hours_Per_Week", "Screen_Time_Hours_Per_Day",
            "Assignments_Missed", "Avg_Score", "Commute_Minutes"]

for col in text_cols:
    df[col] = df[col].astype(str).str.strip().str.title() # Consistent Formatting

for col in num_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce") # Convert all words to numerical value.

for col in num_cols:
    # Selects a number(median?) to match bell curve for missing values
    df[col] = df[col].fillna(df[col].median())

for col in text_cols:
# Fills values, show model that data is None
    df[col] = df[col].replace("Nan", "Unknown")
    df[col] = df[col].fillna("Unknown")

# Keeps values that humans call realistic
df = df[(df["Study_Hours_Per_Week"] >= 0) & (df["Study_Hours_Per_Week"] <= 40)]
df = df[(df["Screen_Time_Hours_Per_Day"] >= 0) & (df["Screen_Time_Hours_Per_Day"] <= 16)]
df = df[(df["Assignments_Missed"] >= 0) & (df["Assignments_Missed"] <= 10)]
df = df[(df["Avg_Score"] >= 0) & (df["Avg_Score"] <= 100)]
df = df[(df["Commute_Minutes"] >= 0) & (df["Commute_Minutes"] <= 120)]

# Product
print(df.info())
print(df.isnull().sum())
df.head()

# Part 4
df["App_Category_Code"] = df["Favorite_App_Category"].astype("category").cat.codes

# Feature Engineering
df["Study_to_Screen_Ratio"] = df["Study_Hours_Per_Week"] / df["Screen_Time_Hours_Per_Day"]
# Flagging column(feature)
df["High_Screen_Time"] = df["Screen_Time_Hours_Per_Day"].apply(lambda x: 1 if x >= 6 else 0)
# Scales Values
df["Study_Hours_Scaled"] = (
    (df["Study_Hours_Per_Week"] - df["Study_Hours_Per_Week"].min()) /
    (df["Study_Hours_Per_Week"].max() - df["Study_Hours_Per_Week"].min())
)

# Part 5
# Bar chart
df["Favorite_App_Category"].value_counts().plot(kind="bar")
plt.title("Favorite App Category")
plt.xlabel("Category")
plt.ylabel("Count")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Scatter plot
plt.scatter(df["Screen_Time_Hours_Per_Day"], df["Avg_Score"])
plt.title("Screen Time vs Average Score")
plt.xlabel("Screen Time Hours Per Day")
plt.ylabel("Average Score")
plt.tight_layout()
plt.show()