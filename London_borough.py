from geopy.geocoders import Nominatim # Import the geocoding library
import pandas as pd # Import pandas for data manipulation

# List of London's boroughs
boroughs = [
    "Barking and Dagenham", "Barnet", "Bexley", "Brent", "Bromley", "Camden", "Croydon", 
    "Ealing", "Enfield", "Greenwich", "Hackney", "Hammersmith and Fulham", "Haringey", 
    "Harrow", "Havering", "Hillingdon", "Hounslow", "Islington", "Kensington and Chelsea", 
    "Kingston upon Thames", "Lambeth", "Lewisham", "Merton", "Newham", "Redbridge", 
    "Richmond upon Thames", "Southwark", "Sutton", "Tower Hamlets", "Waltham Forest", 
    "Wandsworth", "Westminster", "City of London"
]

# Initialise the geolocator with a user agent to access the geocoding service
geolocator = Nominatim(user_agent="london_boroughs_locator")

# Dictionary to store borough names and their corresponding coordinates
borough_coordinates = {}

# Loop through each borough to obtain its geographical coordinates
for b in boroughs:
    location = geolocator.geocode(f"{b}, London, UK") # Geocode the borough's location
    if location:
        borough_coordinates[b] = (location.latitude, location.longitude) # Store latitude and longitude
    else:
        borough_coordinates[b] = (None, None) # Handle cases where coordinates are not found

# Create a pandas DataFrame from the dictionary to organize the data
df = pd.DataFrame(borough_coordinates.items(), columns=['Borough', 'Coordinates'])

# Split the 'Coordinates' column into separate 'Latitude' and 'Longitude' columns
df[['Latitude', 'Longitude']] = pd.DataFrame(df['Coordinates'].tolist(), index=df.index)

# Drop the 'Coordinates' column
df.drop(columns=['Coordinates'], inplace=True)

# Save the final DataFrame to a CSV file
df.to_csv("london_boroughs_coordinates.csv", index=False)

# The data has been saved 
print("The coordinates have been saved to london_boroughs_coordinates.csv")