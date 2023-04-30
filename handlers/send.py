from pyrogram import Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from db.queries import match as match_manager
from config import user_service
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
    
    # todo брать id диалога из кеша. Потому что на каждое сбщ дергать базу - такое себе
    # todo сделать сервис для работы с диалогами, где эта логика будет инкапсулирована
    open_conversation = match_manager.get_active_conversation(message.from_user.id)
    match_id = open_conversation[0] if open_conversation[0] != message.from_user.id else open_conversation[1]
    client.send_message(
        match_id,
        message.text
    )