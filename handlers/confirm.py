from pyrogram import Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery


def quit_conversation(client: Client, message: Message):
    message.reply(
        'Вы действительно хотите выйти из текущего диалога?',
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton(
                "Да",
                callback_data="quit:%d" % message.from_user.id
            ),
            InlineKeyboardButton(
                "Нет",
                callback_data="continue:%d" % message.from_user.id
            ),
        ]])
    )


def continue_conversation(client: Client, callback_query: CallbackQuery):
    callback_query.answer('Ок! Можете продолжать переписку.')


def wait_invite(client: Client, callback_query: CallbackQuery):
    callback_query.answer('Ок! Как скажете.')