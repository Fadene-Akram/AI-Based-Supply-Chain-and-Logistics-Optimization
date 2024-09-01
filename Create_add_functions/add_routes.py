import json
from math import radians, sin, cos, sqrt, atan2

def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate the distance (in kilometers) between two points given their coordinates (latitude and longitude)."""
    # Radius of the Earth in kilometers
    R = 6371.0
    
    # Convert latitude and longitude from degrees to radians
    lat1_rad = radians(lat1)
    lon1_rad = radians(lon1)
    lat2_rad = radians(lat2)
    lon2_rad = radians(lon2)
    
    # Calculate the differences in latitude and longitude
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    # Calculate the distance using Haversine formula
    a = sin(dlat / 2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    
    return distance

def find_adjacent_cities(city_name, adjacent_cities):
    """Find and calculate distances to adjacent cities in the provided JSON file."""
    with open("data/city_products_data_updated.json", "r+") as json_file:
        city_data = json.load(json_file)
        
        # Find the city info from the JSON data
        city_info = next((city for city in city_data["cities"] if city["name"] == city_name), None)
        if not city_info:
            raise ValueError(f"City '{city_name}' not found in the JSON data.")
        
        # Ensure 'routes' key is initialized if missing
        if "routes" not in city_info:
            city_info["routes"] = []
        
        # Get the coordinates of the city
        city_lat = float(city_info["latitude"])
        city_lon = float(city_info["longitude"])
        
        # Calculate distances to adjacent cities and add routes to city object
        for adj_city_name in adjacent_cities:
            adj_city_info = next((city for city in city_data["cities"] if city["name"] == adj_city_name), None)
            if adj_city_info:
                adj_city_lat = float(adj_city_info["latitude"])
                adj_city_lon = float(adj_city_info["longitude"])
                dist = calculate_distance(city_lat, city_lon, adj_city_lat, adj_city_lon)
                city_info["routes"].append((adj_city_name, dist))
        
        # Move to the beginning of the file and update the JSON data
        json_file.seek(0)
        json.dump(city_data, json_file, indent=4)
        json_file.truncate()

# Example usage:
city_name = "Beni Abbes"
adjacent_cities = ["Adrar","Timimoun","Bechar","El Bayadh","Tindouf"]
find_adjacent_cities(city_name, adjacent_cities)
print("Routes updated in JSON file.")
