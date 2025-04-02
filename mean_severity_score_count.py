import pandas as pd

# Load your dataset
df = pd.read_csv('C:/Users/bencr/Downloads/combined_collision_v3/refined_London_dataset.csv')

# Count the number of occurrences of each mean_severity_score in each Borough
result = df.groupby(['Borough', 'mean_severity_score']).size().reset_index(name='count')

# Save the result to a CSV file
result.to_csv('mean_severity_score_counts.csv', index=False)

print("The counts have been saved to 'mean_severity_score_counts.csv'.")

