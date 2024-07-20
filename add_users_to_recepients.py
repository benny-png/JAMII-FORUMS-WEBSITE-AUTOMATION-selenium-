import time
import pyautogui
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
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

# Function to type text in a human-like way
def type_text(element, text, delay=0.1):
    for character in text:
        element.send_keys(character)
        time.sleep(delay)

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

# Function to ensure an element is interactable
def ensure_interactable(by, value, timeout=10):
    WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((by, value)))

# Function to send a message to a single user
def send_message_to_user(user_name):
    # Navigate to the target page
    driver.get('https://www.jamiiforums.com/conversations/add')
    time.sleep(5)  # Wait for the target page to load completely

    # Locate the search field within the select2 element
    search_field = driver.find_element(By.CSS_SELECTOR, 'input.select2-search__field')

    # Clear the search field before typing
    search_field.clear()

    # Locate the title input field and set the title
    title_input = driver.find_element(By.CSS_SELECTOR, 'input.input.input--title')
    title_input.clear()
    type_text(title_input, 'VOTE (Piga Kura) Stories of Change SOC04')

    # Add the user
    type_text(search_field, user_name)
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'li.select2-results__option--highlighted'))
    )
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, 'li.select2-results__option--highlighted').click()
    time.sleep(2)  # Wait for the user to be added

    # Simulate pressing the Tab key twice to move to the message input field
    pyautogui.press('tab')
    time.sleep(0.5)
    pyautogui.press('tab')
    time.sleep(0.5)

    # Clear the message field
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('delete')

    # Add your message content
    message_text = (
        """Habari, nimekupigia kura kwenye chapisho lako kupitia ukurasa wa "The Stories of Change". Nami naomba kura yako kwenye bandiko langu linalohusu "Uundwaji wa Wizara Muhimu ya Sayansi na Teknolojia Tanzania". Unaweza kusoma na kunipigia kura kwa kubofya linki hiki: Dira ya Maendeleo ya Kasi 2035 (Exponential Development Vision 2035).

Asante kwa kusoma na kupiga kura yako.
        """
    )

    pyautogui.typewrite(message_text, interval=0.05)  # Slightly faster typing for longer texts

    time.sleep(5)
    
    # Ensure the send button is interactable before clicking
    send_button = driver.find_element(By.CSS_SELECTOR, 'button.btn-corner[type="submit"]')
    driver.execute_script("arguments[0].click();", send_button)
    time.sleep(5)  # Wait for the message to be sent

    print(f"SENT MESSAGE TO: {user_name}")

# Send messages to each user one by one
for user_name in user_names:
    send_message_to_user(user_name)

# Close the driver
driver.quit()
