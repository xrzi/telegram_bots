#You can find this bot here: https://t.me/vmeste_tv_bot
#It probably works right now

from lxml import html
import requests
from time import sleep
from random import randint
from telegram.ext import CommandHandler
from telegram.ext import CallbackQueryHandler as CQHandler
from functools import lru_cache

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

APItoken = "MYAPITOKEN"

from telegram.ext import Updater
upd = Updater(token=APItoken, use_context=True)
disp = upd.dispatcher
import logging
logging.basicConfig(format='8==>%(asctime)s - %(name)s - %(levelname)s - %(message)s<==8',
                     level=logging.INFO)
#8==>i am funny<==8

default_href="https://vmeste.tv/search/?text="
headers={"User Agent" : "telegram bot (made by https://t.me/Riley_Lvasture_Ka_Linux)"}


#I know, using class here is stoopid and pointless, I'm just too dumb to change that
class kbMarkup:
    def __init__(self, hrefs, current_page):
        self.button_list = list()
        self.columns = 5
        for num in range(len(hrefs)):
            s = str(num+1)
            if num==current_page:
                s = f'<{s}>'
            self.button_list.append(InlineKeyboardButton(s, callback_data = str(num)))
        self.button_list = [self.button_list[i: i+self.columns] for i in range(0, len(hrefs), self.columns)]
        self.keyboard = InlineKeyboardMarkup(self.button_list)

#This fixes the issue with long answering 
#and making requests to the site every time you press button
@lru_cache(maxsize=1000)
def get_href(name):
    response = requests.get(default_href+name, headers = headers)
    tree = html.fromstring(response.text)
    hrefs = tree.xpath('//a[@style="color: #000;"]/@href')
    texts = tree.xpath('//a[@style="color: #000;"]/text()')
    for href in range(len(hrefs)):
        hrefs[href] = "https://vmeste.tv"+hrefs[href]
    return hrefs

def searcher(update, context):
    search_str = "+".join(context.args)
    context.user_data['current_search'] = search_str
    result = context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=get_href(context.user_data['current_search'])[0],
        reply_markup = kbMarkup(get_href(context.user_data['current_search']), 0).keyboard
    )
    context.user_data['current_message_id'] = result.message_id

def callback_catcher(update, context):
    print(update.callback_query.data)
    page = int(update.callback_query.data)
    result = context.bot.edit_message_text(
        chat_id=update.effective_chat.id,
        message_id = context.user_data['current_message_id'],
        text=get_href(context.user_data['current_search'])[page]
    )
    context.user_data['current_message_id'] = result.message_id
    result = context.bot.edit_message_reply_markup(
        chat_id=update.effective_chat.id,
        message_id = context.user_data['current_message_id'],
        reply_markup = kbMarkup(get_href(context.user_data['current_search']), page).keyboard
    )
    context.user_data['current_message_id'] = result.message_id

got_job_handler = CommandHandler("search", searcher)
call_handler = CQHandler(callback_catcher) #CallbackQueryHandler

disp.add_handler(got_job_handler)
disp.add_handler(call_handler)

upd.start_polling()
