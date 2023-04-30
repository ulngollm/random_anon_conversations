from pyrogram import Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from app import user_service, match_service
from model.user import UserStatus


def send_message(client: Client, message: Message):
    user = user_service.authenticate(message.from_user.id)

    if user.status != UserStatus.BUSY:
        message.reply(
            'У вас сейчас нет собеседника',
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "Найти",
                        callback_data="search:%d" % message.from_user.id
                    )
                ],
                [   
                    InlineKeyboardButton(
                        "Подожду, пока мне напишут",
                        callback_data="wait:%d" % message.from_user.id
                    )
                ]
            ])
        )
        return
    
    match = match_service.get_current_match(user.id)
    client.send_message(
        match.match,
        message.text
    )