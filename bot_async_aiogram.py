import random
import asyncio


from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram import types

from config import TOKEN
import TextFiles
import cmc_api


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['menu'])
async def add_menu(message: types.Message):
    itembtn1 = types.KeyboardButton('/cap')
    itembtn2 = types.KeyboardButton('/BTC')
    itembtn3 = types.KeyboardButton('/ETH')
    itembtn4 = types.KeyboardButton('/BCH')
    itembtn5 = types.KeyboardButton('/XMR')
    itembtn6 = types.KeyboardButton('/DCR')
    markup = types.ReplyKeyboardMarkup([[itembtn1, itembtn2, itembtn3], [itembtn4, itembtn5, itembtn6]],
                                       True, False)
    await bot.send_message(chat_id=message.chat.id, text="Push the button", reply_markup=markup)


@dp.message_handler(commands=['idea'])
async def get_idea(message: types.Message):
    quote = random.choice(TextFiles.quotes)
    await bot.send_message(chat_id=message.chat.id, text='_' + quote + '_', parse_mode='Markdown')


@dp.message_handler(commands=['coinflip'])
async def coin_flip(message: types.Message):
    sequence = ['Орёл', 'Решка']
    r = random.choice(sequence)
    await bot.send_message(chat_id=message.chat.id, text='*' + r + '*', parse_mode='Markdown')


@dp.message_handler(commands=['cap'])
async def get_market(message: types.Message):
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    temp = await bot.send_message(chat_id=message.chat.id, text=cmc_api.get_market(), parse_mode='Markdown')
    await asyncio.sleep(11)
    await bot.delete_message(chat_id=message.chat.id, message_id=temp.message_id)


@dp.message_handler(func=lambda message: True, content_types=['sticker'])
async def sticker_deleter(message: types.Message):
    s_id = message.message_id
    await asyncio.sleep(22)
    await bot.delete_message(chat_id=message.chat.id, message_id=s_id)


@dp.message_handler(func=lambda m: True)
async def get_price(message: types.Message):
    if message.text[0] != '/':
        pass
    else:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        temp = await bot.send_message(chat_id=message.chat.id,
                                      text=cmc_api.get_markets(message.text[1:]), parse_mode='Markdown')
        await asyncio.sleep(11)
        await bot.delete_message(chat_id=message.chat.id, message_id=temp.message_id)


async def bitcoin_checker():
    while True:
        try:
            price = int((float((await cmc_api.get_markets('BTC'))[20:28])) / 100)
            await asyncio.sleep(305)
            new_price = int((float((await cmc_api.get_markets('BTC'))[20:28])) / 100)
            market_cap_now = await cmc_api.get_market_cap()
            if new_price > price:
                what = 'Биток пробил ' + str(new_price * 100) + '. Цена: ' + str((await cmc_api.get_markets('BTC'))[20:28])
                await bot.send_message(chat_id=-1001081308494, text='``` ' + what + market_cap_now + ' ```', parse_mode='Markdown')
            elif new_price < price:
                what = 'Биток упал ниже ' + str(price * 100) + '. Цена: ' + str((await cmc_api.get_markets('BTC'))[20:28])
                await bot.send_message(chat_id=-1001081308494, text='``` ' + what + market_cap_now + ' ```', parse_mode='Markdown')
            else:
                continue
        except:
            await asyncio.sleep(305)
            continue


if __name__ == '__main__':
    bit_check = asyncio.get_event_loop()
    process = bit_check.create_task(bitcoin_checker())
    executor.start_polling(dp)
    bit_check.close()

'''
menu - вызвать меню 
idea - получить умную мысль
coinflip - бросить монетку
cap - узнать капитализацию
'''