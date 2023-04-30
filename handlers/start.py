from pyrogram import Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from model.user import UserStatus
from app import user_service


def start(client: Client, message: Message):
    user = user_service.authenticate(message.from_user.id) 
    
    if user.status == UserStatus.NEW:
        user_service.add(user.id)
        
        message.reply(
            'Привет! \nЕсли вы хотите найти собеседника прямо сейчас, нажмите кнопку',
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(
                    "Найти собеседника",
                    callback_data="search:%d" % message.from_user.id
                )
            ]])
        )
        return

    user_service.set_active(user.id)
    message.reply(
            'Вы изменили видимость профиля. Теперь вам могут писать. \nЕсли вы хотите найти собеседника прямо сейчас, нажмите кнопку',
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(
                    "Найти собеседника",
                    callback_data="search:%d" % message.from_user.id
                )
            ]])
        )
