from gigachat import GigaChat
import os
import uuid
import requests
import json
from dotenv import load_dotenv


def get_token(url, key):
    payload = 'scope=GIGACHAT_API_PERS'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        "RqUID": str(uuid.uuid4()),
        "Authorization": f"Basic {key}"
    }
    response = requests.request("POST", url, headers=headers, data=payload, verify=False)
    token = json.loads(response.text)
    return token["access_token"]


def ask(prompt, model="GigaChat-2"):
    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
    load_dotenv()
    key = os.getenv('key')
    token = get_token(url, key)  # Replace with your token variable conten
    API_URL = "https://api.giga.chat/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {token}",
    }
    body = {
        "model": model,
        "messages": [
            {"role": "system", "content": "Ты помощник. Отвечай коротко и по существу."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.3,
    }
    r = requests.post(API_URL, headers=headers, json=body, verify=False, timeout=60)
    r.raise_for_status()
    return r

#token = get_token(url, key)
#print(ask(token, "Объясни в двух предложениях, что такое эмбеддинг."))

