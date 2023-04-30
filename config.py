from dotenv import load_dotenv
from pyrogram import Client
import os

load_dotenv()
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
BOT_API_TOKEN = os.getenv('BOT_API_TOKEN')
DB_NAME = os.getenv('DB_NAME')

app = Client('bot', API_ID, API_HASH, bot_token=BOT_API_TOKEN)
state = dict()