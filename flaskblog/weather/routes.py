import configparser
import os
import requests
from flask import render_template, Blueprint, request

weather = Blueprint('weather', __name__)
OWM_API = os.environ.get('OWM_API')


@weather.route("/weather")
def weather_dashboard():
    return render_template('weather.html')


@weather.route('/weather-results', methods=['POST'])
def get_results():
    cityname = request.form['cityname']
    api_key = get_api()
    data = what_weather(cityname, api_key)
    temp = "{0:.2f}".format(data["main"]["temp"])
    feels_like = "{0:.2f}".format(data["main"]["feels_like"])
    weather = data["weather"][0]["main"]
    location = data["name"]
    return render_template('weather-results.html', temp=temp, feels_like=feels_like,
                           weather=weather, location=location)


def get_api():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['openweathermap']['api']


def what_weather(cityname, api_key):
    api_url = f"http://api.openweathermap.org/data/2.5/weather?q={cityname}&units=metric&appid={api_key}"
    r = requests.get(api_url)
    return r.json()
