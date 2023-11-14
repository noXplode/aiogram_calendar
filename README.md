# Date Selection tool for Aiogram Telegram Bots

## Description
A simple inline calendar, date selection tool for [aiogram](https://github.com/aiogram/aiogram) telegram bots written in Python.
Offers two types of date pickers:
Navigation calendar - user can either select a date or move to the next or previous month/year by clicking a singe button.
Dialog calendar - user selects year on first stage, month on next stage, day on last stage.

From version 0.2 supports aiogram 3, use version 0.1.1 with aiogram 2.

## Usage
Install package

        pip install aiogram_calendar

A full working example on how to use aiogram-calendar is provided in *bot_example.py*. 
You create a calendar and add it to a message with a *reply_markup* parameter and then you can process it in a callbackqueyhandler method using the *process_selection* method.

## Gif demo:

![aiogram_calendar](https://j.gifs.com/nRQlqW.gif)
