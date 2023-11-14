from typing import Optional

from aiogram.filters.callback_data import CallbackData


class CalendarCallback(CallbackData, prefix="calendar"):
    act: str
    year: Optional[int] = None
    month: Optional[int] = None
    day: Optional[int] = None


class SimpleCalendarCallback(CalendarCallback, prefix="simple_calendar"):
    pass


class DialogCalendarCallback(CalendarCallback, prefix="dialog_calendar"):
    pass
