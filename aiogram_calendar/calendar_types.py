from enum import IntEnum

from aiogram.filters.callback_data import CallbackData


# setting callback_data prefix and parts


class DialogCalendarAction(IntEnum):
    IGNORE = 0
    SET_YEAR = 1
    PREV_YEAR = 2
    NEXT_YEAR = 3
    START = 4
    SET_MONTH = 5
    SET_DAY = 6


class SimpleCalendarAction(IntEnum):
    IGNORE = 0
    SET_YEAR = 1
    PREV_YEAR = 2
    NEXT_YEAR = 3
    DAY = 4
    PREV_MONTH = 5
    NEXT_MONTH = 6


class DialogCalendarCallback(CallbackData, prefix='dialog_calendar'):
    act: DialogCalendarAction
    year: int
    month: int
    day: int


class SimpleCalendarCallback(CallbackData, prefix='simple_calendar'):
    act: DialogCalendarAction
    year: int
    month: int
    day: int
