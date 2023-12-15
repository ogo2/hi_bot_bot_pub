from aiogram import types, F, Router
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command
from aiogram import flags
import kb
from db import Data_base
import text
from aiogram import Bot, Dispatcher, types
from aiogram.methods import SendPhoto
from aiogram.methods.send_photo import SendPhoto
from aiogram import flags
from aiogram.fsm.context import FSMContext
import utils
from states import Breef_state, Communi_state
from aiogram import types
from aiogram.enums import ContentType
import random
import config

router = Router()
data_base = Data_base()
bot = Bot(token=config.BOT_TOKEN)

#старт бота
@flags.chat_action("upload_photo")
@router.message(Command("start"))
async def start_handler(msg: Message, state: FSMContext):
    photo = FSInputFile('photo/telegramrobot.png')
    await msg.answer_photo(photo, text.greet, reply_markup = kb.menu)
    
#старт бота || Нажаите на кнопку "Вернуться в меню"
@router.callback_query(F.data == 'reset')
async def start_handler(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()

    photo = FSInputFile('photo/telegramrobot.png')
    await callback.message.answer_photo(photo, text.greet, reply_markup = kb.menu)
    # await callback.message.answer(text.greet, reply_markup = kb.menu)
    await callback.answer()

#Нажатие на кнопку "Напишите нам"
@router.callback_query(F.data == 'tap_me_text')
async def message_me_please(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Breef_state.message_state_user_id)
    await callback.message.answer(text.tap_me_text)
    await callback.answer()
    
#Заполнение формы "Напишите нам"
@router.message(Breef_state.message_state_user_id, F.text)
async def message_user_id(msg: Message, state: FSMContext):
    data_base.add_users_tap_bot(msg.from_user.username, msg.from_user.id, msg.text)
    print(msg.from_user.id)
    await msg.answer(text.message_text_user_id, reply_markup=kb.back_to_menu)
    await bot.send_message(chat_id=6505189011, text=text.info_tap_me_user.format(username=msg.from_user.username, message=msg.text))
    await state.clear()
    

    
#Заполнение формы "Заполнить бриф"
@router.callback_query(F.data == 'breef')
async def breef_client(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Breef_state.name_state)
    await callback.message.answer(text.breef_text)
    await callback.message.answer(text.name_text)
    await callback.answer()
    
#Заполнение формы "Заполнить бриф"
@router.message(Breef_state.name_state, F.text)
async def breef_save_name(msg: Message, state: FSMContext):
    await state.update_data(name_user_state=msg.text)
    await state.set_state(Breef_state.email_state)
    await msg.answer(text.email_text)

#Заполнение формы "Заполнить бриф"
@router.message(Breef_state.email_state, F.text)
async def breef_save_name(msg: Message, state: FSMContext):
    await state.update_data(email_user_state=msg.text)
    user_data = await state.get_data()
    if utils.regular(user_data['email_user_state']) == True:
        await state.set_state(Breef_state.phone_state)
        await msg.answer(text.phone_text, reply_markup=kb.get_contact)
    else:
        await msg.answer(text.email_text_repeat)
        
#Заполнение формы "Заполнить бриф"
@router.message(Breef_state.phone_state)
async def breef_save_name(msg: Message, state: FSMContext):
    try:
        phone = msg.contact.phone_number
        await state.update_data(phone_user_state=phone)
        await state.set_state(Breef_state.message_state)
        await msg.answer(text.message_text, reply_markup=types.ReplyKeyboardRemove())
    except AttributeError:
        if msg.text.isdigit() == True:
            await state.update_data(phone_user_state=msg.text)
            await state.set_state(Breef_state.message_state)
            await msg.answer(text.message_text, reply_markup=types.ReplyKeyboardRemove())
        else:
            await msg.answer(text.phone_error)

#Заполнение формы "Заполнить бриф"
@router.message(Breef_state.message_state, F.text)
async def breef_save_name(msg: Message, state: FSMContext):
    await state.update_data(message_user_state=msg.text)
    user_data = await state.get_data()
    data_base.add_user_breef(msg.from_user.username, msg.from_user.id, user_data['name_user_state'], user_data['email_user_state'], user_data['phone_user_state'], user_data['message_user_state'])
    # print(user_data)
    username = msg.from_user.username
    await bot.send_message(chat_id=6505189011, text=text.info_breef_user.format(name=user_data['name_user_state'], email=user_data['email_user_state'], message=user_data['message_user_state'], phone=user_data['phone_user_state'], username=msg.from_user.username))
    await state.clear()
    await msg.answer(text.breef_result_client, reply_markup=kb.back_to_menu)

#Нажатие на кнопку "сотрудничество"
@router.callback_query(F.data == 'communi')
async def communication(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Communi_state.phone_state_communi)
    await callback.message.answer(text.communi_text)
    await callback.message.answer(text.phone_text, reply_markup=kb.get_contact)
    await callback.answer()

#сохраняем номер телефона
@router.message(Communi_state.phone_state_communi)
async def communi_save_phone(msg: Message, state: FSMContext):
    try:
        phone = msg.contact.phone_number
        await state.update_data(phone_user_state_communi=phone)
        await state.set_state(Communi_state.message_state_communi)
        await msg.answer(text.communi_text_end, reply_markup=types.ReplyKeyboardRemove())
    except AttributeError:
        if msg.text.isdigit() == True:
            await state.update_data(phone_user_state_communi=msg.text)
            await state.set_state(Communi_state.message_state_communi)
            await msg.answer(text.communi_text_end, reply_markup=types.ReplyKeyboardRemove())
        else:
            await msg.answer(text.phone_error)
    

#сохраняем текст предложения о сотрудничестве
@router.message(Communi_state.message_state_communi)
async def communi_save_phone(msg: Message, state: FSMContext):
    await state.update_data(message_user_state_communi=msg.text)
    user_data = await state.get_data()
    f= [msg.from_user.username, msg.from_user.id, user_data['phone_user_state_communi'], user_data['message_user_state_communi']]
    await bot.send_message(chat_id=6505189011, text=text.info_communi_user.format(username=msg.from_user.username, message=msg.text, phone_number=user_data['phone_user_state_communi']))
    data_base.add_user_communi(msg.from_user.username, msg.from_user.id, user_data['phone_user_state_communi'], user_data['message_user_state_communi'])
    await msg.answer(text.message_text_user_id, reply_markup=kb.back_to_menu)

# #О нас
@flags.chat_action("upload_photo")
@router.callback_query(F.data == 'info')
async def message_me_please(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    photo = FSInputFile('photo/telegramrobotonemore.png')
    await callback.message.answer_photo(photo, text.info_kompany, reply_markup=kb.breef_menu)
    await callback.answer()

#Цены
@router.callback_query(F.data == 'price')
async def communication(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    for i in range(len(text.price_array)):
        await callback.message.answer(text.price_array[i])
    await callback.message.answer(text.price_info, reply_markup=kb.breef_menu)
    await callback.answer()

#ответ на любое бесполезное сообщение от пользователя
@router.message(F.text) 
@router.message(F.sticker)
# @router.message(F.ANIMATION)
async def sticker(msg: Message):
    await msg.delete()
    number = random.randint(0, 2)
    await msg.answer_sticker(text.stickers[number])