import pandas as pd 
import matplotlib.pyplot as plt

df = pd.read_csv("Oh_Yeah_Data_Proposal/dirty_csv.csv")

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

# Removing Duplicate rows
df = df.drop_duplicates()

# Changing inconsistent values
df["genre"] = df["genre"].str.strip().str.title()


# Filling missing values
df["average_user_rating"] = df["average_user_rating"].fillna("Unknown")
df["liked"] = df["liked"].fillna("Unknown")

# Edit Incorrect values
df.loc[df['movie_length_minutes']<30, "movie_length_minutes"] = df["movie_length_minutes"].median()

df.to_csv("Oh_Yeah_Data_Proposal/edited_csv.csv", index=False)

# Graphs

# Genre Count
df["genre"].value_counts().plot(kind="bar")
plt.title("Genre Frequency")
plt.xlabel("Genre")
plt.ylabel("Count")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Average Rating Per Genre
filtered_data = df[df['average_user_rating'] != "Unknown"]
genre_averages = filtered_data.groupby('genre')['average_user_rating'].mean()
genre_averages.plot(kind="bar")
plt.title("Average Rating per Genre")
plt.xlabel('Genre')
plt.ylabel('Average User Rating')
plt.xticks(rotation=45) 
plt.tight_layout()      
plt.show()





# Scatterplot(length of movie vs. rating)
filtered = df[df['average_user_rating'] != "Unknown"]
plt.scatter(filtered["movie_length_minutes"], filtered["average_user_rating"])
plt.title("Movie Length vs. Avg User Rating")
plt.xlabel("Movie Length(minutes)")
plt.ylabel("Average User Rating(1-5)")
plt.tight_layout()
plt.show()