from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types
from .callback_data import Year, Genre, genres


def genre_kb() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    for i in genres:
        builder.add(
            types.InlineKeyboardButton(text=i, callback_data=Genre(name=i).pack())
        )

    builder.adjust(2)

    return builder


def years_kb(genre: str) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    for i in range(1965, 2024 + 1, 5):
        years_range = f"{i}-{i+4}"
        builder.add(
            types.InlineKeyboardButton(
                text=years_range,
                callback_data=Year(genre=genre, range=f"{i}-{i+4}").pack(),
            )
        )
    builder.adjust(2)

    return builder
