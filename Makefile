example:
	python example_bot.py

# to run exact test use:
# make tests m=aiogram_calendar/tests/test_dialog_calendar.py
tests:
	pytest $m --capture=tee-sys