from distutils.core import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
  name='aiogram3_calendar',
  packages=['aiogram3_calendar'],
  version='0.1.2b',
  license='MIT',
  description='Simple Inline Calendar & Date Selection tool for Aiogram (version 3.0.0a12 and upper) Telegram bots',
  long_description=long_description,
  author='Andrew Nikolabay, Dmytro Yaroshenko',
  author_email='',
  url='https://github.com/o-murphy/aiogram3_calendar',
  keywords=['Aiogram', 'Aiogram3' 'Telegram', 'Bots', 'Calendar'],
  install_requires=[
          'aiogram~=3.0.0b6',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)
