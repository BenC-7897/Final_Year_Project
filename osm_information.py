import requests
import csv
import os
import time

# Overpass API URL
OVERPASS_URL = "http://overpass-api.de/api/interpreter"

# Function to get OSM ID and type from latitude and longitude
def get_osm_info(lat, lon):
    query = f"""
    [out:json];
    (
      node(around:10, {lat}, {lon});
      way(around:10, {lat}, {lon});
      relation(around:10, {lat}, {lon});
    );
    out center;
    """
    
    response = requests.get(OVERPASS_URL, params={"data": query})
    
    if response.status_code == 200:
        data = response.json()
        if "elements" in data and len(data["elements"]) > 0:
            element = data["elements"][0]  # Get the first element
            return element["id"], element["type"]
    
    return None, None

# Function to process a chunk of coordinates
def chunks(chunk, chunk_index, output_dir):
    c_output_file = os.path.join(output_dir, f'osm_info_chunk_{chunk_index}.csv')
    with open(chunk_output_file, 'w', newline='') as outfile:
        csv_writer = csv.writer(outfile)
        csv_writer.writerow(['Latitude', 'Longitude', 'OSM_ID', 'OSM_Type'])
        
        for lat, lon in chunk:
            osm_id, osm_type = get_osm_info(lat, lon)
            csv_writer.writerow([lat, lon, osm_id, osm_type])
            time.sleep(1)  # Delay to avoid Overpass API rate limits

# Function to process file in chunks
def chunks_file_processing(input_file, chunk_size=2000, output_dir='chunks'):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(input_file, 'r', encoding='utf-8-sig') as infile:
        chunk = []
        chunk_index = 0
        for i, line in enumerate(infile):
            if i == 0:
                continue  # Skip header
            lat, lon = map(float, line.strip().split(','))
            chunk.append((lat, lon))
            if len(chunk) >= chunk_size:
                chunks(chunk, chunk_index, output_dir)
                chunk = []
                chunk_index += 1
        if chunk:
            chunks(chunk, chunk_index, output_dir)

    merge_chunks(output_dir, 'osm_info.csv')

# Merge chunks into a single output file
def merge_chunks(output_dir, output_file):
    with open(output_file, 'w', newline='') as outfile:
        csv_writer = csv.writer(outfile)
        csv_writer.writerow(['Latitude', 'Longitude', 'OSM_ID', 'OSM_Type'])
        for chunk_file in os.listdir(output_dir):
            with open(os.path.join(output_dir, chunk_file), 'r', encoding='utf-8-sig') as infile:
                csv_reader = csv.reader(infile)
                next(csv_reader)  # Skip header
                for row in csv_reader:
                    csv_writer.writerow(row)

# Run the process
input_file = 'C:/Users/bencr/Downloads/combined_collision_v3/latlong.txt'
chunks_file_processing(input_file)

print("OSM information saved to osm_info.csv")