import pandas as pd
import matplotlib.pyplot as plt 

df = pd.read_csv("Datasets_and_Charts/dataset.csv")
print(df.head)

# Bar Chart
df["Category"].value_counts().plot(kind="bar")
plt.title("Count by Category")
plt.xlabel("Category")
plt.ylabel("Count")
plt.show()

# Line Chart
plt.plot(df["Day"], df["Value"])
plt.title("Value Over Time")
plt.xlabel("Day")
plt.ylabel("Value")
plt.show()

# Scatterplot
plt.scatter(df['StudyHours'], df['Score'])
plt.title("Study Hours vs Score")
plt.xlabel("Study Hours")
plt.ylabel("Score")
plt.show()