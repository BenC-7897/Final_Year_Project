import pandas as pd # Importing pandas for data manipulation and analysis
import osmnx as ox # Importing osmnx for downloading and working with OpenStreetMap data
import networkx as nx # Importing networkx for graph-based operations and algorithms
import folium # Importing folium for creating interactive maps

# Disable the OSMnx caching
ox.settings.use_cache = False
ox.settings.log_console = False  

# Load the dataset
file_path = "C:/Users/bencr/Downloads/combined_collision_v3/refined_London_dataset.csv"
df = pd.read_csv(file_path)

# Select two random points
random_points = df.sample(2)
start_latitude, start_longitude = random_points.iloc[0][["Latitude", "Longitude"]]
finish_latitude, finish_longitude = random_points.iloc[1][["Latitude", "Longitude"]]
start = (start_latitude, start_longitude)
finish = (finish_latitude, finish_longitude)

# Fetch the road network around the start point 
Graph = ox.graph_from_point(start, dist=20000, network_type="drive", retain_all=True, simplify=False)

# Ensure the start and end nodes are in the same connected component
start_node = ox.distance.nearest_nodes(Graph, start_longitude, start_latitude)
finish_node = ox.distance.nearest_nodes(Graph, finish_longitude, finish_latitude)
if not nx.has_path(Graph, start_node, finish_node):
    raise ValueError("No path exists between the selected start and end points.")

# Initialise the edge attributes efficiently
for _, _, _, data in Graph.edges(keys=True, data=True):
    data.setdefault('mean_severity_score', 0)  
    data.setdefault('number_of_accidents', 0)

# Vectorised nearest node search
df["nearest_node"] = ox.distance.nearest_nodes(Graph, df["Longitude"], df["Latitude"])

# Apply the severity scores to edges efficiently
severity_map = df.set_index("nearest_node")[["mean_severity_score", "number_of_accidents"]].to_dict()

# Iterate through all the edges in the graph, extracting nodes (i, j), edge key and edge data
for i, j, key, data in Graph.edges(keys=True, data=True):
    if i in severity_map["mean_severity_score"]:
        data["mean_severity_score"] = severity_map["mean_severity_score"][i]
        data["number_of_accidents"] = severity_map["number_of_accidents"][i]
    elif j in severity_map["mean_severity_score"]:
        data["mean_severity_score"] = severity_map["mean_severity_score"][j]
        data["number_of_accidents"] = severity_map["number_of_accidents"][j]

# Compute shortest and safest paths using Dijkstra's algorithm
shortest_path = nx.dijkstra_path(Graph, source=start_node, target=finish_node, weight="length")
safest_path = nx.dijkstra_path(Graph, source=start_node, target=finish_node, weight=lambda u, v, d: d.get("mean_severity_score", 0) + 1)

# Compute the path metrics
def path_metrics(Graph, path):
    edges = [Graph[i][j][0] for i, j in zip(path[:-1], path[1:])]
    total_distance = sum(edge["length"] for edge in edges)
    mean_severity = round(sum(edge["mean_severity_score"] for edge in edges) / len(edges))
    return total_distance, mean_severity

shortest_distance, shortest_severity = path_metrics(Graph, shortest_path)
safest_distance, safest_severity = path_metrics(Graph, safest_path)

# Create the folium map
map = folium.Map(location=start, zoom_start=13)

# Add the start and end points
folium.Marker(location=(Graph.nodes[start_node]['y'], Graph.nodes[start_node]['x']), popup="Start", icon=folium.Icon(color="green")).add_to(map)
folium.Marker(location=(Graph.nodes[finish_node]['y'], Graph.nodes[finish_node]['x']), popup="Finish", icon=folium.Icon(color="red")).add_to(map)

# Function to plot the paths
def path_plot(map, Graph, path, colour, label, distance, severity):
    coordinates = [(Graph.nodes[node]['y'], Graph.nodes[node]['x']) for node in path]
    folium.PolyLine(coordinates, color=colour, weight=5, opacity=0.8, popup=f"{label} (Distance: {distance:.2f} m, Severity: {severity})").add_to(map)

path_plot(map, Graph, shortest_path, "blue", "Shortest Path", shortest_distance, shortest_severity)
path_plot(map, Graph, safest_path, "cyan", "Safest Path", safest_distance, safest_severity)

# Save and print the results
map.save("london_routes.html")

# Print the shortest and safest paths with severity scores
print(f"Shortest Path: Distance = {round(shortest_distance, 2)}m | Mean Severity Score = {shortest_severity}")
print(f"Safest Path: Distance = {round(safest_distance, 2)}m | Mean Severity Score = {safest_severity}")
