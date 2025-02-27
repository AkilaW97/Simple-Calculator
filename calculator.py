#Calculation functions

def add(x, y):
    return x + y

def subtract(x, y):
    return  x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y == 0:
        return "Error! Division by zero"
    return x / y

def display_history(history):
    if not history:
        print("No calculations in history.")
    else:
        print("\nCalculation History:")
        for i, calc in enumerate(history, 1):
            print(f"{i}. {calc}")

def main():
    # List to store calculation history
    history = []

    #Main program
    while True:
        print("\nSelect operation:")
        print("1. Add")
        print("2. Subtract")
        print("3. Multiply")
        print("4. Divide")
        print("5. View History")
        print("6. Exit")

        #Take input from the user
        choice = input("Enter choice (1/2/3/4/5/6): ")

        #check if the user wants to exit
        if choice == '6':
            print("Exiting the calculator. Goodbye!")
            break

        if choice == '5':
            display_history(history)
            continue

        #check if he input is valid
        if choice in ['1', '2', '3', '4']:
            try:
                num1 = float(input("Enter the number: "))
                num2 = float(input("Enter the second number: "))
            except ValueError:
                print("Invalid input! Please enter numeric values.")
                continue

            result = None
            if choice == '1':
                result = add(num1, num2)
                operation = "+"
            elif choice == '2':
                result = subtract(num1, num2)
                operation = "-"
            elif choice == '3':
                result = multiply(num1, num2)
                operation = "*"
            elif choice == '4':
                result = divide(num1, num2)
                operation = "/"

            if result is not None:
                calculation = f"{num1} {operation} {num2} = {result}"
                print(calculation)
                history.append(calculation) #Add calculation to history
        else:
            print("Invalid input! Please enter a valid choice.")

#Run the program (ensures the program runs only when the script is executed directly)
if __name__ == "__main__":
    main()