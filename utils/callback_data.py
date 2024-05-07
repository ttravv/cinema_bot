from typing import Optional
from aiogram.filters.callback_data import CallbackData


class Genre(CallbackData, prefix="genre"):
    name: str


class Year(CallbackData, prefix="year"):
    genre: str
    range: str


genres = [
    "аниме",
    "биография",
    "боевик",
    "вестерн",
    "военный",
    "детектив",
    "детский",
    "для взрослых",
    "документальный",
    "драма",
    "игра",
    "история",
    "комедия",
    "концерт",
    "короткометражка",
    "криминал",
    "мелодрама",
    "музыка",
    "мультфильм",
    "мюзикл",
    "новости",
    "приключения",
    "реальное ТВ",
    "семейный",
    "спорт",
    "триллер",
    "ужасы",
    "фантастика",
    "фильм-нуар",
    "фэнтези",
]
