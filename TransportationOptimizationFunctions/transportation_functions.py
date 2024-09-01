from classes.project_classes import haversine_distance,GeneralGraphSearch,CityNode
from collections import deque
from Auxiliary_Functions_Visualization.load_update_plot import plot_path_on_map,update_city_product_api

def find_product_with_highest_total_deficitt(cities_data):
    max_deficit_product = None
    max_deficit_amount = float('-inf')

    for city in cities_data['cities']:
        for product in city['products']:
            if 'deficit' in product:
                if product['deficit'] > max_deficit_amount:
                    max_deficit_amount = product['deficit']
                    max_deficit_product = product

    return max_deficit_product

def find_product_with_highest_total_deficit(cities_data, season):
    max_deficit_product = None
    max_deficit_amount = float('-inf')

    for city in cities_data['cities']:
        for product in city['products']:
            if 'deficit' in product and product['season'] == season:
                if product['deficit'] > max_deficit_amount:
                    max_deficit_amount = product['deficit']
                    max_deficit_product = product

    return max_deficit_product


def find_product_index_by_name(products, product_name):
    """
    Find the index of a product with a given name in a list of products.

    Args:
        products (list): List of products.
        product_name (str): Name of the product to search for.

    Returns:
        int or None: Index of the product if found, or None if not found.
    """
    for index, product in enumerate(products):
        if product['name'] == product_name:
            return index
    return None  # Product not found in the list
  

def find_city_with_highest_deficit(data, product_name):
    max_product_deficit = float('-inf')  # Initialize with a very small value
    city_with_max_deficit = None
    
    for city in data['cities']:
        product_found = next((product for product in city['products'] if product['name'] == product_name), None)
        if product_found and 'deficit' in product_found:
            product_deficit = product_found['deficit']
            if product_deficit > max_product_deficit:
                max_product_deficit = product_deficit
                city_with_max_deficit = city
                
    return city_with_max_deficit

def find_nearest_city_for_product_need(city_name, product_name, cities_data):
    """Find the nearest city with a surplus of the specified product to fulfill the deficit."""
    target_city = None
    target_product = None
    nearest_city = None  # Initialize nearest_city

    # Find the target city and product within the cities_data
    for city in cities_data['cities']:
        if city['name'] == city_name:
            target_city = city
            for product in city['products']:
                if product['name'] == product_name and product['deficit'] > 0:
                    target_product = product
                    break
            break

    # If the target city or product is not found, return None
    if not target_city or not target_product:
        print(f"No suitable city or product found for {city_name} and {product_name}.")
        return None, None, None  # Return None for all variables

    # Initialize a queue for BFS [(current_city, current_distance, path)]
    queue = deque()
    visited = set()
    visited.add(city_name)  # Mark the starting city as visited

    # Enqueue neighboring cities (cities connected by routes) of the target city
    for neighbor_name, neighbor_distance in target_city['routes']:
        for neighbor_city in cities_data['cities']:
            if neighbor_city['name'] == neighbor_name:
                queue.append((neighbor_city, neighbor_distance, [city_name, neighbor_name]))

    # Perform BFS to find the nearest city with a surplus of the specified product
    while queue:
        current_city, current_distance, path = queue.popleft()

        # Check if the current city has a surplus of the specified product
        for product in current_city['products']:
            if product['name'] == product_name and product['deficit'] < 0:  # Check for surplus
                return current_city, path, current_distance

        # Enqueue neighboring cities of the current city if not visited
        for neighbor_name, neighbor_distance in current_city['routes']:
            for neighbor_city in cities_data['cities']:
                if neighbor_city['name'] == neighbor_name and neighbor_city['name'] not in visited:
                    visited.add(neighbor_city['name'])
                    queue.append((neighbor_city, current_distance + neighbor_distance, path + [neighbor_name]))

    # If no suitable city is found, print message and return None for all variables
    print("No suitable city found to fulfill product need.")
    return None, None, None

def find_nearest_company_to_city(city, companies_data):
    """ Find the nearest delivery company to a given city. """
    nearest_company = None
    nearest_distance = float('inf')
    
    city_lat = float(city['latitude'])
    city_lon = float(city['longitude'])
    
    for company in companies_data['companies']:
        company_city_name = company['city_name']
        for truck in company['trucks']:
            # Calculate distance between company location and given city
            company_lat = float(company['latitude'])
            company_lon = float(company['longitude'])
            distance = haversine_distance(city_lat, city_lon, company_lat, company_lon)
            if distance < nearest_distance:
                nearest_company = company
                nearest_distance = distance
    
    return nearest_company

def select_best_truck_for_product(nearest_company, product_name, product_quantity):
    best_truck = None
    min_price = float('inf')
    
    for truck in nearest_company['trucks']:
        if truck['capacity'] >= product_quantity and truck['price'] < min_price:
            best_truck = truck
            best_truck['company_city'] = nearest_company['city_name']  # Include company city in truck info
            min_price = truck['price']
    
    return best_truck


