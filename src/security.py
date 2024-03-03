import os
import json

def check_credentials(username: str, password: str):
    creds_raw = os.environ["STICKER_CREDENTIALS"]
    creds = json.loads(creds_raw)

    return username in creds and creds[username] == password
