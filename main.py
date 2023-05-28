import os
import telebot

# BOT_TOKEN = os.environ.get('BOT_TOKEN')
BOT_TOKEN = "6108579809:AAGWA1jfIwFOrTHuN9ctOVFtzNEr6f8am64"
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, message.text)

bot.polling()


