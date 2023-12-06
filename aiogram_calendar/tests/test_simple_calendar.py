import calendar
from datetime import datetime
from unittest.mock import AsyncMock

import pytest

from aiogram_calendar import SimpleCalendar
from aiogram_calendar.schemas import SimpleCalendarCallback
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def test_init():
    assert SimpleCalendar()


# checking that overall structure of returned object is correct
@pytest.mark.asyncio
async def test_start_calendar():
    result = await SimpleCalendar().start_calendar()

    assert isinstance(result, InlineKeyboardMarkup)
    assert result.row_width == 7
    assert result.inline_keyboard
    kb = result.inline_keyboard
    assert isinstance(kb, list)

    for i in range(0, len(kb)):
        assert isinstance(kb[i], list)

    assert isinstance(kb[0][1], InlineKeyboardButton)
    now = datetime.now()
    # also testing here that year will be highlighted with []
    assert kb[0][1].text == f'[{str(now.year)}]'
    assert isinstance(kb[0][1].callback_data, str)


@pytest.mark.asyncio
async def test_start_calendar_locale():
    result = await SimpleCalendar(locale='uk_UA').start_calendar()
    assert result.inline_keyboard[2][0].text == 'Пн'
    assert result.inline_keyboard[2][6].text == 'Нд'

    result = await SimpleCalendar(locale='ru_Ru').start_calendar()
    assert result.inline_keyboard[2][0].text == 'Пн'
    assert result.inline_keyboard[2][6].text == 'Вс'


# checking if we can pass different years & months as start periods
testset = [
    (2022, 2, '2022', 'Feb'),
    (2022, None, '2022', f'{calendar.month_name[datetime.now().month][:3]}'),
    # also testing here that year will be highlighted with []
    (None, 5, f'[{datetime.now().year}]', 'May'),
]


@pytest.mark.asyncio
@pytest.mark.parametrize("year, month, expected, expected_2", testset)
async def test_start_calendar_params(year, month, expected, expected_2):
    if year and month:
        result = await SimpleCalendar().start_calendar(year=year, month=month)
    elif year:
        result = await SimpleCalendar().start_calendar(year=year)
    elif month:
        result = await SimpleCalendar().start_calendar(month=month)
    kb = result.inline_keyboard
    assert kb[0][1].text == expected
    assert kb[1][1].text == expected_2

now = datetime.now()
testset = [
    (SimpleCalendarCallback(**{'act': 'IGNORE', 'year': 2022, 'month': 8, 'day': 0}), (False, None)),
    (SimpleCalendarCallback(**{'act': 'DAY', 'year': '2022', 'month': '8', 'day': '1'}), (True, datetime(2022, 8, 1))),
    (
        SimpleCalendarCallback(**{'act': 'DAY', 'year': '2021', 'month': '7', 'day': '16'}),
        (True, datetime(2021, 7, 16))
    ),
    (
        SimpleCalendarCallback(**{'act': 'DAY', 'year': '1900', 'month': '10', 'day': '8'}),
        (True, datetime(1900, 10, 8))
    ),
    (SimpleCalendarCallback(**{'act': 'PREV-YEAR', 'year': '2022', 'month': '8', 'day': '1'}), (False, None)),
    (SimpleCalendarCallback(**{'act': 'PREV-MONTH', 'year': '2021', 'month': '8', 'day': '0'}), (False, None)),
    (SimpleCalendarCallback(**{'act': 'NEXT-YEAR', 'year': '2022', 'month': '8', 'day': '1'}), (False, None)),
    (SimpleCalendarCallback(**{'act': 'NEXT-MONTH', 'year': '2021', 'month': '8', 'day': '0'}), (False, None)),
    (SimpleCalendarCallback(**{'act': 'CANCEL', 'year': '2021', 'month': '8', 'day': '0'}), (False, None)),
    (SimpleCalendarCallback(**{'act': 'TODAY', 'year': '2021', 'month': '8', 'day': '1'}), (False, None)),
]


@pytest.mark.asyncio
@pytest.mark.parametrize("callback_data, expected", testset)
async def test_process_selection(callback_data, expected):
    query = AsyncMock()
    result = await SimpleCalendar().process_selection(query=query, data=callback_data)
    assert result == expected
