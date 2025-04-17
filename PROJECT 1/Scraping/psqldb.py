import pandas as pd
from sqlalchemy import create_engine

# PostgreSQL connection details
DB_USER = "postgres"
DB_PASSWORD = "avalan"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "imdp"
TABLE_NAME = "imdb_movies"

# Create PostgreSQL connection using SQLAlchemy
engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

# Load the cleaned IMDb CSV file
df = pd.read_csv("cleaned_imdb_data.csv")

# Store the data in PostgreSQL
df.to_sql(TABLE_NAME, engine, if_exists='replace', index=False)

print(f"Data successfully stored in PostgreSQL table '{TABLE_NAME}'!")
