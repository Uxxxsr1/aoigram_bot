import asyncio
from aiogram import Bot, Dispatcher
from config import TOKEN
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from keyboards import get_main_menu, get_confirm_kb
BOT_TOKEN = TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command('start'))
async def start_command(message: Message):
    await message.answer(f"Привет, <b>{message.from_user.first_name}</b>, выберите действие", reply_markup=get_main_menu(), parse_mode="HTML")
@dp.message(lambda message: message.text == "О боте")
async def about_bot(message: Message):
    await message.answer(f"Это учебный бот", reply_markup=get_confirm_kb())
@dp.callback_query(lambda c: c.data == "confirm")
async def confirm_callback(callback_query: CallbackQuery):
    await callback_query.answer("Вы подтвердили действие")
    await callback_query.message.edit_text("Спасибо за подтверждение!")
@dp.callback_query(lambda c: c.data == "cancel")
async def confirm_callback(callback_query: CallbackQuery):
    await callback_query.answer("Вы отменили действие")
    await callback_query.message.delete()

async def main():
    await dp.start_polling(bot)
if __name__ == "__main__":
    asyncio.run(main())