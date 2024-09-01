import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import main  # Import the main script
import sys

photo = None  # Define the photo variable globally

class TextRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, message):
        self.text_widget.insert(tk.END, message)
        self.text_widget.see(tk.END)  # Automatically scroll to the end

    def flush(self):
        pass  # Not needed for this use case

def run_main():
    season_map = {
        "Summer": 1,
        "Winter": 2,
        "Spring": 3,
        "Automatically": 4
    }
    algorithm_map = {
        "BFS": 1,
        "DFS": 2,
        "A*": 3,
        "Simulated Annealing": 4
    }
    season = season_map[season_var.get()]
    search_algorithm = algorithm_map[algorithm_var.get()]
    output_text.delete(1.0, tk.END)  # Clear previous output

    # Redirect stdout to the text widget
    old_stdout = sys.stdout
    sys.stdout = TextRedirector(output_text)

    # Call the Supply_and_Chain_solution function from main.py
    try:
        main.Supply_and_Chain_solution(season, search_algorithm)
    except Exception as e:
        output_text.insert(tk.END, f"An error occurred: {e}\n")

    # Restore stdout
    sys.stdout = old_stdout

def show_image():
    global photo  # Use the globally defined photo variable
    image_path = "paths_on_map.png"
    if os.path.exists(image_path):
        image = Image.open(image_path)
        resized_image = image.resize((500, 500), Image.LANCZOS)  # Resize the image to 500x500 pixels
        photo = ImageTk.PhotoImage(resized_image)

        # Clear existing image labels in the image frame but keep the button
        for widget in image_frame.winfo_children():
            if isinstance(widget, ttk.Label) and hasattr(widget, 'image'):
                widget.destroy()

        # Create the image label and pack it into the image frame
        image_label = ttk.Label(image_frame, image=photo)
        image_label.image = photo  # Keep a reference to the image to prevent it from being garbage collected
        image_label.pack(pady=10, padx=(0, 20), side=tk.RIGHT)  # Align to the right (east)

        # Ensure the "Show Image" button is at the top
        show_image_button.lift()
    else:
        output_text.insert(tk.END, "Image not found!\n")

def exit_program():
    root.destroy()

# Create the main window
root = tk.Tk()
root.title("Supply Chain Management System")

# Dark mode colors
bg_color = "#b0b3b8"
fg_color = "#18191a"
button_bg_color = "#3a3b3c"
button_fg_color = "#ffffff"
entry_bg_color = "#3e3e3e"
entry_fg_color = "#ffffff"
hover_color = "#ffffff"  # Color when hovered
hover_text_color = "#3a3b3c"  # Text color when hovered

# Apply the dark mode colors
style = ttk.Style()
style.theme_use('clam')

style.configure("TFrame", background=bg_color)
style.configure("TLabel", background=bg_color, foreground=fg_color)
style.configure("TButton", background=button_bg_color, foreground=button_fg_color)
style.configure("TOptionMenu", background=entry_bg_color, foreground=entry_fg_color)
style.configure("TText", background=entry_bg_color, foreground=entry_fg_color)

root.configure(bg=bg_color)

# Get screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate 80% of screen width and height
window_width = int(screen_width * 0.8)
window_height = int(screen_height * 0.8)

# Calculate position to center the window
position_x = (screen_width // 2) - (window_width // 2)
position_y = (screen_height // 2) - (window_height // 2)

# Set the window size and position
root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

# Custom label spanning the entire width with colored background
custom_label = tk.Label(root, text="Welcome to Supply Chain Management System", font=("Helvetica", 16),
                        background="#3a3b3c", foreground="#ffffff", height=2)  # Increased height
custom_label.pack(fill=tk.X, padx=10, pady=10)

# Frame for the main content
main_frame = ttk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)

# Frame for the left part (selection and text widget)
left_frame = ttk.Frame(main_frame, padding=(10, 10))
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Season selection
season_label = ttk.Label(left_frame, text="Select Season:", font=("Helvetica", 13))  # Match font size
season_label.grid(row=0, column=0, sticky="w", padx=(20, 40), pady=(20, 10))  # Increased padding and space
season_var = tk.StringVar()
season_var.set("Automatically")  # Default to "Automatically"
season_options = ["Summer", "Winter", "Spring", "Automatically"]
season_menu = ttk.OptionMenu(left_frame, season_var, season_options[3], *season_options)
season_menu.grid(row=0, column=1, sticky="w")

# Search algorithm selection
algorithm_label = ttk.Label(left_frame, text="Select Search Algorithm:", font=("Helvetica", 13))  # Match font size
algorithm_label.grid(row=1, column=0, sticky="w", padx=(20, 40), pady=(10, 20))  # Increased padding and space
algorithm_var = tk.StringVar()
algorithm_var.set("A*")  # Default to A*
algorithm_options = ["BFS", "DFS", "A*", "Simulated Annealing"]
algorithm_menu = ttk.OptionMenu(left_frame, algorithm_var, algorithm_options[2], *algorithm_options)
algorithm_menu.grid(row=1, column=1, sticky="w")

# Output text widget
output_text = tk.Text(left_frame, height=20, width=50, bg=entry_bg_color, fg=entry_fg_color)
output_text.grid(row=2, column=0, columnspan=2, pady=10, sticky="nsew")

left_frame.grid_rowconfigure(2, weight=1)
left_frame.grid_columnconfigure(1, weight=1)

# Frame for the buttons
button_frame = ttk.Frame(left_frame, padding=(0, 20))
button_frame.grid(row=3, column=0, columnspan=2, pady=(20, 0))

# Start button
start_button = ttk.Button(button_frame, text="Start Program", command=run_main)
start_button.grid(row=0, column=0, padx=(0, 40))

# Exit button
exit_button = ttk.Button(button_frame, text="Exit", command=exit_program)
exit_button.grid(row=0, column=1)

# Apply hover color and text color
style.map("TButton",
          background=[('active', hover_color)],
          foreground=[('active', hover_text_color)])

# Vertical separator
separator = ttk.Frame(main_frame, width=2, relief=tk.SUNKEN)
separator.pack(side=tk.LEFT, fill=tk.Y, padx=5)

# Frame for the right part (image)
right_frame = ttk.Frame(main_frame, padding=(10, 10))
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Frame to contain the image label and the "Show Image" button
image_frame = ttk.Frame(right_frame)
image_frame.pack(pady=10, fill=tk.BOTH, expand=True)

# Button to show image
show_image_button = ttk.Button(image_frame, text="Show Image", command=show_image)
show_image_button.pack(pady=10, padx=10)  # Added padding

# Image label
image_label = ttk.Label(image_frame)

root.mainloop()
