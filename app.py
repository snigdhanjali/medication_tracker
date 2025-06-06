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

# When you take input for the sign up use a dictionary. How?
# user_detail = {
#     'name': '',
#     'age':'',
#     'gender': '',
#     'password': ''
# }
# This dictionary can then be stored in a larger dictionary called users.
# Store this information in a file and then read from it later.
import getpass
user_database = {}
import pprint
from datetime import datetime, timedelta
print("what would you like to do?")
print("1.login")
print("2.sign_up")
choose_action= input("Enter 1 or 2: ").strip()
    
def sign_up():
    user_name = str(input("user_name: ")).lower()
    age = int(input("age: "))
    gender = str(input("gender(male/female/trans):")).lower()
    password = getpass.getpass("set a password(hidden): ")

    user_database[user_name] = {
        "age":age,
        "gender":gender,
        "pasword":password
    }    

    if gender == 'male':
         print("gender set to male. ")
    elif gender == 'female':
        print("gender set to female.")
    elif gender == 'trans':
        print("gender set to trans. ")
    elif gender == 'unknown':
        print("unknown gender")
    print("✅ sign_up complete. you can now login.")
    login()

def login():       
    login_user = input("enter your user_name: ")
    password = getpass.getpass("enter your password(hidden): ")
    if login_user in user_database.keys() and user_database [login_user].get(password) == password: 
        print("✅ login sucessfully!")
    else:
        print("❌ user name not found!")

def create_reminder(user):
    print("Creating a new reminder...")
    reminder_name = input("Reminder name: ").strip()
    dosage = input("Dosage details: ").strip()
    time = input("Time: ").strip()

    reminder_data = {
        "Dosage": dosage,
        "Time": time
    }

    user_database[user].setdefault("Reminders", {})[reminder_name] = reminder_data
    print("✅ Reminder created.")

def read_reminders(user):
    print("Your reminders:")
    reminders = user_database[user].get("Reminders", {})
    if reminders:
        pprint.pprint(reminders)
    else:
        print("No reminders found.")

def update_reminder(user):
    reminders = user_database[user].get("Reminders", {})
    if not reminders:
        print("❌ No reminders to update.")
        return

    print("🔁 Available reminders:")
    for name in reminders:
        print(f" - {name}")
    reminder_name = input("Which reminder do you want to update? ").strip()

    if reminder_name in reminders:
        new_dosage = input("New dosage: ").strip()
        new_time = input("New time: ").strip()
        reminders[reminder_name] = {
            "Dosage": new_dosage,
            "Time": new_time
        }
        print("✅ Reminder updated.")
    else:
        print("❌ Reminder not found.")

def delete_reminder(user):
    reminders = user_database[user].get("Reminders", {})
    if not reminders:
        print("❌ No reminders to delete.")
        return

    print("🗑️ Available reminders:")
    for name in reminders:
        print(f" - {name}")
    reminder_name = input("Which reminder do you want to delete? ").strip()

    if reminder_name in reminders:
        del reminders[reminder_name]
        print("🗑️ Reminder deleted.")
    else:
        print("❌ Reminder not found.")

def reminder_menu(user):
    while True:
        print("What would you like to do?")
        print("1. Create a reminder")
        print("2. Read your reminders")
        print("3. Update a reminder")
        print("4. Delete a reminder")
        print("5. Exit")

        choice = input("Enter choice (1-5): ").strip()

        if choice == "1":
            create_reminder(user)
        elif choice == "2":
            read_reminders(user)
        elif choice == "3":
            update_reminder(user)
        elif choice == "4":
            delete_reminder(user)
        elif choice == "5":
            print("👋 Exiting reminder manager.")
            break
        else:
            print("❌ Invalid choice. Please select 1-5.")

if choose_action == "1":
    login()
elif choose_action == "2":
    sign_up()
else:
    print("invalid option. please enter 1 or 2.")

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


