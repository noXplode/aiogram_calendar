# Date Selection tool for Aiogram Telegram Bots

## Description
A simple inline calendar, date selection tool for [aiogram](https://github.com/aiogram/aiogram) telegram bots written in Python. 
Initially based on [calendar-telegram](https://github.com/unmonoqueteclea/calendar-telegram).
The user can either select a date or move to the next or previous month/year by clicking a singe button.
Package provides the user with two methods:
* **create_calendar**: This method returns a InlineKeyboardMarkup object with the calendar in the provided year and month.
* **process_calendar_selection:** This method can be used inside a CallbackQueryHandler method to check if the user has selected a date or wants to move to a different month. It also creates a new calendar with the same text if necessary.

## Usage
Install package

        pip install aiogram_calendar

A full working example on how to use aiogram-calendar is provided in *bot_example.py*. 
You create a calendar and add it to a message with a *reply_markup* parameter and then you can process it in a callbackqueyhandler method using the *process_calendar_selection* method.