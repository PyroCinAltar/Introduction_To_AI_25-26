import pandas as pd

data = {
    "Song": ["Song A", "Song B", "Song C", "Song D"],
    "Tempo": [120, 95, 110, 130],
    "Energy": [0.8, 0.6, 0.75, 0.9],
    "Danceability": [0.7, 0.5, 0.6, 0.85],
    "Popularity": [78, 64, 70, 90]
}

df = pd.DataFrame(data)
print(df)
print(df.info())
print(df.head())
print(df.shape)
print(df["Tempo"])
print(df.sort_values(by="Popularity", ascending=False))