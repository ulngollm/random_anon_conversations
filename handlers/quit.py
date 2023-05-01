from pyrogram import Client
from pyrogram.types import  CallbackQuery
from app import user_service, match_service

def close_conversation(client: Client, callback_query: CallbackQuery):
    user = user_service.authenticate(callback_query.from_user.id)
    cur_match = match_service.get_current_match(user.id)

    match_service.close_conversation(cur_match)
    user_service.set_active(cur_match.match)
    user_service.set_active(user.id)

    callback_query.message.reply(
        'Окей, мы отправим уведомление пользователю. Можете найти другого собеседника.'
    )
    client.send_message(
        cur_match.match,
        'Пользователь завершил диалог. Вы можете выбрать другого собеседника.'
    )