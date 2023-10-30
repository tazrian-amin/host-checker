import socket
import smtplib
from email.message import EmailMessage
import asyncio
import json
import os
from dotenv import load_dotenv
import logging
from datetime import datetime

load_dotenv()


def load_config():
    with open('config.json') as config_file:
        config = json.load(config_file)
        return config


config = load_config()

logging.basicConfig(
    filename='host_checker.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

hosts_to_check = config.get('hosts', [])
# default interval is 300 seconds
check_interval = int(config.get('check_interval', 300))


async def check_host_reachability(host, port=80):
    try:
        socket.setdefaulttimeout(2)  # Set a timeout for the connection
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return host, "is reachable"
    except socket.error:
        return host, "is unreachable"


async def check_multiple_hosts():
    unreachable_hosts = []

    while True:
        results = await asyncio.gather(*(check_host_reachability(host) for host in hosts_to_check))
        for result in results:
            print(f"{result[0]} {result[1]}")
            if "is unreachable" in result:
                unreachable_hosts.append(result[0])
                logging.error(f"{result[0]} is unreachable at {
                              datetime.now()}")

        if unreachable_hosts:
            send_notification(unreachable_hosts)
            unreachable_hosts = []

        await asyncio.sleep(check_interval)


def send_notification(unreachable_hosts):
    email = os.getenv("EMAIL")
    password = os.getenv("PASSWORD")
    to_email = os.getenv("TO_EMAIL")

    if not email or not password or not to_email:
        logging.error(
            "Email configuration is missing in the JSON config file.")
        return

    msg = EmailMessage()
    msg.set_content("\n".join(unreachable_hosts) +
                    " is unreachable. Time: " + str(datetime.now()))

    msg['Subject'] = "Unreachable Hosts Notification"
    msg['From'] = email
    msg['To'] = to_email

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(email, password)
            smtp.send_message(msg)
            logging.info("Email sent successfully at " + str(datetime.now()))
            print("Email sent successfully")
    except Exception as e:
        logging.error(f"Failed to send email: {e}")


if __name__ == '__main__':
    asyncio.run(check_multiple_hosts())
