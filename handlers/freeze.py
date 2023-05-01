from pyrogram import Client
from pyrogram.types import Message
from app import user_service
from model.user import UserStatus


def set_status_inactive(client: Client, message: Message):
    user = user_service.authenticate(message.from_user.id)
    if user.status == UserStatus.BUSY:
        message.reply(
            'У вас есть открытый диалог. Если хотите выйти из текущего диалога, используйте команду /quit'
        )
        return

    if user.status == UserStatus.FREEZED:
        message.reply(
            'Вы уже приостановили получение приглашений. Чтобы вернуться к переписке, используйте /start'
        )
        return

    user_service.set_freeze(user.id)
    message.reply(
        'Вы приостановили переписку. Чтобы снова получать приглашения, нажмите команду /start'
    )