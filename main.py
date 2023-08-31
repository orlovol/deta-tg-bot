import logging

from aiogram import Bot, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.webhook import SendMessage
from aiogram.utils.executor import start_webhook
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton,
)
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

from os import getenv

# Bot token can be obtained via https://t.me/BotFather
API_TOKEN = getenv("BOT_TOKEN")

RENDER_EXTERNAL_HOSTNAME = getenv("RENDER_EXTERNAL_HOSTNAME")

# webhook settings
WEBHOOK_HOST = RENDER_EXTERNAL_HOSTNAME
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# webserver settings
WEBAPP_HOST = "0.0.0.0"
WEBAPP_PORT = getenv("PORT", 8080)

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


# test commands

kb_greetings = InlineKeyboardMarkup(row_width=2)
kb_greetings.add(
    InlineKeyboardButton(text="Давай 😊 ", callback_data="yes"),
    InlineKeyboardButton(text="Пізніше 👌 ", callback_data="no"),
)

talk = KeyboardButton("Поговоримо про секс?")
quiz = KeyboardButton("Квізи для дорослих 😻")
story = KeyboardButton("Sex Stories 😜")
kamasutra = KeyboardButton("ПОЗА ДНЯ😏")
review = KeyboardButton("Відкрий скарбничку з іграшками 🧸")
subscribe = KeyboardButton("Підписатись на щоденний контент 🔔")
need_help = KeyboardButton("Консультація з менеджером 📞")

kb_main_menu = ReplyKeyboardMarkup(
    one_time_keyboard=True,
    resize_keyboard=True,
    keyboard=[[talk], [quiz, story], [kamasutra, review], [subscribe], [need_help]],
)


class Greetings(StatesGroup):
    age = State()
    gender = State()
    orientation = State()


async def start_on(message: types.Message):
    await message.answer("Привіт!")
    await message.answer("Давай познайомимось?😉", reply_markup=kb_greetings)


@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    await start_on(message)


@dp.callback_query_handler(lambda query: query.data in ["yes", "no"])
async def greetings_start(callback_query: types.CallbackQuery, state: FSMContext):
    await greetings(callback_query, state)


async def greetings(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == "yes":
        await bot.send_message(
            chat_id=callback_query.from_user.id, text="Скільки тобі років?"
        )
        await Greetings.age.set()
    elif callback_query.data == "no":
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text="Тоді познайомимся пізніше😉. Дивись що у нас є в меню ⬇️ ",
            reply_markup=kb_main_menu,
        )


# default


@dp.message_handler()
async def echo(message: types.Message):
    # Regular request
    # await bot.send_message(message.chat.id, message.text)

    # or reply INTO webhook
    return SendMessage(message.chat.id, message.text)


async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)
    # insert code here to run it after start


async def on_shutdown(dp):
    logging.warning("Shutting down..")

    # insert code here to run it before shutdown

    # Remove webhook (not acceptable in some cases)
    await bot.delete_webhook()

    # Close DB connection (if used)
    await dp.storage.close()
    await dp.storage.wait_closed()

    logging.warning("Bye!")


if __name__ == "__main__":
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
