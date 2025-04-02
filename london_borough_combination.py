import pandas as pd # Pandas is used for data manipulation and analysis
from geopy.distance import geodesic # Geopy is used to calculate geographical distances

# Load this dataset 
london_df = pd.read_csv("C:/Users/bencr/Downloads/combined_collision_v3/London_dataset.csv")

# Load the dataset containing the coordinates of London boroughs
coordinates_df = pd.read_csv("C:/Users/bencr/Downloads/combined_collision_v3/london_boroughs_coordinates.csv")

# Define a function to find the closest borough based on latitude and longitude
def borough(latitude, longitude, coordinates_df):
    minimum_distance = float("inf") # Initialise the minimum distance to infinity
    closest_borough = None  # Initialise the closest borough as None
    # Iterate through each row in the borough coordinates dataset
    for _, row in coordinates_df.iterrows():
        # Calculate the distance between the given coordinates and the borough's coordinates
        distance = geodesic((latitude, longitude), (row["Latitude"], row["Longitude"])).meters
        # If the calculated distance is smaller than the current minimum distance
        if distance < minimum_distance:
            minimum_distance = distance # Update the minimum distance
            closest_borough = row["Borough"] # Update the closest borough
    return closest_borough # Return the name of the closest borough

# This determines the closest borough for the given latitude and longitude of each incident
london_df["Borough"] = london_df.apply(
    lambda row: borough(row["Latitude"], row["Longitude"], coordinates_df),
    axis=1 # Apply the function row-wise
)

# Save the updated London dataset with the newly added "Borough" column to a new CSV file
london_df.to_csv("london_dataset_with_boroughs.csv", index=False) 
