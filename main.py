import os
import sys
import gui

from Auxiliary_Functions_Visualization.load_update_plot import load_json_data
from supply_chain import Supply_and_Chain_solution

sys.path.append(os.path.join(os.path.dirname(__file__), 'utility_functions'))
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





if __name__ == "__main__":
    
    while True:
        print('-'*60)
        print("Welcome to the Supply Chain Management System!")
        print('-'*60)

        print("1. Start the program")
        print("2. Exit")
        choice = input("Enter your value: ")
        print('-'*60)
        if choice.isdigit() and 1 <= int(choice) <= 2:
            if int(choice) == 1:
                print("- Before starting, choose which season you want to search for the product in:")
                print("1. Summer")
                print("2. Winter")  
                print("3. Spring")
                print("4. Automatically choose the season")
                season = input("Enter your value: ")
                print("-"*60)
                if choice.isdigit() and 1 <= int(choice) <= 5:
                    print("Choose the search algorithm:")
                    print("1. BFS")
                    print("2. DFS")
                    print("3. A*")
                    print("4. Simulated Annealing")
                    search_algorithm = input("Enter your value: ")
                    if choice.isdigit() and 1 <= int(choice) <= 4:
                        print("-"*60)
                        print("result:")
                        Supply_and_Chain_solution(int(season),search_algorithm)
                        print("-"*60)
                    else:
                        print("Invalid search algorithm input. Please enter a valid choice.")
                else:
                    print("Invalid season input. Please enter a valid choice.")
            else:
                print("-"*60)
                print("Supply chain management system terminated.")
                print("-"*60)
                sys.exit()
        else:
            print("Invalid input. Please enter a valid choice.")

        

        