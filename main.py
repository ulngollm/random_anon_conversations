from dotenv import load_dotenv
from pyrogram import Client
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import os


load_dotenv()
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
BOT_API_TOKEN = os.getenv('BOT_API_TOKEN')

app = Client('bot', API_ID, API_HASH, bot_token=BOT_API_TOKEN)


def start(client: Client, message: Message):
    message.reply(
        'Привет! Теперь вас могут найти. \nЕсли вы хотите найти собеседника прямо сейчас, нажмите кнопку',
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton(
                "Найти собеседника",
                callback_data="search:%d" % message.from_user.id
            )
        ]])
    )


def set_status_inactive(client: Client, message: Message):
    message.reply(
        'Вы приостановили переписку. Чтобы снова вернуться в поиск, нажмите команду /start'
    )


def init_search(client: Client, message: Message):
    message.reply(
        'Сейчас найдем вам пару для переписки...'
    )
    # todo search
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
    callback_query.message.reply(
        'Окей, мы отправим уведомление пользователю. Можете найти другого собеседника.'
    )

def search_button(client: Client, callback_query: CallbackQuery):
    init_search(client, callback_query.message)


def send_message(client: Client, message: Message):
    has_open_conversation = False
    # todo проверить, есть ли открытый диалог
    # todo если есть, перенаправить сообщение собеседнику
    # если нет, то 
    if not has_open_conversation:
        message.reply(
            'У вас сейчас нет собеседника',
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(
                    "Найти",
                    callback_data="search:%d" % message.from_user.id
                ),
                InlineKeyboardButton(
                    "Подожду, пока мне напишут",
                    callback_data="wait:%d" % message.from_user.id
                )
            ]])
        )


def continue_conversation(client: Client, callback_query: CallbackQuery):
    callback_query.answer('Ок! Можете продолжать переписку.')


app.add_handler(MessageHandler(start, filters.command(['start'])))
app.add_handler(MessageHandler(set_status_inactive, filters.command(['freeze'])))
app.add_handler(MessageHandler(init_search, filters.command(['search'])))
app.add_handler(MessageHandler(quit_conversation, filters.command(['quit'])))
app.add_handler(CallbackQueryHandler(close_conversation, filters.regex('quit:(\d*)')))
app.add_handler(CallbackQueryHandler(continue_conversation, filters.regex('continue:(\d*)')))

app.add_handler(CallbackQueryHandler(search_button, filters.regex('search:(\d*)')))
app.add_handler(MessageHandler(send_message, filters.text))


app.run()