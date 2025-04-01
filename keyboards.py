from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

builder = InlineKeyboardBuilder
button = InlineKeyboardButton

def confirm_menu():
    return builder(markup=[
        [
            button(text="HA", callback_data="HA"),
            button(text="YO'Q", callback_data="YO'Q"),
        ]
    ]).as_markup()

def channel_menu(bot: str, ssh: str):
    return builder(markup=[
        [
            button(text="BOT", url=f"https://t.me/{bot}")
        ],
        [
            button(text="SSH", url=f"{ssh}")
        ]
    ]).as_markup()