# Whatsapp_Message-Media_Automator
# WhatsApp Automation with Selenium and Python

Automate sending scheduled messages and attachments to WhatsApp groups using Selenium and Python. This project includes scripts for sending text messages, attachments, and both combined, based on predefined schedules. Easily customizable and equipped with optimal delay settings to minimize the risk of WhatsApp bans.

## Features

- **Scheduled Messaging:** Send messages to WhatsApp groups at specified times.
- **Attachment Handling:** Schedule and send attachments with optional captions.
- **Customizable Configurations:** Configure WhatsApp elements and schedules via JSON files.
- **Session Management:** Use cookies to avoid repeated logins.
- **Human-like Behavior:** Implemented delays to mimic human interactions and reduce ban risks.

## Project Structure

### Main Python File
-**`execute.py`**: Main executable file to run. Gives user the chance to choose which type of message to be sent and it further runs the respective files only.

### Sub Python Files
- **`main.py`**: Sends scheduled text messages to WhatsApp groups.
- **`attachment.py`**: Sends scheduled attachments to WhatsApp groups.
- **`msg&attach.py`**: Sends both attachments and captions to WhatsApp groups on a schedule.

### JSON Files
- **`config.json`**: Contains XPath or CSS selectors for WhatsApp elements.
- **`msg_schedule.json`**: Defines the schedule and messages to be sent.
- **`attach_schedule.json`**: Defines the schedule, attachment paths, and captions.

### Helper Files
- **`msg.txt`, `msg_1.txt`**: Text files containing messages to be sent; users can modify or add more message files.
- **`groups.txt`**: A list of group names where the messages are to be sent.

### Cookie Files
- Store login data to avoid repeated logins and facilitate session management.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/your-username/whatsapp-automation.git
    cd whatsapp-automation
    ```

2. Install the required Python packages:
    ```sh
    pip install selenium
    ```

3. Download and configure the WebDriver for your browser (e.g., ChromeDriver for Chrome).

## Configuration

1. **config.json**: Define the XPath or CSS selectors for WhatsApp elements.
    ```json
    {
        "search_box": "//*[@id='search']",
        "message_box": "//*[@id='input']",
        "send_button": "//*[@id='send']",
        "caption_box": "//*[@id='caption']"
    }
    ```

2. **msg_schedule.json**: Define the schedule and messages.
    ```json
    {
        "schedule": [
            {
                "time": "2024-06-15T10:00:00",
                "message": "msg.txt"
            },
            {
                "time": "2024-06-15T12:00:00",
                "message": "msg_1.txt"
            }
        ]
    }
    ```

3. **attach_schedule.json**: Define the schedule, attachment paths, and captions.
    ```json
    {
        "schedule": [
            {
                "time": "2024-06-15T10:00:00",
                "attachment": "/path/to/file1.jpg",
                "caption": "Here is the file1"
            },
            {
                "time": "2024-06-15T12:00:00",
                "attachment": "/path/to/file2.pdf",
                "caption": "Please find the attached document"
            }
        ]
    }
    ```

4. **groups.txt**: List all group names where the messages are to be sent.

## Usage

1. **Send Scheduled Messages:**
    ```sh
    python main.py
    ```

2. **Send Scheduled Attachments:**
    ```sh
    python attachment.py
    ```

3. **Send Both Messages and Attachments:**
    ```sh
    python msg&attach.py
    ```

## Best Practices and Tips

- **Optimal Delay:** Ensure there is a delay between messages to avoid triggering WhatsApp's anti-spam measures. Implement random delays if possible to mimic human behavior.
- **Error Handling:** Add error handling to manage scenarios where WhatsApp web elements are not found or if there is a network issue.
- **Logging:** Implement logging to keep track of sent messages, errors, and other significant events.
- **Security:** Be cautious with storing sensitive data like cookies. Ensure they are stored securely and are not exposed to unauthorized users.





