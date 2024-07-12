import json
import requests
from bs4 import BeautifulSoup
import os



# Get the current directory of the script
current_directory = os.path.dirname(os.path.abspath(__file__))

# Define the target folder name in the parent directory
scrap_leads_name = 'scrap_leads'
data_name = 'data'
# Construct the path to the parent folder
scrap_leads_path = os.path.abspath(os.path.join(current_directory, os.path.pardir, scrap_leads_name))
data_path = os.path.abspath(os.path.join(current_directory, os.path.pardir, data_name))

if not os.path.exists(scrap_leads_path):
    print(f"The parent folder path {scrap_leads_path} does not exist")

if not os.path.exists(data_path):
    print(f"The parent folder path {data_path} does not exist")



def ask_file_path():
    try:
        choices_files = ['onlineData_BLB_full.json', 'onlineData_SUNRISE_full.json', 'onlineData_Sphere.json']
        #ask for the file path with acnumbered choices , one choice in each line and a associated number for each choice, and thecinout the number of the choice
        file_path = input("Enter the file path of the data you want to retrieve users from: \n1. onlineData_BLB.json\n2. onlineData.json\n3. onlineData_Sphere.json\n")
        if file_path == "1":
            file_path = "onlineData_BLB_full.json"
        elif file_path == "2":
            file_path = "onlineData_SUNRISE_full.json"
        elif file_path == "3":
            file_path = "onlineData_Sphere.json"
        else:
            print("Please enter a valid choice.")
            exit()
        #add the folder path knowing that the folder is in ../scrap_leads
        file_path = os.path.join(scrap_leads_path, file_path)
    except FileNotFoundError:
        print("File not found. Please enter a valid file path.")
        exit()

    except KeyboardInterrupt:
        print("\nExiting...")
        exit()

    return file_path


# Function to check if a username exists on Telegram
def check_username(username):
    try:
        url = f'https://t.me/{username}'
        response = requests.get(url)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            if 'tgme_page_title' in str(soup):
                return True, f'User {username} exists.'
            else:
                return False, f'User {username} does not exist.'
        elif response.status_code == 404:
            return False, f'User {username} does not exist.'
        else:
            return False, "Error"
    except requests.exceptions.RequestException as e:
        return False, "Error"
    except KeyboardInterrupt:
        print("\nExiting...")
        exit()
    except Exception as e:
        return False, "Error"

def move_users_exist(username, profile_link, avatar_link):

    # Path to the exist_users.json file
    exist_file_path = os.path.join(data_path, 'exist_users.json')
    
    # Check if the file exists; if not, create an empty list as a JSON file
    if not os.path.exists(exist_file_path):
        with open(exist_file_path, 'w') as file:
            json.dump([], file)

    # Read the existing data from the file
    with open(exist_file_path, 'r') as file:
        data = json.load(file)

    # Check if the user already exists in the file
    user_exists = False
    for user in data:
        if user.get('username') == username:
            user_exists = True
            break

    # If the user doesn't exist, add them to the data list
    if not user_exists:
        user_entry = {
            "username": username,
            "profileLink": profile_link,
            "avatar": avatar_link
        }
        data.append(user_entry)

    # Write the updated data back to the file
    with open(exist_file_path, 'w') as file:
        json.dump(data, file, indent=4)


def move_users_does_not_exist(username, profile_link, avatar_link):
    # Path to the does_not_exist_users.json file
    does_not_exist_file_path = os.path.join(data_path, 'does_not_exist_users.json')

    # Check if the file exists; if not, create an empty list as a JSON file
    if not os.path.exists(does_not_exist_file_path):
        with open(does_not_exist_file_path, 'w') as file:
            json.dump([], file)

    # Read the existing data from the file
    with open(does_not_exist_file_path, 'r') as file:
        data = json.load(file)

    # Check if the user already exists in the file
    user_exists = False
    for user in data:
        if user.get('username') == username:
            user_exists = True
            break

    # If the user doesn't exist, add them to the data list
    if not user_exists:
        user_entry = {
            "username": username,
            "profileLink": profile_link,
            "avatar": avatar_link
        }
        data.append(user_entry)

    # Write the updated data back to the file
    with open(does_not_exist_file_path, 'w') as file:
        json.dump(data, file, indent=4)




