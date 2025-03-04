from operator import index
import tkinter as tk
from tkinter import messagebox
import csv

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

#GUI Application
class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Calculator")
        self.history = []

        #Input and result display
        self.display = tk.Entry(root, font=("Arial", 20), justify="right", bd=10, insertwidth=4)
        self.display.grid(row=0, column=0, columnspan=4)

        #Buttons
        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', '=', '+',
            'C', 'History', 'Export', 'Import'
        ]

        row = 1
        col = 0
        for button in buttons:
            action = lambda x=button: self.on_button_click(x)
            tk.Button(root, text=button, font=("Arial", 15), width=5, height=2, command=action).grid(row=row, column=col)
            col += 1
            if col > 3:
                col = 0
                row += 1

    def on_button_click(self, value):
        if value == '=':
            try:
                result = str(eval(self.display.get()))
                self.history.append(f"{self.display.get()} = {result}")
                self.display.delete(0, tk.END)
                self.display.insert(0, result)
            except Exception as e:
                messagebox.showerror("Error", "Invalid input!")
        elif value == 'C':
            self.display.delete(0, tk.END)
        elif value == 'History':
            self.show_history() #display_history
        elif value == 'Export':
            self.export_history()
        elif value == 'Import':
            self.import_history()
        else:
            self.display.insert(tk.END, value)

    def show_history(self):
        if not self.history:
            messagebox.showinfo("History", "No calculation in history.")
        else:
            history_text = "\n".join(self.history)
            messagebox.showinfo("History", history_text)

    def export_history(self):
        if not self.history:
            messagebox.showinfo("Export",  "No calculations to export.")
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


# Run the program (ensures the program runs only when the script is executed directly)
if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()