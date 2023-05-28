import os
import openai
import telebot
from datetime import datetime, timedelta
from FlightSearcher import FlightSearcher

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN = os.environ.get('BOT_TOKEN')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

bot = telebot.TeleBot(BOT_TOKEN)
openai.api_key = OPENAI_API_KEY

flightSearcher = FlightSearcher()

# Origin City and year
ORIGIN_CITY = "SIN"
YEAR = datetime.now().year

# fromTime = datetime.now()
# toTime = fromTime + timedelta(days=7)
# testData = flightSearcher.check_flights(ORIGIN_CITY, "LON", fromTime, toTime)

@bot.message_handler(commands=['start', 'search'])
def get_dest_city(message):
    prompt = bot.send_message(
        message.chat.id,
        "Howdy, which city would you like to travel to?\n"
        "(Please provide the city's airport IATA Code, eg LON for London airport)")
    bot.register_next_step_handler(prompt, get_dates)  # User response will call the next function

def get_dates(message):
    dest_city = message.text
    prompt = bot.send_message(
        message.chat.id,
        "When is your duration of travel? (Please provide input in the following format:\n"
        "'dd/mm to dd/mm', eg 03/11 to 10/11 which represents 3rd Nov to 10th Nov)"
    )
    bot.register_next_step_handler(prompt, search_flight, dest_city)

def search_flight(message, dest_city):
    duration = ''.join(c for c in message.text if c.isdigit())
    from_time = datetime(YEAR, int(duration[2:4]), int(duration[0:2]))
    to_time = datetime(YEAR, int(duration[6:8]), int(duration[4:6]))
    flight = flightSearcher.check_flights(ORIGIN_CITY, dest_city, from_time, to_time)
    flight_string = f"Price: S${flight.price}\n" \
                          f"Departure date: {flight.out_date}\n" \
                          f"Return date: {flight.return_date}"
    reply = f"Here are the closest available flight(s) to {dest_city}:\n" \
            f"{flight_string}\n\n" \
            f"To search another duration to {dest_city},\n" \
            f"reply in the format 'dd/mm - dd/mm',\n" \
            f"else reply 'end' to terminate the current session."
    prompt = bot.send_message(message.chat.id, reply)
    bot.register_next_step_handler(prompt, search_again, dest_city)

def search_again(message, dest_city):
    if (len(message.text) < 8):
        bot.reply_to(message, "Thank you for using this service, goodbye!")
        return;
    search_flight(message, dest_city)

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
    bot.register_next_step_handler(sent_msg, fetch_flight, origin, destination, date_from)

def fetch_flight(message, origin, destination, date_from):
    date_to = message.text
    flight = FlightSearch.get_flight_data(origin, destination, date_from, date_to)
    flight_message = f'*Flight: {flight.price}*'
    bot.send_message(message.chat.id, flight_message, parse_mode="Markdown")

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
