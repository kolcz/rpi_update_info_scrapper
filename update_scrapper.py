import requests
import subprocess
import time
import os.path

if __name__ == "__main__":

    url = "https://downloads.raspberrypi.org/raspios_armhf/release_notes.txt"
    p = "last_date.txt"

    response_code = 0
    while True:
        try:
            response = requests.get(url)
        except:
            time.sleep(5)
        else:
            break

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
