import calendar
import locale

from aiogram.types import User
from datetime import datetime

from .schemas import CalendarLabels, superscript


async def get_user_locale(from_user: User) -> str:
    "Returns user locale in format en_US, accepts User instance from Message, CallbackData etc"
    loc = from_user.language_code
    return locale.locale_alias[loc].split(".")[0]


class GenericCalendar:

    def __init__(self, locale: str = None, cancel_btn: str = None, today_btn: str = None) -> None:
        "Pass labels if you need to have alternative language of buttons"
        self._labels = CalendarLabels()
        if locale:
            # getting month names and days of week in specified locale
            with calendar.different_locale(locale):
                self._labels.days_of_week = list(calendar.day_abbr)
                self._labels.months = calendar.month_abbr[1:]

        if cancel_btn:
            self._labels.cancel_caption = cancel_btn
        if today_btn:
            self._labels.today_caption = today_btn

        self.min_date = None
        self.max_date = None

    def set_dates_range(self, min_date: datetime, max_date: datetime):
        self.min_date = min_date
        self.max_date = max_date
