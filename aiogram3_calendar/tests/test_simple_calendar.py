# pylint: disable=duplicate-code
import calendar
from datetime import datetime
from unittest.mock import AsyncMock

import pytest  # pylint: disable=import-error
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from aiogram3_calendar import SimpleCalendar
from aiogram3_calendar.calendar_types import SimpleCalendarAction, SimpleCalendarCallback


def test_init():
    assert SimpleCalendar()


# checking that overall structure of returned object is correct
@pytest.mark.asyncio
async def test_start_calendar():
    result = await SimpleCalendar().start_calendar()

    assert isinstance(result, InlineKeyboardMarkup)
    # assert result.row_width == 7
    assert hasattr(result, 'inline_keyboard')
    kb = result.inline_keyboard
    assert isinstance(kb, list)

    for i in kb:
        assert isinstance(i, list)

    assert isinstance(kb[0][1], InlineKeyboardButton)
    now = datetime.now()
    assert kb[0][1].text == f'{calendar.month_name[now.month]} {str(now.year)}'
    assert isinstance(kb[0][1].callback_data, str)


# checking if we can pass different years & months as start periods
testset = [
    (2022, 2, 'February 2022'),
    (2022, None, f'{calendar.month_name[datetime.now().month]} 2022'),
    (None, 5, f'May {datetime.now().year}'),
]


@pytest.mark.asyncio
@pytest.mark.parametrize("year, month, expected", testset)
async def test_start_calendar_params(year, month, expected):
    result = None
    if year and month:
        result = await SimpleCalendar().start_calendar(year=year, month=month)
    elif year:
        result = await SimpleCalendar().start_calendar(year=year)
    elif month:
        result = await SimpleCalendar().start_calendar(month=month)
    kb = result.inline_keyboard
    assert kb[0][1].text == expected


testset = [
    ({'@': 'simple_calendar', 'act': SimpleCalendarAction.IGNORE,
      'year': '2022', 'month': '8', 'day': '0'}, (False, None)),
    ({'@': 'simple_calendar', 'act': SimpleCalendarAction.DAY,
      'year': '2022', 'month': '8', 'day': '1'}, (True, datetime(2022, 8, 1))),
    ({'@': 'simple_calendar', 'act': SimpleCalendarAction.DAY,
      'year': '2021', 'month': '7', 'day': '16'}, (True, datetime(2021, 7, 16))),
    ({'@': 'simple_calendar', 'act': SimpleCalendarAction.DAY,
      'year': '1900', 'month': '10', 'day': '8'}, (True, datetime(1900, 10, 8))),
    ({'@': 'simple_calendar', 'act': SimpleCalendarAction.PREV_YEAR,
      'year': '2022', 'month': '8', 'day': '1'}, (False, None)),
    ({'@': 'simple_calendar', 'act': SimpleCalendarAction.PREV_MONTH,
      'year': '2021', 'month': '8', 'day': '0'}, (False, None)),
    ({'@': 'simple_calendar', 'act': SimpleCalendarAction.NEXT_YEAR,
      'year': '2022', 'month': '8', 'day': '1'}, (False, None)),
    ({'@': 'simple_calendar', 'act': SimpleCalendarAction.NEXT_MONTH,
      'year': '2021', 'month': '8', 'day': '0'}, (False, None)),
]


@pytest.mark.asyncio
@pytest.mark.parametrize("callback_data, expected", testset)
async def test_process_selection(callback_data, expected):
    query = AsyncMock()
    result = await SimpleCalendar().process_selection(
        query=query, data=SimpleCalendarCallback(**callback_data))
    assert result == expected
