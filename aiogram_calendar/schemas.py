from typing import Optional
from enum import Enum

from aiogram.filters.callback_data import CallbackData


class SimpleCalAct(str, Enum):
    ignore = 'IGNORE'
    prev_y = 'PREV-YEAR'
    next_y = 'NEXT-YEAR'
    prev_m = 'PREV-MONTH'
    next_m = 'NEXT-MONTH'
    cancel = 'CANCEL'
    today = 'TODAY'
    day = 'DAY'


class DialogCalAct(str, Enum):
    ignore = 'IGNORE'
    set_y = 'SET-YEAR'
    set_m = 'SET-MONTH'
    prev_y = 'PREV-YEAR'
    next_y = 'NEXT-YEAR'
    cancel = 'CANCEL'
    start = 'START'
    day = 'SET-DAY'


class CalendarCallback(CallbackData, prefix="calendar"):
    act: str
    year: Optional[int] = None
    month: Optional[int] = None
    day: Optional[int] = None


class SimpleCalendarCallback(CalendarCallback, prefix="simple_calendar"):
    act: SimpleCalAct


class DialogCalendarCallback(CalendarCallback, prefix="dialog_calendar"):
    act: DialogCalAct
