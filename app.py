print("🩺 Welcome to medication reminder app🩺 ")
# Ask to either login or Signup. Choose login or signup.
    # if signup then ask for name, age, gender and password.
    # Validate that Name should be always string.
    # validate that age is always number and between 0-200.
    # validate that gender is string and it is Male/Female/Trans
    # validate that passowrd is atleast 8 char long and max 20 char. If time: Combination of atleast 1 special char, 1 digit, 1 lower case and 1 uper case
    # Once Signup is done. Ask the person to login. Login takes name and password as entry. If time: Password entry should be invisible.
    # Now the person can add Medication name, dosage, frequency(think about this later.)
# If person chooses to login:
    # Then directly ask them medication details as above.
# When you take input for the sign up use a dictionary. How?
# user_detail = {
#     'name': '',
#     'age':'',
#     'gender': '',
#     'password': ''
# }
# This dictionary can then be stored in a larger dictionary called users.
# Store this information in a file and then read from it later.

from datetime import datetime, timedelta
import getpass
import json
import os

user_database = {}  # Initialize an empty dictionary to store user data.

def sign_up(user_database):
    print("📝 Please fill in the details to sign up:")

    while True:
        user_name = str(input("Username: ").strip())
        if user_name:
            break
        print("❌ Username cannot be blank.")

    # Get valid integer age
    while True:
        age_input = input("Age: ").strip()
        if not age_input:
            print("❌ Age cannot be blank.")
            continue
        if not age_input.isdigit():
            print("❌ Please enter a valid number for age.")
            continue
        age = int(age_input)
        break

    # Get valid gender
    while True:
        gender = str(input("Gender (Male/Female/Trans): ").strip())
        if gender in ["Male", "Female", "Trans"]:
            break
        print("❌ Please enter 'Male', 'Female', or 'Trans'.")

    # Get password (just check it's not blank)
    while True:
        password = str(getpass.getpass("Set a Password (hidden): ").strip())
        if password:
            break
        print("❌ Password cannot be blank.")

    user_database[user_name] = {
        "Username": user_name,
        "Age":age,
        "Gender":gender,
        "Password":password
    }

    with open("users.json", "w") as file:
        json.dump(user_database, file, indent=4) # Save the user database to a JSON file.

    print(f"✅ User {user_name} signed up successfully!")
    print("✅ sign_up complete. you can now login.")
    login()

def login():       
    login_user = str(input("Enter your Username: "))
    password = str(getpass.getpass("Enter your password(hidden): "))

    if not os.path.exists("users.json"):
        with open("users.json", "w") as file: # Create an empty dictionary and save to file
            json.dump({}, file, indent=4)

    with open("users.json", "r") as file: # Open the JSON file to read the user database.
        login_database = json.load(file)

    if login_user in login_database.keys() and login_database[login_user]['Password'] == password: #keys() will force to search in the keys of the dictionary as a list and see how the password value is accessed by double square brackets.
        print("✅ login sucessfully!")
    else:
        print("❌ Username not found or password is incorrect.")
        choose_action = input("Please try again. Press 1 to try again or 2 to sign up: ").strip()
        choose_action_func(choose_action)

def choose_action_func(choose_action):
    if choose_action == '1':
        print("You chose to login.")
        login()
    elif choose_action == '2':
        print("You chose to sign up.")
        sign_up(user_database)
    else:
        print("Invalid option. Please enter 1 for Login or 2 for Sign Up.")
        choose_action = input("Enter either 1 or 2: ").strip()
        choose_action_func(choose_action) # Using recursion to call the function again if the input is invalid.

# Made the messages more clear and concise.
print("Kindly choose an action:")
print("1 for Login") 
print("2 for Sign Up")

# Brought thr choose_action here so that code looks cleaner and more organized.
choose_action = input("Enter either 1 or 2: ").strip() # Made the input more robust by stripping whitespace.
choose_action_func(choose_action) # Call the choose_action function with the user's input.  
        
pt_name = input("Name: ")
pt_age = input("Age: ")
pt_sex =input ("Gender: ")
med_name = input("Medication name: ")
med_dose = input("Dosages: ")
medication_frequency = input("Frequency: ")
now = datetime.now()
print("⏰ Current time:", now.strftime("%Y-%m-%d %H:%M:%S"))
frequency_hour = input("hourly: ")
next_time = now + timedelta(frequency_hour)


