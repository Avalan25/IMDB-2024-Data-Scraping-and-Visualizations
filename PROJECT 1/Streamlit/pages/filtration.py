import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# PostgreSQL connection details
DB_USER = "postgres"
DB_PASSWORD = "avalan"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "imdp"
TABLE_NAME = "imdb_movies"

# Create SQLAlchemy engine and load data
engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
df = pd.read_sql(f"SELECT * FROM {TABLE_NAME};", engine)

st.title("🎬 Filter Movies by Genre, Rating, Duration & Votes")

# Detect relevant columns
genre_col = rating_col = duration_col = votes_col = None

for col in df.columns:
    if col.lower() == "genre":
        genre_col = col
    elif col.lower() == "rating":
        rating_col = col
    elif col.lower() == "duration":
        duration_col = col
    elif col.lower() == "votes":
        votes_col = col

if not all([genre_col, rating_col, duration_col, votes_col]):
    st.error("❌ Required columns ('genre', 'rating', 'duration', 'votes') not found in the table.")
    st.stop()

# Genre dropdown
genres = sorted(df[genre_col].dropna().unique().tolist())
genres.insert(0, "All Movies")
selected_genre = st.selectbox("🎯 Choose a Genre", genres)

# Rating dropdown
rating_values = sorted(df[rating_col].dropna().unique())
ratings = ["All Ratings"] + [str(r) for r in rating_values]
selected_rating = st.selectbox("⭐ Choose a Rating", ratings)

# Duration category dropdown
duration_categories = {
    "All Durations": None,
    "Below 1 hour": lambda d: d < 60,
    "1 hour or more": lambda d: d >= 60,
    "1.5 hours or more": lambda d: d >= 90,
    "Below 2 hours": lambda d: d < 120,
    "2 hours or more": lambda d: d >= 120,
    "2.5 hours or more": lambda d: d >= 150,
    "Below 3 hours": lambda d: d < 180,
    "3 hours or more": lambda d: d >= 180,
    # "3.5 hours or more": lambda d: d >= 210,
    # "Below 4 hours": lambda d: d < 240,
    # "4 hours or more": lambda d: d >= 240,
    # "5 hours or more": lambda d: d >= 300,
    # "6 hours or more": lambda d: d >= 360,
    # "7 hours or more": lambda d: d >= 420,
}
duration_options = list(duration_categories.keys())
selected_duration = st.selectbox("⏱️ Choose Duration Range", duration_options)

# Votes count dropdown
vote_options = ["All Votes", "Above 10000", "Below 10000"]
selected_votes = st.selectbox("🗳️ Choose Voting Count", vote_options)

# Apply filters
filtered_df = df.copy()

if selected_genre != "All Movies":
    filtered_df = filtered_df[filtered_df[genre_col] == selected_genre]

if selected_rating != "All Ratings":
    filtered_df = filtered_df[filtered_df[rating_col] == float(selected_rating)]

duration_filter = duration_categories[selected_duration]
if duration_filter:
    filtered_df = filtered_df[filtered_df[duration_col].apply(duration_filter)]

if selected_votes == "Above 10000":
    filtered_df = filtered_df[filtered_df[votes_col] > 10000]
elif selected_votes == "Below 10000":
    filtered_df = filtered_df[filtered_df[votes_col] < 10000]

# Format duration column for display
def format_duration(mins):
    mins = int(mins)
    hours = mins // 60
    minutes = mins % 60
    return f"{hours} hr {minutes} mins" if hours > 0 else f"{minutes} mins"

filtered_df[duration_col] = filtered_df[duration_col].apply(format_duration)

# Display results
st.markdown("---")
st.subheader("📽️ Filtered Movies List")
st.dataframe(filtered_df.reset_index(drop=True))
