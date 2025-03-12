import requests
import subprocess
import time
import os.path

if __name__ == "__main__":

    url = "https://downloads.raspberrypi.com/raspios_lite_armhf/release_notes.txt"
    p = "last_date.txt"
    max_responses = 5

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
        notification_text = "New update here!"
        with open(p, "w") as f:
            f.write(curr_date)
    else:
        notification_text = "No updates yet."

    cmd = ("powershell.exe", "-File", "./update_notifier.ps1", f"{notification_text}")
    p = subprocess.run(cmd)
