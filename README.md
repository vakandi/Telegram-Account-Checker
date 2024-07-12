# Telegram Username Checker

This Python script checks the existence of Telegram usernames by parsing data from JSON files and classifying the usernames into existing and non-existing categories. The script uses the `requests` library to make HTTP requests and the `BeautifulSoup` library to parse HTML content.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Functions](#functions)
- [Report](#report)
- [License](#license)

## Prerequisites
- Python 3.x
- The following Python libraries:
  - `requests`
  - `beautifulsoup4`

## Installation
1. Clone this repository:
   ```bash
   git clone <repository_url>
   ```
2. Navigate to the project directory:
   ```bash
   cd telegram-username-checker
   ```
3. Install the required libraries:
   ```bash
   pip install requests beautifulsoup4
   ```

## Usage
1. Ensure you have the required JSON files in the `scrap_leads` directory, located in the parent directory of the script:
   - `onlineData_1.json`
   - `onlineData_2.json`
   - `online_3.json`

2. Create a `data` directory in the parent directory of the script. This will store the results:
   - `exist_users.json`
   - `does_not_exist_users.json`

3. Run the script:
   ```bash
   python telegram_username_checker.py
   ```

4. Follow the on-screen instructions to check usernames.

## Functions
### `ask_file_path()`
Prompts the user to select a JSON file to retrieve usernames from. The user selects the file by entering the associated number.

### `check_username(username)`
Checks if a given Telegram username exists by making an HTTP request to the Telegram URL and parsing the response.

### `move_users_exist(username, profile_link, avatar_link)`
Moves usernames that exist to the `exist_users.json` file.

### `move_users_does_not_exist(username, profile_link, avatar_link)`
Moves usernames that do not exist to the `does_not_exist_users.json` file.

### `main_checker()`
Main function that processes the usernames from the selected JSON file, checks their existence, and categorizes them accordingly.

### `final_report()`
Generates a final report on the usernames checked, including percentages of existing and non-existing users.

## Report
The script generates a report at the end of the checking process, showing:
- Total number of users checked
- Percentage of users that exist
- Percentage of users that do not exist


