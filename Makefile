example:
	python example_bot.py

# to run exact test use:
# make tests m=aiogram_calendar/tests/test_dialog_calendar.py
tests:
	pytest $m --capture=tee-sys

dev:
	pip install -r requirements_dev.txt

undev:
	pip uninstall -y -r requirements_dev.txt

.PHONY: build publish

build:
	python -m build

publish:
	python -m twine upload dist/*
