from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from pyrogram import filters
from handlers.search import init_search, search_button
from handlers.start import start
from handlers.freeze import set_status_inactive
from handlers.quit import close_conversation
from handlers.confirm import quit_conversation, continue_conversation, wait_invite
from handlers.send import send_message
from app import client


client.add_handler(MessageHandler(start, filters.command(['start'])))
client.add_handler(MessageHandler(set_status_inactive, filters.command(['freeze'])))
client.add_handler(MessageHandler(init_search, filters.command(['search'])))
client.add_handler(MessageHandler(quit_conversation, filters.command(['quit'])))
client.add_handler(CallbackQueryHandler(close_conversation, filters.regex('quit:(\d*)')))
client.add_handler(CallbackQueryHandler(continue_conversation, filters.regex('continue:(\d*)')))
client.add_handler(CallbackQueryHandler(search_button, filters.regex('search:(\d*)')))
client.add_handler(CallbackQueryHandler(wait_invite, filters.regex('wait:(\d*)')))
client.add_handler(MessageHandler(send_message, filters.text))


client.run()