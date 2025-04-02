import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Define London boundaries
min_latitude, max_latitude = 51.3550556, 51.6517156
min_longitude, max_longitude = -0.453256, 0.15050513

# Load the dataset
df = pd.read_csv('C:/Users/bencr/Downloads/combined_collision_v3/combined_collisions_v3.csv')

# Filter the dataset based on London boundaries
df_london = df[(df['Latitude'] >= min_latitude) & (df['Latitude'] <= max_latitude) &
               (df['Longitude'] >= min_longitude) & (df['Longitude'] <= max_longitude)]

# Extract hour from the Time column
df_london['Hour'] = pd.to_datetime(df_london['Time']).dt.hour

# Create a pivot table
pivot_table = df_london.pivot_table(index='Hour', columns='Accident_Severity', aggfunc='size', fill_value=0)

# Create the heatmap
plt.figure(figsize=(10, 6))
sns.heatmap(pivot_table, annot=True, cmap='YlGnBu', cbar=True)
plt.title('Heatmap of Accident Severity in London')
plt.xlabel('Accident Severity')
plt.ylabel('Hour of the Day')
plt.show()