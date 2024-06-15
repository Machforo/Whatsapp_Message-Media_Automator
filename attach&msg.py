import time
import pickle
import json
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
import os

# Setup logging  to provide information and errors during execution
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load configuration from config.json
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# Extract configuration values
SERVICE_PATH = config['service_path']
COOKIES_FILE = config['cookies_file']
SCHEDULE_FILE = config['schedule_file']
GROUPS_FILE = config['groups_file']
SEARCH_BOX_XPATH = config['search_box_xpath']
SEND_BUTTON_XPATH = config['send_button_xpath']
ATTACHMENT_BUTTON_XPATH = config['attachment_button_xpath']
IMAGE_BOX_XPATH = config['image_box_xpath']
CAPTION_BOX_XPATH = config['caption_box_xpath']

# Set the console encoding to UTF-8 to handle Unicode characters
sys.stdout.reconfigure(encoding='utf-8')

# Initialize Edge WebDriver for Selenium automation
service = Service(SERVICE_PATH)
options = Options()
browser = webdriver.Edge(service=service, options=options)
browser.maximize_window()

# Function to filter out non-BMP characters from text
def filter_non_bmp(text):
    return ''.join(c for c in text if ord(c) <= 0xFFFF)

# Function to load cookies into the WebDriver session
def load_cookies(browser, cookies_file):
    if os.path.exists(cookies_file):
        with open(cookies_file, 'rb') as file:
            cookies = pickle.load(file)
            for cookie in cookies:
                if 'expiry' in cookie:
                    del cookie['expiry']
                browser.add_cookie(cookie)
        logging.info("Cookies loaded successfully.")
    else:
        logging.warning("Cookies file not found.")

# Function to save cookies from the WebDriver session to a file
def save_cookies(browser, cookies_file):
    with open(cookies_file, 'wb') as file:
        pickle.dump(browser.get_cookies(), file)
    logging.info("Cookies saved successfully.")

# Load schedule data from JSON file
def load_schedule(schedule_file):
    with open(schedule_file, 'r', encoding='utf-8') as file:
        return json.load(file)

# Load groups from text file
def load_groups(groups_file):
    with open(groups_file, 'r', encoding="utf8") as f:
        return [group.strip() for group in f.readlines()]

# Load message from a text file
def load_message(message_file):
    with open(message_file, 'r', encoding='utf-8') as file:
        return file.read()

# Function to wait until the specified time
def wait_until(target_time):
    now = datetime.now()
    target_time = datetime.strptime(target_time, '%Y-%m-%d %H:%M:%S')
    sleep_time = (target_time - now).total_seconds()
    if sleep_time > 0:
        time.sleep(sleep_time)

# Function to send a message to a specified group with optional attachment
def send_message_to_group(group, message, attachment_path):
    try:
        # Locate and interact with the search box
        search_box = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, SEARCH_BOX_XPATH))
        )
        search_box.clear()  # Clear any previous input
        time.sleep(0.1)  # Allow time for the search box to clear
        search_box.send_keys(Keys.CONTROL + "a")
        search_box.send_keys(Keys.DELETE)
        time.sleep(0.1)  # Allow time for the search box to clear
        search_box.send_keys(group)
        search_box.send_keys(Keys.ENTER)

        # Wait for the chat to open and be ready
        chat_header_xpath = f'//span[@title="{group}"]'
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, chat_header_xpath))
        )

        time.sleep(1)  # Ensure chat is fully loaded

        if attachment_path:
            # Click the attachment button
            attachment_button = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.XPATH, ATTACHMENT_BUTTON_XPATH))
            )
            attachment_button.click()

            time.sleep(0.1)  # Ensure attachment menu is fully loaded

            # Upload the image or file
            image_box = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH, IMAGE_BOX_XPATH))
            )
            image_box.send_keys(os.path.abspath(attachment_path))

            time.sleep(0.1)  # Ensure the image is uploaded



            # Send the message as a caption
            caption_box = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH, CAPTION_BOX_XPATH))
            )

            # Split message by non-BMP characters and send each part
            for part in filter_non_bmp(message).split('\n'):
                caption_box.send_keys(part)
                caption_box.send_keys(Keys.SHIFT, Keys.ENTER)

            caption_box.send_keys(Keys.ENTER)

            time.sleep(1)  # Ensure the caption is added

            # Click the send button
            send_button = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.XPATH, SEND_BUTTON_XPATH))
            )
            send_button.click()

        time.sleep(0.01)  # Delay before moving to the next group

    except Exception as e:
        logging.error(f"An error occurred while processing group {group}: {e}")

# Main logic
try:
    # Check if cookies file exists to determine if session can be restored
    cookies_exist = os.path.exists(COOKIES_FILE)

    # open WhatsApp Web in the WebDriver
    browser.get('https://web.whatsapp.com')

     # If cookies exist, load them into the browser session and refresh
    if cookies_exist:
        # Load cookies into browser
        load_cookies(browser, COOKIES_FILE)
        browser.refresh()

    # Wait for WhatsApp Web to load and the search box to be present
    try:
        WebDriverWait(browser, 60).until(EC.presence_of_element_located((By.XPATH, SEARCH_BOX_XPATH)))
    except Exception as e:
        logging.error(f"Failed to locate the search box: {e}")
        browser.quit()
        sys.exit(1)

    # If cookies were not loaded successfully, prompt user to scan QR code and save cookies
    if not cookies_exist or "WhatsApp Web" in browser.title:
        input("Please scan the QR code and press Enter to continue...")
        save_cookies(browser, COOKIES_FILE)

    # Load groups and schedule from respective files
    groups = load_groups(GROUPS_FILE)
    schedule = load_schedule(SCHEDULE_FILE)
    logging.info("Groups to message: %s", groups)

    # Iterate through scheduled messages
    for item in schedule:
        message_file = item['message_file']
        scheduled_time = item['time']
        attachment_path = item['attachment_path']

        # Load message from the specified file
        message = load_message(message_file)
        logging.info(f"Scheduled message from '{message_file}' at {scheduled_time}")

        # Wait until the scheduled time to send the message
        wait_until(scheduled_time)

        # Send the loaded message to each group in the list
        logging.info(f"Sending message from '{message_file}' to all groups")
        for group in groups:
            send_message_to_group(group, message, attachment_path)

finally:
    # Wait a bit before closing the browser to ensure all tasks are completed
    time.sleep(10)
    browser.quit()  # Close the WebDriver session
