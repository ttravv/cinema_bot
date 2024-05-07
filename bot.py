import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.filters.command import Command, CommandObject
from dotenv import dotenv_values
from utils.callback_data import Year, Genre
from utils.keyboards import genre_kb, years_kb
from utils.network import get_request, movie_by_genre_year, parsing

# Включаем логирование
logging.basicConfig(level=logging.INFO)
# Объект бота
config = dotenv_values(".env")
bot = Bot(token=config["BOT_TOKEN"])
kinopoisk = config['API_TOKEN']
# Диспетчер
dp = Dispatcher()
dp['my_list'] = []

@dp.message(Command('start'))
async def start_button(message: types.Message):
    kb = [
        [types.KeyboardButton(text='Хочу посмотреть фильм')]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, 
                                        resize_keyboard = True,
                                        one_time_keyboard=True)
    
    await message.answer('Выберите команду', reply_markup=keyboard)

@dp.message(F.text== "Хочу посмотреть фильм")
async def after(message: types.Message):
    builder = genre_kb()
    await message.answer('Выберите жанр', 
                         reply_markup=builder.as_markup())

@dp.callback_query(Genre.filter())
async def genre_handler(callback: types.CallbackQuery, callback_data: Genre):
    genre = callback_data.name
    builder = years_kb(genre)
    await callback.message.answer(f'Вы выбрали жанр {genre}. Выберите год.',
                                  reply_markup=builder.as_markup())
    await callback.answer()

@dp.callback_query(Year.filter())
async def year_handler(callback: types.CallbackQuery, callback_data: Year):
    years = callback_data.range
    genre = callback_data.genre
    url = movie_by_genre_year(genre, years)
    about_films = await get_request(url)
    for i in about_films:
        card = parsing(i)
        await callback.message.answer(card)
    await callback.answer()


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
