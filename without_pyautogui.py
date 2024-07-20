import time
import random
import pyperclip
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configure Chrome options for the website
brave_path = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
options = Options()
options.binary_location = brave_path
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# Initialize the Chrome WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Open the login page
driver.get('https://www.jamiiforums.com/login')

# Wait for the login page to load completely
time.sleep(2)

# Locate and fill the username field by name attribute
username_field = driver.find_element(By.NAME, 'login')
username_field.clear()
username_field.send_keys('mazikuben2@gmail.com')

# Locate and fill the password field by name attribute
password_field = driver.find_element(By.NAME, 'password')
password_field.clear()
password_field.send_keys('Bstar7Bstar7')

# Submit the login form
password_field.send_keys(Keys.RETURN)

# Wait for the login process to complete
time.sleep(5)

# Read the user names from the file
with open('jamii_users_SOC04.txt', 'r') as f:
    user_names = [line.strip() for line in f if line.strip()]

# Specify the number of users to add as recipients at a time
num_users_to_add = 1  # Change this number as needed

# Function to simulate human typing
def human_type(element, text):
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.05, 0.2))  # Random delay between keystrokes

# Function to clear all previously selected usernames
def clear_usernames():
    # Locate the search field within the select2 element
    search_field = driver.find_element(By.CSS_SELECTOR, 'input.select2-search__field')
    search_field.click()  # Move the cursor to the field
    time.sleep(1)  # Allow some time after the click

    # Send backspace keys to clear all selected usernames
    for _ in range(100):  # Assuming a max of 50 usernames to remove
        search_field.send_keys(Keys.BACKSPACE)
         # Small delay between each key press

# Function to send a message to multiple users
def send_message_to_users(user_names):
    # Navigate to the target page
    driver.get('https://www.jamiiforums.com/conversations/add')
    time.sleep(5)  # Wait for the target page to load completely

    # Clear all previously selected usernames
    clear_usernames()

    # Locate the title input field and set the title
    title_input = driver.find_element(By.CSS_SELECTOR, 'input.input.input--title')
    title_input.clear()
    #title_input.send_keys('VOTE (Piga Kura) Stories of Change SOC04')
    human_type(title_input, 'VOTE (Piga Kura) Stories of Change SOC04')

    # Locate the search field within the select2 element
    search_field = driver.find_element(By.CSS_SELECTOR, 'input.select2-search__field')

    # Add the users
    for user_name in user_names:
        human_type(search_field, user_name)
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'li.select2-results__option--highlighted'))
        )
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, 'li.select2-results__option--highlighted').click()
        time.sleep(1)  # Wait for the user to be added

    # Locate the message input field using the data-placeholder attribute
    message_input = driver.find_element(By.CSS_SELECTOR, '[data-placeholder="Message"] .ql-editor')
    message_input.click()
    time.sleep(1)  # Allow some time after the click
    message_input.clear()  # Clear any existing content in the message input

    # Add your message content
    message_text = 'Hello, nimekupigia kura kwenye chapisho lako kupitia ukurasa wa "The Stories of Change". Nami naomba kura yako kwenye bandiko langu linalohusu "Maoni ya kibunifu ya kwa ajili ya maendeleo ya Tanzania". Unaweza kusoma na kunipigia kura kwa kubofya kiungo hiki: 👉 Exponential Development Vision 2035: Dira ya Maendeleo ya Kasi 2035 👈.'

    # Copy the message to clipboard
    pyperclip.copy(message_text)
    actions = ActionChains(driver)
    actions.click(message_input)
    actions.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()

    time.sleep(180)

    # Ensure the send button is interactable before clicking
    send_button = driver.find_element(By.CSS_SELECTOR, 'button.btn-corner[type="submit"]')
    driver.execute_script("arguments[0].click();", send_button)
    time.sleep(5)  # Wait for the message to be sent

    print(f"SENT MESSAGE TO: {', '.join(user_names)}")

# Send messages to each user group one by one
for i in range(0, len(user_names), num_users_to_add):
    send_message_to_users(user_names[i:i + num_users_to_add])
    time.sleep(5)  # Wait a bit before proceeding to the next batch

# Close the driver
driver.quit()
