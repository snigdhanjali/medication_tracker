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
from graphics import *
import os, sys, time, select, getpass, json

print("what would you like to do?")
print("1.login")
print("2.sign_up")

user_database = {}

def calculate_next_reminder(frequency,last_time):
    date_format = "%d-%m-%Y %H:%M"
    now = datetime.now()

    try:
        # Convert string dates to datetime objects
        date_list = [
            datetime.strptime(date_str, date_format)
            for date_str in frequency['Date']
        ]

        # Filter future dates only
        future_dates = [d for d in date_list if d > now]

        if not future_dates:
            return None  # No future reminders

        # Get the nearest upcoming date
        next_reminder_dt = min(future_dates)

        # Return as formatted string
        return next_reminder_dt.strftime(date_format)
    except Exception as e:
        print(f"❌ Error calculating next reminder: {e}")
        return None
    
def clear_screen():
    os.system("clear")

def show_flashing_reminder(reminder, user, login_database):
    date_format = "%d-%m-%Y %H:%M"

    message = f"💊 Time to take your medicine: {reminder['Medicine_Name']} ({reminder['Dosage']})"

    print("💡 Press Enter to stop the reminder...\n")

    # Flashing loop
    while True:
        clear_screen()
        print("💡 Press Enter to stop the reminder...\n")
        print(f"\033[1;33m{message}\033[0m")
        time.sleep(0.5)

        clear_screen()
        print("💡 Press Enter to stop the reminder...\n")
        print("")
        time.sleep(0.5)

        # Break if Enter is pressed
        if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            sys.stdin.readline()
            break

    # Update reminder info
    now = datetime.now()
    reminder["last_time"] = now.strftime(date_format)

    # Recalculate next_reminder
    try:
        upcoming = [
            datetime.strptime(date, date_format)
            for date in reminder["Frequency"]["Date"]
            if datetime.strptime(date, date_format) > now
        ]
        reminder["next_reminder"] = (
            min(upcoming).strftime(date_format) if upcoming else None
        )
    except Exception as e:
        print(f"⚠️ Error updating next reminder: {e}")
        reminder["next_reminder"] = None

    # Show result to user
    print(f"\n✅ Reminder dismissed at {reminder['last_time']}")
    if reminder["next_reminder"]:
        print(f"🔔 Next reminder scheduled at {reminder['next_reminder']}")
    else:
        print("🛑 No more scheduled reminders.")

    # Save updated reminder to users.json
    try:
        reminder_name = reminder["Reminder_Name"]
        login_database[user]["Reminders"][reminder_name] = reminder

        with open("users.json", "w") as file:
            json.dump(login_database, file, indent=4)

        print("💾 Reminder saved to users.json.")
    except Exception as e:
        print(f"❌ Error saving to file: {e}")

def add_medication():
    while True:
        unit = input('Kindly enter in what frequency would you like to have the medicine (day/week/month): ').strip().lower()
        if unit in ["day", "week", "month"]:
            break
        print("❌ Please enter 'day', 'week', or 'month'.")

    while True:
        try:
            times = int(input('How many times would you like to take the medicine for the unit you entered above?: ').strip())
            if times > 0:
                break
            print("❌ Please enter a positive number.")
        except ValueError:
            print("❌ Please enter a valid number.")

    valid_time_format = "%H%M"
    valid_date_format = "%d%m%Y"

    if unit == 'day':
        # For daily, ask for N times in HHMM format
        date_list = []
        for i in range(times):
            while True:
                time_input = input(f"Enter time #{i+1} in military format (e.g., 1530 for 3:30 PM): ").strip()
                try:
                    time_obj = datetime.strptime(time_input, valid_time_format).time()
                    today = datetime.now().date()
                    combined = datetime.combine(today, time_obj)
                    date_str = combined.strftime("%d-%m-%Y %H:%M")  # Save as string
                    date_list.append(date_str)
                    break
                except ValueError:
                    print("❌ Invalid time format. Please use HHMM (e.g., 0830 or 1930).")

        schedule = {
            "Schedule": unit,
            "Times": times,
            "Date": date_list
        }

    elif unit == 'week':
        # Ask for N days of the week and time
        Days = []
        for i in range(times):
            while True:
                weekday = input(f"Enter weekday #{i+1} (e.g., Monday): ").strip().capitalize()
                if weekday in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
                    break
                print("❌ Please enter a valid weekday.")

            while True:
                time_input = input(f"Enter time for {weekday} in military format (HHMM): ").strip()
                try:
                    time_obj = datetime.strptime(time_input, valid_time_format).time()

                    today = datetime.now()
                    weekday_index = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'].index(weekday)
                    days_ahead = (weekday_index - today.weekday()) % 7

                    while True:
                        reminder_date = today + timedelta(days=days_ahead)
                        combined = datetime.combine(reminder_date.date(), time_obj)
                        date_str = combined.strftime("%d-%m-%Y %H:%M")

                        if date_str not in Days:
                            Days.append(date_str)
                            break
                        else:
                            days_ahead += 7  # Push to next week if duplicate
                    break
                except ValueError:
                    print("❌ Invalid time format. Please use HHMM.")
        schedule = {
            "Schedule": unit,
            "Times": times,
            "Date": Days
        }

    elif unit == 'month':
        # For each month, ask for date in ddmmyyyy and one time
        date_list = []
        for i in range(times):
            while True:
                date_input = input(f"Enter date #{i+1} in ddmmyyyy format: ").strip()
                try:
                    date_obj = datetime.strptime(date_input, valid_date_format).date()
                    break
                except ValueError:
                    print("❌ Invalid date format. Please use ddmmyyyy (e.g. 11062025).")
            while True:
                time_input = input(f"Enter time for {date_input} in HHMM format: ").strip()
                try:
                    time_obj = datetime.strptime(time_input, valid_time_format).time()
                    combined = datetime.combine(date_obj, time_obj)
                    date_str = combined.strftime("%d-%m-%Y %H:%M")
                    date_list.append(date_str)
                    break
                except ValueError:
                    print("❌ Invalid time format. Please use HHMM.")
        
        schedule = {
            "Schedule": unit,
            "Times": times,
            "Date": date_list
        }

    return schedule

