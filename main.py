import json
import time
from selenium import webdriver
from datetime import datetime, timedelta
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys

# Set the console encoding to UTF-8 for proper character display
sys.stdout.reconfigure(encoding='utf-8')

# Specify the path to the Edge WebDriver
service = Service('msedgedriver.exe')  # Adjust the path accordingly

# Initialize Edge options
options = Options()

# Create a new instance of the Edge driver
browser = webdriver.Edge(service=service, options=options)
browser.maximize_window()

# Function to wait for an element to be present in the DOM
def wait_for_element(xpath, timeout=30):
    return WebDriverWait(browser, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))


# Function to load WhatsApp Web and handle retries if it fails to load
def load_whatsapp_web(retries=3):
    for attempt in range(retries):
        try:
            browser.get('https://web.whatsapp.com')
            # Wait for WhatsApp Web to load and the search box to be present
            wait_for_element('//div[@contenteditable="true" and @data-tab="3"]', timeout=60)
            print("WhatsApp Web loaded successfully.")
            return True
        except Exception as e:
            print(f"Error loading WhatsApp Web (Attempt {attempt + 1}/{retries}): {e}")
            time.sleep(5)  # Wait a bit before retrying
    return False

# Attempt to load WhatsApp Web, exit if unsuccessful
if not load_whatsapp_web():
    print("Failed to load WhatsApp Web after multiple attempts.")
    sys.exit(1)

# Wait for user to scan QR code and log in to WhatsApp Web
input("Please scan the QR code and press Enter to continue...")


# Function to filter out non-BMP characters to prevent potential issues with certain characters
def filter_non_bmp(text):
    return ''.join(c for c in text if ord(c) <= 0xFFFF)

try:
     # Load the schedule of messages from a JSON file
    with open('msg_schedule.json', 'r', encoding="utf8") as f:
        schedule = json.load(f)

     # Load the list of groups from a text file
    with open('groups.txt', 'r', encoding="utf8") as f:
        groups = [group.strip() for group in f.readlines()]
    print("Groups to message:", groups)


    # Prepare the messages to send by reading from the specified files
    messages = []
    for item in schedule:
        message_file = item['message_file']
        with open(message_file, 'r', encoding="utf8") as mess:
            message = mess.read().strip()
            messages.append(filter_non_bmp(message))
    print("Messages to send:", messages)

    # Schedule and send messages at the specified times
    for i, item in enumerate(schedule):
        schedule_time = item['time']
        schedule_time_dt = datetime.strptime(schedule_time, '%Y-%m-%d %H:%M:%S')

        # Calculate the delay in seconds until the scheduled time
        now = datetime.now()
        if schedule_time_dt < now:
            schedule_time_dt += timedelta(days=1)

        delay = (schedule_time_dt - now).total_seconds()
        print(f"Waiting for {delay} seconds to send message '{messages[i]}'")

     # Wait until the scheduled time to send the message
        if delay > 0:
            time.sleep(delay)

     # Send the message to each group
        for group in groups:
            try:
                print(f"Processing group: {group}")

                # Locate and interact with the search box to find the group
                search_box = wait_for_element('//div[@contenteditable="true" and @data-tab="3"]', timeout=10)
                search_box.clear()
                search_box.send_keys(group)
                search_box.send_keys(Keys.ENTER)

                # Wait for the chat to open and be ready
                chat_header_xpath = f'//span[@title="{group}"]'
                wait_for_element(chat_header_xpath, timeout=10)

                # Find the message box and send the message
                message_box_xpath = '//div[@contenteditable="true" and @data-tab="10"]'
                message_box = wait_for_element(message_box_xpath, timeout=10)
                message_box.click()

                 # Type and send the message, handling multi-line messages
                for part in messages[i].split('\n'):
                    message_box.send_keys(part)
                    message_box.send_keys(Keys.SHIFT, Keys.ENTER)

                message_box.send_keys(Keys.ENTER)

                # Minimal delay before moving to the next group
                time.sleep(1)

            except Exception as e:
                print(f"An error occurred while processing group {group}: {e}")

finally:
    # Short delay before closing the browser to ensure all messages are sent
    time.sleep(5)
    browser.quit()