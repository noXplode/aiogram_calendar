# Date Selection tool for Aiogram Telegram Bots

## Description
A simple inline calendar, date selection tool for [aiogram](https://github.com/aiogram/aiogram) telegram bots written in Python. 
Based on [calendar-telegram](https://github.com/unmonoqueteclea/calendar-telegram).
The user can either select a date or move to the next or previous month by clicking a singe button.
The file **aiogramcalendar.py** provides the user with two methods:
* **create_calendar**: This method returns a InlineKeyboardMarkup object with the calendar in the provided year and month.
* **process_calendar_selection:** This method can be used inside a CallbackQueryHandler method to check if the user has selected a date or wants to move to a different month. It also creates a new calendar with the same text if necessary.

## Usage
To use the aiogram_calendar you need to install [aiogram](https://github.com/aiogram/aiogram) first. Then add **aiogramcalendar.py** to your project.
A full working example on how to use aiogram_calendar is provided in *bot_example.py*. 
You create a calendar and add it to a message with a *reply_markup* parameter and then you can process it in a callbackqueyhandler method using the *process_calendar_selection* method.
