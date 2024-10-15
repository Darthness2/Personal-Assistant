#Imports
import json
import math
from datetime import date
from datetime import datetime
is_registered = False

#Load and Save User Details
def load_user_data():
    try:
        with open(USER_DATA_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_user_data(users):
    with open(USER_DATA_FILE, 'w') as f:
        json.dump(users, f, indent=4)

#Needed Stuff
USER_DATA_FILE = 'users.json'
current_time = datetime.now().time()
current_date = date.today()
weekend_days = {5, 6}
holidays = []
tasks = []
users = load_user_data()
def is_school_day(date):
    day_of_week = date.weekday()
    if day_of_week in weekend_days:
        return False
    elif date in holidays:
        return False
    else:
        return True

#Times    
school_start = current_time.replace(hour=8, minute=0, second=0, microsecond=0)
school_end = current_time.replace(hour=14, minute=25, second=0, microsecond=0)
normal_day_start = current_time.replace(hour=8, minute=0, second=0, microsecond=0)
normal_day_end = current_time.replace(hour=20, minute=0, second=0, microsecond=0)
wind_down_time = current_time.replace(hour=21, minute=30, second=0, microsecond=0)

#Client Username, Password, and Registration
client_username = input("Username: ")
client_password = input("Password: ")

if client_username == "a" and client_password == "a":
    print("Welcome admin!")
    is_registered = True
if client_username in users and users[client_username]['password'] == client_password:
    print(f"Welcome back {users[client_username]['name']}!")
    user_info = users[client_username]
    print(f"Job: {user_info['job']}")
    tasks = user_info.get('tasks', [])
    is_registered = True
else:
    registration = input("You have not made an account. Would you like to register? (Y/N) ").strip().upper()
    if registration == ("Y"):
        def register_user():
            global saved_users
            global is_registered
            global client_name
            global client_job
            client_name = input("What is your name? ")
            client_job = input("What is your occupation? (If a student say \"Student\") ")
            users[client_username] = {
            "password": client_password,
            "name": client_name,
            "job": client_job,
            "tasks": tasks
        }
            save_user_data(users)
            print("User registered successfully!")
            print(f"Hello {client_username}")
            is_registered = True
        register_user()
    elif registration == ("N"):
        print("Goodbye Then!")
        exit()

#Main Menu Functionality
if is_registered == True:
    while True:
        print("\n" * 1)
        print(" == Main Menu == ")
        print("1. Add Tasks")
        print("2. List Tasks")
        print("3. Remove Tasks")
        print("4. Date")
        print("5. Calculator")
        print("6. Settings")
        print("7. Exit")
        menu = input("So what would you like to do today? ")
        if menu == "Add Tasks" or menu == "1":
            def add_task():
                while True:
                    task = input("What is 1 task you would like to finish today? (Say \"None\" for no task) ")
                    if task == "None":
                        print("No tasks added.")
                        break
                    tasks.append(task)
                    print(f"Task '{task}' added.")
                    another_task = input("Would you like to add another task? (Y/N): ").strip().upper()
                    if another_task == "N":
                        break
                    elif another_task != "Y":
                        print("Error: Please enter 'Y' or 'N'.")
            add_task()
        elif menu == "List Tasks" or menu == "2":
            def list_tasks():
                print("Your tasks for today:")
                for task in tasks:
                    print(f"- {task}")
            list_tasks()
        elif menu == "Remove Tasks" or menu == "3":
            def remove_tasks():
                while True:
                    removing_a_task = input("Would you like to remove a task? (Y/N): ")
                    if removing_a_task == "Y":
                        if tasks:
                            print("Here are your tasks:")
                            for i, task in enumerate(tasks, 1):
                                print(f"{i}. {task}")
                            try:
                                which_task_will_be_removed = int(input("Which task would you like to remove? (By number; 1, 2, 3, etc...) "))
                    
                                if 1 <= which_task_will_be_removed <= len(tasks):
                                    removed_task = tasks.pop(which_task_will_be_removed - 1)
                                    print(f"Task '{removed_task}' removed.")
                                    users[client_username]['tasks'] = tasks
                                    save_user_data(users)
                                else:
                                    print("Invalid task number.")
                            except ValueError:
                                print("Please enter a valid number.")
                        else:
                            print("No tasks to remove.")
                            break
                    elif removing_a_task == "N":
                      break
                    else:
                        print("Error: Please enter 'Y' or 'N'.")
            remove_tasks()
        elif menu == "Date" or menu == "4":
            def time_variable():
                global time_variable
                if USER_DATA_FILE[-1] == "Student":
                    if is_school_day(current_date) == True and current_time > school_end:
                        input(f"Today is, {current_date} which is a school day. So how was your school day today? ")
                    elif is_school_day(current_date) == True:
                        print(f"Today is, {current_date} which is a school day. Have a good day at school today!")
                    elif is_school_day(current_date) == False and current_time > normal_day_end:
                        input(f"Today is, {current_date} which is not a school day. So how did your day go today? ")
                    elif is_school_day(current_date) == False:
                        print(f"Today is, {current_date} which is not a school day. Have a good day!")
                    elif current_time >= wind_down_time:
                        print(f"Your about to go to sleep. Good Night!")
                else:
                    if is_school_day(current_date) == True and current_time > school_end:
                        input(f"Today is, {current_date} which is a work day. So how was your day today? ")
                    elif is_school_day(current_date) == True:
                        print(f"Today is, {current_date} which is a work day. Have a good day at school today!")
                    elif is_school_day(current_date) == False and current_time > normal_day_end:
                        input(f"Today is, {current_date} which is not a work day. So how did your day go today? ")
                    elif is_school_day(current_date) == False:
                        print(f"Today is, {current_date} which is not a work day. Have a good day!")
                    elif current_time >= wind_down_time:
                        print(f"Your about to go to sleep. Good Night!")
            time_variable()
        elif menu == "Calculator" or menu == "5":
            def calculator():
                while True:
                    print("\n--- Advanced Calculator ---")
                    try:
                        x = input("Enter the first number (or type 'exit' to quit): ")
                        if x.lower() == "exit":
                            break
                        x = float(x)
                        y = input("Enter the second number: ")
                        y = float(y)
                        operation = input("Choose an operation: 'add', 'subtract', 'multiply', 'divide', 'power', 'sqrt', 'log', 'sin', 'cos', 'tan': ")
                        if operation == "sqrt":
                            if x < 0:
                                print("Error: Cannot take the square root of a negative number!")
                            else:
                                print(f"Result: {math.sqrt(x)}")
                        elif operation == "log":
                            base = input("Enter the base for the logarithm (default is 10): ")
                            base = float(base) if base else 10
                            if x <= 0 or base <= 0 or base == 1:
                                print("Error: Invalid input for logarithm.")
                            else:
                                print(f"Result: {math.log(x, base)}")
                        elif operation == "sin":
                            print(f"Result: {math.sin(math.radians(x))}")
                        elif operation == "cos":
                            print(f"Result: {math.cos(math.radians(x))}")
                        elif operation == "tan":
                            print(f"Result: {math.tan(math.radians(x))}")
                        elif operation in ["add", "subtract", "multiply", "divide", "power"]:
                            if operation == "add":
                                print(f"Result: {x + y}")
                            elif operation == "subtract":
                                print(f"Result: {x - y}")
                            elif operation == "multiply":
                                print(f"Result: {x * y}")
                            elif operation == "divide":
                                if y != 0:
                                    print(f"Result: {x / y}")
                                else:
                                    print("Error: Cannot divide by zero!")
                            elif operation == "power":
                                print(f"Result: {x ** y}")
                        else:
                            print("Invalid operation. Please try again.")      
                    except ValueError:
                        print("Error: Invalid number entered. Please enter valid numbers.")  
                    except Exception as e:
                        print(f"An error occurred: {e}. Please try again.")
            calculator()
        elif menu == "Settings" or menu == "6":
            while True:
                def settings_menu():
                    print("\n" * 2)
                    print(" == Settings Menu == ")
                    print("1. Change Password")
                    print("2. Change Occupation")
                    print("3. Exit")
                    settings_menu_choice = input("What would you like to do today? ")
                    if settings_menu_choice == "1" or settings_menu_choice == "Change Password":
                        def change_password():
                            new_password = input("What will be your new password?: ")
                            confirm_new_password = input("Confirm new password: ")
                            if new_password == confirm_new_password:
                                users[client_username]['password']
                                save_user_data(users)
                                print("Your password has been updated successfully")
                            else:
                                print("Passwords do not match")
                        change_password()
                    elif settings_menu_choice == "2" or settings_menu_choice == "Change Occupation":
                        def change_occupation():
                            new_occupation = input("What will be your new occupation?: ")
                            confirm_new_occupation = input("Confirm new occupation: ")
                            if new_occupation == confirm_new_occupation:
                                users[client_username]['job']
                                save_user_data(users)
                                print("Your occupation has been updated successfully")
                            else:
                                print("Passwords do not match")
                        change_occupation()
                    elif settings_menu_choice == "3" or settings_menu_choice == "Exit":
                        print("Returning to the Main Menu")
                        break
                settings_menu()

        elif menu == "Exit" or menu == "7":
            print(f"\n","Goodbye {client_username}")
            break
        else:
            print("That is not valid. Put a valid option!")

    users[client_username]['tasks'] = tasks
    save_user_data(users)