def perform_transportation(best_truck, nearest_city, city_in_need, product_name, cities_data, type_of_search):
    company_city_name = best_truck['company_city']
    graph_search = GeneralGraphSearch()
    city_names = [city['name'] for city in cities_data['cities']]

    if company_city_name not in city_names:
        print(f"Error: '{company_city_name}' not found in cities_data. Check city names and data consistency.")
        return

    company_city = next(city for city in cities_data['cities'] if city['name'] == company_city_name)

    nearest_city_product = next(product for product in nearest_city['products'] if product['name'] == product_name)
    city_in_need_product = next(product for product in city_in_need['products'] if product['name'] == product_name)

    deficit_to_transport = min(best_truck['capacity'], -nearest_city_product['deficit'], city_in_need_product['deficit'])
    transported_quantity = abs(deficit_to_transport)

    nearest_city_product['deficit'] += transported_quantity
    nearest_city_product['quantity'] -= transported_quantity
    city_in_need_product['deficit'] -= transported_quantity
    city_in_need_product['quantity'] += transported_quantity

    start_city_node = CityNode(company_city_name, float(company_city['latitude']), float(company_city['longitude']))
    goal_city_node = CityNode(nearest_city['name'], float(nearest_city['latitude']), float(nearest_city['longitude']))

    search_function = None

    if type_of_search == "A*":
        search_function = graph_search.a_star_search
    elif type_of_search == "DFS":
        search_function = graph_search.dfs_search
    elif type_of_search == "BFS":
        search_function = graph_search.bfs
    elif type_of_search == "Hill Climbing":
        search_function = graph_search.hill_climbing_steepest_ascent
    elif type_of_search == "Simulated Annealing":
        search_function = GeneralGraphSearch.simulated_annealing
    else:
        print("Invalid type of search. Please choose from 'A*', 'DFS', 'Hill Climbing', 'BFS', or 'Simulated Annealing'.")
        return

    if search_function:
        if type_of_search == "Simulated Annealing":
            # Parameters for simulated annealing
            initial_temperature = 1000
            cooling_rate = 0.003
            max_iterations = 1000
            
            result_nearest_city = search_function(start_city_node, goal_city_node, cities_data, initial_temperature, cooling_rate, max_iterations)
        else:
            result_nearest_city = search_function(start_city_node, goal_city_node, cities_data)

        if result_nearest_city:
            path_to_nearest_city, total_distance_to_nearest_city = result_nearest_city[:2]
            if isinstance(path_to_nearest_city[0], str):  # Check if the path is a list of strings
                print(f"Path to nearest city: {' -> '.join(path_to_nearest_city)}")
            else:  
                # If the path is a list of tuples, extract the city names
                print(f"Path to nearest city: {' -> '.join(city[0] for city in path_to_nearest_city)}")
            print(f"    Total distance: {round(total_distance_to_nearest_city, 2)}")

            start_city_node = goal_city_node
            goal_city_node = CityNode(city_in_need['name'], float(city_in_need['latitude']), float(city_in_need['longitude']))

            if type_of_search == "Simulated Annealing":
                result_city_in_need = search_function(start_city_node, goal_city_node, cities_data, initial_temperature, cooling_rate, max_iterations)
            else:
                result_city_in_need = search_function(start_city_node, goal_city_node, cities_data)

            if result_city_in_need:
                path_to_city_in_need, total_distance_to_city_in_need = result_city_in_need[:2]
                if isinstance(path_to_city_in_need[0], str):  # Check if the path is a list of strings
                    print(f"Path to city in need: {' -> '.join(path_to_city_in_need)}")
                else:  # If the path is a list of tuples, extract the city names
                    print(f"Path to city in need: {' -> '.join(city[0] for city in path_to_city_in_need)}")
                print(f"    Total distance: {round(total_distance_to_city_in_need, 2)}")

                update_city_product_api(cities_data)

                start_city_node = goal_city_node
                goal_city_node = CityNode(company_city_name, float(company_city['latitude']), float(company_city['longitude']))

                if type_of_search == "Simulated Annealing":
                    result_company_city = search_function(start_city_node, goal_city_node, cities_data, initial_temperature, cooling_rate, max_iterations)
                else:
                    result_company_city = search_function(start_city_node, goal_city_node, cities_data)
                    
                if result_company_city:
                    if len(result_company_city) == 3:
                        path_to_company_city, total_distance_to_company_city, path = result_company_city
                    else:
                        path_to_company_city, total_distance_to_company_city = result_company_city[:2]

                    # Debugging print statements
                    if isinstance(path_to_company_city[0], str):  
                        print(f"Path of return: {' -> '.join(path_to_company_city)}")
                    else:  
                        print(f"Path of return: {' -> '.join(city[0] for city in path_to_company_city)}")
                    print(f"    Total distance: {round(total_distance_to_company_city, 2)}")

                    # Concatenate the paths
                    full_path = [path_to_nearest_city, path_to_city_in_need, path_to_company_city]
                    colors = ['red', 'blue', 'green']
                    print("Full path of transportation:",full_path)

                    # Visualize the full path
                    plot_path_on_map(full_path,colors, cities_data)
                else:
                    print("Error: Could not find a path from company city to nearest city.")
            else:
                print("Error: Could not find a path from nearest city to city in need.")
        else:
            print("Error: Could not find a path from company city to nearest city.")
    else:
        print("Error: Search function not found.")

