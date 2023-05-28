import os
import telebot

from InfoManager import FlightSearch

# BOT_TOKEN = os.environ.get('BOT_TOKEN') Not working for some reason
BOT_TOKEN = "6273422459:AAEQS63MWd4oQ6VLPGZTMn_aB0IfRKTd12Q"
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(commands=['flight'])
def origin_handler(message):
    text = "Origin:"
    sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
    bot.register_next_step_handler(sent_msg, destination_handler)

def destination_handler(message):
    origin = message.text.capitalize()
    text = "Destination:"
    sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
    bot.register_next_step_handler(sent_msg, date_from_handler, origin)

def date_from_handler(message, origin):
    destination = message.text.capitalize()
    text = "Date from:"
    sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
    bot.register_next_step_handler(sent_msg, date_to_handler, origin, destination)

def date_to_handler(message, origin, destination):
    date_from = message.text
    text = "Date to:"
    sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
    bot.register_next_step_handler(sent_msg, date_to_handler, origin, destination, date_from)

def fetch_flight(message, origin, destination, date_from):
    date_to = message.text
    flight = FlightSearch.get_flight_data(origin, destination, date_from, date_to)
    flight_message = f'*Flight: {flight.price}*'
    bot.send_message(message.chat.id, flight_message, parse_mode="Markdown")

bot.polling()
