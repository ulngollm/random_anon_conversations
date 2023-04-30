from pyrogram import Client
from pyrogram.types import Message
from app import user_service


def set_status_inactive(client: Client, message: Message):
    user_service.set_freeze(message.from_user.id)
    message.reply(
        'Вы приостановили переписку. Чтобы снова вернуться в поиск, нажмите команду /start'
    )