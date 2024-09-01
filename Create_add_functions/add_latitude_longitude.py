import json

# Load city product data
with open("city_products_data.json", "r") as json_file:
    city_data = json.load(json_file)

# Load city location data with explicit encoding
with open("Wilaya_Of_Algeria.json", "r", encoding='utf-8') as json_file:
    city_locations = json.load(json_file)

# Create a mapping dictionary for city names to their respective latitude and longitude
city_location_map = {city_info["name"]: (city_info["latitude"], city_info["longitude"]) for city_info in city_locations}

# Update city data with latitude and longitude
for city_info in city_data["cities"]:
    city_name = city_info["name"]
    if city_name in city_location_map:
        latitude, longitude = city_location_map[city_name]
        city_info["latitude"] = latitude
        city_info["longitude"] = longitude
    else:
        # Handle case where city name is not found in location data
        print(f"Warning: No location data found for city '{city_name}'")

# Save the updated city product data back to the original JSON file
with open("city_products_data_updated.json", "w") as json_file:
    json.dump(city_data, json_file, indent=4)

print("City product data updated and saved.")
