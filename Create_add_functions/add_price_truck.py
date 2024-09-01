import json
import random
import os

# Function to generate a random price within a specified range for a truck type
def generate_random_price(min_price, max_price):
    return round(random.uniform(min_price, max_price), 2)

current_dir = os.path.dirname(os.path.abspath(__file__))

json_file_path = os.path.join(current_dir, '..', '..', 'data', 'transportation_companies_generated.json')
# Load the JSON data from file
with open(json_file_path, 'r') as f:
    data = json.load(f)

# Access the list of companies
companies = data['companies']

# Define price ranges for each truck type
truck_price_ranges = {
    "Box Truck": (6000, 7500),      # Example price range for Box Truck (in dollars)
    "Refrigerated": (7500, 10000),   # Example price range for Refrigerated Truck
    "Flatbed": (5000, 6000)         # Example price range for Flatbed Truck
}

# Iterate over each company
for company in companies:
    company_name = company['name']
    city_name = company['city_name']
    
    print(f"Company: {company_name}")
    print(f"City: {city_name}")
    
    # Access trucks information for the company
    trucks = company['trucks']
    print("Trucks:")
    for truck in trucks:
        truck_type = truck['type']
        capacity = truck['capacity']
        current_load = truck['current_load']
        
        # Generate a random price within the specified range for the truck type
        if truck_type in truck_price_ranges:
            min_price, max_price = truck_price_ranges[truck_type]
            truck_price = generate_random_price(min_price, max_price)
        else:
            # Default price range if truck type not found in the specified ranges
            min_price, max_price = (10000, 15000)
            truck_price = generate_random_price(min_price, max_price)
        
        # Add price to the truck information
        truck['price'] = truck_price
        
        print(f"  Type: {truck_type}, Capacity: {capacity}, Current Load: {current_load}, Price: ${truck_price}")
    
    print("")  # Blank line for better readability between companies

# Save the updated JSON data back to file
with open('transportation_companies_generated.json', 'w') as outfile:
    json.dump(data, outfile, indent=2)

print("JSON file updated successfully.")
