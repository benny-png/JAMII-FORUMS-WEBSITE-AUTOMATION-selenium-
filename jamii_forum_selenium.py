import time
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
username_field.send_keys('mazikuben2@gmail.com')

# Locate and fill the password field by name attribute
password_field = driver.find_element(By.NAME, 'password')
password_field.send_keys('XXXXXXpassword')

# Submit the login form
password_field.send_keys(Keys.RETURN)

# Wait for the login process to complete
time.sleep(5)

# Read the user names from the file
with open('jamii_users_SOC04.txt', 'r') as f:
    user_names = [line.strip() for line in f if line.strip()]

# Function to chunk the list into parts of n elements
def chunk_list(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

# Function to ensure an element is interactable
def ensure_interactable(by, value, timeout=10):
    WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((by, value)))

# Function to send a message to a chunk of users
def send_message_to_users(user_chunk):
    # Navigate to the target page
    driver.get('https://www.jamiiforums.com/conversations/add')
    time.sleep(5)  # Wait for the target page to load completely

    # Locate the search field within the select2 element
    search_field = driver.find_element(By.CSS_SELECTOR, 'input.select2-search__field')

    # Add each user from the chunk
    for user_name in user_chunk:
        time.sleep(2)  
        search_field.send_keys(user_name)
        ensure_interactable(By.CSS_SELECTOR, 'li.select2-results__option--highlighted')
        driver.find_element(By.CSS_SELECTOR, 'li.select2-results__option--highlighted').click()
        time.sleep(2)  # Wait for the user to be added

    # Add your message content
    message_field = driver.find_element(By.NAME, 'message')

    # Click the message field before sending keys
    message_field.click()
    time.sleep(1)  # Allow some time after the click

    message_text = (
        'Habari, nimekupigia kura kwenye chapisho lako kupitia ukurasa wa "The Stories of Change". Nami naomba kura yako kwenye bandiko langu linalohusu '
        '"Uundwaji wa Wizara Muhimu ya Sayansi na Teknolojia Tanzania". Unaweza kusoma na kunipigia kura kwa kubofya kiungo hiki👉👉: '
        'Dira ya Maendeleo ya Kasi 2035 (Exponential Development Vision 2035).'
        '\n\nAsante kwa kusoma na kupiga kura yako.'
    )
    message_field.send_keys(message_text)

    # Select the specific text
    actions = ActionChains(driver)
    actions.move_to_element(message_field)
    actions.click(message_field)
    actions.key_down(Keys.SHIFT)

    # Locate the start and end positions of the text
    start_index = message_text.find('Dira ya Maendeleo ya Kasi 2035 (Exponential Development Vision 2035)')
    for _ in range(start_index):
        actions.send_keys(Keys.ARROW_RIGHT)
    actions.key_down(Keys.SHIFT)
    for _ in range(len('Dira ya Maendeleo ya Kasi 2035 (Exponential Development Vision 2035)')):
        actions.send_keys(Keys.ARROW_RIGHT)
    actions.key_up(Keys.SHIFT)
    actions.perform()

    # Ensure the link button is interactable before clicking
    link_button = driver.find_element(By.CSS_SELECTOR, 'button.ql-strike')
    driver.execute_script("arguments[0].click();", link_button)

    # Wait for the link dialog to appear
    time.sleep(2)

    # Enter the URL in the link dialog (update the selector if needed)
    url_input = driver.find_element(By.CSS_SELECTOR, 'input[type="text"]')
    url_input.send_keys('https://www.jamiiforums.com/threads/exponential-development-vision-2035-dira-ya-maendeleo-ya-kasi-2035.2217724/')
    url_input.send_keys(Keys.RETURN)

    # Ensure the send button is interactable before clicking
    send_button = driver.find_element(By.CSS_SELECTOR, 'button.btn-corner[type="submit"]')
    driver.execute_script("arguments[0].click();", send_button)
    time.sleep(5)  # Wait for the message to be sent

# Chunk the user names and send messages to 5 users each iteration
for user_chunk in chunk_list(user_names, 5):
    send_message_to_users(user_chunk)

# Close the driver
driver.quit()
