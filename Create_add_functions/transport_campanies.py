import json

def update_truck_ids(json_data):
    last_truck_id = 0
    
    # Iterate over each company in the JSON data
    for company in json_data["companies"]:
        trucks = company["trucks"]
        
        # Update truck IDs starting from the last recorded ID
        for truck in trucks:
            last_truck_id += 1
            truck["id"] = last_truck_id
            
    return json_data

# Load JSON data from file
with open('transportation_companies_generated.json', 'r') as file:
    data = json.load(file)

# Update truck IDs in the JSON data
updated_data = update_truck_ids(data)

# Write the updated JSON data back to the file
with open('transportation_companies_generated_updated.json', 'w') as file:
    json.dump(updated_data, file, indent=4)

print("Truck IDs updated successfully.")
