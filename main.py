import os
import telebot
import requests
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Welcome! Use /info to get country info.")

@bot.message_handler(commands=['info'])
def get_country_info(message):
    chat_id = message.chat.id
    try:
        country_name = message.text.split()[1]
        response = get_country_info_api(country_name)
        bot.send_message(chat_id, response)
    except KeyError:
        bot.reply_to(message, "Incorrect data! Use /info to get country info.")

def get_country_info_api(name):
    url = f"https://restcountries.com/v3.1/name/{name}"
    response = requests.get(url)
    data = response.json()
    return f"Country: {data[0]['name']['common']}\nCapital: {data[0]['capital'][0]}\nPopulation: {data[0]['population']}"

def main():
    bot.polling(none_stop=True, interval=0)

if __name__ == '__main__':
    main()
