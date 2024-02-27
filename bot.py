import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.filters.command import Command, CommandObject
from dotenv import dotenv_values
import datetime
import webbrowser


# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
config = dotenv_values(".env")
bot = Bot(token=config["BOT_TOKEN"])
# Диспетчер
dp = Dispatcher()
dp['my_list'] = []

@dp.message(Command('datetime'))
async def add_to_list(message: types.Message, my_list: list):
    my_list.append(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
    await message.reply(f'Список временных мерок {str(my_list)}')

@dp.message(Command('dice'))
async def dice(message: types.Message):
    await message.answer_dice(emoji='🎲')

@dp.message(Command('settimer'))
async def cmd_settimer(
        message: types.Message,
        command: CommandObject
):
    if command.args is None:
        await message.answer(
            "Ошибка: не переданы аргументы"
)

    try:
        delay_time, text_to_send = command.args.split(" ", maxsplit=1)
    except ValueError:
        await message.answer(
            "Ошибка: неправильный формат команды. Пример:\n"
            "/settimer <time> <message>"
)
        return
    if delay_time == 20:
        await message.answer('....'
)
    else:
        await message.answer(
        "Таймер добавлен!\n"
        f"Время: {delay_time}\n"
        f"Текст: {text_to_send}"
)

@dp.message(Command("ugadaika"))
async def reply_builder(message: types.Message):
    builder = ReplyKeyboardBuilder()
    for i in range(1, 17):
        builder.add(types.KeyboardButton(text=str(i)))
    builder.adjust(4)
    await message.answer(
        "Выберите число:",
        reply_markup=builder.as_markup(resize_keyboard=True))
    
@dp.message(Command('start'))
async def start_button(message: types.Message, bot: Bot):
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
    builder.row(types.InlineKeyboardButton(
        text="Детективы", url="https://yandex.ru/search/?text=топ+5+фильмов+детективов")
)
    builder.row(types.InlineKeyboardButton(
        text="Триллеры",
        url="https://yandex.ru/search/?text=топ+5+фильмов+триллеров")
)
    builder.row(types.InlineKeyboardButton(
        text='Слешеры', 
        url='https://yandex.ru/search/?text=топ+5+фильмов+слешеров')
)
    builder.row(types.InlineKeyboardButton(
        text='Боевики', 
        url='https://yandex.ru/search/?text=топ+5+фильмов+боевиков')
)
    builder.row(types.InlineKeyboardButton(
        text='Ужасы',
        url='https://yandex.ru/search/?text=топ+5+фильмов+ужасов')
)
    await message.answer(
        'Выберите жанр',
        reply_markup=builder.as_markup(), 
)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())



