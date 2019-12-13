#!/usr/bin/python3
import json
import sys
import requests
from email.mime.text import MIMEText
from subprocess import Popen, PIPE

r = requests.get('https://plex.tv/api/downloads/5.json')
if r.status_code != 200:
    print("Failed to get latest update JSON")
    sys.exit(1)

latest_version = r.json()["computer"]["Linux"]["version"]

# Read in the file with the previous latest version
f = open("latest_version.txt", "a+")
f.seek(0)
current_version = f.readline()

if current_version == latest_version:
    print("Version is up to date")
    f.close()
    sys.exit(0)

print("New version found!")
# Write out the new version to the file
f.seek(0)
f.truncate()
f.write(latest_version)
f.close()

# Email an update
msg = MIMEText("A new version of Plex Media Server has been released: " + latest_version)
msg["From"] = "ss23+crisp@ss23.geek.nz"
msg["To"] = "ss23@ss23.geek.nz"
msg["Subject"] = "Plex Update: " + latest_version
p = Popen(["/usr/sbin/sendmail", "-t", "-oi"], stdin=PIPE)
p.communicate(msg.as_string().encode("utf-8"))
