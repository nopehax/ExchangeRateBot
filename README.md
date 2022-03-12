# ExchangeRateBot
A telegram bot that gives you the exchange rate of 2 given currencies

usage: /x FROM TO e.g. /x HKD CAD \
try it at <https://t.me/twconvert_bot>

Was using the python-telegram-bot library initially, however it'll always have a ConnectionError if the bot is inactive for a while, so I decided to try using HTTPS requests
