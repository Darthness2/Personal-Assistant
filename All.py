#Use Python 3.12.4
#Imports
import json
import math
import os
import ollama
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
USER_DATA_FILE = os.path.expanduser('~/users.json')
current_time = datetime.now().time()
current_date = date.today()
weekend_days = {5, 6}
holidays = []
tasks = []
notes = []
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
        print("1. Chat with LLM")
        print("2. Tasks")
        print("3. Notes")
        print("4. Date")
        print("5. Calculator")
        print("6. Settings")
        print("7. Exit")
        menu = input("So what would you like to do today? ").strip().upper()
        if menu == "Chat with LLM" or menu == "1":
            def ask_llm():
                model_to_use = input("\nWhat LLM would you like to use? \n(mistral-nemo, gemma2, llama3.1, qwen2.5, dolpin-llama3, etc...) \nMust be perfect spelling! ")
                while True:
                    prompt = input("\nWhat is your question to the AI? (To end \"q\", To change model \"c\") ")
                    if prompt == "q":
                        break
                    elif prompt == "c":
                        ask_llm()
                    response = ollama.chat(model=model_to_use, messages=[{'role': 'user', 'content': prompt}])
                    print('\n')
                    print(response['message']['content'].strip())
                    print('\n')
            ask_llm()
        elif menu == "Tasks" or menu == "2":
            def all_tasks():
                print("\n" * 1)
                print(" == Tasks Menu == ")
                print("1. Add Task")
                print("2. List Tasks")
                print("3. Remove Tasks")
                what_tasks = input("What would you like to do with your tasks? ")
                if what_tasks == "1" or what_tasks == "Add Task":
                    def add_task():
                        while True:
                            global task
                            task = input("What is 1 task you would like to finish today? ")
                            task_priority = input("What is the priority level? (High/Medium?Low) ").capitalize()
                            if task_priority not in ['High', 'Medium', 'Low']:
                                print("That's not a priority level!")
                                return
                            tasks.append({"task": task, "priority": task_priority})
                            print(f"Task {task} with task priority {task_priority} added")
                            another_task = input("Would you like to add another task? (Y/N): ").strip().upper()
                            if another_task == "N":
                                break
                            elif another_task != "Y":
                                print("Error: Please enter 'Y' or 'N'.")
                    add_task()
                elif what_tasks == "List Tasks" or what_tasks == "2":
                    def list_tasks():
                        print("Your tasks for today:")
                        sorted_tasks = sorted(tasks, key=lambda x: x["priority"], reverse=True)
                        for idk, task in enumerate(sorted_tasks, 1):
                            print(f"{idk}. {task['task']} (Priority: {task['priority']})")
                    list_tasks()
                elif what_tasks == "Remove Tasks" or what_tasks == "3":
                    def remove_tasks():
                        while True:
                            if tasks:
                                print("Here are your tasks:")
                                for i, task in enumerate(tasks, 1):
                                    print(f"{i}. {task}")
                                try:
                                    which_task_will_be_removed = int(input("Which task would you like to remove? "))
                    
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
                    remove_tasks()
            all_tasks()    
        elif menu == "Notes" or menu == "3":
            print("\n" * 2)
            print(" == Notes Menu == ")
            print("1. Write a Note")
            print("2. View a Note")
            print("3. Edit a Note")
            print("4. Remove a Note")
            notes_menu = input("What would you like to do with your notes? ").upper().strip()
            if notes_menu == "Write a Note" or notes_menu == "1":
                def make_note():
                    global note_title
                    global note
                    note_title = input("What is the title of your new note? ")
                    note_content = input("Enter the Note: ")
                    users = load_user_data()
                    user_notes = users.get(client_username, {}).get("notes", [])
                    note = {
                            "title": note_title,
                            "content": note_content,
                    }
                    user_notes.append({"note": note, "title": note_title})
                    users[client_username]["notes"] = user_notes
                    save_user_data(users)
                    print(f"Note {note_title} saved successfully!")
                make_note()   
            elif notes_menu == "View a Note" or notes_menu == "2":
                def list_notes():
                    global notes
                    global note_title
                    user_notes = users.get(client_username, {}).get("notes", [])
                    if user_notes:
                        print("Your notes:")
                        for idk, note in enumerate(user_notes, 1):
                            print(f"{idk}. {note['title']}")
                    else:
                        print("No Notes Found")
                list_notes()
            elif notes_menu == "Edit a Note" or notes_menu == "3":
                def edit_note():
                    user_notes = users.get(client_username, {}).get("notes", [])
                    if user_notes:
                        print("Here are your notes:")
                        for i, note in enumerate(user_notes, 1):
                            print(f"{i}. {note['title']}")

                    try:
                        note_to_edit = int(input("Which note would you like to edit? "))
                        if 1 <= note_to_edit <= len(user_notes):
                            selected_note = user_notes[note_to_edit - 1]
                            new_title = input(f"New title (leave blank to keep '{selected_note['title']}'): ")
                            new_content = input(f"New content (leave blank to keep current content): ")
                            if new_title:
                                selected_note['title'] = new_title
                            if new_content:
                                selected_note['content'] = new_content

                            users[client_username]['notes'] = user_notes
                            save_user_data(users)
                            print("Note updated successfully!")
                        else:
                            print("Invalid note number.")
                    except ValueError:
                        print("Please enter a valid number.")
                    else:
                        print("No Notes to Edit")
                edit_note()
            elif notes_menu == "Remove a Note" or notes_menu == "4":
                def remove_note():
                            user_notes = users.get(client_username, {}).get("notes", [])
                            if user_notes:
                                print("Here are your notes:")
                                for i, note in enumerate(user_notes, 1):
                                    print(f"{i}. {note['title']}")
                                try:
                                    note_to_remove = int(input("Which note would you like to remove? "))
                                    if 1 <= note_to_remove <= len(user_notes):
                                        removed_note = user_notes.pop(note_to_remove - 1)  
                                        print(f"Note '{removed_note['title']}' removed.")
                                        users[client_username]['notes'] = user_notes 
                                        save_user_data(users)  
                                    else:
                                        print("Invalid note number.")
                                except ValueError:
                                    print("Please enter a valid number.")
                            else:
                                print("No Notes to Remove")
                remove_note()
            else:
                print("Not a Valid Option!")
        elif menu == "Date" or menu == "4":
            def time_variable():
                global time_variable
                global client_job
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
                    print("\n" * 2)
                    print("--- Advanced Calculator ---")
                    try:
                        x = input("Enter the first number (or type 'q' to quit): ")
                        if x.lower() == "q":
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
            def settings_menu():
                while True:
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
            print(f"Goodbye {client_username}")
            break
        else:
            print("That is not valid. Put a valid option!")

    users[client_username]['tasks'] = tasks
    users[client_username]['notes'] = notes
    save_user_data(users)
