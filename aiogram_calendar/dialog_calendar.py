import calendar
from datetime import datetime, timedelta

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from aiogram.types import CallbackQuery


# setting callback_data prefix and parts
calendar_callback = CallbackData('calendar', 'act', 'year', 'month', 'day')
ignore_callback = calendar_callback.new("IGNORE", -1, -1, -1)  # for buttons with no answer


class DialogCalendar:

    async def start_calendar(
        self,
        year: int = datetime.now().year,
        month: int = datetime.now().month
    ) -> InlineKeyboardMarkup:
        inline_kb = InlineKeyboardMarkup(row_width=5)
        # first row - years
        inline_kb.row()
        for value in range(year - 2, year + 3):
            inline_kb.insert(InlineKeyboardButton(
                value,
                callback_data=calendar_callback.new("SET-YEAR", year, -1, -1)
            ))
        # nav buttons
        inline_kb.row()
        inline_kb.insert(InlineKeyboardButton(
            '<<',
            callback_data=ignore_callback
        ))
        inline_kb.insert(InlineKeyboardButton(
            '>>',
            callback_data=ignore_callback
        ))

        return inline_kb

    async def process_selection(self, query: CallbackQuery, data: CallbackData) -> tuple:
        pass
