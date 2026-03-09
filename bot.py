import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from config import TOKEN
from db import init_db, save_user, get_user_info
from keyboards import get_main_menu, get_confirm_kb, get_help_kb
from states import Regestration

BOT_TOKEN = TOKEN

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

@dp.message(Command('start'))
async def start_command(message: Message):
    await message.answer(
        f"Привет, <b>{message.from_user.first_name}</b>, выберите действие",
        reply_markup=get_main_menu()
    )

@dp.message(lambda message: message.text == "О боте")
async def about_bot(message: Message):
    await message.answer("Это учебный бот", reply_markup=get_help_kb())

@dp.message(lambda message: message.text == "Регестрация")  # Исправлено название
async def start_registration(message: Message, state: FSMContext):  # Исправлено название функции
    await state.set_state(Regestration.name)  # Исправлено название состояния
    await message.answer("Введите ваше имя")

@dp.message(Regestration.name)
async def process_name(message: Message, state: FSMContext):
    name = message.text.strip()
    if not name:
        await message.answer("Имя не может быть пустым")
        return
    await state.update_data(name=name)
    await state.set_state(Regestration.age)
    await message.answer("Введите ваш возраст")

@dp.message(Regestration.age)
async def process_age(message: Message, state: FSMContext):
    age_text = message.text.strip()
    if not age_text.isdigit():
        await message.answer("Возраст должен быть числом")
        return
    age = int(age_text)
    if age < 1 or age > 80:
        await message.answer("Введите ваш реальный возраст")
        return
    await state.update_data(age=age)
    await state.set_state(Regestration.confirm)
    data = await state.get_data()
    text = (
        f"Проверьте данные:\n"
        f"Имя: <b>{data['name']}</b>\n"
        f"Возраст: <b>{data['age']}</b>\n\nВсе верно?"
    )
    await message.answer(text, reply_markup=get_confirm_kb())

@dp.callback_query(lambda c: c.data == "confirm")
async def confirm_callback(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = callback_query.from_user.id
    save_user(
        user_id,
        data['name'],
        data['age']
    )
    await state.clear()
    await callback_query.answer("Регистрация завершена")
    await callback_query.message.edit_text("Спасибо за регистрацию!")


@dp.callback_query(lambda c: c.data == "cancel")
async def cancel_callback(callback_query: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback_query.answer("Вы отменили действие")
    await callback_query.message.edit_text("Регистрация отменена")

@dp.callback_query(lambda c: c.data == "doc")
async def doc_callback(callback_query: CallbackQuery):
    await callback_query.answer("Документация")
    await callback_query.message.edit_text("бла бла бла бла бла бла")

@dp.callback_query(lambda c: c.data == "support")
async def support_callback(callback_query: CallbackQuery):
    await callback_query.answer("Поддержка находится по ссылке t.me/openi486")

@dp.message(lambda message: message.text == 'Моя анкета')
async def show_profile(message: Message):
    user = get_user_info(message.from_user.id)
    if not user:
        await message.answer('Вы еще не были зарегистрированны')
        return
    text = f'''
        <b>Ваша анкета</b>
        Имя: {user['Name']}
        Возраст {user['Age']}
        Дата регестрации {user['CreatedAt']} 
    '''
    await message.answer(text)

async def main():
    init_db()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())