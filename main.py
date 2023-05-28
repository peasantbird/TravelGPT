# import os
import telebot
from datetime import datetime, timedelta
from FlightSearcher import FlightSearcher

flightSearcher = FlightSearcher()

# BOT_TOKEN = os.environ.get('BOT_TOKEN')
BOT_TOKEN = "YOUR TOKEN"
bot = telebot.TeleBot(BOT_TOKEN)

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


bot.polling()







