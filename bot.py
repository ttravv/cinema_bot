import asyncio
import logging
from typing import Optional
from aiogram import Bot, Dispatcher, types, F
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.filters.command import Command, CommandObject
from aiogram.filters.callback_data import CallbackData
from dotenv import dotenv_values
import httpx


class Genre(CallbackData, prefix='genre'):
    genre: str
    year_start: Optional[int] = None
    year_end: Optional[int] = None


genres = ['аниме', 
          'биография', 
          'боевик', 'вестерн', 'военный', 'детектив', 'детский', 'для взрослых', 'документальный', 'драма', 'игра', 'история', 'комедия', 'концерт', 'короткометражка', 'криминал', 'мелодрама', 'музыка', 'мультфильм', 'мюзикл', 'новости', 'приключения', 'реальное ТВ', 'семейный', 'спорт', 'ток-шоу', 'триллер', 'ужасы', 'фантастика', 'фильм-нуар', 'фэнтези', 'церемония']
# Включаем логирование, чтобы не пропустить важные сообщения
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
    builder = InlineKeyboardBuilder()
    for genre in genres:
        builder.add(types.InlineKeyboardButton(text=genre, callback_data=Genre(genre=genre).pack()))
        

    builder.adjust(2)
    await message.answer('Выберите жанр', 
                         reply_markup=builder.as_markup()
        ) 

@dp.callback_query(Genre.filter())
async def genre_handler(callback: types.CallbackQuery, 
                        callback_data: Genre):
    await callback.message.answer(callback_data.genre)
    builder = InlineKeyboardBuilder()
    for i in range(1955, 2020+1, 5):
        builder.add(types.InlineKeyboardButton(text=f'{i} - {i+4}', callback_data=Genre(genre=callback_data.genre,
                                                                                        year_start=i,
                                                                                        year_end=i + 4).pack()))
    params = {
        "page": 1,
        "limit": 5,
        "votes.imdb": "100000-10000000000",
        "type": ["!tv-series", "!animated-series"],
        "genres.name": callback_data.genre,
        "sortField": "rating.imdb",
        "sortType": "-1",
        "year": f"{callback_data.year_start}-{callback_data.year_end}",
    }
    headers = {"X-API-KEY": "J7GTCYS-4VR49VC-N17VZK7-7EQK9SF"}

    r = httpx.get(
        "https://api.kinopoisk.dev/v1.4/movie", params=params, headers=headers
    )

    for movie in r.json()['docs']:
        name = movie['name']
        year = movie['year']
        



    builder.adjust(2)
    await callback.answer(callback_data.genre, reply_markup=builder.as_markup())

    await callback.answer()
    
@dp.callback_query(F.data_startswith('genre_'))
async def genre_handler(callback: types.CallbackQuery):
    genre = callback.data.split('_')[1]
    params = {'page': 1,
              'limit': 5,
              'sortField': 'rating.imdb',
              'votes.imdb': '100000-6666666666666',
              'sortType': '-1',
              'sortField': 'rating.imdb',
              'genres_name': genre
               }
    headers = {'X-API-KEY': 'RD6G77R-HXC4DRJ-Q9VHH42-V16YKE1'}
    r = httpx.get('https://api.kinopoisk.dev/v1.4/movie', params=params, headers=headers)

    movie = r.json()['docs'][0]
    name = movie['name']
    year = movie['year']
    imdb = movie['year']
    description = movie['description']

    await callback.message.answer(f'{name}\n'
                                  f'{year}\n'
                                  f"{imdb}\n"
                                  f'{description}\n'
                                 )
    


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())


dict_of_types = {'page': '1', 'limit': '10', 'sortField': 'rating.imdb', 'sortType': '-1', 'type': 'movie', 'votes.imdb': '100000-6666666666666'}