# Importing pandas and matplotlib
import pandas as pd
import matplotlib.pyplot as plt

# Read in the Netflix CSV as a DataFrame
netflix_df = pd.read_csv("netflix_data.csv")

# Initialize netflix_subset to include only movies
netflix_subset = netflix_df[netflix_df['type'] >= 'Movie']

# Create another subset for movies which were released on 1990-1999
subset = netflix_subset[(netflix_subset["release_year"] >= 1990)]
movies_1990s = subset[(subset["release_year"] < 2000)]

# Create histogram for duration of movies created in the 1990s
plt.hist(movies_1990s["duration"])
plt.title('Distribution of Movie Durations in the 1990s')
plt.xlabel('Duration (minutes)')
plt.ylabel('Number of Movies')
plt.show()

# Declare duration based on the most frequent duration shown
duration = 100

# Filter the data again to keep only the action movies
action_movies_1990s = movies_1990s[movies_1990s["genre"] == "Action"]

# Iterate through the labels and rows of the DataFrame of action movies
short_movie_count = 0
for label, row in action_movies_1990s.iterrows() :
    if row["duration"] < 90 :
        short_movie_count += 1

# Display the number of short-length action movies
print(short_movie_count)
