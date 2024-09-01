import json
import random

# Define the list of products with their attributes
products = [
    {
        "name": "Wheat",
        "quantity": 1000,
        "season": "Winter",
        "required_quantity": 500
    },
    {
        "name": "Potatoes",
        "quantity": 800,
        "season": "Spring",
        "required_quantity": 400
    },
    {
        "name": "Dates",
        "quantity": 1200,
        "season": "Summer",
        "required_quantity": 600
    },
    {
        "name": "Tomatoes",
        "quantity": 1500,
        "season": "Summer",
        "required_quantity": 700
    },
    {
        "name": "Citrus",
        "quantity": 2000,
        "season": "Winter",
        "required_quantity": 1000
    }
]

# Define the number of cities
num_cities = 58

# Create a list to store city data
cities = []

# Generate random product data for each city
for i in range(num_cities):
    city_name = f"City_{i+1}"
    city_products = []
    
    for product in products:
        # Randomly adjust the quantity of each product for the city
        min_quantity = max(0, product["required_quantity"] - 200)  # Ensure a minimum amount is available
        max_quantity = product["required_quantity"] + 200
        quantity = random.randint(min_quantity, max_quantity)
        
        # Adjust the season based on the city's index (odd/even)
        season = product["season"]
        if i % 2 == 0:
            season = "Winter" if season != "Winter" else "Summer"
        
        # Create product data for the city
        city_products.append({
            "name": product["name"],
            "quantity": quantity,
            "season": season,
            "required_quantity": product["required_quantity"]
        })
    
    # Append city data to the list
    cities.append({
        "name": city_name,
        "products": city_products
    })

# Create dictionary for all cities
city_data = {
    "cities": cities
}

# Define the file path to save the JSON data
file_path = "../../updated_cities_data.json"

# Write the JSON data to the file
with open(file_path, "w") as json_file:
    json.dump(city_data, json_file, indent=4)

print(f"City product data saved to {file_path}")
