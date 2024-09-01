import os
import sys
import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
from Auxiliary_Functions_Visualization.load_update_plot import load_json_data
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

def print_to_text_widget(text_widget, message):
    text_widget.configure(state='normal')
    text_widget.insert(tk.END, message + '\n')
    text_widget.configure(state='disabled')
    text_widget.see(tk.END)

def supply_chain_solution(season=None, search_algorithm=None, text_widget=None):
    """ the start of main program """
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
    elif season == 4:
        product_with_max_deficit = find_product_with_highest_total_deficit(cities_data, "Autumn")
    else:
        product_with_max_deficit = find_product_with_highest_total_deficitt(cities_data)

    if product_with_max_deficit:
        product_name = product_with_max_deficit['name']
        result_text = f"- Product with highest total deficit: {product_name}\n"
        print_to_text_widget(text_widget, result_text)

        # Find city with the highest deficit for a specific product
        city_with_max_deficit = find_city_with_highest_deficit(cities_data, product_name)
        if city_with_max_deficit:
            city_name = city_with_max_deficit['name']
            result_text = f"- City with highest deficit for {product_name}: {city_name}\n"
            print_to_text_widget(text_widget, result_text)
            try:
                nearest_city, path, total_distance = find_nearest_city_for_product_need(city_name, product_name,
                                                                                         cities_data)
            except Exception as e:
                result_text = "An error occurred: " + str(e) + "\n"
                print_to_text_widget(text_widget, result_text)
            # Find nearest city to fulfill product need
            if nearest_city:
                result_text = f"- Nearest city to fulfill product need: {nearest_city['name']}\n"
                print_to_text_widget(text_widget, result_text)
                result_text = f"    Total distance to nearest city: {round(total_distance, 2)}\n"
                print_to_text_widget(text_widget, result_text)

                # Now perform further operations with 'nearest_city'
                nearest_company = find_nearest_company_to_city(nearest_city, companies_data)
                if nearest_company:
                    result_text = f"- Nearest company for transportation: {nearest_company['name']}\n"
                    print_to_text_widget(text_widget, result_text)

                    # Find the index of the specified product within the city's products
                    products = nearest_city['products']
                    product_index = find_product_index_by_name(products, product_name)

                    if product_index is not None:
                        deficit = products[product_index]['deficit']
                        # Find best truck for the product in this company
                        best_truck = select_best_truck_for_product(nearest_company, product_name, deficit)
                        if best_truck:
                            result_text = "- Best truck selected for transport:\n"
                            print_to_text_widget(text_widget, result_text)
                            result_text = f"  - ID: {best_truck['id']}\n"
                            print_to_text_widget(text_widget, result_text)
                            result_text = f"  - Capacity: {best_truck['capacity']}\n"
                            print_to_text_widget(text_widget, result_text)
                            result_text = f"  - Price: {best_truck['price']}\n"
                            print_to_text_widget(text_widget, result_text)
                            result_text = f"  - Product Quantity: {abs(deficit)}\n"
                            print_to_text_widget(text_widget, result_text)
                            result_text = f"  - Product Name: {product_name}\n"
                            print_to_text_widget(text_widget, result_text)

                            # Perform transportation using A* search
                            if search_algorithm == 1:
                                perform_transportation(best_truck, nearest_city, city_with_max_deficit, product_name,
                                                       cities_data, "BFS")
                            elif search_algorithm == 2:
                                perform_transportation(best_truck, nearest_city, city_with_max_deficit, product_name,
                                                       cities_data, "DFS")
                            elif search_algorithm == 3:
                                perform_transportation(best_truck, nearest_city, city_with_max_deficit, product_name,
                                                       cities_data, "A*")
                            elif search_algorithm == 4:
                                perform_transportation(best_truck, nearest_city, city_with_max_deficit, product_name,
                                                       cities_data, "Simulated Annealing")
                            else:
                                perform_transportation(best_truck, nearest_city, city_with_max_deficit, product_name,
                                                       cities_data, "A*")
                            result_text = "Transportation completed successfully.\n"
                            print_to_text_widget(text_widget, result_text)

                        else:
                            result_text = "No suitable truck found.\n"
                            print_to_text_widget(text_widget, result_text)
                    else:
                        result_text = f"Product '{product_name}' not found in the city's products.\n"
                        print_to_text_widget(text_widget, result_text)
                else:
                    result_text = "No company found near the nearest city.\n"
                    print_to_text_widget(text_widget, result_text)
                pass
            else:
                result_text = "No suitable city found.\n"
                print_to_text_widget(text_widget, result_text)
        else:
            result_text = f"No city found with a deficit for {product_name}.\n"
            print_to_text_widget(text_widget, result_text)
    else:
        result_text = "No product found with a deficit.\n"
        print_to_text_widget(text_widget, result_text)

def start_program():
    season = season_var.get()
    search_algorithm = search_algorithm_var.get()
    supply_chain_solution(season, search_algorithm, result_text_widget)


def exit_program():
    if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
        root.destroy()


root = tk.Tk()
root.title("Supply Chain Management System")

season_var = tk.IntVar()
search_algorithm_var = tk.IntVar()

season_label = tk.Label(root, text="Choose Season:")
season_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
season_radio1 = tk.Radiobutton(root, text="Summer", variable=season_var, value=1)
season_radio1.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)
season_radio2 = tk.Radiobutton(root, text="Winter", variable=season_var, value=2)
season_radio2.grid(row=0, column=2, padx=10, pady=5, sticky=tk.W)
season_radio3 = tk.Radiobutton(root, text="Spring", variable=season_var, value=3)
season_radio3.grid(row=0, column=3, padx=10, pady=5, sticky=tk.W)
season_radio4 = tk.Radiobutton(root, text="Autumn", variable=season_var, value=4)
season_radio4.grid(row=0, column=4, padx=10, pady=5, sticky=tk.W)
season_radio5 = tk.Radiobutton(root, text="Automatically choose", variable=season_var, value=5)
season_radio5.grid(row=0, column=5, padx=10, pady=5, sticky=tk.W)

search_algorithm_label = tk.Label(root, text="Choose Search Algorithm:")
search_algorithm_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
search_algorithm_radio1 = tk.Radiobutton(root, text="BFS", variable=search_algorithm_var, value=1)
search_algorithm_radio1.grid(row=1, column=1, padx=10, pady=5, sticky=tk.W)
search_algorithm_radio2 = tk.Radiobutton(root, text="DFS", variable=search_algorithm_var, value=2)
search_algorithm_radio2.grid(row=1, column=2, padx=10, pady=5, sticky=tk.W)
search_algorithm_radio3 = tk.Radiobutton(root, text="A*", variable=search_algorithm_var, value=3)
search_algorithm_radio3.grid(row=1, column=3, padx=10, pady=5, sticky=tk.W)
search_algorithm_radio4 = tk.Radiobutton(root, text="Simulated Annealing", variable=search_algorithm_var, value=4)
search_algorithm_radio4.grid(row=1, column=4, padx=10, pady=5, sticky=tk.W)

start_button = tk.Button(root, text="Start", command=start_program)
start_button.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)

result_text_widget = ScrolledText(root, height=10, width=50)
result_text_widget.grid(row=3, column=0, columnspan=6, padx=10, pady=5, sticky=tk.W)

exit_button = tk.Button(root, text="Exit", command=exit_program)
exit_button.grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)

root.mainloop()