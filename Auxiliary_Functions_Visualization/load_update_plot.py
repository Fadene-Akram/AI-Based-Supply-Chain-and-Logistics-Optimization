import json
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimgt


def load_json_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data  


def update_city_product_api(cities_data):
    # Update the product deficits based on current quantities
    for city in cities_data['cities']:
        for product in city['products']:
            product['deficit'] = product['required_quantity'] - product['quantity']

    # Save the updated cities_data to a JSON file
    with open('updated_cities_data.json', 'w') as f:
        json.dump(cities_data, f, indent=4)


def blend_colors(color1, color2):
    """
    Blend two colors by taking their average.
    """
    if isinstance(color1, str):
        color1 = mcolors.to_rgb(color1)
    if isinstance(color2, str):
        color2 = mcolors.to_rgb(color2)

    r1, g1, b1 = color1
    r2, g2, b2 = color2
    blended_color = [(r1 + r2) / 2, (g1 + g2) / 2, (b1 + b2) / 2]
    return blended_color


def plot_path_on_map(paths, colors, cities_data):
    # Initialize an empty dictionary for city coordinates
    city_coordinates = {}

    # Extract city coordinates from cities_data
    for city in cities_data['cities']:
        city_name = city.get('name')
        longitude = city.get('longitude')
        latitude = city.get('latitude')
        if city_name is not None and longitude is not None and latitude is not None:
            city_coordinates[city_name] = (float(longitude), float(latitude))

    # Plot the paths on the map
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())

    # Add OpenStreetMap background tiles
    request = cimgt.OSM()
    ax.add_image(request, 5, zorder=0)

    # Plot each path segment with its respective color
    for path, color in zip(paths, colors):
        for i in range(len(path) - 1):
            start_city = path[i]
            end_city = path[i + 1]
            start_coordinates = city_coordinates.get(start_city)
            end_coordinates = city_coordinates.get(end_city)
            if start_coordinates is not None and end_coordinates is not None:
                start_lon, start_lat = start_coordinates
                end_lon, end_lat = end_coordinates
                plt.plot([start_lon, end_lon], [start_lat, end_lat], color=color, linewidth=2, transform=ccrs.PlateCarree())

    # Plot the cities (plot each city only once)
    plotted_cities = set()  # To avoid plotting the same city multiple times
    for path in paths:
        for city_name in path:
            if city_name not in plotted_cities:
                city_coordinates_tuple = city_coordinates.get(city_name)
                if city_coordinates_tuple is not None:
                    lon, lat = city_coordinates_tuple
                    plt.plot(lon, lat, 'bo', markersize=6, transform=ccrs.PlateCarree())
                    plt.text(lon, lat, city_name, fontsize=8, ha='left', transform=ccrs.PlateCarree())
                    plotted_cities.add(city_name)

    # Dictionary to keep track of intersecting paths
    intersecting_cities = set()

    # Find intersecting cities
    for i in range(len(paths)):
        for j in range(i + 1, len(paths)):
            common_cities = set(paths[i]) & set(paths[j])
            intersecting_cities.update(common_cities)

    # Blend colors for intersecting paths
    for city in intersecting_cities:
        paths_with_city = [idx for idx, path in enumerate(paths) if city in path]
        if len(paths_with_city) > 1:
            blended_color = blend_colors(*[colors[idx] for idx in paths_with_city[:2]])  # Blend the first two colors
            for idx in paths_with_city:
                if idx not in paths_with_city[:2]:  # Skip the first two paths used for blending
                    colors[idx] = blended_color

    plt.title('Paths on Map')
    plt.savefig('paths_on_map.png')  # Save the plot as an image
    plt.show()