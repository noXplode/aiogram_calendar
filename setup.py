from distutils.core import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
  name='aiogram_calendar',
  packages=['aiogram_calendar'],
  version='0.1.1',
  license='MIT',
  description='Simple Inline Calendar & Date Selection tool for Aiogram Telegram bots',
  long_description=long_description,
  author='Andrew Nikolabay',
  author_email='',
  url='https://github.com/noXplode/aiogram_calendar',
  download_url='https://github.com/noXplode/aiogram_calendar/archive/refs/tags/0.1.1.tar.gz',
  keywords=['Aiogram', 'Telegram', 'Bots', 'Calendar'],
  install_requires=[
          'aiogram',
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
