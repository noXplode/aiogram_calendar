from datetime import datetime
from unittest.mock import AsyncMock

import pytest

from aiogram_calendar import DialogCalendar
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def test_init():
    dialog = DialogCalendar()
    assert dialog
    assert dialog.year == datetime.now().year
    assert dialog.month == datetime.now().month


# checking that overall structure of returned object is correct
@pytest.mark.asyncio
async def test_start_calendar():
    result = await DialogCalendar().start_calendar()

    assert type(result) == InlineKeyboardMarkup
    assert result.row_width == 5

    assert 'inline_keyboard' in result
    kb = result['inline_keyboard']
    assert type(kb) == list

    for i in range(0, len(kb)):
        assert type(kb[i]) == list

    assert type(kb[0][0]) == InlineKeyboardButton
    year = datetime.now().year
    assert kb[0][0]['text'] == year - 2
    assert type(kb[0][0]['callback_data']) == str


# checking if we can pass different years start period to check the range of buttons
testset = [
    (2020, 2018, 2022),
    (None, datetime.now().year - 2, datetime.now().year + 2),
]


@pytest.mark.asyncio
@pytest.mark.parametrize("year, expected1, expected2", testset)
async def test_start_calendar_params(year, expected1, expected2):
    if year:
        result = await DialogCalendar().start_calendar(year=year)
    else:
        result = await DialogCalendar().start_calendar()
    kb = result['inline_keyboard']
    assert kb[0][0]['text'] == expected1
    assert kb[0][4]['text'] == expected2


testset = [
    ({'@': 'dialog_calendar', 'act': 'IGNORE', 'year': '2022', 'month': '8', 'day': '0'}, (False, None)),
    (
        {'@': 'dialog_calendar', 'act': 'SET-DAY', 'year': '2022', 'month': '8', 'day': '1'},
        (True, datetime(2022, 8, 1))
    ),
    (
        {'@': 'dialog_calendar', 'act': 'SET-DAY', 'year': '2021', 'month': '7', 'day': '16'},
        (True, datetime(2021, 7, 16))
    ),
    (
        {'@': 'dialog_calendar', 'act': 'SET-DAY', 'year': '1900', 'month': '10', 'day': '8'},
        (True, datetime(1900, 10, 8))
    ),
    ({'@': 'dialog_calendar', 'act': 'PREV-YEARS', 'year': '2022', 'month': '8', 'day': '1'}, (False, None)),
    ({'@': 'dialog_calendar', 'act': 'NEXT-YEARS', 'year': '2021', 'month': '8', 'day': '0'}, (False, None)),
    ({'@': 'dialog_calendar', 'act': 'SET-MONTH', 'year': '2022', 'month': '8', 'day': '1'}, (False, None)),
    ({'@': 'dialog_calendar', 'act': 'SET-YEAR', 'year': '2021', 'month': '8', 'day': '0'}, (False, None)),
    ({'@': 'dialog_calendar', 'act': 'START', 'year': '2021', 'month': '8', 'day': '0'}, (False, None)),
]


@pytest.mark.asyncio
@pytest.mark.parametrize("callback_data, expected", testset)
async def test_process_selection(callback_data, expected):
    query = AsyncMock()
    result = await DialogCalendar().process_selection(query=query, data=callback_data)
    assert result == expected
