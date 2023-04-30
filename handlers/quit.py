from pyrogram import Client
from pyrogram.types import  CallbackQuery
from db.queries import match as match_manager
from config import user_service

def close_conversation(client: Client, callback_query: CallbackQuery):
    user = user_service.authenticate(callback_query.from_user.id)
    match_manager.close_current_conversation(user.id)
    user_service.set_active(user.id)

    callback_query.message.reply(
        'Окей, мы отправим уведомление пользователю. Можете найти другого собеседника.'
    )