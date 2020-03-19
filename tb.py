import telebot
import json
import requests
import re
import urllib.parse
from telebot import types

bot = telebot.TeleBot("1008578392:AAEP2V3AX9GHBWOGtDY4jSep3vkpHeEcoqY")
api = 'http://api.urbandictionary.com/v0/define?term='
keyboard1 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard1.row('Привет', 'Пока', 'love you')
keyboard1.row('Физмат?','Кто ты?')
digits_pattern = re.compile(r'(\b\w+\b)')
k=True

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start', reply_markup=keyboard1)
@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, 'Пока')
    elif message.text.lower() == 'пока':
        bot.send_message(message.chat.id, 'О, привет, а я тебя знаю')
    elif message.text.lower() == 'я тебя люблю' or message.text.lower() == 'love you':
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAILiV5hT8-CaKzCUsTXKJgU2BqbLpZhAAKBDwACT20qAAHBgmMzXjiXHhgE')
    elif message.text.lower() == 'физмат?':
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAILol5hVKiUBcFwyZwH8FxiczU3oaOUAAJeBQEAAWOLRgzUJ3hovmI4DBgE')
    elif message.text.lower() == 'кто ты?':
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAILn15hVGiGt5sAAc4oAmycLaqCNFm6zwACDGwBAAFji0YMe4_uoQbUVQEYBA')
    elif re.fullmatch(r'(\b\w+\b)', message.text.lower()):
        search=api+urllib.parse.quote_plus(message.text.lower())
        response = requests.get(search)
        bot.send_message(message.chat.id, response.json()['list'][0]['definition']) 
    else:
        if k==False:
            bot.send_message(message.chat.id, 'Я тебя не понимаю')

@bot.inline_handler(func=lambda query: len(query.query) > 0)
def query_text(query):
    #try:
    #    matches = re.match(digits_pattern, query.query)
    #except AttributeError as ex:
    #    return
    if query.query != '':
    #    matches = query.query
    #else:
    #    return
    #matches = query.query
        #text = matches.group()
        text= query.query
        search=api+urllib.parse.quote_plus(text.lower())
        response = requests.get(search)
        a=response.json()['list'][0]['definition']
        r_sum = types.InlineQueryResultArticle(
            id='1', title="Result",
            description="Запрос: {!s}".format(a),
            input_message_content=types.InputTextMessageContent(
            message_text=a)
        )
        k=False
        bot.answer_inline_query(query.id, [r_sum])
        


@bot.message_handler(content_types=['sticker'])
def sticker_id(message):
    print(message)


bot.polling()