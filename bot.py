import config
import telebot
from telebot import types
import time
import cmc_api
import random
import TextFiles
from telebot import AsyncTeleBot
from multiprocessing import Process


bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['menu'])
def get_market1(message):
    markup = types.ReplyKeyboardMarkup(True, False)
    itembtn1 = types.KeyboardButton('/market')
    itembtn2 = types.KeyboardButton('/ETH')
    itembtn3 = types.KeyboardButton('/BTC')
    itembtn4 = types.KeyboardButton('/LTC')
    itembtn5 = types.KeyboardButton('/ETC')
    itembtn6 = types.KeyboardButton('/DCR')
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn6)
    bot.send_message(message.chat.id, "Push the button", reply_markup=markup)


@bot.message_handler(commands=['cap'])
def go_coin_market_cap(message):
    keyboard = types.InlineKeyboardMarkup()
    url_button = types.InlineKeyboardButton(text="Перейти на coinmarketcap.com", url="https://coinmarketcap.com/")
    keyboard.add(url_button)
    bot.send_message(message.chat.id, "Push the button", reply_markup=keyboard)


@bot.message_handler(commands=['vital'])
def vital_check(message):
    bot.send_message(message.chat.id, '@spielbergos - Спилбергос стивенушечка!')
    quote = random.choice(TextFiles.quotes)
    bot.send_message(message.chat.id, '``` ' + quote + ' ```', parse_mode='Markdown')


@bot.message_handler(commands=['coinflip'])
def get_market(message):
    sequence = ['Орёл', 'Решка']
    r = random.choice(sequence)
    bot.send_message(message.chat.id, r)


@bot.message_handler(commands=['market'])
def get_market(message):
    bot.send_message(message.chat.id, cmc_api.get_market())


def bitcoin_checker():
    while True:
        try:
            price = int((float((cmc_api.get_markets('BTC'))[20:28])) / 100)
            time.sleep(305)
            new_price = int((float((cmc_api.get_markets('BTC'))[20:28])) / 100)
            if new_price > price:
                what = 'Биток пробил ' + str(new_price * 100) + '. Цена: ' + str((cmc_api.get_markets('BTC'))[20:28])
                bot.send_message(chat_id=-1001081308494, text='``` ' + what + ' ```', parse_mode='Markdown')
            elif new_price < price:
                what = 'Биток упал ниже ' + str(price * 100) + '. Цена: ' + str((cmc_api.get_markets('BTC'))[20:28])
                bot.send_message(chat_id=-1001081308494, text='``` ' + what + ' ```', parse_mode='Markdown')
            else:
                continue
        except:
            time.sleep(305)
            continue


@bot.message_handler(func=lambda message: True, content_types=['sticker'])
def sticker_deleter(message):
    sticker = message.message_id
    time.sleep(22)
    bot.delete_message(message.chat.id, sticker)


@bot.message_handler(func=lambda m: True)
def get_price(message):
    bot.send_message(message.chat.id, cmc_api.get_markets(message.text[1:]))


if __name__ == '__main__':
    Process(target=bitcoin_checker).start()
    bot.polling(none_stop=True)


'''
menu - вызвать меню
vital - вызвать виталика
cap - перейти на coinmarketcap.com
coinflip - бросить монетку
market - узнать капитализацию
'''