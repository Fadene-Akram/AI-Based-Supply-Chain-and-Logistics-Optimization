import json
import random
import os

# Function to generate a random price within a specified range for a product
def generate_random_price(min_price, max_price):
    return round(random.uniform(min_price, max_price), 2)

# Define price ranges for each product
product_price_ranges = {
    "Wheat": (50, 60),    # Example price range for Wheat (in dollars per unit)
    "Potatoes": (50, 80), # Example price range for Potatoes
    "Dates": (300, 650),    # Example price range for Dates
    "Tomatoes": (45, 70), # Example price range for Tomatoes
    "Citrus": (80, 130)    # Example price range for Citrus
}

# Load the JSON data from file
current_dir = os.path.dirname(os.path.abspath(__file__))
json_file_path = os.path.join(current_dir, '..', '..', 'data', 'city_products_data_updated.json')

# Load the JSON data from file
with open(json_file_path, 'r') as f:
    data = json.load(f)

# Access the list of cities
cities = data['cities']

# Iterate over each city
for city in cities:
    # Access products information for the city
    products = city['products']
    for product in products:
        product_name = product['name']
        if product_name in product_price_ranges:
            min_price, max_price = product_price_ranges[product_name]
            unit_price = generate_random_price(min_price, max_price)
        else:
            # Default price range if product not found in the specified ranges
            min_price, max_price = (0.5, 2.0)
            unit_price = generate_random_price(min_price, max_price)
        
        # Add or update unit price to the product information
        product['unit_price'] = unit_price

# Save the updated JSON data back to file
with open(json_file_path, 'w') as outfile:
    json.dump(data, outfile, indent=2)

print("JSON file updated successfully.")
