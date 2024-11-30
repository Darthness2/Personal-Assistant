## Overview
This Python script is designed to function as a personal assistant, offering a variety of utilities such as user management, grade calculation, task management, weather updates, and more. It integrates multiple APIs and libraries to achieve these functionalities.
### Requirements
- Python 3.13
- Libraries: `json`, `requests`, `datetime`, `tqdm`, `icecream`, `openai`, and custom library `ollama`.

### Major Classes and Methods:
1. **NeededFunctions**
    - `load_user_data()`: Loads user data from a specified JSON file.
    - `save_user_data(users)`: Saves user data into a JSON file.
    - `wait(seconds=5)`: Pauses execution for a specified number of seconds.
    - `colored_text(text, r, g, b)`: Returns text formatted with specified RGB colors for terminal display.
    - `find_all_in_nested_dict(nested_dict, key)`: Searches for a key in nested dictionaries and lists and returns a list of values.
    - `is_it_a_work_day(date)`: Determines if a given date is a workday (Monday-Friday).

2. **Grades**
    - `calculate_final_grades(class__=None)`: Computes final grades for classes with weighted grading categories.
    - `calculate_needed_grades(current_grade, desired_grade, class_for_grade, weight_category_in_class)`: Calculates the grade needed on an assignment to achieve a desired final grade.

3. **Weather**
    - `us_weather()`: Fetches current weather data in the United States from a specified API.
    - `metric_weather()`: Fetches current weather data in metric units.

4. **Unofficial**
    - `add_stuff_to_class()`: Prompts the user to enter additional information about a class and updates the user data.

### Key Functionalities:
- **User Management**: Allows login, registration, and user data management.
- **Grade Calculation**: Manage and calculate academic grades with different weight categories.
- **Weather Information**: Fetch and display weather updates using external API.
- **Task Management**: Add, list, and remove tasks with priorities.
- **Notes Management**: Write, view, and remove personal notes.
- **Calculator**: A simple text-based calculator for basic arithmetic and scientific calculations.
- **Settings Management**: Modify user details and manage additional class-related functionalities.

### Initialization and Execution:
- The script begins by greeting the user and guiding them through login or registration using stored data.
- The `main()` function serves as the entry point after user verification, providing a menu-driven interface for accessing all features.

### API Integrations:
- Utilizes `requests` to access weather information.
- Integrates with `openai` for advanced language model interactions.
