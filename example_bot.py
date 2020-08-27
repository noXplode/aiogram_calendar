import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogramcalendar import create_calendar, process_calendar_selection

API_TOKEN = ''    # insert your telegram bot API key here

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


# starting bot when user sends `/start` command
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer("Please select a date: ", reply_markup=create_calendar())


@dp.callback_query_handler()
async def process_name(callback_query):
    selected,date = await process_calendar_selection(bot, callback_query)
    if selected:
        await bot.send_message(chat_id=callback_query.from_user.id,
                        text="You selected %s" % (date.strftime("%d/%m/%Y")),
                        reply_markup=types.ReplyKeyboardRemove())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
