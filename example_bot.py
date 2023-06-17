import logging

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton
from aiogram_calendar import calendar_callback_filter, SimpleCalendar, dialog_callback_filter, DialogCalendar

from config import API_TOKEN

# API_TOKEN = '' uncomment and insert your telegram bot API key here

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

start_kb = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=
                               [[KeyboardButton(text='Navigation Calendar'), KeyboardButton(text='Dialog Calendar')]])


# starting bot when user sends `/start` command, answering with inline calendar
@dp.message(F.text.startswith('/start'))
async def cmd_start(message: Message):
    await message.reply('Pick a calendar', reply_markup=start_kb)


@dp.message(F.text.lower() == 'Navigation Calendar'.lower())
async def nav_cal_handler(message: Message):
    await message.answer("Please select a date: ", reply_markup=await SimpleCalendar().start_calendar())


# simple calendar usage
@dp.callback_query(calendar_callback_filter)
async def process_simple_calendar(callback_query: CallbackQuery):
    selected, date = await SimpleCalendar().process_selection(callback_query)
    if selected:
        await callback_query.message.answer(
            f'You selected {date.strftime("%d/%m/%Y")}',
            reply_markup=start_kb
        )


@dp.message(F.text.lower() == 'Dialog Calendar'.lower())
async def simple_cal_handler(message: Message):
    await message.answer("Please select a date: ", reply_markup=await DialogCalendar().start_calendar())


# dialog calendar usage
@dp.callback_query(dialog_callback_filter)
async def process_dialog_calendar(callback_query: CallbackQuery):
    selected, date = await DialogCalendar().process_selection(callback_query)
    if selected:
        await callback_query.message.answer(
            f'You selected {date.strftime("%d/%m/%Y")}',
            reply_markup=start_kb
        )


if __name__ == '__main__':
    dp.run_polling(bot)
