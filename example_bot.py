import logging
import asyncio
import sys


# from aiogram.types import Message, CallbackQuery
# from aiogram.dispatcher.filters import Text
# from aiogram_calendar import simple_cal_callback, SimpleCalendar, dialog_cal_callback, DialogCalendar
from aiogram import Bot, Dispatcher     # , Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.markdown import hbold

from config import API_TOKEN

# API_TOKEN = '' uncomment and insert your telegram bot API key here


# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()


# initialising keyboard
kb = [
    [   # 1 row of buttons
        KeyboardButton(text='Navigation Calendar'),
        KeyboardButton(text='Navigation Calendar w month'),
    ],
    [   # 2 row of buttons
        KeyboardButton(text='Dialog Calendar'),
        KeyboardButton(text='Dialog Calendar w year'),
        KeyboardButton(text='Dialog Calendar w month'),
    ],
]
start_kb = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)


# when user sends `/start` command, answering with inline calendar
@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.reply(f"Hello, {hbold(message.from_user.full_name)}! Pick a calendar", reply_markup=start_kb)


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(API_TOKEN, parse_mode=ParseMode.HTML)

    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())


# @dp.message_handler(Text(equals=['Navigation Calendar'], ignore_case=True))
# async def nav_cal_handler(message: Message):
#     await message.answer("Please select a date: ", reply_markup=await SimpleCalendar().start_calendar())


# @dp.message_handler(Text(equals=['Navigation Calendar w month'], ignore_case=True))
# async def nav_cal_handler_date(message: Message):
#     await message.answer("Calendar opened on feb 1999. Please select a date: ", reply_markup=await SimpleCalendar().start_calendar(1999, 2))


# # simple calendar usage
# @dp.callback_query_handler(simple_cal_callback.filter())
# async def process_simple_calendar(callback_query: CallbackQuery, callback_data: dict):
#     selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
#     if selected:
#         await callback_query.message.answer(
#             f'You selected {date.strftime("%d/%m/%Y")}',
#             reply_markup=start_kb
#         )


# @dp.message_handler(Text(equals=['Dialog Calendar'], ignore_case=True))
# async def dialog_cal_handler(message: Message):
#     await message.answer("Please select a date: ", reply_markup=await DialogCalendar().start_calendar())


# # starting calendar with year 1989
# @dp.message_handler(Text(equals=['Dialog Calendar w year'], ignore_case=True))
# async def dialog_cal_handler_year(message: Message):
#     await message.answer(
#         "Calendar opened years selection around 1989. Please select a date: ",
#         reply_markup=await DialogCalendar().start_calendar(1989)
#     )


# # starting calendar with year 1989 & month
# @dp.message_handler(Text(equals=['Dialog Calendar w month'], ignore_case=True))
# async def dialog_cal_handler_month(message: Message):
#     await message.answer(
#         "Calendar opened on sep 1989. Please select a date: ",
#         reply_markup=await DialogCalendar().start_calendar(1989, 9)
#     )


# # dialog calendar usage
# @dp.callback_query_handler(dialog_cal_callback.filter())
# async def process_dialog_calendar(callback_query: CallbackQuery, callback_data: dict):
#     selected, date = await DialogCalendar().process_selection(callback_query, callback_data)
#     if selected:
#         await callback_query.message.answer(
#             f'You selected {date.strftime("%d/%m/%Y")}',
#             reply_markup=start_kb
#         )
