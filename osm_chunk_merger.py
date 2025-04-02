import os
import pandas as pd

# Change this to the path of your folder with the CSV files
chunks = 'C:/Users/bencr/Downloads/chunks'

# Get all the CSV files in chunks
osm_files = [f for f in os.listdir(chunks) if f.endswith('.csv')]

# Sort the files in order
osm_files.sort()

# Initialise an empty dataframe
merged_df = pd.DataFrame()

# Loop through the files whilst appending
for file in osm_files:
    file_path = os.path.join(chunks, file)
    df = pd.read_csv(file_path)
    # Swap the latitude and longitude columns if needed
    df = df[['Latitude', 'Longitude'] + [col for col in df.columns if col not in ['Latitude', 'Longitude']]]
    # Update merged_df with new data
    merged_df = pd.concat([merged_df, df], ignore_index=True)

# Sort the merged dataframe by the 'Latitude' column
merged_df = merged_df.sort_values(by='Latitude')

# Save the sorted dataframe to a new CSV file
merged_df.to_csv(os.path.join(chunks, 'osm_info.csv'), index=False)