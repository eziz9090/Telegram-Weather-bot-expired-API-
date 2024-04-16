import telebot

import requests
from telebot import types
from env import API_KEY




GIS_API = "7188650ece6e4df0b23212605241504"

def get_weather_forecast(location):
    url = f'http://api.weatherapi.com/v1/current.json?key={GIS_API}&q={location}&aqi=no'
    headers = {
        'X-Gismeteo-Token': GIS_API
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None

bot = telebot.TeleBot(API_KEY, parse_mode=None)

@bot.message_handler(commands=["start"])
def ask_for_location(message):
    bot.send_message(message.chat.id, "Welcome! Please enter your location:")

@bot.message_handler(func=lambda message: True)
def handle_location(message):
    location = message.text
    forecast = get_weather_forecast(location)
    if forecast:
        condition = forecast['current']['condition']['text']
        temperature_c = forecast['current']['temp_c']
        weather_info = f"Weather in {location}:\nCondition: {condition}\nTemperature: {temperature_c}°C"
        bot.send_message(message.chat.id, weather_info)
    else:
        bot.send_message(message.chat.id, "Failed to fetch weather forecast for the provided location")


bot.polling()

