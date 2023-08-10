import os

import requests
import urllib.parse

from fastapi import FastAPI, Request

TOKEN = os.getenv("TOKEN", "")  # in Spacefile
HOST = os.getenv("DETA_SPACE_APP_HOSTNAME", "")

BOT_API = f"https://api.telegram.org/bot{TOKEN}"
WEBHOOK_PATH = "/webhook"  # also in Spacefile public_routes


def _https(url: str) -> str:
    """Prepend https:// to url"""

    p = urllib.parse.urlparse(url)
    return p._replace(
        scheme="https",
        netloc=(p.netloc or p.path),
        path=(p.path if p.netloc else ""),
    ).geturl()


def send_msg(chat_id, text):
    return requests.post(
        f"{BOT_API}/sendMessage",
        json={"chat_id": chat_id, "text": text},
    ).json()


# APP

app = FastAPI()


@app.get("/")
def home():
    """Shows webhook info (optional)"""
    resp = requests.get(f"{BOT_API}/getWebhookInfo")
    return resp.json()


@app.get("/setup")
def setup():
    """Sets webhook url on bot (optional)"""
    resp = requests.get(
        f"{BOT_API}/setWebHook",
        params={"url": urllib.parse.urljoin(_https(HOST), WEBHOOK_PATH)},
    )
    return resp.json()


@app.get("/forget")
def forget():
    """Removes webhook url from bot (optional)"""
    resp = requests.get(f"{BOT_API}/deleteWebhook")
    return resp.json()


@app.post(WEBHOOK_PATH)
async def http_handler(request: Request):
    """
    Handles incoming request from telegram chat
    Receives Update object: https://core.telegram.org/bots/api#update
    """
    data = await request.json()

    chat_id = data["message"]["chat"]["id"]
    prompt = data["message"]["text"]

    return send_msg(chat_id, prompt)
