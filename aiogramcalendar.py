from aiogram import types
from datetime import datetime, timedelta
import calendar


def create_callback_data(action,year,month,day):
    """ Create the callback data associated to each button"""
    return ";".join([action,str(year),str(month),str(day)])


def separate_callback_data(data):
    """ Separate the callback data"""
    return data.split(";")


def create_calendar(year=datetime.now().year, month=datetime.now().month):
    """
    Creates an inline keyboard with the provided year and month
    :param int year: Year to use in the calendar, if None the current year is used.
    :param int month: Month to use in the calendar, if None the current month is used.
    :return: Returns InlineKeyboardMarkup object with the calendar.
    """
    inline_kb = types.InlineKeyboardMarkup(row_width=7)
    data_ignore = create_callback_data("IGNORE", year, month, 0)
    #First row - Month and Year
    inline_kb.row(types.InlineKeyboardButton(f'{calendar.month_name[month]} {str(year)}', callback_data=data_ignore))
    #Second row - Week Days
    inline_kb.row()
    for day in ["Mo","Tu","We","Th","Fr","Sa","Su"]:
        inline_kb.insert(types.InlineKeyboardButton(day, callback_data=data_ignore))
    
    #Calendar rows - Days of month
    month_calendar = calendar.monthcalendar(year, month)
    for week in month_calendar:
        inline_kb.row()
        for day in week:
            if(day==0):
                inline_kb.insert(types.InlineKeyboardButton(" ",callback_data=data_ignore))
            else:
                inline_kb.insert(types.InlineKeyboardButton(str(day),callback_data=create_callback_data("DAY",year,month,day)))

    #Last row - Buttons
    inline_kb.row()
    inline_kb.insert(types.InlineKeyboardButton("<",callback_data=create_callback_data("PREV-MONTH",year,month,day)))
    inline_kb.insert(types.InlineKeyboardButton(" ",callback_data=data_ignore))
    inline_kb.insert(types.InlineKeyboardButton(">",callback_data=create_callback_data("NEXT-MONTH",year,month,day)))

    return inline_kb


async def process_calendar_selection(bot, query):
    """
    Process the callback_query. This method generates a new calendar if forward or
    backward is pressed. This method should be called inside a CallbackQueryHandler.
    :param aiogram.Bot bot: The bot, as provided by the CallbackQueryHandler
    :param callback_query query: callback_query, as provided by the CallbackQueryHandler
    :return: Returns a tuple (Boolean,datetime), indicating if a date is selected
                and returning the date if so.
    """
    return_data = (False,None)
    (action,year,month,day) = separate_callback_data(query.data)
    temp_date = datetime(int(year), int(month), 1)
    # processing empty buttons, answering with no action
    if action == "IGNORE":
        await bot.answer_callback_query(callback_query_id=query.id)  
    # user picked a day button, return date    
    elif action == "DAY":
        await bot.edit_message_text(text=query.message.text,
            chat_id=query.message.chat.id,
            message_id=query.message.message_id
            )
        return_data = True,datetime(int(year),int(month),int(day))
    # user navigates to previous month, editing message with new calendar
    elif action == "PREV-MONTH":
        prev_date = temp_date - timedelta(days=1)
        await bot.edit_message_text(text=query.message.text,
            chat_id=query.message.chat.id,
            message_id=query.message.message_id,
            reply_markup=create_calendar(int(prev_date.year),int(prev_date.month)))
    # user navigates to next month, editing message with new calendar
    elif action == "NEXT-MONTH":
        next_date = temp_date + timedelta(days=31)
        await bot.edit_message_text(text=query.message.text,
            chat_id=query.message.chat.id,
            message_id=query.message.message_id,
            reply_markup=create_calendar(int(next_date.year),int(next_date.month)))
    else:
        await bot.answer_callback_query(callback_query_id=query.id, text="Something went wrong!")
    
    #at some point user clicks DAY button, returning date
    return return_data