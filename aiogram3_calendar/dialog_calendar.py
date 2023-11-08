# pylint: disable=duplicate-code
import calendar
from datetime import datetime

from aiogram.filters.callback_data import CallbackData
from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from aiogram3_calendar.calendar_types import DialogCalendarCallback, DialogCalendarAction, WEEKDAYS

ignore_callback = DialogCalendarCallback(act=DialogCalendarAction.IGNORE, year=-1, month=-1, day=-1)


class DialogCalendar:
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    def __init__(self, year: int = datetime.now().year, month: int = datetime.now().month):
        self.year = year
        self.month = month

    @staticmethod
    async def start_calendar(
            year: int = datetime.now().year
    ) -> InlineKeyboardMarkup:
        markup = [[  # first row - years

            InlineKeyboardButton(
                text=str(value),
                callback_data=DialogCalendarCallback(
                    act=DialogCalendarAction.SET_YEAR,
                    year=value,
                    month=-1,
                    day=-1).pack()
            ) for value in range(year - 2, year + 3)
        ], [  # nav buttons

            InlineKeyboardButton(
                text='<<',
                callback_data=DialogCalendarCallback(
                    act=DialogCalendarAction.PREV_YEARS, year=year, month=-1,
                    day=-1).pack()
            ),
            InlineKeyboardButton(
                text='>>',
                callback_data=DialogCalendarCallback(
                    act=DialogCalendarAction.NEXT_YEARS, year=year, month=-1,
                    day=-1).pack()
            ),
        ]]

        inline_kb = InlineKeyboardMarkup(inline_keyboard=markup)
        return inline_kb

    async def _get_month_kb(self, year: int):

        markup = [[  # first row with year button

            InlineKeyboardButton(text=" ", callback_data=ignore_callback.pack()),
            InlineKeyboardButton(
                text=str(year),
                callback_data=DialogCalendarCallback(
                    act=DialogCalendarAction.START, year=year, month=-1, day=-1).pack()
            ),
            InlineKeyboardButton(text=" ", callback_data=ignore_callback.pack()),
        ], [  # two rows with 6 months buttons

            InlineKeyboardButton(
                text=month,
                callback_data=DialogCalendarCallback(
                    act=DialogCalendarAction.SET_MONTH, year=year,
                    month=self.months.index(month) + 1, day=-1).pack()
            ) for month in self.months[0:6]
        ], [
            InlineKeyboardButton(
                text=month,
                callback_data=DialogCalendarCallback(
                    act=DialogCalendarAction.SET_MONTH, year=year,
                    month=self.months.index(month) + 1, day=-1).pack()
            ) for month in self.months[6:12]
        ]]

        inline_kb = InlineKeyboardMarkup(inline_keyboard=markup)
        return inline_kb

    async def _get_days_kb(self, year: int, month: int):
        markup = [[
            InlineKeyboardButton(
                text=str(year),
                callback_data=DialogCalendarCallback(
                    act=DialogCalendarAction.START, year=year, month=-1, day=-1).pack()
            ),
            InlineKeyboardButton(
                text=self.months[month - 1],
                callback_data=DialogCalendarCallback(
                    act=DialogCalendarAction.SET_YEAR, year=year, month=-1,
                    day=-1).pack()
            ),

        ], [
            InlineKeyboardButton(
                text=day, callback_data=ignore_callback.pack()
            ) for day in WEEKDAYS
        ]]

        month_calendar = calendar.monthcalendar(year, month)
        for week in month_calendar:
            calendar_row = []
            for day in week:
                if day == 0:
                    calendar_row.append(
                        InlineKeyboardButton(text=" ", callback_data=ignore_callback.pack()))
                    continue
                calendar_row.append(InlineKeyboardButton(
                    text=str(day),
                    callback_data=DialogCalendarCallback(
                        act=DialogCalendarAction.SET_DAY, year=year, month=month,
                        day=day).pack()
                ))
            markup.append(calendar_row)

        inline_kb = InlineKeyboardMarkup(inline_keyboard=markup)
        return inline_kb

    async def process_selection(self, query: CallbackQuery,
                                data: [CallbackData, DialogCalendarCallback]) -> tuple:
        return_data = (False, None)
        if data.act == DialogCalendarAction.IGNORE:
            await query.answer(cache_time=60)
        if data.act == DialogCalendarAction.SET_YEAR:
            await query.message.edit_reply_markup(
                reply_markup=await self._get_month_kb(int(data.year))
            )
        if data.act == DialogCalendarAction.PREV_YEARS:
            new_year = int(data.year) - 5
            await query.message.edit_reply_markup(
                reply_markup=await self.start_calendar(new_year)
            )
        if data.act == DialogCalendarAction.NEXT_YEARS:
            new_year = int(data.year) + 5
            await query.message.edit_reply_markup(
                reply_markup=await self.start_calendar(new_year)
            )
        if data.act == DialogCalendarAction.START:
            await query.message.edit_reply_markup(
                reply_markup=await self.start_calendar(int(data.year))
            )
        if data.act == DialogCalendarAction.SET_MONTH:
            await query.message.edit_reply_markup(
                reply_markup=await self._get_days_kb(int(data.year), int(data.month))
            )
        if data.act == DialogCalendarAction.SET_DAY:
            await query.message.delete_reply_markup()  # removing inline keyboard
            return_data = True, datetime(int(data.year), int(data.month), int(data.day))
        return return_data
