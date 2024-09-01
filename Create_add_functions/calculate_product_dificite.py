import json
import os

def compute_product_deficit_inplace(json_file):
    # Construct the full path to the JSON file
    file_path = os.path.join(os.path.dirname(__file__), json_file)

    # Load JSON data from input file
    with open(file_path, 'r+') as file:
        data = json.load(file)
        
        # Iterate over each city in the data
        for city in data['cities']:
            # Iterate over each product in the city
            for product in city['products']:
                # Compute deficit for the product
                deficit = product['required_quantity'] - product['quantity']
                # Store the computed deficit in the product
                product['deficit'] = deficit
        
        # Reset file pointer to the beginning of the file
        file.seek(0)
        
        # Write updated JSON data back to the same file
        json.dump(data, file, indent=4)
        
        # Truncate the file in case the new content is shorter than the original content
        file.truncate()

if __name__ == '__main__':
    # Specify the relative path to the JSON file within the data directory
    json_filename = '../../data/city_products_data_updated.json'
    
    # Call the function to compute and update deficits in the specified JSON file
    compute_product_deficit_inplace(json_filename)
    
    print(f"Deficits computed and updated directly in '{json_filename}'.")