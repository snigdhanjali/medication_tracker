print("🩺 Welcome to medication reminder app🩺 ")
# Ask to either login or Signup. Choose login or signup.
    # if signup then ask for name, age, gender and password.
    # Validate that Name should be always string.
    # validate that age is always number and between 0-200.
    # validate that gender is string and it is Male/Female/Trans
    # validate that passowrd is atleast 8 char long and max 20 char. If time: Combination of atleast 1 special char, 1 digit, 1 lower case and 1 uper case
    # Once Signup is done. Ask the person to login. Login takes name and password as entry. If time: Password entry should be invisible.
    # If person chooses to login:
    # Then directly ask them medication details as above.
    # Now the person can add Medication name, dosage, frequency(think about this later.)
    # Once the person is logged in ask him if he is trying to create or update or read or delete a reminder.
    # If he is trying to read a reminder then just print out the contents of his user_name key use pprint module.
    # if he is trying to delete a reminder let him delete it by calling dict.del() function.
    # if he is trying to update his reminder then asking him for new content of the reminder and replace the exisiting content can be done by dict[user_name][reminder][dosage]=dosage.
    # if he is trying to create a reminder ask him for reminder name, dosage etc store it in a disctionary and then this dictionary can be added to the username disctionary
    # try to decompose this storage into small problems and use fucntions so that code is re-used.
    # we will worry about sound and reminders later.
# Next step is to validate all the inputs same as in signup function
# Figure out date time and how to set reminders.
# Implement a simple remionder system that creates a canvas and flashes a message on the screen when the time comes.

from datetime import datetime, timedelta
import getpass
import pprint
import json
import os

print("what would you like to do?")
print("1.login")
print("2.sign_up")

user_database = {}

def create_reminder(user, login_database):
    print("Creating a new reminder...")
    reminder_name = input("Reminder name: ").strip()
    dosage = input("Dosage details: ").strip()
    time = input("Time: ").strip()

    reminder_data = {
        "Reminder_Name": reminder_name,
        "Dosage": dosage,
        "Time": time
    }

    login_database[user].setdefault("Reminders", {})[reminder_name] = reminder_data

    with open("users.json", "w") as file:
        json.dump(login_database, file, indent=4)

    print("✅ Reminder created.")

def read_reminders(user, login_database):
    print("Your reminders:")
    reminders = login_database[user].get("Reminders", {})
    if reminders:
        print(json.dumps(reminders, indent=4))
    else:
        print("No reminders found.")

def update_reminder(user,login_database): # VALIDATE THIS FUNCTION
    reminders = login_database[user].get("Reminders", {})
    if not reminders:
        print("❌ No reminders to update.")
        return

    
    print(json.dumps(reminders, indent=4))
    
    reminder_name = input("Which reminder do you want to update? ").strip()

    if reminder_name in reminders:
        new_name = input("New reminder name (leave blank to keep current): ").strip()
        new_dosage = input("New dosage: ").strip()
        new_time = input("New time: ").strip()
        reminders[reminder_name] = {
            "Reminder_Name": new_name,
            "Dosage": new_dosage,
            "Time": new_time
        }
        print("✅ Reminder updated.")
        print(json.dumps(reminders, indent=4))
        with open("users.json", "w") as file:
            json.dump(login_database, file, indent=4)
    else:
        print("❌ Reminder not found.")

def delete_reminder(user, login_database):
    if not login_database[user].get("Reminders", {}):
        print("❌ No reminders to delete.")
        return

    print("🗑️ Available reminders:")
    for name in login_database[user].get("Reminders", {}):
        print(f" - {name}")

    reminder_name = input("Which reminder do you want to delete? ").strip()

    if reminder_name in login_database[user].get("Reminders", {}):
        del login_database[user]['Reminders'][reminder_name]
        print("🗑️ Reminder deleted.")
        print(json.dumps(login_database[user].get("Reminders", {}), indent=4))
        with open("users.json", "w") as file:
            json.dump(login_database, file, indent=4)
    else:
        print("❌ Reminder not found.")

def ask_user(user_name,login_database):
    print("What would you like to do?")
    print("1. Creat Reminders")
    print("2. Reading Reminders")
    print("3. Update Reminders")
    print("4. Delete Reminders")
    print("5. Exit")

    choice = input("Enter choice (1-5): ").strip()

    if choice == "1":
        create_reminder(user_name,login_database)
    elif choice == "2":
        read_reminders(user_name, login_database)
    elif choice == "3":
        update_reminder(user_name, login_database)
    elif choice == "4":
        delete_reminder(user_name, login_database)
    elif choice == "5":
        print("Goodbye!")
        exit()
    else:
        print("❌ Invalid option. Please enter a number between 1 and 5.")
        ask_user(user_name, login_database)

def sign_up(user_database):
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
    
    print(f"✅ User {user_name} signed up successfully. You can now login.")
    login()

def login():       
    login_user = input("Enter your username: ")
    password = str(getpass.getpass("Enter your password(hidden): "))

    if not os.path.exists("users.json"):
        with open("users.json", "w") as file: # Create an empty dictionary and save to file
            json.dump({}, file, indent=4)

    with open("users.json", "r") as file: # Open the JSON file to read the user database.
        login_database = json.load(file)

    if login_user in login_database.keys() and login_database[login_user].get('Password') == password: 
        print("✅ login sucessfully!")
        ask_user(login_user,login_database) # Call the ask_user function with the logged-in username.
    else:
        print("❌ Username not found or password is incorrect.")
        choose_action = input("Please try again. Press 1 to try again or 2 to sign up: ").strip()
        choose_action_func(choose_action)

def choose_action_func(choose_action):
    if choose_action == "1":
        login()
    elif choose_action == "2":
        sign_up(user_database)
    else:
        print("Invalid option. Please enter 1 for Login or 2 for Sign Up.")
        choose_action = input("Enter either 1 or 2: ").strip()
        choose_action_func(choose_action)

# Brought the choose_action here so that code looks cleaner and more organized.
choose_action = input("Enter either 1 or 2: ").strip() # Made the input more robust by stripping whitespace.
choose_action_func(choose_action) # Call the choose_action function with the user's input.

#comment is ctrl + / in vscode
# pt_name = input("Name: ")
# pt_age = input("Age: ")
# pt_sex =input ("Gender: ")
# med_name = input("Medication name: ")
# med_dose = input("Dosages: ")
# medication_frequency = input("Frequency: ")
# now = datetime.now()
# print("⏰ Current time:", now.strftime("%Y-%m-%d %H:%M:%S"))
# frequency_hour = input("hourly: ")
# next_time = now + timedelta(frequency_hour)