def main_checker():
    # Read the JSON file
    file_path = ask_file_path()
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Asking how many users to check
    num_users = int(input("How many users do you want to check? "))
    asked_users = num_users

    # Ensure the files exist
    exist_file_path = os.path.join(data_path, 'exist_users.json')
    does_not_exist_file_path = os.path.join(data_path, 'does_not_exist_users.json')
    
    if not os.path.exists(exist_file_path):
        with open(exist_file_path, 'w') as file:
            json.dump([], file)

    if not os.path.exists(does_not_exist_file_path):
        with open(does_not_exist_file_path, 'w') as file:
            json.dump([], file)

    with open(exist_file_path, 'r') as file:
        exist_data = {user['username'] for user in json.load(file)}

    with open(does_not_exist_file_path, 'r') as file:
        does_not_exist_data = {user['username'] for user in json.load(file)}

    nb_users_ok = 0
    nb_users_not_ok = 0

    for entry in data:
        members = entry.get('members', [])
        for member in members:
            username = member.get('username')
            profile_link = member.get('profileLink')
            avatar_link = member.get('avatar')

            if username in exist_data or username in does_not_exist_data:
                print(f"🆗 User {username} has already been checked.")
                continue

            print(f"🔁 Checking user {username}...")
            exists, message = check_username(username)
            if message == 'Error':
                print(f"Error checking user {username}, retrying...")
                exists, message = check_username(username)
                if message == 'Error':
                    print(f"Error checking user {username}, skipping...")
                    continue

            if exists:
                nb_users_ok += 1
                print(f"✅ {username} exists")
                move_users_exist(username, profile_link, avatar_link)
                exist_data.add(username)
            else:
                nb_users_not_ok += 1
                print(f"❌ {username} does not exist")
                move_users_does_not_exist(username, profile_link, avatar_link)
                does_not_exist_data.add(username)

            num_users -= 1
            if num_users == 0:
                break
        if num_users == 0:
            break

    print(f"Done checking {asked_users} users. {nb_users_ok} users exist and {nb_users_not_ok} users do not exist.")
    print("\n\nReport:")
    print(f"✅ Percentage of users that exist: {nb_users_ok / asked_users * 100:.2f}%")
    print(f"❌ Percentage of users that do not exist: {nb_users_not_ok / asked_users * 100:.2f}%")



def final_report():
    #read the files
    if not os.path.exists(os.path.join(data_path, 'exist_users.json')):
        with open(os.path.join(data_path, 'exist_users.json'), 'w') as file:
            json.dump([], file)
    if not os.path.exists(os.path.join(data_path, 'does_not_exist_users.json')):
        with open(os.path.join(data_path, 'does_not_exist_users.json'), 'w') as file:
            json.dump([], file)
    with open(os.path.join(data_path, 'exist_users.json'), 'r') as file:
        exist_data = json.load(file)
    with open(os.path.join(data_path, 'does_not_exist_users.json'), 'r') as file:
        does_not_exist_data = json.load(file)
    print("\n\n")
    print("Final Report:")
    #display the number of users that exist and do not exist
    print(f"Total Checked {len(exist_data) + len(does_not_exist_data)}")
    
    total_checked = len(exist_data) + len(does_not_exist_data)
    #calculate the percentage of users chcked based on the total number of users in onlineData_BLB_full.json and onlineData_SUNRISE_full.json and onlineData_Sphere.json
    total_users_checked = 0
    with open(os.path.join(scrap_leads_path, 'onlineData_BLB_full.json'), 'r') as file:
        data = json.load(file)
        for entry in data:
            members = entry.get('members', [])
            total_users_checked += len(members)
    with open(os.path.join(scrap_leads_path, 'onlineData_SUNRISE_full.json'), 'r') as file:
        data = json.load(file)
        for entry in data:
            members = entry.get('members', [])
            total_users_checked += len(members)

    with open(os.path.join(scrap_leads_path, 'onlineData_Sphere.json'), 'r') as file:
        data = json.load(file)
        total_users_checked += len(data)
        
    percent_checked = total_checked/total_users_checked*100
    #keep onmy 2 decimal places
    percent_checked = "{:.2f}".format(percent_checked)
    #print(f"Total Users: {total_users_checked} \nUsers Checked: {total_checked} || Percentage Checked: {percent_checked}%")
    print(f"\033[34mTotal Users: {total_users_checked}\033[0m \n\033[35mUsers Checked: {total_checked}\033[0m || \033[34mPercentage Checked: {percent_checked}%\033[0m")


    print(f"\n________________________________")
    #print(f"✅ Existing Users : {len(exist_data)} || ❌ Non-existant Users: {len(does_not_exist_data)}")
    print(f"\033[32m ✅ Existing Users : {len(exist_data)}\033[0m || \033[31m❌ Non-existant Users: {len(does_not_exist_data)}\033[0m")
    print(f"________________________________")
    if len(exist_data) + len(does_not_exist_data) == 0:
        print("No users found")
        return

    percent_exist = len(exist_data)/(len(exist_data) + len(does_not_exist_data))*100
    #keep onmy 2 decimal places
    percent_exist = "{:.2f}".format(percent_exist)


