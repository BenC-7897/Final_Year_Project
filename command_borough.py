import pandas as pd
import osmnx as ox
import networkx as nx
import folium
import random

# Disable OSMnx caching to avoid outdated data
ox.settings.use_cache = False
ox.settings.log_console = False  

# Load dataset
file_path = "C:/Users/bencr/Downloads/combined_collision_v3/refined_London_dataset.csv"
df = pd.read_csv(file_path)

# Remove rows without accidents
df = df[df["number_of_accidents"] > 0].copy()

# Validate data
assert not df[["Latitude", "Longitude", "Borough"]].isnull().any().any(), "Dataset contains missing latitude/longitude or boroughs."

# Get unique boroughs
unique_boroughs = df["Borough"].unique()
print("Available Boroughs:", unique_boroughs)

# Function to get valid borough input
def borough_input():
    while True:
        borough = input("Enter a borough: ").strip()
        if borough in unique_boroughs:
            return borough
        print("Invalid borough name. Try again.")

# Get user-selected boroughs
first_borough = borough_input()
second_borough = borough_input()

# Filter dataset by boroughs
df_filtered = df[df["Borough"].isin([first_borough, second_borough])].copy()

# Generate road network 
initial_point = (df_filtered["Latitude"].mean(), df_filtered["Longitude"].mean())
G = ox.graph_from_point(initial_point, dist=15000, network_type="drive", retain_all=True, simplify=True)

# Assign default values to edges
for _, _, _, data in G.edges(keys=True, data=True):
    data["mean_severity_score"] = 1  # Default severity
    data["number_of_accidents"] = 0  # Default accident count

# Find nearest nodes for dataset points
df_filtered["nearest_node"] = ox.distance.nearest_nodes(G, df_filtered["Longitude"], df_filtered["Latitude"])

# Create severity mapping
severity_map = df_filtered.groupby("nearest_node")[["mean_severity_score", "number_of_accidents"]].mean().to_dict()

# Assign severity scores to edges efficiently
for u, v, key, data in G.edges(keys=True, data=True):
    data["mean_severity_score"] = round(severity_map["mean_severity_score"].get(u, 1))
    data["number_of_accidents"] = severity_map["number_of_accidents"].get(u, 0)

# Function to find valid start and end nodes
def get_valid_nodes(df_filtered, G, max_retries=20):
    nodes = df_filtered["nearest_node"].values
    for _ in range(max_retries):
        start_node, end_node = random.sample(list(nodes), 2)
        if nx.has_path(G, start_node, end_node):
            return start_node, end_node
    raise RuntimeError("Could not find valid start and end nodes.")

# Get start and end nodes
start_node, end_node = get_valid_nodes(df_filtered, G)

# Compute shortest and safest paths
shortest_path = nx.shortest_path(G, source=start_node, target=end_node, weight="length")
safest_path = nx.shortest_path(G, source=start_node, target=end_node, weight="mean_severity_score")

# Function to compute path metrics
def path_metrics(G, path):
    edges = [G[u][v][0] for u, v in zip(path[:-1], path[1:])]
    total_distance = sum(edge.get("length", 0) for edge in edges)
    mean_severity = round(sum(edge.get("mean_severity_score", 1) for edge in edges) / len(edges))
    return total_distance, mean_severity

# Compute path statistics
shortest_distance, shortest_severity = path_metrics(G, shortest_path)
safest_distance, safest_severity = path_metrics(G, safest_path)

# Create folium map
m = folium.Map(location=(G.nodes[start_node]['y'], G.nodes[start_node]['x']), zoom_start=13)

# Add start and end markers
folium.Marker((G.nodes[start_node]['y'], G.nodes[start_node]['x']), popup="Start", icon=folium.Icon(color="green")).add_to(m)
folium.Marker((G.nodes[end_node]['y'], G.nodes[end_node]['x']), popup="End", icon=folium.Icon(color="red")).add_to(m)

# Function to plot paths
def plot_path(m, G, path, color, label):
    coords = [(G.nodes[node]['y'], G.nodes[node]['x']) for node in path]
    folium.PolyLine(coords, color=color, weight=5, opacity=0.8, popup=label).add_to(m)

# Plot paths
plot_path(m, G, shortest_path, "blue", f"Shortest Path ({shortest_distance:.2f} m)")
plot_path(m, G, safest_path, "cyan", f"Safest Path ({safest_distance:.2f} m)")

# Save and print results
m.save("heatmap.html")
print(f"Shortest Path: Distance = {round(shortest_distance, 2)}m | Mean Severity Score = {shortest_severity}")
print(f"Safest Path: Distance = {round(safest_distance, 2)}m | Mean Severity Score = {safest_severity}")