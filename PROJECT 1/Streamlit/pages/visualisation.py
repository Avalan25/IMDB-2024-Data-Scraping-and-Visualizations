import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from sqlalchemy import create_engine
import seaborn as sns

# --------------------------------------------
# 🔗 PostgreSQL connection details
# --------------------------------------------
DB_USER = "postgres"
DB_PASSWORD = "avalan"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "imdp"
TABLE_NAME = "imdb_movies"

# --------------------------------------------
# 🔌 Create SQLAlchemy engine and load data
# --------------------------------------------
engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
df = pd.read_sql(f"SELECT * FROM {TABLE_NAME};", engine)

st.title("🎬 Movie Ratings Visualization")
st.markdown("---")

# --------------------------------------------
# 📊 Rating Distribution - Boxplot
# --------------------------------------------
if "Rating" in df.columns:
    st.subheader("📊 Rating Distribution - Boxplot")
    fig, ax = plt.subplots()
    ax.boxplot(df["Rating"].dropna())
    ax.set_title("Boxplot of Movie Ratings")
    ax.set_ylabel("Rating")
    st.pyplot(fig)
else:
    st.error("❌ 'Rating' column not found in the data.")

# --------------------------------------------
# 📈 Voting Trends by Genre
# --------------------------------------------
st.markdown("---")
st.subheader("📈 Voting Trends by Genre")

if "Genre" in df.columns and "Votes" in df.columns:
    genre_votes = df.groupby("Genre")["Votes"].mean().sort_values(ascending=False).reset_index()

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(genre_votes["Genre"], genre_votes["Votes"], color="skyblue")
    ax.set_xlabel("Genre")
    ax.set_ylabel("Average Votes")
    ax.set_title("Average Voting Count by Genre")
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)
else:
    st.warning("Required columns 'Genre' and/or 'Votes' are missing from the dataset.")

# --------------------------------------------
# ⏱️ Average Duration by Genre - Horizontal Bar Chart
# --------------------------------------------
st.markdown("---")
st.subheader("⏱️ Average Duration by Genre")

if "Genre" in df.columns and "Duration" in df.columns:
    df["Duration"] = pd.to_numeric(df["Duration"], errors='coerce')

    duration_by_genre = df.groupby("Genre")["Duration"].mean().sort_values(ascending=True).reset_index()

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(duration_by_genre["Genre"], duration_by_genre["Duration"], color="salmon")
    ax.set_xlabel("Average Duration (minutes)")
    ax.set_ylabel("Genre")
    ax.set_title("Average Duration by Genre")
    st.pyplot(fig)
else:
    st.warning("Required columns 'Genre' and/or 'Duration' are missing from the dataset.")

# --------------------------------------------
# 🎭 Genre Distribution - Movie Count by Genre
# --------------------------------------------
st.markdown("---")
st.subheader("🎭 Genre Distribution")

if "Genre" in df.columns:
    genre_counts = df["Genre"].value_counts().reset_index()
    genre_counts.columns = ["Genre", "Movie Count"]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(genre_counts["Genre"], genre_counts["Movie Count"], color="mediumseagreen")
    ax.set_xlabel("Genre")
    ax.set_ylabel("Number of Movies")
    ax.set_title("Movie Count per Genre")
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)
else:
    st.warning("⚠️ 'Genre' column not found in the dataset.")

# --------------------------------------------
# 🌟 Genre-Based Rating Leaders
# --------------------------------------------
st.markdown("---")
st.subheader("🌟 Genre-Based Rating Leaders: Top-Rated Movie per Genre")

def format_duration(minutes):
    if pd.isnull(minutes):
        return "Unknown"
    try:
        minutes = int(float(minutes))
        hours = minutes // 60
        mins = minutes % 60
        return f"{hours} hr {mins} min"
    except:
        return str(minutes)

if "Genre" in df.columns and "Rating" in df.columns:
    genre_rating_df = df.dropna(subset=["Genre", "Rating"])
    top_movies_by_genre = genre_rating_df.sort_values("Rating", ascending=False).groupby("Genre").first().reset_index()

    if "Duration" in top_movies_by_genre.columns:
        top_movies_by_genre["Duration"] = top_movies_by_genre["Duration"].apply(format_duration)

    columns_to_show = ["Genre", "Title", "Rating", "Duration", "Votes"] if "Title" in df.columns else ["Genre", "Rating", "Duration", "Votes"]
    st.dataframe(top_movies_by_genre[columns_to_show])
else:
    st.warning("Required columns 'Genre' and/or 'Rating' are missing from the dataset.")

# --------------------------------------------
# 🥧 Most Popular Genres by Voting
# --------------------------------------------
st.markdown("---")
st.subheader("🥧 Most Popular Genres by Voting")

if "Genre" in df.columns and "Votes" in df.columns:
    genre_votes_df = df.dropna(subset=["Genre", "Votes"])
    genre_votes_df["Votes"] = pd.to_numeric(genre_votes_df["Votes"], errors="coerce")
    genre_votes_sum = genre_votes_df.groupby("Genre")["Votes"].sum().sort_values(ascending=False)

    fig, ax = plt.subplots()
    ax.pie(genre_votes_sum, labels=genre_votes_sum.index, autopct='%1.1f%%', startangle=140)
    ax.axis("equal")
    st.pyplot(fig)
else:
    st.warning("Required columns 'Genre' and/or 'Votes' are missing from the dataset.")

# --------------------------------------------
# 🔥 Ratings by Genre Heatmap
# --------------------------------------------
st.markdown("---")
st.subheader("🔥 Ratings by Genre Heatmap")

if "Genre" in df.columns and "Rating" in df.columns:
    genre_rating_df = df.dropna(subset=["Genre", "Rating"])
    genre_rating_df["Rating"] = pd.to_numeric(genre_rating_df["Rating"], errors="coerce")
    genre_avg_rating = genre_rating_df.groupby("Genre")["Rating"].mean().sort_values(ascending=False)
    genre_avg_rating_df = pd.DataFrame(genre_avg_rating).T

    fig, ax = plt.subplots(figsize=(12, 1))
    sns.heatmap(genre_avg_rating_df, annot=True, fmt=".1f", cmap="YlGnBu", ax=ax)
    ax.set_title("Average Ratings by Genre")
    st.pyplot(fig)
else:
    st.warning("Required columns 'Genre' and/or 'Rating' are missing.")

# --------------------------------------------
# 🏆 Top 10 Most Voted Movies
# --------------------------------------------
st.markdown("---")
st.subheader("🏆 Top 10 Most Voted Movies")
st.markdown("Displays the top 10 movies with the highest number of votes from the IMDb dataset.")

try:
    df.columns = [col.strip().title() for col in df.columns]

    if "Votes" in df.columns:
        df["Votes"] = pd.to_numeric(df["Votes"], errors="coerce")
        df = df.dropna(subset=["Votes"])
        top_voted = df.sort_values(by="Votes", ascending=False).head(10).reset_index(drop=True)
        top_voted.index = range(1, 11)
        top_voted.index.name = "Rank"
        st.dataframe(top_voted)
    else:
        st.error("❌ 'Votes' column not found in the dataset. Please verify your table structure.")
except Exception as e:
    st.error(f"❌ Failed to load data: {e}")
