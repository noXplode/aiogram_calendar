import calendar
from typing import Optional
from datetime import datetime

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData
from aiogram.types import CallbackQuery


# setting callback_data prefix and parts
# calendar_callback = CallbackData('dialog_calendar', 'act', 'year', 'month', 'day')
# ignore_callback = calendar_callback.new("IGNORE", -1, -1, -1)  # for buttons with no answer

class DialogCallback(CallbackData, prefix="dialog_calendar"):
    act: str
    year: Optional[int] = None
    month: Optional[int] = None
    day: Optional[int] = None


ignore_callback = DialogCallback(act="IGNORE").pack()


class DialogCalendar:
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    async def start_calendar(
        self,
        year: int = datetime.now().year,
        month: int = None
    ) -> InlineKeyboardMarkup:
        if month:
            return await self._get_days_kb(year, month)
        kb = []
        # inline_kb = InlineKeyboardMarkup(row_width=5)
        # first row - years
        years_row = []
        for value in range(year - 2, year + 3):
            years_row.append(InlineKeyboardButton(
                text=str(value),
                callback_data=DialogCallback(act="SET-YEAR", year=value, month=-1, day=-1).pack()
            ))
        kb.append(years_row)
        # nav buttons
        nav_row = []
        nav_row.append(InlineKeyboardButton(
            text='<<',
            callback_data=DialogCallback(act="PREV-YEAR", year=year, month=-1, day=-1).pack()
        ))
        nav_row.append(InlineKeyboardButton(
            text="Cancel",
            callback_data=DialogCallback(act="CANCEL", year=year, month=1, day=1).pack()
        ))
        nav_row.append(InlineKeyboardButton(
            text='>>',
            callback_data=DialogCallback(act="NEXT-YEARS", year=year, month=1, day=1).pack()
        ))
        kb.append(nav_row)
        return InlineKeyboardMarkup(row_width=5, inline_keyboard=kb)

    async def _get_month_kb(self, year: int):
        kb = []
        # first row with year button
        years_row = []
        years_row.append(
            InlineKeyboardButton(
                text="Cancel",
                callback_data=DialogCallback(act="CANCEL", year=year, month=1, day=1).pack()
            )
        )
        years_row.append(InlineKeyboardButton(
            text=str(year),
            callback_data=DialogCallback(act="START", year=year, month=-1, day=-1).pack()
        ))
        years_row.append(InlineKeyboardButton(text=" ", callback_data=ignore_callback))
        kb.append(years_row)
        # two rows with 6 months buttons
        month6_row = []
        for month in self.months[0:6]:
            month6_row.append(InlineKeyboardButton(
                text=month,
                callback_data=DialogCallback(act="SET-MONTH", year=year, month=self.months.index(month) + 1, day=-1).pack()
            ))
        month12_row = []
        for month in self.months[6:12]:
            month12_row.append(InlineKeyboardButton(
                text=month,
                callback_data=DialogCallback(act="SET-MONTH", year=year, month=self.months.index(month) + 1, day=-1).pack()
            ))
        kb.append(month6_row)
        kb.append(month12_row)
        return InlineKeyboardMarkup(row_width=6, inline_keyboard=kb)

    async def _get_days_kb(self, year: int, month: int):
        kb = []
        nav_row = []
        nav_row.append(
            InlineKeyboardButton(
                text="Cancel",
                callback_data=DialogCallback(act="CANCEL", year=year, month=1, day=1).pack()
            )
        )
        nav_row.append(InlineKeyboardButton(
            text=str(year),
            callback_data=DialogCallback(act="START", year=year, month=-1, day=-1).pack()
        ))
        nav_row.append(InlineKeyboardButton(
            text=self.months[month - 1],
            callback_data=DialogCallback(act="SET-YEAR", year=year, month=-1, day=-1).pack()
        ))
        kb.append(nav_row)

        week_days_labels_row = []
        for day in ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]:
            week_days_labels_row.append(InlineKeyboardButton(text=day, callback_data=ignore_callback))
        kb.append(week_days_labels_row)

        month_calendar = calendar.monthcalendar(year, month)
        for week in month_calendar:
            days_row = []
            for day in week:
                if (day == 0):
                    days_row.append(InlineKeyboardButton(text=" ", callback_data=ignore_callback))
                    continue
                days_row.append(InlineKeyboardButton(
                    text=str(day), callback_data=DialogCallback(act="SET-DAY", year=year, month=month, day=day).pack()
                ))
            kb.append(days_row)
        return InlineKeyboardMarkup(row_width=7, inline_keyboard=kb)

    async def process_selection(self, query: CallbackQuery, data: DialogCallback) -> tuple:
        return_data = (False, None)
        if data.act == "IGNORE":
            await query.answer(cache_time=60)
        if data.act == "SET-YEAR":
            await query.message.edit_reply_markup(reply_markup=await self._get_month_kb(int(data.year)))
        if data.act == "PREV-YEARS":
            new_year = int(data.year) - 5
            await query.message.edit_reply_markup(reply_markup=await self.start_calendar(year=new_year))
        if data.act == "NEXT-YEARS":
            new_year = int(data.year) + 5
            await query.message.edit_reply_markup(reply_markup=await self.start_calendar(year=new_year))
        if data.act == "START":
            await query.message.edit_reply_markup(reply_markup=await self.start_calendar(int(data.year)))
        if data.act == "SET-MONTH":
            await query.message.edit_reply_markup(reply_markup=await self._get_days_kb(int(data.year), int(data.month)))
        if data.act == "SET-DAY":
            await query.message.delete_reply_markup()   # removing inline keyboard
            return_data = True, datetime(int(data.year), int(data.month), int(data.day))
        if data.act == "CANCEL":
            await query.message.delete_reply_markup()
        return return_data
