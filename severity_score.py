import pandas as pd

# Load the data
data = pd.read_csv('C:/Users/bencr/Downloads/combined_collision_v3/filtered_London_dataset.csv')

# Ensure that 'accident_severity_scores' are treated as integers
data['accident_severity_scores'] = data['Accident_Severity'].astype(int)

# Group by Latitude and Longitude, calculate number of accidents, collect severity scores and mean severity score
summary = data.groupby(['Latitude', 'Longitude']).agg(
    number_of_accidents=('Accident_Severity', 'size'), 
    accident_severity_scores=('accident_severity_scores', list),  
    mean_severity_score=('accident_severity_scores', 'mean')  
).reset_index()

# Save the main columns to a CSV file
summary[['Latitude', 'Longitude', 'number_of_accidents', 'accident_severity_scores', 'mean_severity_score']].to_csv(
    'accidents_summary_filtered.csv', 
    index=False
)

print("The result with selected columns has been saved to 'accidents_summary_filtered.csv'.")