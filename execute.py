import subprocess

# Function to execute a given script using subprocess
def execute_script(script_name):
    try:
        subprocess.run(["python", script_name], check=True)  # Run the script with Python interpreter
    except subprocess.CalledProcessError as e:
        print(f"Error executing {script_name}: {e}")  # Print error message if script execution fails

# Main function to present a menu to the user and execute the selected script
def main():
    # Display the menu options
    print("Select an option:")
    print("1: Send message only")
    print("2: Send attachment only")
    print("3: Send both message and attachment")
    print("4: Invalid choice")

    # Get user input for the menu choice
    choice = input("Enter your choice (1-4): ")

    # Execute the corresponding script based on user choice
    if choice == "1":
        print("Executing main.py...")  # Inform the user about the script being executed
        execute_script("main.py")  # Execute the script for sending messages only
    elif choice == "2":
        print("Executing attachment.py...")  # Inform the user about the script being executed
        execute_script("attachment.py")  # Execute the script for sending attachments only
    elif choice == "3":
        print("Executing attach&msg.py...")  # Inform the user about the script being executed
        execute_script("attach&msg.py")  # Execute the script for sending both messages and attachments
    elif choice == "4":
        print("Invalid choice")  # Inform the user about the invalid choice
    else:
        print("Invalid input. Please enter a number between 1 and 4.")  # Inform the user about the invalid input

# Entry point of the script
if __name__ == "__main__":
    main()  # Call the main function
