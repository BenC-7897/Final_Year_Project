
# Safety Analysis for Micromobility Systems 

This was a final year project that used a Kaggle dataset to determine the safety of electric bikes and electric scooters 

- A dataset about traffic accidents in Greater London between 2005 and 2018 was obtained from Kaggle (having been put together by the UK Transport Ministry) 

- The traffic accidents' geospatial and location data were extracted and placed in a separate data frame (along with the accident severity) (this acted as the analysis for the project) 

- These accidents' location data were converted to OpenStreetMap IDs (by two APIs) in order to place the accident locations on a streetmap (this acted the prediction for the project) which was colour-coded to indicate the safety of London's streets 

- Based on the streetmaps, two route-optimisation algorithms were created to determine the quickest routes and the safest routes between two points (an edge-based graph method and the Dijkstra Algorithm), this used Python Folium and NetworkX in order to determine the safety scores and the distances for the two routes. This indicated where the accident hotspots in London. (this acted as the optimisation) 


## Skills
Python, Python Folium, Python Pandas, Nominatim API, Overpass API, Dijkstra Algorithm, Geocoders, NetworkX, OSMNX, Python Matplotlib, ThreadPoolExecutor, Python Seaborn


## Optimisations

What optimisations did you make in your code? 

- Skipped the accident locations that weren't able to be matched on the OpenStreetMap database 

- The accident locations were converted in chunks and then merged back together (to prevent the Nominatim API from failing) 

- Caching was disabled to ensure that fresh OSM ID data was used and graph_from_point allowed for more accurate map creation 

- Vectorised operations were used with the accident OSM IDs in order to loop through the map locations quicker (by linking the closest street to the OSM ID) 

- Edge and nodal usage on the graph ensured that as many accident severity scores were listed 

- Dijkstra algorithm had a lambda weight function to ensure that none of the edges had zero 


## Acknowledgements

 - “Here’s how ThreadPoolExecutor works: ” from Anup Chakole, “Understanding ThreadPoolExecutor - Anup Chakole - Medium,” Medium, Aug. 28, 2024. https://medium.com/@anupchakole/understanding-threadpoolexecutor-2eed095d21aa 
 - “Reverse Geocoding: How it works” from “Reverse - Nominatim 4.3.2 Manual,” nominatim.org. https://nominatim.org/release-docs/latest/api/Reverse/ 
 - “osmnx.distance.nearest_nodes”, “osmnx.graph.graph_from_point”, “osmnx.settings module”, “osmnx.convert.graph_to_gdfs” and “osmnx.graph.graph_from_place” from “User Reference - OSMnx 1.7.0 documentation,” osmnx.readthedocs.io. https://osmnx.readthedocs.io/en/stable/user-reference.html 
 - “matplotlib.colors.to_rgba” and “class matplotlib.cm.ScalarMappable(colorizer, **kwargs)” “matplotlib.cm — Matplotlib 3.10.1 documentation,” Matplotlib.org, 2025. https://matplotlib.org/stable/api/cm_api.html#matplotlib.cm.ScalarMappable 
 - “LineStrings” and “shapely.MultiLineString” from “The Shapely User Manual — Shapely 2.0.6 documentation,” Readthedocs.io, 2024. https://shapely.readthedocs.io/en/2.0.6/manual.html#LineString https://shapely.readthedocs.io/en/2.0.6/reference/shapely.MultiLineString.html 
 - “Graph.set_edge_attributes” and “Graph.nodes” from “Software for Complex Networks — NetworkX 2.5 documentation,” networkx.org. https://networkx.org/documentation/stable/index.html 
 - “dijkstra_path: Parameters” from “dijkstra_path — NetworkX 3.2.1 documentation,” networkx.org. https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.shortest_paths.weighted.dijkstra_path.html  
 

