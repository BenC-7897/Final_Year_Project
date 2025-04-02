import pandas as pd
import os

# Load your dataset
df = pd.read_csv('C:/Users/bencr/Downloads/combined_collision_v3/combined_collisions_v3.csv')

# Sort the DataFrame by the 'Accident_Severity' column in the order of 1, 2 and 3 and then by the 'Unnamed: 0' column
df_sorted = df.sort_values(by=['Accident_Severity', 'Unnamed: 0'], key=lambda x: x.map({1: 0, 2: 1, 3: 2} if x.name == 'Accident_Severity' else x))

# Save the sorted dataset as a CSV file 
output_path = os.path.join('C:/Users/bencr/Downloads/combined_collision_v3', 'sorted_collision_dataset_modified.csv')
df_sorted.to_csv(output_path, index=False)

print(f"The sorted dataset has been saved as '{output_path}'.")