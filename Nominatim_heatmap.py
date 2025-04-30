import pandas as pd # For handling and processing data
import folium # For creating the map and visualizing data
import osmnx as ox # For retrieving street network data
import matplotlib.cm as cm # For colour maps
import matplotlib.colors as colors # For normalising and working with colours

# Disable OSMnx cache to ensure fresh data
ox.settings.use_cache = False

# File path
file_path = 'C:/Users/bencr/Downloads/combined_collision_v3/enriched_file.csv'
chunk_size = 2000

# Initialise folium map
m = folium.Map(location=[51.5074, -0.1278], zoom_start=12)

# Load London street network
print("Loading London street network...")
street = ox.graph_from_place('London, England', network_type='drive', simplify=False)
edges = ox.graph_to_gdfs(street, nodes=False)

# Convert `osmid` to integers (fix cases where it's a list)
edges['osmid'] = edges['osmid'].apply(lambda x: int(x[0]) if isinstance(x, list) else int(x))
edges = edges.set_index('osmid')

# Load accident data and aggregate by OSM_ID
print("Aggregating accident data by street...")
accident_data = pd.read_csv(file_path, usecols=['OSM_ID', 'mean_severity_score'])
accident_data = accident_data.dropna(subset=['OSM_ID']) # Remove NaN OSM_IDs
accident_data['OSM_ID'] = accident_data['OSM_ID'].astype(int)

# Use mean street severity
mean_street_severity = accident_data.groupby('OSM_ID')['mean_severity_score'].mean()

# Get min/max severity for colour scale
vmin, vmax = mean_street_severity.min(), mean_street_severity.max()
colour_map = cm.ScalarMappable(norm=colors.Normalize(vmin=vmin, vmax=vmax), cmap='YlOrRd')

# Process streets
total_processed = 0
print("Processing and adding streets to map...")

for osm_id, mean_severity in mean_street_severity.items():
    if osm_id not in edges.index:
        continue # Skip streets not found in OSMnx
    try:
        # Retrieve street geometry data, including multiple geometries
        geometry_data = edges.loc[osm_id, 'geometry']
        if isinstance(geometry_data, pd.Series):
            geometries = geometry_data.tolist()
        else:
            geometries = [geometry_data]
        # Map the severity score to a colour on the colour scale
        color = colors.to_hex(colour_map.to_rgba(mean_severity))
        # Add the street geometries to the Folium map
        for geometry in geometries:
            if geometry.geom_type == 'LineString':
                locations = [(point[1], point[0]) for point in geometry.coords]
                folium.PolyLine(locations, color=color, weight=5).add_to(m)
            elif geometry.geom_type == 'MultiLineString':
                for line in geometry:
                    locations = [(point[1], point[0]) for point in line.coords]
                    folium.PolyLine(locations, color=color, weight=5).add_to(m)
        # Increment the counter for successfully processed streets
        total_processed += 1
    except Exception as e:
        print(f"Error processing OSM ID {osm_id}: {e}")

print(f"\nTotal streets processed: {total_processed}")
m.save('london_street_heatmap.html')
print("Heatmap saved as 'london_street_heatmap.html'.")
