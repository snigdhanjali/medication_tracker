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
import getpass
user_database = {}
from datetime import datetime, timedelta
print("what would you like to do?")
print("1.login")
print("2.sign_up")
choose_action= input("Enter 1 or 2: ").strip()
    
def sign_up():
    user_name = str(input("user_name: ")).lower()
    age = int(input("age: "))
    gender = str(input("gender(male/female/trans):")).lower()
    pasword = getpass.getpass("set a pasword(hidden): ")

    user_database[user_name] = {
        "age":age,
        "gender":gender,
        "pasword":pasword
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

def login():       
    login_user = input("enter your user_name: ")
    pasword = getpass.getpass("enter your pasword(hidden): ")
    if login_user in user_database and user_database [login_user] == pasword:
        print("✅ login sucessfully!")
    else:
        print("❌ user name not found!")

if choose_action == "1":
    login()
elif choose_action == "2":
    sign_up()
else:
    print("invalid option. please enter 1 or 2.")
if choose_action == "sign_up":
    sign_up()
    if login():
        pass
elif choose_action == login:
    if not login():    
        choice = input("Do you want to sign_up or try again ?(type \"sign_up\",try): ").lower()
        if choice == "sign_up":
            sign_up()
            login()
        elif choice == "tyr":
            login()
            print("exiting...")      
        
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


