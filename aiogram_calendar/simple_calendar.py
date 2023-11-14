import calendar
from datetime import datetime, timedelta

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import CallbackQuery

from .schemas import SimpleCalendarCallback


class SimpleCalendar:

    async def start_calendar(
        self,
        year: int = datetime.now().year,
        month: int = datetime.now().month
    ) -> InlineKeyboardMarkup:
        """
        Creates an inline keyboard with the provided year and month
        :param int year: Year to use in the calendar, if None the current year is used.
        :param int month: Month to use in the calendar, if None the current month is used.
        :return: Returns InlineKeyboardMarkup object with the calendar.
        """
        # building a calendar keyboard
        kb = []
        ignore_callback = SimpleCalendarCallback(act="IGNORE").pack()  # placeholder for buttons with no answer

        # inline_kb = InlineKeyboardMarkup(row_width=7)
        # First row - Year
        years_row = []
        years_row.append(InlineKeyboardButton(
            text="<<",
            callback_data=SimpleCalendarCallback(act="PREV-YEAR", year=year, month=month, day=1).pack()
        ))
        years_row.append(InlineKeyboardButton(
            text=f'{calendar.month_name[month]} {str(year)}',
            callback_data=ignore_callback
        ))
        years_row.append(InlineKeyboardButton(
            text=">>",
            callback_data=SimpleCalendarCallback(act="NEXT-YEAR", year=year, month=month, day=1).pack()
        ))
        kb.append(years_row)

        # Second row - Week Days
        week_days_labels_row = []
        for day in ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]:
            week_days_labels_row.append(InlineKeyboardButton(text=day, callback_data=ignore_callback))
        kb.append(week_days_labels_row)

        # Calendar rows - Days of month
        month_calendar = calendar.monthcalendar(year, month)
        for week in month_calendar:
            days_row = []
            for day in week:
                if (day == 0):
                    days_row.append(InlineKeyboardButton(text=" ", callback_data=ignore_callback))
                    continue
                days_row.append(InlineKeyboardButton(
                    text=str(day),
                    callback_data=SimpleCalendarCallback(act="DAY", year=year, month=month, day=day).pack()
                ))
            kb.append(days_row)

        # Month nav Buttons & cancel button
        month_row = []
        month_row.append(InlineKeyboardButton(
            text="<", callback_data=SimpleCalendarCallback(act="PREV-MONTH", year=year, month=month, day=day).pack()
        ))
        month_row.append(InlineKeyboardButton(
            text="Cancel", callback_data=SimpleCalendarCallback(act="CANCEL", year=year, month=month, day=day).pack()
        ))
        month_row.append(InlineKeyboardButton(
            text="Today", callback_data=SimpleCalendarCallback(act="TODAY", year=year, month=month, day=day).pack()
        ))
        month_row.append(InlineKeyboardButton(
            text=">", callback_data=SimpleCalendarCallback(act="NEXT-MONTH", year=year, month=month, day=day).pack()
        ))
        kb.append(month_row)
        return InlineKeyboardMarkup(row_width=7, inline_keyboard=kb)

    async def _update_calendar(self, query: CallbackQuery, with_date: datetime):
        await query.message.edit_reply_markup(
            reply_markup=await self.start_calendar(int(with_date.year), int(with_date.month))
        )

    async def process_selection(self, query: CallbackQuery, data: SimpleCalendarCallback) -> tuple:
        """
        Process the callback_query. This method generates a new calendar if forward or
        backward is pressed. This method should be called inside a CallbackQueryHandler.
        :param query: callback_query, as provided by the CallbackQueryHandler
        :param data: callback_data, dictionary, set by calendar_callback
        :return: Returns a tuple (Boolean,datetime), indicating if a date is selected
                    and returning the date if so.
        """
        return_data = (False, None)

        # processing empty buttons, answering with no action
        if data.act == "IGNORE":
            await query.answer(cache_time=60)
            return return_data

        temp_date = datetime(int(data.year), int(data.month), 1)

        # user picked a day button, return date
        if data.act == "DAY":
            await query.message.delete_reply_markup()   # removing inline keyboard
            return_data = True, datetime(int(data.year), int(data.month), int(data.day))
        # user navigates to previous year, editing message with new calendar
        if data.act == "PREV-YEAR":
            prev_date = datetime(int(data.year) - 1, int(data.month), 1)
            await self._update_calendar(query, prev_date)
        # user navigates to next year, editing message with new calendar
        if data.act == "NEXT-YEAR":
            next_date = datetime(int(data.year) + 1, int(data.month), 1)
            await self._update_calendar(query, next_date)
        # user navigates to previous month, editing message with new calendar
        if data.act == "PREV-MONTH":
            prev_date = temp_date - timedelta(days=1)
            await self._update_calendar(query, prev_date)
        # user navigates to next month, editing message with new calendar
        if data.act == "NEXT-MONTH":
            next_date = temp_date + timedelta(days=31)
            await self._update_calendar(query, next_date)
        if data.act == "TODAY":
            next_date = datetime.now()
            if next_date.year != int(data.year) or next_date.month != int(data.month):
                await self._update_calendar(query, datetime.now())
            else:
                await query.answer(cache_time=60)
        if data.act == "CANCEL":
            await query.message.delete_reply_markup()
        # at some point user clicks DAY button, returning date
        return return_data
