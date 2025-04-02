import pandas as pd

# Load your dataset
df = pd.read_csv('C:/Users/bencr/Downloads/combined_collision_v3/combined_collisions_v3.csv')

# Define London's borough boundaries
minimum_latitude, maximum_latitude = 51.3550556, 51.6517156
minimum_longitude, maximum_longitude = -0.453256, 0.15050513

# Filter the dataset to include only accidents within the defined boundaries
filtered_df = df[(df['Latitude'] >= minimum_latitude) & (df['Latitude'] <= maximum_latitude) &
                 (df['Longitude'] >= minimum_longitude) & (df['Longitude'] <= maximum_longitude)]

# Keep only the required columns
filtered_London_df = filtered_df[['Latitude', 'Longitude', 'Accident_Severity']]

# Sort the dataset by Latitude, Longitude and Accident_Severity in ascending order
filtered_London_df = filtered_London_df.sort_values(by=['Latitude', 'Longitude', 'Accident_Severity'],
                                                    ascending=[True, True, True])

# Save the sorted dataset to a CSV file
output_file = 'filtered_London_dataset.csv'
filtered_London_df.to_csv(output_file, index=False)

print(f"Dataset sorted by Latitude, Longitude and properly ordered Accident_Severity saved to {output_file}")