from pyrogram import Client
from pyrogram.types import Message, CallbackQuery
from model.user import UserStatus
from app import user_service, match_manager, match_service

def init_search(client: Client, message: Message, user = None):
    user_id = message.from_user.id if not user else user.id 
    user = user_service.authenticate(user_id)

    if user.status == UserStatus.BUSY:
        message.reply(
            'У вас уже есть открытый диалог. Если хотите закрыть его и начать новый, выполните команду /quit.'
        )
        return
    

    message.reply(
        'Сейчас найдем вам пару для переписки...'
    )
    # match = match_manager.search_match(user.id, UserStatus.ACTIVE)
    match = match_service.search(user.id)
    if match == None:
        message.reply(
            'Мы пока не смогли найти вам собеседника. Они все заняты. Попробуйте позднее.'
        )
        return
    
    match_service.open_conversation(user.id, match)
    user_service.set_busy(user.id)
    user_service.set_busy(match)
    
    client.send_message(
        match, 
        'Мы нашли вам собеседника! Все, что вы напишете после этого сообщения, отправится ему 🔽'
    )
    message.reply(
        'Мы нашли вам собеседника и уведомили его. Все, что вы напишете после этого сообщения, отправится ему 🔽'
    )





def search_button(client: Client, callback_query: CallbackQuery):
    init_search(client, callback_query.message, callback_query.from_user)