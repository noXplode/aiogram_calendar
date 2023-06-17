import calendar
from datetime import datetime

from aiogram import F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import CallbackQuery


# setting callback_data prefix and parts
dialog_callback_filter = F.data.startswith('dialog_calendar')


def build_data(action: str, year: int, month: int, day: int): return f"dialog_calendar&{action}&{year}&{month}&{day}"
def process_data(data: str) -> dict: data = data.split("&")[1:]; return {"act": data[0], "year": data[1], "month": data[2], "day": data[3]}


ignore_callback = build_data("IGNORE", -1, -1, -1)


class DialogCalendar:
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    def __init__(self, year: int = datetime.now().year, month: int = datetime.now().month):
        self.year = year
        self.month = month

    async def start_calendar(
        self,
        year: int = datetime.now().year
    ) -> InlineKeyboardMarkup:
        inline_kb = []
        # first row - years
        inline_row = []
        for value in range(year - 2, year + 3):
            inline_row.append(InlineKeyboardButton(
                text=value,
                callback_data=build_data("SET-YEAR", value, -1, -1)
            ))
        # nav buttons
        inline_kb.append(inline_row)
        inline_row = []
        inline_row.append(InlineKeyboardButton(
            text='<<',
            callback_data=build_data("PREV-YEARS", year, -1, -1)
        ))
        inline_row.append(InlineKeyboardButton(
            text='>>',
            callback_data=build_data("NEXT-YEARS", year, -1, -1)
        ))
        inline_kb.append(inline_row)

        return InlineKeyboardMarkup(row_width=5, inline_keyboard=inline_kb)

    async def _get_month_kb(self, year: int):
        inline_kb = []
        # first row with year button
        inline_row = []
        inline_row.append(InlineKeyboardButton(text=" ", callback_data=ignore_callback))
        inline_row.append(InlineKeyboardButton(
            text=year,
            callback_data=build_data("START", year, -1, -1)
        ))
        inline_row.append(InlineKeyboardButton(text=" ", callback_data=ignore_callback))
        # two rows with 6 months buttons
        inline_kb.append(inline_row)
        inline_row = []
        for month in self.months[0:6]:
            inline_row.append(InlineKeyboardButton(
                text=month,
                callback_data=build_data("SET-MONTH", year, self.months.index(month) + 1, -1)
            ))
        inline_kb.append(inline_row)
        inline_row = []
        for month in self.months[6:12]:
            inline_row.append(InlineKeyboardButton(
                text=month,
                callback_data=build_data("SET-MONTH", year, self.months.index(month) + 1, -1)
            ))
        inline_kb.append(inline_row)
        return InlineKeyboardMarkup(row_width=6, inline_keyboard=inline_kb)

    async def _get_days_kb(self, year: int, month: int):
        inline_kb = []
        inline_row = []
        inline_row.append(InlineKeyboardButton(
            text=year,
            callback_data=build_data("START", year, -1, -1)
        ))
        inline_row.append(InlineKeyboardButton(
            text=self.months[month - 1],
            callback_data=build_data("SET-YEAR", year, -1, -1)
        ))
        inline_kb.append(inline_row)
        inline_row = []
        for day in ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]:
            inline_row.append(InlineKeyboardButton(text=day, callback_data=ignore_callback))
        inline_kb.append(inline_row)

        month_calendar = calendar.monthcalendar(year, month)
        for week in month_calendar:
            inline_row = []
            for day in week:
                if (day == 0):
                    inline_row.append(InlineKeyboardButton(text=" ", callback_data=ignore_callback))
                    continue
                inline_row.append(InlineKeyboardButton(
                    text=str(day), callback_data=build_data("SET-DAY", year, month, day)
                ))
            inline_kb.append(inline_row)
        return InlineKeyboardMarkup(row_width=7, inline_keyboard=inline_kb)

    async def process_selection(self, query: CallbackQuery) -> tuple:
        return_data = (False, None)
        data = process_data(query.data)
        if data['act'] == "IGNORE":
            await query.answer(cache_time=60)
        if data['act'] == "SET-YEAR":
            await query.message.edit_reply_markup(reply_markup=await self._get_month_kb(int(data['year'])))
        if data['act'] == "PREV-YEARS":
            new_year = int(data['year']) - 5
            await query.message.edit_reply_markup(reply_markup=await self.start_calendar(new_year))
        if data['act'] == "NEXT-YEARS":
            new_year = int(data['year']) + 5
            await query.message.edit_reply_markup(reply_markup=await self.start_calendar(new_year))
        if data['act'] == "START":
            await query.message.edit_reply_markup(reply_markup=await self.start_calendar(int(data['year'])))
        if data['act'] == "SET-MONTH":
            await query.message.edit_reply_markup(reply_markup=await self._get_days_kb(int(data['year']), int(data['month'])))
        if data['act'] == "SET-DAY":
            await query.message.delete_reply_markup()   # removing inline keyboard
            return_data = True, datetime(int(data['year']), int(data['month']), int(data['day']))
        return return_data
