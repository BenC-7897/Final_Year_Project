import requests # For sending HTTP requests to the Overpass API
import csv # For reading from and writing to CSV files
import os # For interacting with the file system
from concurrent.futures import ThreadPoolExecutor # For parallel processing of tasks

# URL of the Overpass API endpoint
OVERPASS_URL = "http://overpass-api.de/api/interpreter"

# Function to query OpenStreetMap (OSM) data for a given latitude and longitude
def osm(latitude, longitude):
    # Define the Overpass query to find OSM elements (nodes, ways, relations) within a 10-metre radius
    query = f"""
    [out:json]; # Output format in JSON
    (
      node(around:10, {latitude}, {longitude});  
      way(around:10, {latitude}, {longitude});   
      relation(around:10, {latitude}, {longitude});  
    );
    out center; # Output with central geometry
    """
    # Send the query to the Overpass API and get the response
    response = requests.get(OVERPASS_URL, params={"data": query})
    if response.status_code == 200: # Check if the request was successful
        data = response.json() # Parse the JSON response
        # If there are elements in the response, retrieve the first element's ID and type
        if "elements" in data and len(data["elements"]) > 0:
            element = data["elements"][0]
            return element["id"], element["type"] # Return the OSM ID and type of the element
    return None, None # Return None if no data is found or the request fails

# Function to process a single coordinate (latitude and longitude)
def coordinate(latitude, longitude):
    try:
        # Call the osm function to get the OSM ID and type for the given coordinates
        osm_id, osm_type = osm(latitude, longitude)
        # Print the result for debugging purposes
        print(f"Latitude: {latitude}\nLongitude: {longitude}\nOSM_ID: {osm_id}\nOSM_Type: {osm_type}\n")
        return latitude, longitude, osm_id, osm_type # Return the results
    except Exception as e: # Handle any exceptions that occur
        # Print an error message and return None for OSM ID and type
        print(f"Error processing coordinate {latitude}, {longitude}: {e}\n")
        return latitude, longitude, None, None

# Function to process a chunk of coordinates stored in a CSV file
def chunks(chunk_file):
    # Define the name of the output file by appending "_processed" to the input file name
    output_file = chunk_file.replace('.csv', '_processed.csv')
    
    try:
        # Open the input CSV file for reading and the output file for writing
        with open(chunk_file, 'r', encoding='utf-8-sig') as infile, open(output_file, 'w', newline='') as outfile:
            csv_reader = csv.reader(infile) # Initialise the CSV reader
            csv_writer = csv.writer(outfile) # Initialise the CSV writer
            # Write the header row for the output file
            csv_writer.writerow(['Latitude', 'Longitude', 'OSM_ID', 'OSM_Type'])
            
            next(csv_reader) # Skip the header row in the input file
            chunk = [] # Initialise a list to store coordinate tuples
            for row in csv_reader: # Iterate through each row in the input file
                # Convert the latitude and longitude from strings to floating-point numbers
                latitude, longitude = map(float, row[:2])
                chunk.append((latitude, longitude)) # Add the coordinates to the chunk list
                
            # Use ThreadPoolExecutor to process coordinates in parallel
            with ThreadPoolExecutor(max_workers=9) as executor:
                # Map the coordinate function to each coordinate in the chunk
                results = list(executor.map(lambda coord: coordinate(coord[0], coord[1]), chunk))
                
            # Write the results to the output file
            for result in results:
                csv_writer.writerow(result)
                
        # Print a success message indicating the output file location
        print(f"Written to {output_file}\n")
    except FileNotFoundError as e: # Handle the case where the input file is not found
        print(f"FileNotFoundError: {e}. Make sure the file exists.\n")
    except Exception as e: # Handle any other exceptions that occur
        print(f"Error processing chunk: {e}\n")

# Example usage: Call the process_chunk function with a specific chunk file
chunk_file = 'C:/Users/bencr/Downloads/chunks/osm_info_chunk_18.csv'
chunks(chunk_file) # Process the specified chunk file