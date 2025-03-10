from idlelib.history import History
from operator import index
import tkinter as tk
from tkinter import messagebox
import csv
import math

# Calculation functions
def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y == 0:
        return "Error! Division by zero"
    return x / y

# GUI Application
class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Calculator")
        self.history = []
        # Track scientific mode
        self.scientific_mode = False
        self.dark_mode = False  # Track the dark mode

        # Theme colors
        self.light_theme = {
            "bg": "#FFFFFF",
            "fg": "#000000",
            "button_bg": "#E0E0E0",
            "button_fg": "#000000",
        }

        self.dark_theme = {
            "bg": "#2E2E2E",
            "fg": "#FFFFFF",
            "button_bg": "#424242",
            "button_fg": "#FFFFFF",
        }

        # Input and result display
        self.display = tk.Entry(root, font=("Arial", 20), justify="right", bd=10, insertwidth=4)
        self.display.grid(row=0, column=0, columnspan=6)

        # Buttons for basic mode
        basic_buttons = [
            '7', '8', '9', '/', 'C', 'History',
            '4', '5', '6', '*', '(', ')',
            '1', '2', '3', '-', 'π', 'e',
            '0', '.', '=', '+', '√', '^',
            'sin', 'cos', 'tan', 'Export', 'Import', 'Mode', 'Theme', 'Help', 'Convert'
        ]

        # Create buttons
        self.buttons = {}
        row = 1
        col = 0
        for button in basic_buttons:
            action = lambda x=button: self.on_button_click(x)
            self.buttons[button] = tk.Button(root, text=button, font=("Arial", 15), width=5, height=2, command=action)
            self.buttons[button].grid(row=row, column=col)
            col += 1
            if col > 5:
                col = 0
                row += 1

        # Hide scientific buttons initially
        self.toggle_scientific_buttons()
        # Apply initial theme
        self.apply_theme()

    def on_button_click(self, value):
        if value == '=':
            try:
                expression = self.display.get()
                result = str(eval(expression))
                self.history.append(f"{expression} = {result}")
                self.display.delete(0, tk.END)
                self.display.insert(0, result)
            except Exception as e:
                messagebox.showerror("Error", "Invalid input!")
        elif value == 'C':
            self.display.delete(0, tk.END)
        elif value == 'History':
            self.show_history()  # display_history
        elif value == 'Export':
            self.export_history()
        elif value == 'Import':
            self.import_history()
        elif value == 'Mode':
            self.scientific_mode = not self.scientific_mode
            self.toggle_scientific_buttons()
        elif value == 'Theme':
            self.dark_mode = not self.dark_mode
            self.apply_theme()
        elif value == 'Help':
            self.show_help()
        elif value == '√':
            self.display.insert(tk.END, 'math.sqrt(')
        elif value == '^':
            self.display.insert(tk.END, '**')
        elif value == 'π':
            self.display.insert(tk.END, str(math.pi))
        elif value == 'e':
            self.display.insert(tk.END, str(math.e))
        elif value in ['sin', 'cos', 'tan']:
            self.display.insert(tk.END, f'math.{value}(')
        elif value == 'Convert':
            self.convert_temperature()
        else:
            self.display.insert(tk.END, value)

    # Toggle scientific button
    def toggle_scientific_buttons(self):
        # Show/hide scientific buttons based on mode
        scientific_buttons = ['√', '^', 'sin', 'cos', 'tan', 'π', 'e']
        for button in scientific_buttons:
            if button in self.buttons:  # Check if the button exists
                if self.scientific_mode:
                    self.buttons[button].grid()
                else:
                    self.buttons[button].grid_remove()

        # Update mode button text
        self.buttons['Mode'].config(text="Basic" if self.scientific_mode else "Scientific")

    # Apply theme
    def apply_theme(self):
        # Apply the current theme (light or dark)
        theme = self.dark_theme if self.dark_mode else self.light_theme
        self.root.config(bg=theme["bg"])
        self.display.config(bg=theme["bg"], fg=theme["fg"], insertbackground=theme["fg"])
        for button in self.buttons.values():
            button.config(bg=theme["button_bg"], fg=theme["button_fg"])

    # Show history
    def show_history(self):
        if not self.history:
            messagebox.showinfo("History", "No calculation in history.")
        else:
            history_text = "\n".join(self.history)
            messagebox.showinfo("History", history_text)

    # Export history
    def export_history(self):
        if not self.history:
            messagebox.showinfo("Export", "No calculations to export.")
            return

        with open("history.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Calculation"])  # Write header
            for calc in self.history:
                writer.writerow([calc])  # Write each calculation as a row
        messagebox.showinfo("Export", "History exported to history.csv")

    # Import history
    def import_history(self):
        try:
            with open("history.csv", "r") as file:
                reader = csv.reader(file)
                next(reader)  # Skip the header row
                imported_calcs = [row[0] for row in reader]  # Read all calculations
                self.history.extend(imported_calcs)  # Add imported calculation to history

                messagebox.showinfo("Import", f"Imported {len(imported_calcs)} calculations.")
        except FileNotFoundError:
            messagebox.showinfo("Import", "No history CSV file found.")

    # Show help
    def show_help(self):
        help_text = """
        **Basic Mode:**
        - Use numbers (0-9) and basic operations (+, -, *, /).
        - Press '=' to calculate the result.
        - Press 'C' to clear the display.

        **Scientific Mode:**
        - Toggle scientific mode using the 'Mode' button.
        - Use advanced operations (√, ^, sin, cos, tan, π, e).

        **History:**
        - View past calculations using the 'History' button.
        - Export/import history using the 'Export' and 'Import' buttons.

        **Theme:**
        - Toggle between light and dark themes using the 'Theme' button.

        **Convert:**
        - Convert temperatures between Celsius and Fahrenheit.
        """
        messagebox.showinfo("Help", help_text)

    # Convert temperature
    def convert_temperature(self):
        try:
            temp = float(self.display.get())
            if self.scientific_mode:
                # Convert Celsius to Fahrenheit
                converted_temp = (temp * 9 / 5) + 32
                self.display.delete(0, tk.END)
                self.display.insert(0, f"{temp}°C = {converted_temp}°F")
            else:
                # Convert Fahrenheit to Celsius
                converted_temp = (temp - 32) * 5 / 9
                self.display.delete(0, tk.END)
                self.display.insert(0, f"{temp}°F = {converted_temp}°C")
        except ValueError:
            messagebox.showerror("Error", "Invalid input! Please enter a numeric value.")

# Run the program
if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()