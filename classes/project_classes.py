
import random
import math
from collections import deque
import heapq


def haversine_distance(lat1, lon1, lat2, lon2):
    """ Calculate the Haversine distance between two points given by latitude and longitude. """
    R = 6371  # Radius of the Earth in kilometers
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    
    a = math.sin(delta_phi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    distance = R * c
    return distance

class CityNode:
    def __init__(self, name, latitude, longitude):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.g = float('inf')  # Initialize g to infinity #
        self.parent = None
        self.distance = 0  
    
    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return isinstance(other, CityNode) and \
               self.name == other.name and \
               self.latitude == other.latitude and \
               self.longitude == other.longitude

    
class GeneralGraphSearch:
    @staticmethod
    def a_star_search(start_city_node, goal_city_node, city_lookup):
        open_list = []
        closed_set = set()

        start_city_node.g = 0
        start_city_node.h = haversine_distance(start_city_node.latitude, start_city_node.longitude, goal_city_node.latitude, goal_city_node.longitude)
        start_city_node.f = start_city_node.g + start_city_node.h

        heapq.heappush(open_list, (start_city_node.f, start_city_node))

        while open_list:
            current_f, current_city = heapq.heappop(open_list)

            if current_city == goal_city_node:
                # Reconstruct path
                path = []
                total_distance = 0
                while current_city:
                    path.append(current_city.name)  # Append only city names
                    total_distance += current_city.distance
                    current_city = current_city.parent
                path.reverse()
                return path, total_distance  # return the path and the total distance

            closed_set.add(current_city)

            for neighbor_data in city_lookup['cities']:
                neighbor_name = neighbor_data['name']
                neighbor_routes = neighbor_data['routes']

                if neighbor_name == current_city.name:
                    for neighbor_route in neighbor_routes:
                        neighbor_city_name, distance = neighbor_route
                        neighbor_city = CityNode(neighbor_city_name, 0, 0)  # Initialize with name only

                        # Find the actual neighbor_city from city_lookup
                        for city in city_lookup['cities']:
                            if city['name'] == neighbor_city_name:
                                neighbor_city = CityNode(city['name'], float(city['latitude']), float(city['longitude']))
                                break

                        if neighbor_city not in closed_set:
                            tentative_g = current_city.g + distance

                            if tentative_g < neighbor_city.g:
                                neighbor_city.parent = current_city
                                neighbor_city.g = tentative_g
                                neighbor_city.h = haversine_distance(neighbor_city.latitude, neighbor_city.longitude, goal_city_node.latitude, goal_city_node.longitude)
                                neighbor_city.f = neighbor_city.g + neighbor_city.h
                                neighbor_city.distance = distance  # update the distance from the current city to the neighbor
                                heapq.heappush(open_list, (neighbor_city.f, neighbor_city))

        return None, 0  # No path found

    @staticmethod
    def hill_climbing_steepest_ascent(start_city_node, goal_city_node, city_lookup):
        current_city = start_city_node
        total_distance = 0
        path = []

        while current_city != goal_city_node:
            neighbors = []

            for neighbor_data in city_lookup['cities']:
                neighbor_name = neighbor_data['name']
                neighbor_routes = neighbor_data['routes']

                if neighbor_name == current_city.name:
                    for neighbor_route in neighbor_routes:
                        neighbor_city_name, distance = neighbor_route
                        neighbor_city = CityNode(neighbor_city_name, 0, 0)  # Initialize with name only

                        # Find the actual neighbor_city from city_lookup
                        for city in city_lookup['cities']:
                            if city['name'] == neighbor_city_name:
                                neighbor_city = CityNode(city['name'], float(city['latitude']), float(city['longitude']))
                                break

                        neighbors.append((neighbor_city, distance))

            # If there are no neighbors, return None
            if not neighbors:
                return None, total_distance, []

            # Find the neighbor with the shortest distance
            next_city, next_distance = min(neighbors, key=lambda x: x[1])

            # If the next city does not improve the distance, return the current city
            if next_distance >= current_city.distance:
                path.append(current_city.name)
                return current_city, total_distance, path

            # Move to the next city
            current_city = next_city
            total_distance += next_distance
            path.append(current_city.name)

        path.append(goal_city_node.name)
        return current_city, total_distance, path

    @staticmethod
    def dfs_search(start_city_node, goal_city_node, city_lookup):
        stack = [start_city_node]  # Store nodes to visit
        visited = set()  # Initialize the visited set

        while stack:
            current_city = stack.pop()

            if current_city == goal_city_node:
                # Reconstruct path
                path = []
                total_distance = 0
                while current_city:
                    path.append(current_city.name)  # Append only city names
                    total_distance += current_city.distance
                    current_city = current_city.parent
                path.reverse()
                return path, total_distance  # Return the path and the total distance

            if current_city not in visited:
                visited.add(current_city)

                for neighbor_data in city_lookup['cities']:
                    neighbor_name = neighbor_data['name']
                    neighbor_routes = neighbor_data['routes']

                    if neighbor_name == current_city.name:
                        for neighbor_route in neighbor_routes:
                            neighbor_city_name, distance = neighbor_route
                            neighbor_city = None

                            # Find the actual neighbor_city from city_lookup
                            for city in city_lookup['cities']:
                                if city['name'] == neighbor_city_name:
                                    neighbor_city = CityNode(city['name'], float(city['latitude']), float(city['longitude']))
                                    neighbor_city.distance = distance  # Store the distance from the current city to the neighbor
                                    break

                            if neighbor_city and neighbor_city not in visited:
                                neighbor_city.parent = current_city
                                stack.append(neighbor_city)  # Update the stack with the neighbor city

        return None, 0  # No path found

    @staticmethod
    def bfs(start_city_node, goal_city_node, city_lookup):
        open_queue = deque()
        closed_set = set()

        open_queue.append(start_city_node)

        while open_queue:
            current_city = open_queue.popleft()

            if current_city == goal_city_node:
                # Reconstruct path
                path = []
                total_distance = 0
                while current_city:
                    path.append(current_city.name)  # Append only city names
                    total_distance += current_city.distance
                    current_city = current_city.parent
                path.reverse()
                return path, total_distance  # return the path and the total distance

            closed_set.add(current_city)

            for neighbor_data in city_lookup['cities']:
                neighbor_name = neighbor_data['name']
                neighbor_routes = neighbor_data['routes']

                if neighbor_name == current_city.name:
                    for neighbor_route in neighbor_routes:
                        neighbor_city_name, distance = neighbor_route
                        neighbor_city = CityNode(neighbor_city_name, 0, 0)  # Initialize with name only

                        # Find the actual neighbor_city from city_lookup
                        for city in city_lookup['cities']:
                            if city['name'] == neighbor_city_name:
                                neighbor_city = CityNode(city['name'], float(city['latitude']), float(city['longitude']))
                                break

                        if neighbor_city not in closed_set and neighbor_city not in open_queue:
                            neighbor_city.parent = current_city
                            neighbor_city.distance = distance  # update the distance from the current city to the neighbor
                            open_queue.append(neighbor_city)

        return None, 0  # No path found

    @staticmethod
    def simulated_annealing(start_city_node, goal_city_node, city_lookup, initial_temperature, cooling_rate, max_iterations):
        current_node = start_city_node
        current_distance = 0
        temperature = initial_temperature
        
        # Initialize best solution
        best_node = start_city_node
        best_distance = float('inf')
        
        for iteration in range(max_iterations):
            # Generate a neighboring solution by randomly selecting a neighboring city
            neighbor_data = random.choice(city_lookup['cities'])
            neighbor_name = neighbor_data['name']
            neighbor_routes = neighbor_data['routes']
            
            neighbor_city = None
            for city in city_lookup['cities']:
                if city['name'] == neighbor_name:
                    neighbor_city = CityNode(city['name'], float(city['latitude']), float(city['longitude']))
                    break
            
            # Calculate the distance to the neighbor
            distance = None
            for neighbor_route in neighbor_routes:
                if neighbor_route[0] == current_node.name:
                    distance = neighbor_route[1]
                    break
            
            if distance is None:
                # Handle the case when distance is not found
                continue
                    
            # Update the current node and distance
            new_node = neighbor_city
            new_node.parent = current_node  # Update the parent attribute
            new_distance = current_distance + distance
            
            # Calculate the change in cost (distance)
            delta_distance = new_distance - current_distance
            
            # Accept the neighbor if it leads to a better solution or with a probability based on temperature
            if delta_distance < 0 or random.random() < math.exp(-delta_distance / temperature):
                current_node = new_node
                current_node.distance = distance  # Update the distance attribute of the current node
                current_distance = new_distance
            
            # Update the best solution if needed
            if current_distance < best_distance:
                best_node = current_node
                best_distance = current_distance
            
            # Decrease the temperature
            temperature *= cooling_rate
        
        # Reconstruct path
        path = []
        total_distance = 0
        while current_node:
            path.append(current_node.name)  # Append only city names
            total_distance += current_node.distance  # Use the distance attribute of CityNode
            current_node = current_node.parent
        path.reverse()
        
        return path, total_distance
