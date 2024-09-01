import os
from Auxiliary_Functions_Visualization.load_update_plot import load_json_data
from TransportationOptimizationFunctions.transportation_functions import (
    find_product_with_highest_total_deficitt,
    find_product_with_highest_total_deficit,
    find_city_with_highest_deficit,
    find_nearest_city_for_product_need,
    find_product_index_by_name,
    find_nearest_company_to_city,
    select_best_truck_for_product,
    perform_transportation
)


def Supply_and_Chain_solution(season=None,search_algorithm=None):

    """ the start of main progranm """
    # Specify the paths to the JSON data files
    current_dir = os.path.dirname(os.path.realpath(__file__))
    cities_data_file = os.path.join(current_dir, 'updated_cities_data.json')
    companies_data_file = os.path.join(current_dir, 'data/transportation_companies.json')

    # Load cities and companies data from JSON files
    cities_data = load_json_data(cities_data_file)
    companies_data = load_json_data(companies_data_file)

    # Find product with the highest total deficit
    if season == 1:
        product_with_max_deficit = find_product_with_highest_total_deficit(cities_data, "Summer")
    elif season == 2:
        product_with_max_deficit = find_product_with_highest_total_deficit(cities_data, "Winter")
    elif season == 3:
        product_with_max_deficit = find_product_with_highest_total_deficit(cities_data, "Spring")
    else:
        product_with_max_deficit = find_product_with_highest_total_deficitt(cities_data)

    if product_with_max_deficit:
        product_name = product_with_max_deficit['name']
        print(f"- Product with highest total deficit: {product_name}")

        # Find city with the highest deficit for a specific product
        city_with_max_deficit = find_city_with_highest_deficit(cities_data, product_name)
        if city_with_max_deficit:
            city_name = city_with_max_deficit['name']
            print(f"- City with highest deficit for {product_name}: {city_name}")
            try:
                nearest_city, path, total_distance = find_nearest_city_for_product_need(city_name, product_name, cities_data)
            except Exception as e:
                print("An error occurred:", e)
            # Find nearest city to fulfill product need
            if nearest_city:
                print(f"- Nearest city to fulfill product need: {nearest_city['name']}")
                print(f"    Total distance to nearest city: {round(total_distance, 2)}")

                # Now perform further operations with 'nearest_city'
                nearest_company = find_nearest_company_to_city(nearest_city, companies_data)
                if nearest_company:
                    print(f"- Nearest company for transportation: {nearest_company['name']}")

                    # Find the index of the specified product within the city's products
                    products = nearest_city['products']
                    product_index = find_product_index_by_name(products, product_name)

                    if product_index is not None:
                        deficit = products[product_index]['deficit']
                        # Find best truck for the product in this company
                        best_truck = select_best_truck_for_product(nearest_company, product_name, deficit)
                        if best_truck:
                            print(f"- Best truck selected for transport:")
                            print(f"  - ID: {best_truck['id']}")
                            print(f"  - Capacity: {best_truck['capacity']}")
                            print(f"  - Price: {best_truck['price']}")
                            print(f"  - Product Quantity: {abs(deficit)}")
                            print(f"  - Product Name: {product_name}")

                            # Perform transportation using A* search
                            if search_algorithm == 1:
                                perform_transportation(best_truck, nearest_city, city_with_max_deficit, product_name, cities_data,"BFS")
                            elif search_algorithm == 2:
                                perform_transportation(best_truck, nearest_city, city_with_max_deficit, product_name, cities_data,"DFS")
                            elif search_algorithm == 3:
                                perform_transportation(best_truck, nearest_city, city_with_max_deficit, product_name, cities_data,"A*")
                            elif search_algorithm == 4:
                                perform_transportation(best_truck, nearest_city, city_with_max_deficit, product_name, cities_data,"Simulated Annealing")
                            else:
                                perform_transportation(best_truck, nearest_city, city_with_max_deficit, product_name, cities_data,"A*")
                            print("Transportation completed successfully.")
                            
                        else:
                            print("No suitable truck found.")
                    else:
                        print(f"Product '{product_name}' not found in the city's products.")
                else:
                    print("No company found near the nearest city.")
                pass
            else:
                print("No suitable city found.")
        else:
            print(f"No city found with a deficit for {product_name}.")
    else:
        print("No product found with a deficit.")