def create_reminder(user, login_database):
    print("Creating a new reminder...")
    while True:
        reminder_name = input("Reminder name: ").strip()
        if not reminder_name:
            print("❌ Reminder name cannot be blank.")
            continue
        if reminder_name in login_database[user].get("Reminders", {}):
            print("❌ A reminder with this name already exists. Please choose a different name.")
            continue
        break
    medicine_name = input('Medicine name: ').strip()
    dosage = input("Dosage details: ").strip()
    
    frequency = add_medication()
    last_time = None

    reminder_data = {
        "Reminder_Name": reminder_name,
        "Medicine_Name": medicine_name,
        "Dosage": dosage,
        "Frequency": frequency,
        "last_time": last_time,
        "next_reminder": calculate_next_reminder(frequency,last_time)
    }

    login_database[user].setdefault("Reminders", {})[reminder_name] = reminder_data

    print(print(json.dumps(login_database[user], indent=4)))

    with open("users.json", "w") as file:
        json.dump(login_database, file, indent=4)

    print("✅ Reminder created.")

    ask_user(user,login_database)

def read_reminders(user, login_database):
    print("Your reminders:")
    reminders = login_database[user].get("Reminders", {})
    if reminders:
        print(json.dumps(reminders, indent=4))
    else:
        print("No reminders found.")

    ask_user(user,login_database)

def update_reminder(user, login_database):
    if not login_database[user]['Reminders']:
        print("❌ No reminders to update.")
        ask_user(user, login_database)

    # Print all current reminders
    print("\n📋 Current Reminders:\n")
    for key, value in login_database[user]['Reminders'].items():
        print(f"🔹 {key}")

    reminder_name = input("\nWhich reminder do you want to update? ").strip()

    if reminder_name not in login_database[user]['Reminders']:
        print("❌ Reminder not found.")
        ask_user(user, login_database)

    current_data = login_database[user]['Reminders'][reminder_name]

    # Update each field
    new_rem_name = input("New reminder name (leave blank to keep current): ").strip()
    new_dosage = input("New dosage (leave blank to keep current): ").strip()
    new_medicine_name = input("New medicine name (leave blank to keep current): ").strip()

    # Ask whether to update schedule
    update_schedule = input("Do you want to update the medication frequency/schedule? (yes/no): ").strip().lower()

    if update_schedule == "yes":
        new_frequency = add_medication()
    else:
        new_frequency = current_data["Frequency"]

    # Final data to update
    updated_data = {
        "Reminder_Name": new_rem_name if new_rem_name else current_data["Reminder_Name"],
        "Dosage": new_dosage if new_dosage else current_data["Dosage"],
        "Medicine_Name": new_medicine_name if new_medicine_name else current_data["Medicine_Name"],
        "Frequency": new_frequency,
        "last_time": None,
        "next_reminder": None
    }

    # Update the dictionary key if reminder name changed
    final_reminder_name = new_rem_name if new_rem_name else reminder_name

    # If name is unchanged
    if final_reminder_name == reminder_name:
        login_database[user]["Reminders"][reminder_name] = updated_data
    else:
        # Delete old key and add new key
        del login_database[user]["Reminders"][reminder_name]
        login_database[user]["Reminders"][final_reminder_name] = updated_data

    # Save to file
    with open("users.json", "w") as file:
        json.dump(login_database, file, indent=4)

    print("✅ Reminder updated successfully!\n")
    print(json.dumps(login_database[user]['Reminders'][final_reminder_name], indent=4))

    ask_user(user,login_database)

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

    ask_user(user,login_database)

