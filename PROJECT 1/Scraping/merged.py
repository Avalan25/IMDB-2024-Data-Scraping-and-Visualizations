# import pandas as pd
# import os

# # List of CSV files to merge (update with actual filenames)
# csv_files = [
#     "action_movies.csv", 
#     "crime_movies.csv", 
#     "comedy_movies.csv",
#     "horror_movies.csv",
#     "adventure_movies.csv",
#     "romance_movies.csv",
#     "thriller_movies.csv",
#     "animation_movies.csv",
#     "fantacy_movies.csv",
#     "documentary_movies.csv"
# ]

# # Create an empty DataFrame
# merged_df = pd.DataFrame()

# # Loop through all CSV files and append to merged_df
# for file in csv_files:
#     if os.path.exists(file):
#         df = pd.read_csv(file)
#         merged_df = pd.concat([merged_df, df], ignore_index=True)
#     else:
#         print(f"File not found: {file}")

# # Save merged DataFrame to a new CSV file
# merged_df.to_csv("merged_movies.csv", index=False)

# print("All CSV files have been merged into 'merged_movies.csv'")

#--------------------------------------

# import pandas as pd
# import os
# import re

# # List of CSV files to merge (update with actual filenames)
# csv_files = [
#     "action_movies.csv", 
#     "comedy_movies.csv", 
#     "drama_movies.csv",
#     "horror_movies.csv",
#     "crime_movies.csv",
#     "romance_movies.csv",
#     "thriller_movies.csv",
#     "animation_movies.csv",
#     "fantacy_movies.csv",
#     "documentary_movies.csv"
# ]

# # Create an empty DataFrame
# merged_df = pd.DataFrame()

# # Loop through all CSV files and append to merged_df
# for file in csv_files:
#     if os.path.exists(file):
#         df = pd.read_csv(file)
        
#         # Clean the 'Name' column by removing numeric prefixes (e.g., "1. ", "23. ")
#         df['Name'] = df['Name'].apply(lambda x: re.sub(r'^\d+\.\s+', '', str(x)))
        
#         merged_df = pd.concat([merged_df, df], ignore_index=True)
#     else:
#         print(f"File not found: {file}")

# # Save merged DataFrame to a new CSV file
# merged_df.to_csv("merged1_movies.csv", index=False)

# print("All CSV files have been merged into 'merged_movies.csv' with cleaned movie names.")

#--------------------------------------

# import pandas as pd
# import os
# import re

# # List of CSV files to merge (update with actual filenames)
# csv_files = [
#     "action_movies.csv", 
#     "comedy_movies.csv", 
#     "animation_movies.csv",
#     "horror_movies.csv",
#     "crime_movies.csv",
#     "romance_movies.csv",
#     "thriller_movies.csv",
#     "animation_movies.csv",
#     "fantacy_movies.csv",
#     "documentary_movies.csv"
# ]

# # Function to clean movie names
# def clean_movie_name(name):
#     return re.sub(r'^\d+\.\s+', '', str(name))  # Remove numeric prefixes (e.g., "1. ")

# # Function to convert votes to integer
# def convert_votes(votes):
#     if isinstance(votes, str):  # Ensure votes is a string before processing
#         votes = votes.strip().upper()  # Normalize case
#         if 'K' in votes:  
#             return int(float(votes.replace('K', '')) * 1000)  # Convert "K" to integer
#         elif votes.isdigit():  
#             return int(votes)  # Convert normal numbers directly
#     return 0  # Default if not a valid number

# # Create an empty DataFrame
# merged_df = pd.DataFrame()

# # Loop through all CSV files and append to merged_df
# for file in csv_files:
#     if os.path.exists(file):
#         df = pd.read_csv(file)
        
#         # Clean 'Name' column
#         df['Name'] = df['Name'].apply(clean_movie_name)
        
#         # Convert 'Votes' column to integer
#         df['Votes'] = df['Votes'].apply(convert_votes)
        
#         merged_df = pd.concat([merged_df, df], ignore_index=True)
#     else:
#         print(f"File not found: {file}")

# # Save merged DataFrame to a new CSV file
# merged_df.to_csv("merged_movies2.csv", index=False)

# print("All CSV files have been merged into 'merged_movies.csv' with cleaned movie names and votes converted to integers.")


#--------------------------------------


#HERE WE CHANGE THE DURATION AS MINUTES
import pandas as pd
import os
import re

# List of CSV files to merge (update with actual filenames)
csv_files = [
    "action_movies.csv", 
    "comedy_movies.csv", 
    "animation_movies.csv",
    "horror_movies.csv",
    "crime_movies.csv",
    "romance_movies.csv",
    "thriller_movies.csv",
    "animation_movies.csv",
    "fantacy_movies.csv",
    "documentary_movies.csv"
]

# Function to clean movie names
def clean_movie_name(name):
    return re.sub(r'^\d+\.\s+', '', str(name))  # Remove numeric prefixes (e.g., "1. ")

# Function to convert votes to integer
def convert_votes(votes):
    if isinstance(votes, str):  # Ensure votes is a string before processing
        votes = votes.strip().upper()  # Normalize case
        if 'K' in votes:  
            return int(float(votes.replace('K', '')) * 1000)  # Convert "K" to integer
        elif votes.isdigit():  
            return int(votes)  # Convert normal numbers directly
    return 0  # Default if not a valid number

# Function to convert duration into minutes
def convert_duration(duration):
    if isinstance(duration, str):  # Ensure it's a string
        duration = duration.strip()
        hours = re.search(r'(\d+)h', duration)  # Extract hours
        minutes = re.search(r'(\d+)m', duration)  # Extract minutes

        total_minutes = 0
        if hours:
            total_minutes += int(hours.group(1)) * 60  # Convert hours to minutes
        if minutes:
            total_minutes += int(minutes.group(1))  # Add remaining minutes

        return total_minutes if total_minutes > 0 else None  # Return None for invalid data

    return None  # Default if not a valid string

# Create an empty DataFrame
merged_df = pd.DataFrame()

# Loop through all CSV files and append to merged_df
for file in csv_files:
    if os.path.exists(file):
        df = pd.read_csv(file)
        
        # Clean 'Name' column
        df['Name'] = df['Name'].apply(clean_movie_name)
        
        # Convert 'Votes' column to integer
        df['Votes'] = df['Votes'].apply(convert_votes)
        
        # Convert 'Duration' column to minutes
        df['Duration'] = df['Duration'].apply(convert_duration)
        
        merged_df = pd.concat([merged_df, df], ignore_index=True)
    else:
        print(f"File not found: {file}")

# Save merged DataFrame to a new CSV file
merged_df.to_csv("merged_movies3.csv", index=False)

print("All CSV files have been merged into 'merged_movies.csv' with cleaned movie names, votes converted to integers, and duration in minutes.")
