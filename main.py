import os
import random
import urllib.parse

import requests
from fastapi import FastAPI, Request

TOKEN = os.getenv("TOKEN", "")  # in Spacefile
HOST = os.getenv("DETA_SPACE_APP_HOSTNAME", "")

BOT_API = f"https://api.telegram.org/bot{TOKEN}"
WEBHOOK_PATH = "/webhook"  # also in Spacefile public_routes


GANDALF = [
    "It is not despair, for despair is only for those who see the end beyond all doubt. We do not.",
    "I was talking aloud to myself. A habit of the old: they choose the wisest person present to speak to.",
    "I am a servant of the Secret Fire, wielder of the flame of Anor. You cannot pass.The dark fire will not avail you, flame of Udûn. Go back to the Shadow! You cannot pass.",
    "Something has crept, or has been driven out of dark waters under the mountains. There are older and fouler things than Orcs in the deep places of the world.",
    "I must rest here a moment, even if all the orcs ever spawned are after us.",
    "It may be your task to find the Cracks of Doom; but that quest may be for others: I do not know. At any rate you are not ready for that long road yet.",
    "He is in great fear, not knowing what mighty one may suddenly appear, wielding the Ring, and assailing him with war, seeking to cast him down and take his place. That we should wish to cast him down and have no one in his place is not a thought that occurs to his mind. That we should try to destroy the Ring itself has not yet entered into his darkest dream.",
    "It is a comfort not to be mistaken at all points. Do I not know it only too well!",
    "What a pity that Bilbo did not stab that vile creature, when he had a chance! \nPity? It was Pity that stayed his hand. Pity, and Mercy: not to strike without need. And he has been well rewarded, Frodo. Be sure that he took so little hurt from the evil, and escaped in the end, because he began his ownership of the Ring so. With Pity.",
    "Let folly be our cloak, a veil before the eyes of the Enemy! For he is very wise, and weighs all things to a nicety in the scales of his malice. But the only measure that he knows is desire, desire for power; and so he judges all hearts. Into his heart the thought will not enter that any will refuse it, that having the Ring we may seek to destroy it. If we seek this, we shall put him out of reckoning.",
    "He that breaks a thing to find out what it is has left the path of wisdom.",
    "It is not our part to master all the tides of the world, but to do what is in us for the succour of those years wherein we are set, uprooting the evil in the fields that we know, so that those who live after may have clean earth to till. What weather they shall have is not ours to rule.",
    "Then darkness took me, and I strayed out of thought and time, and I wandered far on roads that I will not tell. Naked I was sent back – for a brief time, until my task is done.",
    "You cannot pass. I am a servant of the Secret Fire, wielder of the flame of Anor. You cannot pass. The dark fire will not avail you, flame of Udûn. Go back to the Shadow! You cannot pass.",
    "Yet it has a bottom, beyond light and knowledge.",
    "It is not our part here to take thought only for a season, or for a few lives of Men, or for a passing age of the world. We should seek a final end of this menace, even if we do not hope to make one.",
    "No! With that power I should have power too great and terrible. And over me the Ring would gain a power still greater and more deadly."
    "Do not tempt me! For I do not wish to become like the Dark Lord himself. Yet the way of the Ring to my heart is by pity, pity for weakness and the desire of strength to do good.",
    "Do not tempt me! I dare not take it, not even to keep it safe, unused. The wish to wield it would be too great for my strength. I shall have such need of it. Great perils lie before me.",
    "To me it would not seem that a Steward who faithfully surrenders his charge is diminished in love or in honour.",
    "I am with you at present, but soon I shall not be. I am not coming to the Shire. You must settle its affairs yourselves; that is what you have been trained for. Do you not yet understand? My time is over: it is no longer my task to set things to rights, nor to help folk to do so. And as for you, my dear friends, you will need no help. You are grown up now. Grown indeed very high; among the great you are, and I have no longer any fear at all for any of you.",
    "The treacherous are ever distrustful.",
    "Fly, you fools!",
    "And he that breaks a thing to find out what it is has left the path of wisdom.",
    "Well, here at last, dear friends, on the shores of the Sea comes the end of our fellowship in Middle-earth. Go in peace!",
    "Only a small part is played in great deeds by any hero.",
    "It is wisdom to recognize necessity, when all other courses have been weighed, though as folly it may appear to those who cling to false hope. Well, let folly be our cloak, a veil before the eyes of the Enemy! For he is very wise, and weighs all things to a nicety in the scales of this malice. But the only measure that he knows is desire, desire for power; and so he judges all hearts. Into his heart the thought will not enter that any will refuse it.",
    "Yet a treacherous weapon is ever a danger to the hand.",
    "So do I, and so do all who live to see such times. But that is not for them to decide. All we have to decide is what to do with the time that is given us.",
    "Deserves it! I daresay he does. Many that live deserve death. And some that die deserve life. Can you give it to them? Then do not be too eager to deal out death in judgement. For even the very wise cannot see all ends.",
    "I will not say: do not weep; for not all tears are an evil.",
    "Do you wish me a good morning, or mean that it is a good morning whether I want it or not; or that you feel good this morning; or that it is a morning to be good on?",
    "May the wind under your wings bear you where the sun sails and the moon walks.",
    "This is the Master-ring, the One Ring to rule them all. This is the One Ring that he lost many ages ago, to the great weakening of his power. He greatly desires it — but he must not get it.",
    "The wise speak only of what they know.",
    "To crooked eyes truth may wear a wry face.",
]


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
    msg = "🤷" if prompt.startswith("/") else random.choice(GANDALF)
    return send_msg(chat_id, msg)
