import logging

from aiogram import Bot, Dispatcher
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, ReplyKeyboardMarkup
from aiogram.utils import executor
from aiogram.dispatcher.filters import Text
from aiogram_calendar import simple_cal_callback, SimpleCalendar, dialog_cal_callback, DialogCalendar

from config import API_TOKEN

# API_TOKEN = '' uncomment and insert your telegram bot API key here

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

start_kb = ReplyKeyboardMarkup(resize_keyboard=True,)
start_kb.row('Navigation Calendar', 'Dialog Calendar')


# starting bot when user sends `/start` command, answering with inline calendar
@dp.message_handler(commands=['start'])
async def cmd_start(message: Message):
    await message.reply('Pick a calendar', reply_markup=start_kb)


@dp.message_handler(Text(equals=['Navigation Calendar'], ignore_case=True))
async def nav_cal_handler(message: Message):
    await message.answer("Please select a date: ", reply_markup=await SimpleCalendar().start_calendar())


# simple calendar usage
@dp.callback_query_handler(simple_cal_callback.filter())
async def process_simple_calendar(callback_query: CallbackQuery, callback_data: dict):
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    if selected:
        await callback_query.message.answer(
            f'You selected {date.strftime("%d/%m/%Y")}',
            reply_markup=start_kb
        )


@dp.message_handler(Text(equals=['Dialog Calendar'], ignore_case=True))
async def simple_cal_handler(message: Message):
    await message.answer("Please select a date: ", reply_markup=await DialogCalendar().start_calendar())


# dialog calendar usage
@dp.callback_query_handler(dialog_cal_callback.filter())
async def process_dialog_calendar(callback_query: CallbackQuery, callback_data: dict):
    selected, date = await DialogCalendar().process_selection(callback_query, callback_data)
    if selected:
        await callback_query.message.answer(
            f'You selected {date.strftime("%d/%m/%Y")}',
            reply_markup=start_kb
        )


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
