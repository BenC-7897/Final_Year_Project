import pandas as pd

# Load your dataset into a DataFrame 
df = pd.read_csv("C:/Users/bencr/Downloads/combined_collision_v3/refined_London_dataset.csv")

# Group streets by mean_severity_score and count the number of streets in each group
street_severity_count = df.groupby('mean_severity_score').size().reset_index(name='Number_of_Streets')

# Rename columns for better readability
street_severity_count.columns = ['Mean Severity Score', 'Number of Streets']

# Print the results as a table
print("Number of Streets by Mean Severity Score:")
print(street_severity_count)

# Optional: Save the results to a CSV file
street_severity_count.to_csv("streets_by_mean_severity_score.csv", index=False)
print("Results saved to 'streets_by_mean_severity_score.csv'")