def final_report_old():
    #read the files
    if not os.path.exists(os.path.join(data_path, 'exist_users.json')):
        with open(os.path.join(data_path, 'exist_users.json'), 'w') as file:
            json.dump([], file)
    if not os.path.exists(os.path.join(data_path, 'does_not_exist_users.json')):
        with open(os.path.join(data_path, 'does_not_exist_users.json'), 'w') as file:
            json.dump([], file)
    with open(os.path.join(data_path, 'exist_users.json'), 'r') as file:
        exist_data = json.load(file)
    with open(os.path.join(data_path, 'does_not_exist_users.json'), 'r') as file:
        does_not_exist_data = json.load(file)


    print("\n\n")
    print("Final Report:")
    #display the number of users that exist and do not exist
    print(f"Total Checked {len(exist_data) + len(does_not_exist_data)}")
    
    total_checked = len(exist_data) + len(does_not_exist_data)
    #calculate the percentage of users chcked based on the total number of users in onlineData_BLB_full.json and onlineData_SUNRISE_full.json and onlineData_Sphere.json
    total_users_checked = 0
    with open(os.path.join(scrap_leads_path, 'onlineData_BLB_full.json'), 'r') as file:
        data = json.load(file)
        for entry in data:
            members = entry.get('members', [])
            total_users_checked += len(members)
    with open(os.path.join(scrap_leads_path, 'onlineData_SUNRISE_full.json'), 'r') as file:
        data = json.load(file)
        for entry in data:
            members = entry.get('members', [])
            total_users_checked += len(members)

    with open(os.path.join(scrap_leads_path, 'onlineData_Sphere.json'), 'r') as file:
        data = json.load(file)
        for entry in data:
            members = entry.get('members', [])
            total_users_checked += len(members)
    percent_checked = total_checked/total_users_checked*100
    print(f"Total Users: {total_users_checked} \nUsers Checked: {total_checked} || Percentage Checked: {percent_checked}%")


    print(f"\n________________________________")
    print(f"✅ Existing Users : {len(exist_data)} || ❌ Non-existant Users: {len(does_not_exist_data)}")
    print(f"________________________________")
    #chexk if itscnot a division by zero
    if len(exist_data) + len(does_not_exist_data) == 0:
        print("No users checked.")
        return
    #calculate the percentage of users that exist and do not exist
    percent_exist = len(exist_data)/(len(exist_data) + len(does_not_exist_data))*100
    #keep onmy 2 decimal places
    percent_exist = "{:.2f}".format(percent_exist)
    percent_dontexist = len(does_not_exist_data)/(len(exist_data) + len(does_not_exist_data))*100
    percent_dontexist = "{:.2f}".format(percent_dontexist)
    print(f"\n________________________________")
    print(f"Percentage :\n")
    print(f"\033[32m ✅ Exist: {percent_exist}%\033[0m  ❌ Does not exist: {percent_dontexist}%")
    

    


if __name__ == '__main__':
    final_report()
    try:
        input_check = input("Do you want to check usernames? (y/n): ")
        if input_check == "y":
            main_checker()
        else:
            print("Exiting...")
            exit()
    except KeyboardInterrupt:
        print("\nExiting...")
        exit()

    
