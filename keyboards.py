from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
)

def get_main_menu():
    buttons = [
        [KeyboardButton(text="Моя анкета")],
        [KeyboardButton(text="Регестрация")],
        [KeyboardButton(text="О боте")],
    ]
    return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=buttons)
def get_confirm_kb():
    buttons = [
        [InlineKeyboardButton(text="Потвердить", callback_data="confirm")],
        [InlineKeyboardButton(text="Отменить", callback_data="cancel")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)