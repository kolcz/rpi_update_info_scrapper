import requests
import subprocess
from dotenv import load_dotenv
import time
import os
from smtplib import SMTP_SSL
from email.message import EmailMessage

if __name__ == "__main__":

    url = "https://downloads.raspberrypi.com/raspios_lite_armhf/release_notes.txt"
    p = "last_date.txt"
    max_responses = 5
    load_dotenv()
    smtp_host = os.environ.get("SMTP_HOST")
    smtp_port = os.environ.get("SMTP_PORT")
    smtp_username = os.environ.get("SMTP_USERNAME")
    smtp_password = os.environ.get("SMTP_PASSWORD")

    response_counter = 0
    response_code = 0

    while response_code != 200:
        try:
            response = requests.get(url)
            response_code = response.status_code
        except:
            time.sleep(5)
            response_counter += 1

        if response_counter > max_responses:
            exit()

    content = response.text
    
    curr_date = content.split("\n")[0].rstrip(":")

    if not os.path.exists(p):
        with open(p, "w") as f:
            f.write(curr_date)
        last_date = curr_date
    else:
        with open(p) as f:
            last_date = f.read().strip()

    if curr_date != last_date:
        with open(p, "w") as f:
            f.write(curr_date)

        with SMTP_SSL(smtp_host, smtp_port) as smtp_client:
            smtp_client.login(smtp_username, smtp_password)

            msg  = EmailMessage()
            msg.set_content("New update here!")
            msg['Subject'] = "RPi update scrapper message"
            msg['From'] = smtp_username
            msg['To'] = smtp_username

            smtp_client.send_message(msg)
