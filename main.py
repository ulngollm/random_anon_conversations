from dotenv import load_dotenv
from pyrogram import Client
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import os
from db.queries import user as user_manager, match as match_manager
from user import UserStatus

load_dotenv()
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
BOT_API_TOKEN = os.getenv('BOT_API_TOKEN')

app = Client('bot', API_ID, API_HASH, bot_token=BOT_API_TOKEN)


def start(client: Client, message: Message):
    user = user_manager.find(message.from_user.id)
    if user == None:
        user_manager.add(message.from_user.id)
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

    user_manager.set_status(message.from_user.id, UserStatus.ACTIVE)
    message.reply(
            'Вы изменили видимость профиля. Теперь вам могут писать. \nЕсли вы хотите найти собеседника прямо сейчас, нажмите кнопку',
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(
                    "Найти собеседника",
                    callback_data="search:%d" % message.from_user.id
                )
            ]])
        )


def set_status_inactive(client: Client, message: Message):
    user_manager.set_status(message.from_user.id, UserStatus.FREEZED)
    message.reply(
        'Вы приостановили переписку. Чтобы снова вернуться в поиск, нажмите команду /start'
    )


def init_search(client: Client, message: Message, user: None):
    message.reply(
        'Сейчас найдем вам пару для переписки...'
    )
    user = message.from_user if not user else user 
    match = match_manager.search_match(user.id, UserStatus.ACTIVE)
    if match == None:
        message.reply(
            'Мы пока не смогли найти вам собеседника. Они все заняты. Попробуйте позднее.'
        )
        return
    
    client.send_message(
        match, 
        'Мы нашли вам собеседника! Все, что вы напишете после этого сообщения, отправится ему 🔽'
    )
    message.reply(
        'Мы нашли вам собеседника и уведомили его. Все, что вы напишете после этого сообщения, отправится ему 🔽'
    )


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


def close_conversation(client: Client, callback_query: CallbackQuery):
    match_manager.close_current_conversation(callback_query.from_user.id)
    callback_query.message.reply(
        'Окей, мы отправим уведомление пользователю. Можете найти другого собеседника.'
    )

def search_button(client: Client, callback_query: CallbackQuery):
    init_search(client, callback_query.message, callback_query.from_user)


def send_message(client: Client, message: Message):
    open_conversation = match_manager.get_active_conversation(message.from_user.id)
    # todo проверить, есть ли открытый диалог
    # todo если есть, перенаправить сообщение собеседнику
    # если нет, то 
    if not open_conversation:
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
    
    match_id = open_conversation[0] if open_conversation[0] != message.from_user.id else open_conversation[1]
    client.send_message(
        match_id,
        message.text
    )

def continue_conversation(client: Client, callback_query: CallbackQuery):
    callback_query.answer('Ок! Можете продолжать переписку.')


def wait_invite(client: Client, callback_query: CallbackQuery):
    callback_query.answer('Ок! Как скажете.')


app.add_handler(MessageHandler(start, filters.command(['start'])))
app.add_handler(MessageHandler(set_status_inactive, filters.command(['freeze'])))
app.add_handler(MessageHandler(init_search, filters.command(['search'])))
app.add_handler(MessageHandler(quit_conversation, filters.command(['quit'])))
app.add_handler(CallbackQueryHandler(close_conversation, filters.regex('quit:(\d*)')))
app.add_handler(CallbackQueryHandler(continue_conversation, filters.regex('continue:(\d*)')))
app.add_handler(CallbackQueryHandler(search_button, filters.regex('search:(\d*)')))
app.add_handler(CallbackQueryHandler(wait_invite, filters.regex('wait:(\d*)')))
app.add_handler(MessageHandler(send_message, filters.text))


app.run()