import pandas as pd

df = pd.read_csv('Cleaning with PANDAs/messy_ai_student_survey.csv')
# print(df)
# Drop Duplicates
df = df.drop_duplicates()
# Fills missing age
df["Age"] = df["Age"].fillna(df["Age"].median())
# Formats Favorite_AI_Topic
df["Favorite_AI_Topic"] = df["Favorite_AI_Topic"].str.strip().str.title()
# Reformats State
us_states = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR",
    "California": "CA", "Colorado": "CO", "Connecticut": "CT",
    "Delaware": "DE", "Florida": "FL", "Georgia": "GA",
    "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL", "Indiana": "IN",
    "Iowa": "IA", "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA",
    "Maine": "ME", "Maryland": "MD", "Massachusetts": "MA",
    "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS",
    "Missouri": "MO", "Montana": "MT", "Nebraska": "NE",
    "Nevada": "NV", "New Hampshire": "NH", "New Jersey": "NJ",
    "New Mexico": "NM", "New York": "NY", "North Carolina": "NC",
    "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK",
    "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI",
    "South Carolina": "SC", "South Dakota": "SD", "Tennessee": "TN",
    "Texas": "TX", "Utah": "UT", "Vermont": "VT", "Virginia": "VA",
    "Washington": "WA", "West Virginia": "WV", "Wisconsin": "WI",
    "Wyoming": "WY"
}

df["State"] = df["State"].str.strip().str.title().replace(us_states)


# Reformat grade(get only number, optional)
df["Grade"] = df["Grade"].str.extract('(\d+)')
df["Grade"] = pd.to_numeric(df["Grade"], errors='coerce')
# Removes the incorret records.
df = df[df["Age"] <= 100]

print(df)