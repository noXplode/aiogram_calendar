import calendar
from datetime import datetime

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import CallbackQuery
from .calendar_types import DialogCalendarCallback, CalendarAction


ignore_callback = DialogCalendarCallback(act=CalendarAction.IGNORE, year=-1, month=-1, day=-1)


class DialogCalendar:
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    def __init__(self, year: int = datetime.now().year, month: int = datetime.now().month):
        self.year = year
        self.month = month

    async def start_calendar(
        self,
        year: int = datetime.now().year
    ) -> InlineKeyboardMarkup:
        inline_kb = InlineKeyboardMarkup(row_width=5)
        # first row - years
        inline_kb.row()
        for value in range(year - 2, year + 3):
            inline_kb.insert(InlineKeyboardButton(
                text=value,
                callback_data=CalendarCallback(act=CalendarAction.SET_YEAR, year=value, month=-1, day=-1)
            ))
        # nav buttons
        inline_kb.row()
        inline_kb.insert(InlineKeyboardButton(
            text='<<',
            callback_data=CalendarCallback(act=CalendarAction.PREV_YEAR, year=year, month=-1, day=-1)
        ))
        inline_kb.insert(InlineKeyboardButton(
            text='>>',
            callback_data=CalendarCallback(act=CalendarAction.NEXT_YEAR, year=year, month=-1, day=-1)
        ))

        return inline_kb

    async def _get_month_kb(self, year: int):
        inline_kb = InlineKeyboardMarkup(row_width=6)
        # first row with year button
        inline_kb.row()
        inline_kb.insert(InlineKeyboardButton(" ", callback_data=ignore_callback))
        inline_kb.insert(InlineKeyboardButton(
            text=year,
            callback_data=CalendarCallback(act=CalendarAction.START, year=year, month=-1, day=-1)
        ))
        inline_kb.insert(InlineKeyboardButton(" ", callback_data=ignore_callback))
        # two rows with 6 months buttons
        inline_kb.row()
        for month in self.months[0:6]:
            inline_kb.insert(InlineKeyboardButton(
                text=month,
                callback_data=CalendarCallback(act=CalendarAction.SET_MONTH, year=year, month=self.months.index(month) + 1, day=-1)
            ))
        inline_kb.row()
        for month in self.months[6:12]:
            inline_kb.insert(InlineKeyboardButton(
                text=month,
                callback_data=CalendarCallback(act=CalendarAction.SET_MONTH, year=year, month=self.months.index(month) + 1, day=-1)
            ))
        return inline_kb

    async def _get_days_kb(self, year: int, month: int):
        inline_kb = InlineKeyboardMarkup(row_width=7)
        inline_kb.row()
        inline_kb.insert(InlineKeyboardButton(
            text=year,
            callback_data=CalendarCallback(act=CalendarAction.START, year=year, month=-1, day=-1)
        ))
        inline_kb.insert(InlineKeyboardButton(
            text=self.months[month - 1],
            callback_data=CalendarCallback(act=CalendarAction.SET_YEAR, year=year, month=-1, day=-1)
        ))
        inline_kb.row()
        for day in ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]:
            inline_kb.insert(InlineKeyboardButton(text=day, callback_data=ignore_callback))

        month_calendar = calendar.monthcalendar(year, month)
        for week in month_calendar:
            inline_kb.row()
            for day in week:
                if (day == 0):
                    inline_kb.insert(InlineKeyboardButton(text=" ", callback_data=ignore_callback))
                    continue
                inline_kb.insert(InlineKeyboardButton(
                    text=str(day), callback_data=CalendarCallback(act=CalendarAction.SET_DAY, year=year, month=month, day=day)
                ))
        return inline_kb

    async def process_selection(self, query: CallbackQuery, data: [CallbackData, CalendarCallback]) -> tuple:
        return_data = (False, None)
        if data.act == CalendarAction.IGNORE:
            await query.answer(cache_time=60)
        if data.act == CalendarAction.SET_YEAR:
            await query.message.edit_reply_markup(await self._get_month_kb(int(data.year)))
        if data.act == CalendarAction.PREV_YEAR:
            new_year = int(data.year) - 5
            await query.message.edit_reply_markup(await self.start_calendar(new_year))
        if data.act == CalendarAction.NEXT_YEAR:
            new_year = int(data.year) + 5
            await query.message.edit_reply_markup(await self.start_calendar(new_year))
        if data.act == CalendarAction.START:
            await query.message.edit_reply_markup(await self.start_calendar(int(data.year)))
        if data.act == CalendarAction.SET_MONTH:
            await query.message.edit_reply_markup(await self._get_days_kb(int(data.year), int(data.month)))
        if data.act == CalendarAction.SET_DAY:
            await query.message.delete_reply_markup()   # removing inline keyboard
            return_data = True, datetime(int(data.year), int(data.month), int(data.day))
        return return_data