def wait_for_reminder(user, login_database):
    date_format = "%d-%m-%Y %H:%M"

    while True:
        reminders = login_database[user].get("Reminders", {})
        now = datetime.now()

        # ✅ Recalculate next_reminder for each reminder
        for rem_name, reminder in reminders.items():
            new_next = calculate_next_reminder(reminder["Frequency"], reminder["last_time"])
            reminder["next_reminder"] = new_next

        # ✅ Save the recalculated reminders to users.json
        try:
            with open("users.json", "w") as file:
                json.dump(login_database, file, indent=4)
        except Exception as e:
            print(f"❌ Error saving recalculated reminders: {e}")

        # Gather all valid future reminders
        upcoming = []
        for rem_name, reminder in reminders.items():
            try:
                next_time_str = reminder.get("next_reminder")
                if next_time_str:
                    next_time = datetime.strptime(next_time_str, date_format)
                    if next_time > now:
                        upcoming.append((next_time, rem_name, reminder))
            except Exception as e:
                print(f"⚠️ Skipping {rem_name} due to error: {e}")

        if not upcoming:
            print("🛑 No future reminders scheduled. Returning to main menu.")
            ask_user(user,login_database)  # Exit wait mode and return to menu

        # Pick the soonest reminder
        upcoming.sort()
        soonest_time, soonest_name, soonest_reminder = upcoming[0]

        # Show countdown until the time arrives
        while True:
            now = datetime.now()

            # Round to the nearest minute
            now_rounded = now.replace(second=0, microsecond=0)
            soonest_rounded = soonest_time.replace(second=0, microsecond=0)

            if now_rounded >= soonest_rounded:
                break  # Time reached

            # Show countdown
            time_left = (soonest_time - now).total_seconds()
            mins, secs = divmod(int(time_left), 60)
            clear_screen()
            print(f"🕓 Waiting to remind you about '{soonest_name}' at {soonest_time.strftime(date_format)}...")
            print(f"⏳ Time left: {mins} minutes {secs} seconds")
            time.sleep(5)

        # Time reached — flash reminder
        show_flashing_reminder(soonest_reminder, user, login_database)

        # ✅ Loop back again to recalculate and check the next one

def ask_user(user_name,login_database):
    print("What would you like to do?")
    print("1. Create Reminders")
    print("2. Show Reminders")
    print("3. Update Reminders")
    print("4. Delete Reminders")
    print("5. Check for next reminder and wait")
    print("6. Exit")

    choice = input("Enter choice (1-6): ").strip()

    if choice == "1":
        create_reminder(user_name,login_database)
    elif choice == "2":
        read_reminders(user_name, login_database)
    elif choice == "3":
        update_reminder(user_name, login_database)
    elif choice == "4":
        delete_reminder(user_name, login_database)
    elif choice == "5":
        wait_for_reminder(user_name, login_database)
    elif choice == "6":
        print("Goodbye!")
        exit()
    else:
        print("❌ Invalid option. Please enter a number between 1 and 5.")
        ask_user(user_name, login_database)

def sign_up(user_database):
    if os.path.exists("users.json"):
        with open("users.json", "r") as file:
            try:
                user_database = json.load(file)
            except json.JSONDecodeError:
                print("⚠️ Warning: users.json is empty or corrupted. Starting fresh.")
    
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
        password = getpass.getpass("Set a Password (min 8 chars, upper, lower, digit, special): ").strip()
        if len(password) < 8:
            print("❌ Password must be at least 8 characters long.")
            continue
        if (not any(c.islower() for c in password) or
            not any(c.isupper() for c in password) or
            not any(c.isdigit() for c in password) or
            not any(c in "!@#$%^&*()-_=+[]{}|;:',.<>?/`~" for c in password)):
            print("❌ Password must include upper, lower, digit, and special character.")
            continue
        break

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