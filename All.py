#Imports
import json
import math
import os
import time
import ollama
import httpx
import openai
import requests
from datetime import datetime
from tqdm import tqdm
from datetime import date
from icecream import ic

class NeededFunctions:
    @staticmethod
    def load_user_data():
        try:
            with open(USER_DATA_FILE, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    @staticmethod
    def save_user_data(users):
        with open(USER_DATA_FILE, 'w') as file:
            json.dump(users, file, indent=4)

    @staticmethod
    def wait(seconds=5):
        time.sleep(seconds)

    @staticmethod
    def colored_text(text, r, g, b):
        return f"\033[38;2;{r};{g};{b}m{text}\033[0m"

    @staticmethod
    def find_all_in_nested_dict(nested_dict, key):
        results = []
        def recurse(d):
            if isinstance(d, dict):
                for k, v in d.items():
                    if k == key:
                        results.append(v)
                    elif isinstance(v, (dict, list)):
                        recurse(v)
            elif isinstance(d, list):
                for item in d:
                    recurse(item)
        recurse(nested_dict)
        return results

    @staticmethod
    def is_it_a_work_day(date):
        day_of_week = date.weekday()
        if day_of_week < 5:
            return True
        else:
            return False

class Grades:
    @staticmethod
    def calculate_final_grades( class__=None):
        if class__ is None:
            for class_, info in users[str(current_user)]['Other']['classes'].items():
                weight_categories = info.get('weight_categories', {})
                weighted_scores = []
                for category, details in weight_categories.items():
                    weight = details.get('weight', 0) / 100
                    grades = details.get('grades', [])
                    if grades:
                        category_score = sum((grade['points_earned'] / grade['points_possible']) * 100 for grade in grades) / len(grades)
                        weighted_scores.append(category_score * weight)
                overall_grade = sum(weighted_scores)
                yield class_, round(overall_grade, 2)
        else:
            for class_, info in class__.items():
                weight_categories = info.get('weight_categories', {})
                weighted_scores = []
                for category, details in weight_categories.items():
                    weight = details.get('weight', 0) / 100
                    grades = details.get('grades', [])
                    if grades:
                        category_score = sum((grade['points_earned'] / grade['points_possible']) * 100 for grade in grades) / len(grades)
                        weighted_scores.append(category_score * weight)
                overall_grade = sum(weighted_scores)
                yield class_, round(overall_grade, 2)

    @staticmethod
    def calculate_needed_grades(current_grade, desired_grade, class_for_grade, weight_category_in_class):
        current_grade = int(current_grade)
        if current_grade >= desired_grade:
            return f"You don't need to improve your grade"
        if 'grades' not in users[str(current_user)]['Other']['classes'][class_for_grade]['weight_categories'][weight_category_in_class]:
            users[str(current_user)]['Other']['classes'][class_for_grade]['weight_categories'][weight_category_in_class]['grades'] = []
        grades_in_weight_category = users[str(current_user)]['Other']['classes'][class_for_grade]['weight_categories'][weight_category_in_class]['grades']
        weight = users[str(current_user)]['Other']['classes'][class_for_grade]['weight_categories'][weight_category_in_class]['weight']
        try:
            weight_of_assignment = (weight / len(grades_in_weight_category)) / 100
        except ZeroDivisionError:
            weight_of_assignment = weight
        final_answer = round((desired_grade - ((1 - weight_of_assignment) * current_grade)) / weight_of_assignment, 2)
        if final_answer > 100:
            return f'You will unfortunately have to get extra credit on this assignment to achieve your desired grade. You need to score at least {final_answer} on this assignment.'
        else:
            return f"To achieve your desired grade, you need to score at least {final_answer} on this assignment."

class Weather:
    @staticmethod
    def us_weather():
        weather_in_us = requests.request("GET", f"")
        if weather_in_us.status_code != 200:
            return False
        else:
            jsondata_in_us = weather_in_us.json()
            return jsondata_in_us

    @staticmethod
    def metric_weather():
        weather_in_metric = requests.request("GET", f"")
        if weather_in_metric.status_code != 200:
            return False
        else:
            jsondata_in_metric = weather_in_metric.json()
            return jsondata_in_metric

#Needed Stuff
USER_DATA_FILE = os.path.expanduser('')
current_time = datetime.now().time()
current_date = date.today()
tasks = []
openai.api_key = ""

#Client Username, Password, and Registration
client_username = input(NeededFunctions.colored_text("Username: ", 0, 255, 0))
client_password = input(NeededFunctions.colored_text("Password: ", 0, 255, 0))
try:
    users = NeededFunctions.load_user_data()
except json.decoder.JSONDecodeError:
    print('File is not formatted properly')
    exit()
id_counter = max(map(int, users.keys()), default=0) + 1
current_user = next((k for k, v in users.items() if v["user_info"]["username"] == client_username), str(id_counter))

#Login or Register
def login_or_register():
    if client_username in NeededFunctions.find_all_in_nested_dict(users, 'username') and client_password in NeededFunctions.find_all_in_nested_dict(users, 'password'):
        print("\n")
        print(f"\nWelcome back", NeededFunctions.colored_text(users[str(current_user)]['user_info']['name'], 255, 215, 0).strip('{}').strip('\''))
    else:
        registration = input("You have not made an account. Would you like to register? (Y/N) ").strip().upper()
        if registration == "Y":
            def register_user():
                client_name = input("What is your name? ")
                client_job = input("What is your occupation? (If a student say \"Student\") ")
                location = input('What city do you live in? ')
                id_counter = max(map(int, users.keys()), default=0) + 1
                current_user = next((k for k, v in users.items() if v.get("user_info", {}).get("username") == client_username and v.get("user_info", {}).get("password") == client_password), id_counter)
                if current_user not in users:
                    users[str(current_user)] = {}
                if 'user_info' not in users[str(current_user)]:
                    users[str(current_user)]['user_info'] = {}
                if 'Other' not in users[str(current_user)]:
                    users[str(current_user)]['Other'] = {}
                users[str(current_user)]['user_info'] = {"username": client_username, "password": client_password, 'name': client_name, 'job': client_job, 'location': location}
                NeededFunctions.save_user_data(users)
                print("User registered successfully!")
                print(f"Hello {client_username}")
                id_counter += 1
            register_user()
        elif registration == "N":
            print("Goodbye Then!")
            exit()
current_user = next((k for k, v in users.items() if v["user_info"]["username"] == client_username), str(id_counter))

#Main Menu Functionality
def main():
    try:
        while True:
            print("\n")
            print(NeededFunctions.colored_text(" == Main Menu == ", 30, 144, 255))
            print("1. Chat with LLM")
            print('2. Daily Summary')
            print("3. Grades")
            print("4. Tasks")
            print("5. Notes")
            print("6. Calculator")
            print("7. Settings")
            print("8. Exit")
            menu = input("> ").strip().upper()
            if menu == "Chat with LLM" or menu == "1":
                try:
                    def ask_llm():
                        print("\n")
                        new_ollama_list = ollama.list()['models']
                        model_names = [model['name'].replace(":latest", ' ').strip() for model in new_ollama_list]
                        if "ChatGPT" not in model_names:
                            model_names.append("ChatGPT")
                        print(' == LLMS == ')
                        for index, name in enumerate(model_names, start=1):
                            print(f"{NeededFunctions.colored_text(index, 255, 215, 0)}: {name}")
                        model_to_use_index = input("\n> ")
                        if model_to_use_index in model_names or model_to_use_index and 1 <= int(model_to_use_index) <= len(model_names):
                            model_to_use = model_names[int(model_to_use_index) - 1]
                            while True:
                                prompt = input(NeededFunctions.colored_text(f"\n(\"Q\" to quit, \"C\" to change model) \n{client_username}: ", 255, 215, 0)).strip().upper()
                                if prompt == "Q":
                                    break
                                elif prompt == "C":
                                    ask_llm()
                                if model_to_use == "ChatGPT":
                                    try:
                                        response = openai.chat.completions.create(model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}], stream=True)
                                        print('\n' * 2)
                                        print(NeededFunctions.colored_text('A:', 0, 255, 0))
                                        for chunk in response:
                                            print(chunk['message']['content'], end='')
                                    except openai.RateLimitError:
                                        print("\nYou exceeded your current quota")
                                        ask_llm()
                                else:
                                    response = ollama.chat(model=model_to_use, messages=[{'role': 'user', 'content': prompt}], stream=True)
                                    print(NeededFunctions.colored_text('A:', 0, 255, 0))
                                    for chunk in response:
                                        print(chunk['message']['content'], end='')
                                    print("\n")
                        else:
                            print("\n")
                            print(NeededFunctions.colored_text("Please enter a valid model!", 255, 0, 0))
                            ask_llm()
                    ask_llm()
                except httpx.ConnectError:
                    print("\n")
                    print("Ollama is not open!")
            elif menu == "Daily Summary" or menu == "2":
                if not Weather().us_weather() and NeededFunctions.is_it_a_work_day(current_date):
                    print(f"Today is {NeededFunctions.colored_text(current_date.strftime('%A, %B %d, %Y').lower(), 255, 215, 0)} which is a work day. \nThe temperature is currently unavailable \nYou have {NeededFunctions.colored_text(len(users[str(current_user)]['Other']['tasks']), 255, 215, 0)} tasks to complete")
                elif not Weather().us_weather() and not NeededFunctions.is_it_a_work_day(current_date):
                    print(f"Today is {NeededFunctions.colored_text(current_date.strftime('%A, %B %d, %Y').lower(), 255, 215, 0)} which is an off day. \nThe temperature is currently unavailable \nYou have {NeededFunctions.colored_text(len(users[str(current_user)]['Other']['tasks']), 255, 215, 0)} tasks to complete")
                if NeededFunctions.is_it_a_work_day(current_date):
                    print(f"Today is {NeededFunctions.colored_text(current_date.strftime('%A, %B %d, %Y').lower(), 255, 215, 0)} which is a work day. The temperature right now is {NeededFunctions.colored_text(round(Weather().us_weather()['currentConditions']['temp'], 0), 255, 215, 0)} degrees.\nToday will reach a high of {NeededFunctions.colored_text(round(Weather().us_weather()['days'][0]['feelslikemax'], 0), 255, 215, 0)} and a low of {NeededFunctions.colored_text(round(Weather().us_weather()['days'][0]['feelslikemin'], 0), 255, 215, 0)} with {NeededFunctions.colored_text(Weather().us_weather()['days'][0]['description'].lower(), 255, 215, 0)}\nYou have {NeededFunctions.colored_text(len(users[str(current_user)]['Other']['tasks']), 255, 215, 0)} tasks to complete")
                elif not NeededFunctions.is_it_a_work_day(current_date):
                    print(f"Today is {NeededFunctions.colored_text(current_date.strftime('%A, %B %d, %Y').lower(), 255, 215, 0)} which is an off day. The temperature right now is {NeededFunctions.colored_text(round(Weather().us_weather()['currentConditions']['temp'], 0), 255, 215, 0)} degrees.\nToday will reach a high of {NeededFunctions.colored_text(round(Weather().us_weather()['days'][0]['feelslikemax'], 0), 255, 215, 0)} and a low of {NeededFunctions.colored_text(round(Weather().us_weather()['days'][0]['feelslikemin'], 0), 255, 215, 0)} with {NeededFunctions.colored_text(Weather().us_weather()['days'][0]['description'].lower(), 255, 215, 0)} \nYou have {NeededFunctions.colored_text(len(users[str(current_user)]['Other']['tasks']), 255, 215, 0)} tasks to complete")
                list_out_tasks = input('Would you like me to list them out? (Y/N): ').strip().upper()
                if list_out_tasks == 'Y':
                    print("\n == Tasks == ")
                    sorted_tasks = sorted(users[str(current_user)]['Other']['tasks'], key=lambda x: x['priority'], reverse=True)
                    for idk, task in enumerate(sorted_tasks, 1):
                        print(f"{idk}. {task['task']} (Priority: {task['priority']})")
                    NeededFunctions.wait()
                elif list_out_tasks == 'N':
                    print("Ok")
                else:
                    print("Please enter a valid option!")
            elif menu == "Grades" or menu == "3":
                def grades_in_main_menu():
                    while True:
                        print(NeededFunctions.colored_text("\n == Grades Menu == ", 30, 144, 255))
                        print("1. Add Grade")
                        print("2. View Grades")
                        print('3. Experimental Grades')
                        print("4. Exit")
                        grades_menu = input("> ").strip().upper()
                        if grades_menu == "1" or grades_menu == "Add Grade":
                            def add_grade():
                                while True:
                                    filtered_dict = {k: v for k, v in users[str(current_user)]['Other']['classes'].items() if k != 'grades'}
                                    class_name = filtered_dict.keys()
                                    if not class_name:
                                        print('No classes found')
                                        break
                                    print('\n == Classes == ')
                                    for index, name in enumerate(class_name, start=1):
                                        print(f"{NeededFunctions.colored_text(index, 255, 215, 0)}: {name}")
                                    class_for_grade = int(input('> '))
                                    class_name = list(class_name)[class_for_grade - 1]
                                    if 1 <= class_for_grade <= len(class_name):
                                        print(f'\n == Categories in {class_name} == ')
                                        for index, category in enumerate(users[str(current_user)]['Other']['classes'][class_name]['weight_categories'], start=1):
                                            print(f"{NeededFunctions.colored_text(index, 255, 215, 0)}: {category}")
                                        category_for_grade = int(input('> '))
                                        category_name = list(users[str(current_user)]['Other']['classes'][class_name]['weight_categories'])[category_for_grade - 1]
                                        while True:
                                            points_possible = float(input('What were the points possible for the assignment? '))
                                            points = float(input('How many points did you get on the assignment? '))
                                            grade = float(input("What is the percentage grade of the assignment "))
                                            if category_name not in users[str(current_user)]['Other']['classes'][class_name]['weight_categories']:
                                                users[str(current_user)]['Other']['classes'][class_name]['weight_categories'][category_name] = {}
                                            if 'grades' not in users[str(current_user)]['Other']['classes'][class_name]['weight_categories'][category_name]:
                                                users[str(current_user)]['Other']['classes'][class_name]['weight_categories'][category_name]['grades'] = []
                                            full_grade_details = {'points_possible': points_possible, 'points_earned': points, 'grade': grade}
                                            users[str(current_user)]['Other']['classes'][class_name]['weight_categories'][category_name]['grades'].append(full_grade_details)
                                            print(f"Grade for {category_name} in {class_name} added successfully!")
                                            NeededFunctions.save_user_data(users)
                                            again = input("Would you like to add another grade? (Y/N): ").strip().upper()
                                            if again == "N":
                                                return
                                            elif again == "Y":
                                                continue
                                            else:
                                                print("Error: Please enter 'Y' or 'N'.")
                            add_grade()
                        elif grades_menu == "2" or grades_menu == "View Grades":
                            if not users[str(current_user)]['Other']['classes']:
                                print('No classes found')
                                break
                            else:
                                print('\n == Classes == ')
                                for classes, final_grades in Grades().calculate_final_grades():
                                    print(f"{NeededFunctions.colored_text(classes, 255, 215, 0)}: {final_grades}")
                                NeededFunctions.wait()
                        elif grades_menu == "3" or grades_menu == "Experimental Grades":
                            if not users[str(current_user)]['Other']['classes']:
                                print('No classes found')
                            else:
                                print('\n == Classes == ')
                                final_grades_list = Grades().calculate_final_grades()
                                final_grades = {name: grade for name, grade in final_grades_list}
                                for idk, classes in enumerate(users[str(current_user)]['Other']['classes'], start=1):
                                    print(f"{NeededFunctions.colored_text(idk, 255, 215, 0)}: {classes}")
                                which_class = int(input('Which Class Would you like to test? '))
                                which_classes = list(users[str(current_user)]['Other']['classes'])[which_class - 1]
                                current_grades = final_grades[which_classes]
                                print(f'Your Current Grade in {which_classes} is {final_grades[which_classes]}')
                                wanted_grade = int(input('What is your desired grade? '))
                                print(' == Weight Categories == ')
                                for idk, weight in enumerate(users[str(current_user)]['Other']['classes'][which_classes]['weight_categories'], start=1):
                                    print(f"{NeededFunctions.colored_text(idk, 255, 215, 0)}: {weight}")
                                weight = input('Which weight category would you like to put it in? ')
                                which_weight = list(users[str(current_user)]['Other']['classes'][which_classes]['weight_categories'])[int(weight) - 1]
                                print(Grades().calculate_needed_grades(current_grades, wanted_grade, which_classes, which_weight))
                        elif grades_menu == "4" or grades_menu == "Exit":
                            break
                        else:
                            print(NeededFunctions.colored_text("Please enter a valid class!", 255, 0, 0))
                grades_in_main_menu()
            elif menu == "Tasks" or menu == "4":
                def all_tasks():
                    while True:
                        print("\n")
                        print(NeededFunctions.colored_text(" == Tasks Menu == ", 30, 144, 255))
                        print("1. Add Task")
                        print("2. List Tasks")
                        print("3. Remove Tasks")
                        print("4. Exit")
                        what_tasks = input("> ")
                        if what_tasks == "1" or what_tasks == "Add Task":
                            def add_task():
                                while True:
                                    task = input("What is 1 task you would like to finish today? ")
                                    task_priority = input("What is the priority level? (High/Medium?Low) ").capitalize()
                                    if task_priority not in ['High', 'Medium', 'Low']:
                                        print("That's not a priority level!")
                                        return
                                    task_entry = {"priority": task_priority, "task": task}
                                    if 'tasks' not in users[str(current_user)]['Other']:
                                        users[str(current_user)]['Other']['tasks'] = []
                                    users[str(current_user)]['Other']['tasks'].append(task_entry)
                                    NeededFunctions.save_user_data(users)
                                    print(f"Task {task} with task priority {task_priority} added")
                                    another_task = input("Would you like to add another task? (Y/N): ").strip().upper()
                                    if another_task == "N":
                                        break
                                    elif another_task != "Y":
                                        print("Error: Please enter 'Y' or 'N'.")
                            add_task()
                        elif what_tasks == "List Tasks" or what_tasks == "2":
                            def list_tasks():
                                if 'tasks' not in users[str(current_user)]['Other']:
                                    users[str(current_user)]['Other']['tasks'] = []
                                if not users[str(current_user)]['Other']['tasks']:
                                    print("No tasks to list.")
                                else:
                                    print(" == Tasks == ")
                                    sorted_tasks = sorted(users[str(current_user)]['Other']['tasks'], key=lambda x: x['priority'], reverse=True)
                                    for idk, task in enumerate(sorted_tasks, 1):
                                        print(f"{idk}. {task['task']} (Priority: {task['priority']})")
                                    NeededFunctions.wait()
                            list_tasks()
                        elif what_tasks == "Remove Tasks" or what_tasks == "3":
                            def remove_tasks():
                                user_tasks = users[str(current_user)]['Other']['tasks']
                                print("\n == Tasks == ")
                                if not user_tasks:
                                    print("No tasks to remove.")
                                    main()
                                sorted_tasks = sorted(users[str(current_user)]['Other']['tasks'], key=lambda x: x['priority'], reverse=True)
                                for index, task in enumerate(sorted_tasks, 1):
                                    print(f"{index}. {task['task']} (Priority: {task['priority']})")
                                try:
                                    which_task_will_be_removed = int(input("> "))
                                    if 1 <= which_task_will_be_removed <= len(user_tasks):
                                        del users[str(current_user)]['Other']['tasks'][which_task_will_be_removed - 1]
                                        print(f"Task '{which_task_will_be_removed}' removed.")
                                        NeededFunctions.save_user_data(users)
                                    else:
                                        print("Invalid task number.")
                                except ValueError:
                                    print("Please enter a valid number.")
                            remove_tasks()
                        elif what_tasks == "Exit" or what_tasks == "4":
                            break
                        else:
                            print("Not a Valid Option!")
                all_tasks()
            elif menu == "Notes" or menu == "5":
                while True:
                    print("\n")
                    print(NeededFunctions.colored_text(" == Notes Menu == ", 30, 144, 255))
                    print("1. Write a Note")
                    print("2. View a Note")
                    print("3. Remove a Note")
                    print("4. Exit")
                    notes_menu = input("> ").upper().strip()
                    if notes_menu == "Write a Note" or notes_menu == "1":
                        def make_note():
                            note_title = input("What is the title of your new note? ")
                            note_content = input("Enter the Note: ")
                            if 'notes' not in users[str(current_user)]['Other']:
                                users[str(current_user)]['Other']['notes'] = {}
                            users[str(current_user)]['Other']['notes'][note_title] = {}
                            users[str(current_user)]['Other']['notes'][note_title]['note'] =  note_content
                            NeededFunctions.save_user_data(users)
                            print(f"Note {note_title} saved successfully!")
                        make_note()
                    elif notes_menu == "View a Note" or notes_menu == "2":
                        def list_notes():
                            if 'notes' not in users[str(current_user)]['Other']:
                                users[str(current_user)]['Other']['notes'] = {}
                            if not users[str(current_user)]['Other']['notes']:
                                print("No notes to list.")
                            else:
                                print(" == Notes == ")
                                notes = users[str(current_user)]['Other']['notes']
                                for note_title, note in notes.items():
                                    print(f"{NeededFunctions.colored_text(note_title, 255, 215, 0)}: \n{note['note']}")
                                NeededFunctions.wait()
                        list_notes()
                    elif notes_menu == "Remove a Note" or notes_menu == "3":
                        def remove_note():
                            user_notes = list(users[str(current_user)]['Other']['notes'].items())
                            if user_notes:
                                print(" == Notes == ")
                                for i, note in enumerate(user_notes, 1):
                                    print(f"{i}. {note[0]}")
                                try:
                                    note_to_remove = int(input("Which note would you like to remove? "))
                                    if 1 <= note_to_remove <= len(user_notes):
                                        note_title = user_notes[note_to_remove - 1][0]
                                        del users[str(current_user)]['Other']['notes'][note_title]
                                        print(f"Note '{note_title}' removed.")
                                        NeededFunctions.save_user_data(users)
                                    else:
                                        print("Invalid note number.")
                                except ValueError:
                                    print("Please enter a valid number.")
                            else:
                                print("No Notes to Remove")
                        remove_note()
                    elif notes_menu == "Exit" or notes_menu == "4":
                        break
                    else:
                        print("Not a Valid Option!")
            elif menu == "Calculator" or menu == "6":
                def calculator():
                    while True:
                        print("\n" * 2)
                        print(NeededFunctions.colored_text(" == Calculator == ", 30, 144, 255))
                        try:
                            x = float(input("(\"Q\" to quit)\nX: "))
                            if x == "q":
                                break
                            y = float(input("Y: "))
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
            elif menu == "Settings" or menu == "7":
                def settings_menu():
                    while True:
                        print("\n")
                        print(NeededFunctions.colored_text(" == Settings Menu == ", 30, 144, 255))
                        print("1. Change User Details")
                        print("2. LLM Stuff")
                        print("3. Classes Stuff")
                        print("4. Exit")
                        settings_menu_choice = input("> ")
                        if settings_menu_choice == "1" or settings_menu_choice == "Change User Details":
                            def change_user_details():
                                print("\n")
                                print(NeededFunctions.colored_text(" == User Details Menu == ", 30, 144, 255))
                                print("1. Change Password")
                                print("2. Change Occupation")
                                print("3. Exit")
                                change_user_details_input = input("So what would you like to do? ").strip().upper()
                                if change_user_details_input == "1" or change_user_details_input == "Change Password":
                                    def change_password():
                                        new_password = input("What will be your new password?: ")
                                        confirm_new_password = input("Confirm new password: ")
                                        if new_password == confirm_new_password:
                                            users[str(current_user)]['user_info']['password'] = new_password
                                            NeededFunctions.save_user_data(users)
                                            print("Your password has been updated successfully")
                                        else:
                                            print("Passwords do not match")
                                    change_password()
                                elif change_user_details_input == "2" or change_user_details_input == "Change Occupation":
                                    def change_occupation():
                                        new_occupation = input("What will be your new occupation?: ")
                                        confirm_new_occupation = input("Confirm new occupation: ")
                                        if new_occupation == confirm_new_occupation:
                                            users[str(current_user)]['user_info']['job'] = new_occupation
                                            NeededFunctions.save_user_data(users)
                                            print("Your occupation has been updated successfully")
                                        else:
                                            print("Passwords do not match")
                                    change_occupation()
                                elif change_user_details_input == "3" or change_user_details_input == "Exit":
                                    settings_menu()
                                else:
                                    print(NeededFunctions.colored_text("Please put a valid option!", 255, 0, 0))
                            change_user_details()
                        elif settings_menu_choice == "2" or settings_menu_choice == "LLM Stuff" :
                            def llm_menu():
                                while True:
                                    print("\n")
                                    print(NeededFunctions.colored_text(" == LLM Menu == ", 30, 144, 255))
                                    print("1. Pull an LLM")
                                    print("2. Delete an LLM")
                                    print("3. Exit")
                                    llm_menu_choice = input("> ")
                                    if  llm_menu_choice == "1" or llm_menu_choice == "Pull an LLM":
                                        llm_to_pull = input("\nSo what LLM would you like to pull? ")
                                        try:
                                            current_digest, bars = '', {}
                                            for progress in ollama.pull(llm_to_pull, stream=True):
                                                digest = progress.get('digest', '')
                                                if digest != current_digest and current_digest in bars:
                                                    bars[current_digest].close()
                                                if not digest:
                                                    print(progress.get('status'))
                                                    continue
                                                if digest not in bars and (total := progress.get('total')):
                                                    bars[digest] = tqdm(total=total, desc=f'pulling {digest[7:19]}', unit='B', unit_scale=True)
                                                if completed := progress.get('completed'):
                                                    bars[digest].update(completed - bars[digest].n)
                                                current_digest = digest
                                        except ollama._types.ResponseError:
                                            print(NeededFunctions.colored_text("Please pull a valid model!", 255, 0, 0))
                                            llm_menu()
                                    elif llm_menu_choice == "2" or llm_menu_choice == "Delete an LLM":
                                        print("\n")
                                        print(" == Installed LLM == ")
                                        new_ollama_list = ollama.list()['models']
                                        model_names = [model['name'].replace(":latest", ' ').strip() for model in new_ollama_list]
                                        for index, name in enumerate(model_names, start=1):
                                            print(f"{NeededFunctions.colored_text(index, 255, 215, 0)}: {name}")
                                        model_to_delete_index = input("Which model would you like to delete? ")
                                        if model_to_delete_index.isdigit() and 1 <= int(model_to_delete_index) <= len(model_names):
                                            model_to_delete = model_names[int(model_to_delete_index) - 1]
                                            ollama.delete(model_to_delete)
                                    elif llm_menu_choice == "3" or llm_menu_choice == "Exit":
                                        break
                                    else:
                                        print(NeededFunctions.colored_text("Please put a valid option!", 255, 0, 0))
                            llm_menu()
                        elif settings_menu_choice == "3" or settings_menu_choice == "Classes Stuff":
                            print(NeededFunctions.colored_text("\n == Classes Stuff == ", 30, 144, 255))
                            print("1. Add a Class")
                            print("2. Remove a Class")
                            print("3. Exit")
                            classes_stuff_menu_input = input("> ").strip().upper()
                            if classes_stuff_menu_input == "1" or classes_stuff_menu_input == "Add a Class":
                                class_name = input("Enter your class's name: ")
                                if 'classes' not in users[str(current_user)]['Other']:
                                    users[str(current_user)]['Other']['classes'] = {}
                                if class_name not in users[str(current_user)]['Other']['classes']:
                                    users[str(current_user)]['Other']['classes'][str(class_name)] = {}
                                NeededFunctions.save_user_data(users)
                                while True:
                                    category_name = input("Enter a weight category name: ").strip()
                                    weight = float(input(f"Enter the weight for {category_name}: "))
                                    if 'weight_categories' not in users[str(current_user)]['Other']['classes'][str(class_name)]:
                                        users[str(current_user)]['Other']['classes'][str(class_name)]['weight_categories'] = {}
                                    if category_name not in users[str(current_user)]['Other']['classes'][str(class_name)]['weight_categories']:
                                        users[str(current_user)]['Other']['classes'][str(class_name)]['weight_categories'][str(category_name)] = {}
                                    users[str(current_user)]['Other']['classes'][str(class_name)]['weight_categories'][str(category_name)]['weight'] = weight
                                    NeededFunctions.save_user_data(users)
                                    print(f"Class '{class_name}' and {category_name} added successfully.")
                                    add_more = input("Add another category? (Y/N): ").strip().upper()
                                    if add_more  == "Y":
                                        continue
                                    elif add_more == "N":
                                        break
                                    else:
                                        print(NeededFunctions.colored_text("Please put a valid option!", 255, 0, 0))
                            elif classes_stuff_menu_input == "2" or classes_stuff_menu_input == "Remove a Class":
                                print('\n == Classes == ')
                                user_classes = users[str(current_user)]['Other']['classes']
                                for index, classes in enumerate(user_classes.keys(), start=1):
                                    print(f"{NeededFunctions.colored_text(index, 255, 215, 0)}: {classes}")
                                class_to_remove = int(input("> "))
                                if 1 <= class_to_remove <= len(user_classes.keys()):
                                    classs = list(user_classes.keys())[class_to_remove - 1]
                                    del users[str(current_user)]['Other']['classes'][classs]
                                    print(f"Class '{classs}' removed.")
                                    NeededFunctions.save_user_data(users)
                                else:
                                    print("Invalid class number.")
                            elif classes_stuff_menu_input == '3' or classes_stuff_menu_input == "Exit":
                                break
                            else:
                                print(NeededFunctions.colored_text("Please put a valid option!", 255, 0, 0))
                        elif settings_menu_choice == "4" or settings_menu_choice == "Exit":
                            print("Returning to the Main Menu")
                            break
                        else:
                            print(NeededFunctions.colored_text("Please put a valid option!", 255, 0, 0))
                settings_menu()
            elif menu == "Exit" or menu == "8":
                print(f"Goodbye {NeededFunctions.colored_text(client_username, 255, 215, 0)}")
                NeededFunctions.save_user_data(users)
                break
            else:
                print("That is not valid. Put a valid option!")
    except KeyboardInterrupt:
        NeededFunctions.save_user_data(users)
        print("Goodbye!")
        exit()
NeededFunctions.save_user_data(users)

if __name__ == "__main__":
    login_or_register()
    main()
