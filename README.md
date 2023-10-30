# Host Checker

In this project, the Python script, `host_checker.py`, is a tool to check the reachability of specified hosts and send email notifications in case any of the hosts become unreachable.

### Overview

The script is designed to:

- Read configuration data from a `config.json` file.
- Check the reachability of specified hosts at defined intervals.
- Log information regarding the status of each host in `host_checker.log`.
- Send email notifications to a specified email address if any host is found to be unreachable.

### Requirements

- Python 3.6 or higher
- `python-dotenv` library for handling environment variables

### Setup

1. Create a `.env` file to store your email credentials:
    ```
    EMAIL=your_email@gmail.com
    PASSWORD=your_app_password
    TO_EMAIL=recipient_email@example.com
    ```

2. Populate the `config.json` file with the list of hosts to check and the checking interval in seconds.

### Usage

Run the script by executing `python host_checker.py`.

### Important Notes

- Ensure the required Python libraries are installed. You can install necessary libraries using `pip install -r requirements.txt`.
- The `config.json` file contains the list of hosts to be checked and the interval between checks.

### Additional Information

- **Using Gmail for Email Notification:**
  To enable email notifications, ensure that your Gmail account is set up to allow SMTP access. You will need to generate an App password in your Google account settings. Go to the Security options and turn on 2-factor authentication. Then, generate an App password specifically for this script.

- **SMTP Library for Sending Emails:**
  This script uses the `smtplib` library for sending email notifications. Make sure to use the generated App password as the `PASSWORD` in the `.env` file.

The script uses asynchronous programming and asyncio to efficiently handle multiple host checks concurrently.
