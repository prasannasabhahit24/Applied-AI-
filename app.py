import pandas as pd
import matplotlib.pyplot as plt

# LOAD DATASET
df = pd.read_csv("data/PopulationByAgeSex (1).csv")

# SHOW ORIGINAL DATA
print("Original Dataset:")
print(df.head())

# KEEP ONLY REQUIRED COLUMNS
df = df[
    ["Location", "Time"] +
    [col for col in df.columns if "PopMale" in col or "PopFemale" in col]
]

# GET MALE COLUMNS
male_cols = [col for col in df.columns if "PopMale" in col]

# GET FEMALE COLUMNS
female_cols = [col for col in df.columns if "PopFemale" in col]

# CONVERT MALE DATA TO LONG FORMAT
male_df = df.melt(
    id_vars=["Location", "Time"],
    value_vars=male_cols,
    var_name="Age",
    value_name="Male"
)

# CONVERT FEMALE DATA TO LONG FORMAT
female_df = df.melt(
    id_vars=["Location", "Time"],
    value_vars=female_cols,
    var_name="Age",
    value_name="Female"
)

# CLEAN AGE COLUMN
male_df["Age"] = male_df["Age"].str.replace("PopMale_", "")
female_df["Age"] = female_df["Age"].str.replace("PopFemale_", "")

# MERGE BOTH DATAFRAMES
final_df = pd.merge(
    male_df,
    female_df,
    on=["Location", "Time", "Age"]
)

# RENAME COLUMNS
final_df.rename(columns={
    "Location": "Country",
    "Time": "Year"
}, inplace=True)

# SHOW CLEANED DATA
print("\nCleaned Dataset:")
print(final_df.head())

# SELECT COUNTRY
country_name = "India"

# SELECT YEAR
year = 2020

# FILTER DATA
country_df = final_df[
    (final_df["Country"] == country_name) &
    (final_df["Year"] == year)
]

# SORT AGE GROUPS
country_df = country_df.sort_values("Age")

# MALE VALUES NEGATIVE
male = -country_df["Male"]

# FEMALE VALUES POSITIVE
female = country_df["Female"]

# AGE LABELS
ages = country_df["Age"]

# CREATE FIGURE
plt.figure(figsize=(10, 8))

# PLOT MALE POPULATION
plt.barh(ages, male, label="Male")

# PLOT FEMALE POPULATION
plt.barh(ages, female, label="Female")

# AXIS LABELS
plt.xlabel("Population")

# Y LABEL
plt.ylabel("Age Groups")

# TITLE
plt.title(f"Population Pyramid - {country_name} ({year})")

# LEGEND
plt.legend()

# GRID
plt.grid(axis="x")

# SHOW GRAPH
plt.show()