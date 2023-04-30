from dotenv import load_dotenv
from pyrogram import Client
from services.user import UserService
from db.queries.user import UserManager 
from db.queries.match import MatchManager
import os

load_dotenv()
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
BOT_API_TOKEN = os.getenv('BOT_API_TOKEN')
DB_NAME = os.getenv('DB_NAME')

client = Client('bot', API_ID, API_HASH, bot_token=BOT_API_TOKEN)
state = dict()

user_storage = UserManager(DB_NAME)
match_manager = MatchManager(DB_NAME)
user_service = UserService(state, user_storage)
