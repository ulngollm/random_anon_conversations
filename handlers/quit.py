from pyrogram import Client
from pyrogram.types import  CallbackQuery
from app import user_service, match_manager

def close_conversation(client: Client, callback_query: CallbackQuery):
    user = user_service.authenticate(callback_query.from_user.id)
    # напрямую передавать id диалога. Значит и миграции надо переделать так, чтобы был id у диалога
    match_manager.close_current_conversation(user.id)
    user_service.set_active(user.id)

    callback_query.message.reply(
        'Окей, мы отправим уведомление пользователю. Можете найти другого собеседника.'
    )