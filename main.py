from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from pyrogram import filters
import handlers
from config import app


app.add_handler(MessageHandler(handlers.start, filters.command(['start'])))
app.add_handler(MessageHandler(handlers.set_status_inactive, filters.command(['freeze'])))
app.add_handler(MessageHandler(handlers.init_search, filters.command(['search'])))
app.add_handler(MessageHandler(handlers.quit_conversation, filters.command(['quit'])))
app.add_handler(CallbackQueryHandler(handlers.close_conversation, filters.regex('quit:(\d*)')))
app.add_handler(CallbackQueryHandler(handlers.continue_conversation, filters.regex('continue:(\d*)')))
app.add_handler(CallbackQueryHandler(handlers.search_button, filters.regex('search:(\d*)')))
app.add_handler(CallbackQueryHandler(handlers.wait_invite, filters.regex('wait:(\d*)')))
app.add_handler(MessageHandler(handlers.send_message, filters.text))


app.run()