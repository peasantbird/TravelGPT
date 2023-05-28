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

openai.api_key = ""

@bot.message_handler(commands=['itinerary'])
def country_handler(message):
    text = "Where are you planning to go?"
    sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
    bot.register_next_step_handler(sent_msg, fetch_itinerary)

def fetch_itinerary(message):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Can you plan a day-to-day detailed itinerary for a trip to {message.text}",
        temperature=0.5,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=["\n"]
    )
    message.reply(response.choices[0].text)


bot.polling()







