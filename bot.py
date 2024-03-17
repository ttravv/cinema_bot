import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.filters.command import Command, CommandObject
from dotenv import dotenv_values
import httpx

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
    for i in genres:
        builder.add(types.InlineKeyboardButton(text=i, callback_data=f'genre_{i}')
        )

    builder.adjust(2)
    await message.answer('Выберите жанр', 
                         reply_markup=builder.as_markup()
                        )

@dp.callback_query(F.data.startswith('genre_'))
async def genre_handler(callback: types.CallbackQuery):
    genre = callback.data.split('_')[1]
    

    await callback.message.answer(f'Вы выбрали жанр {genre}')
    await callback.answer()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())


dict_of_types = {'page': '1', 'limit': '10', 'sortField': 'rating.imdb', 'sortType': '-1', 'type': 'movie', 'votes.imdb': '100000-6666666666666'}