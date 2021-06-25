import configparser
import os
import requests
from flask import render_template, Blueprint, request

weather = Blueprint('weather', __name__)
# OWM_API = os.environ.get('OWM_API')


# asking what city we are looking for
@weather.route("/weather")
def weather_dashboard():
    return render_template('weather.html')


# filtering through the JSON, getting what I need
@weather.route("/weather-results", methods=['POST'])
def get_results():
    cityname = request.form['cityname']
    api_key = get_api()
    data = what_weather(cityname, api_key)
    temp = "{0:.2f}".format(data["main"]["temp"])
    feels_like = "{0:.2f}".format(data["main"]["feels_like"])
    pressure = "{0:.2f}".format(data["main"]["pressure"])
    humidity = "{0:.2f}".format(data["main"]["humidity"])
    weathers = data["weather"][0]["main"]
    location = data["name"]
    lat = data["coord"]["lat"]
    lon = data["coord"]["lon"]
    country = data["sys"]["country"]
    return render_template('weather-results.html', temp=temp, feels_like=feels_like,
                           pressure=pressure, humidity=humidity, weather=weathers,
                           location=location, lat=lat, lon=lon, country=country)


# getting the API key from config.ini
def get_api():
    config = configparser.ConfigParser()
    config.read('flaskblog/weather/config.ini')
    return config['openweathermap']['api']


# getting the JSON information
def what_weather(cityname, api_key):
    api_url = f"http://api.openweathermap.org/data/2.5/weather?q={cityname}&units=metric&appid={api_key}"
    r = requests.get(api_url)
    return r.json()
