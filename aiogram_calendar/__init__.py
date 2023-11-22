# flake8: noqa
import locale

from aiogram.types import Message

from aiogram_calendar.simple_calendar import SimpleCalendar
from aiogram_calendar.dialog_calendar import DialogCalendar
from aiogram_calendar.schemas import SimpleCalendarCallback, DialogCalendarCallback, CalendarLabels


async def get_locale_from_user(from_user: Message):
    loc = from_user.language_code
    return locale.locale_alias[loc].split(".")[0]
