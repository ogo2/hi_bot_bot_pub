from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram import types

menu = [
    [InlineKeyboardButton(text="📝 Напишите нам", callback_data="tap_me_text"),
    InlineKeyboardButton(text="🤝 Сотрудничество", callback_data="communi")],
    [InlineKeyboardButton(text="💰 Цены", callback_data="price")],
    [InlineKeyboardButton(text="📝 Заполнить бриф", callback_data="breef"),
    InlineKeyboardButton(text="🤖 О нас", callback_data="info")]
]
back_to_menu = [
    [InlineKeyboardButton(text="↩️Вернуться в меню", callback_data="reset")]
]

get_contact = [
    [types.KeyboardButton(text='📞Поделиться номером', request_contact=True)]
]

get_contact = types.ReplyKeyboardMarkup(
    keyboard = get_contact,
    resize_keyboard=True,
    input_field_placeholder="Выберите способ подачи",
    one_time_keyboard=True
    
)
breef_menu = [
    [InlineKeyboardButton(text='↩️Вернуться в меню', callback_data='reset')]
]
breef_menu = InlineKeyboardMarkup(inline_keyboard=breef_menu)
menu = InlineKeyboardMarkup(inline_keyboard=menu)
back_to_menu = InlineKeyboardMarkup(inline_keyboard=back_to_menu)
