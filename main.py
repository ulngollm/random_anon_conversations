from dotenv import load_dotenv
from pyrogram import Client
from pyrogram.handlers import MessageHandler
from pyrogram import filters
import os


load_dotenv()
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
BOT_API_TOKEN = os.getenv('BOT_API_TOKEN')

app = Client('bot', API_ID, API_HASH, bot_token=BOT_API_TOKEN)


def hello(client, message):
    message.reply(
        'Привет!'
    )

app.add_handler(MessageHandler(hello, filters.command(['start'])))

app.run()