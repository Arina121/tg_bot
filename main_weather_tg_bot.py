import requests
from config import tg_bot_token, open_weather_token
from aiogram import Bot, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
    ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor



bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)

#Кнопки
kb = InlineKeyboardMarkup(row_width=1)
button1 = InlineKeyboardButton(text='Лучшая девочка', url='https://vk.com/kiskina_arina')
kb.add(button1)

inkb = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Пока что бесполезная', callback_data='www'))

@dp.message_handler(commands='test')
async def url_command(message: types.Message):
    await message.answer('Кнопка: ', reply_markup=inkb)


@dp.callback_query_handler(text='www')
async def www_call(callback : types.CallbackQuery):
    await callback.message.answer('Абсолютно бесполезная')
    await callback.answer()

@dp.message_handler(commands='help')
async def url_command(message: types.Message):
    await message.answer('Ссылочка: ', reply_markup=kb)


@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    await message.answer('Чтобы узнать погоду, введите город')



@dp.message_handler()
async def get_weather(message: types.Message):
    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
        )
        data = r.json()

        cur_weather = data['main']['temp']
        humidity = data['main']['humidity']
        wind = data['wind']['speed']

        await message.answer(f"Погода в городе {message.text}: {cur_weather} °C\n"
              f"Влажность: {humidity}%\nВетер: {wind} мс")


    except:
        await message.reply('Проверьте название города')


if __name__ == '__main__':
    executor.start_polling(dp)