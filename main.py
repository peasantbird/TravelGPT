# import os
import telebot
from datetime import datetime, timedelta
from FlightSearcher import FlightSearcher

flightSearcher = FlightSearcher()

# BOT_TOKEN = os.environ.get('BOT_TOKEN')
BOT_TOKEN = "YOUR TOKEN"
bot = telebot.TeleBot(BOT_TOKEN)

# Origin City
ORIGIN_CITY = "SIN"

fromTime = datetime.now()
toTime = fromTime + timedelta(days=7)
# testData = flightSearcher.check_flights(ORIGIN_CITY, "LON", fromTime, toTime)

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    prompt = bot.send_message(message.chat.id, "Howdy, where would you like to travel to?")
    bot.register_next_step_handler(prompt, search_flight)  # Next message will call the function
def search_flight(message):
    destCountry = message.text
    result = flightSearcher.check_flights(ORIGIN_CITY, destCountry, fromTime, toTime)
    reply = f"Here are the results: " \
              f"Price: ${result.price}\n" \
              f"Departure date: {result.out_date}\n" \
              f"Return date: {result.return_date}"
    bot.reply_to(message, reply)

@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, message.text)

bot.polling()







