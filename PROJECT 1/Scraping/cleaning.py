import pandas as pd

# Load the IMDb CSV file
df = pd.read_csv("merged_movies3.csv")

# Replace 'N/A' and empty strings with NaN
df.replace(['N/A', ''], pd.NA, inplace=True)

# Fill missing values: numerical columns with 0, others with "Unknown"
for column in df.columns:
    if df[column].dtype == 'object':  # Categorical column
        df[column].fillna("Unknown", inplace=True)
    else:  # Numeric column
        df[column].fillna(0, inplace=True)

# Save cleaned data
df.to_csv("cleaned_imdb_data.csv", index=False)
print("Data cleaned and saved as 'cleaned_imdb_data.csv'")
