import json
import os

# Get the directory path of the script
script_dir = os.path.dirname(__file__)

# Construct the path to the JSON data file
json_file_path = os.path.join(script_dir, '..', 'data', 'city_products_data_updated.json')

# Load the JSON data
with open(json_file_path, 'r') as file:
    data = json.load(file)

# Dictionary to store route distances
route_distances = {}

# Process each city
for city in data.get('cities', []):  # Use .get() to safely access 'cities' array
    city_name = city.get('name')  # Use .get() to safely access 'name'
    routes = city.get('routes', [])  # Use .get() to safely access 'routes' array
    
    if not city_name or not routes:
        continue  # Skip processing if essential keys are missing
    
    # Process each route from this city
    for route in routes:
        target_city_name = route[0]
        distance = route[1]
        
        # Ensure target city entry exists in the dictionary
        if target_city_name not in route_distances:
            route_distances[target_city_name] = {}
        
        # Check if there's a route back from target city to current city
        if city_name in route_distances[target_city_name]:
            # Compare distances and keep the smaller one
            current_distance = route_distances[target_city_name][city_name]
            if distance < current_distance:
                route_distances[target_city_name][city_name] = distance
        else:
            # Define new route distance
            route_distances[target_city_name][city_name] = distance

# Output the symmetric route distances
for target_city in route_distances:
    for city in route_distances[target_city]:
        distance = route_distances[target_city][city]
        print(f"{target_city} to {city}: {distance}")
