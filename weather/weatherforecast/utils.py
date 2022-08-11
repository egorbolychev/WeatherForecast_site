import datetime
import locale

import requests
from django.shortcuts import get_object_or_404
from .models import *

weather_background_dict = {
    '2': '../../../static/weatherforecast/images/гроза.jpeg',
    '3': '../../../static/weatherforecast/images/моросить.jpg',
    '5': '../../../static/weatherforecast/images/дождь.jpg',
    '6': '../../../static/weatherforecast/images/снег.jpg',
    '7': '../../../static/weatherforecast/images/туман.jpg',
    '800': '../../../static/weatherforecast/images/ясная_погода.jpg',
    '8': '../../../static/weatherforecast/images/пасмурно.jpg',
}


class WeatherMixin:
    def current_weather(self, city):
        url = 'https://api.openweathermap.org/data/2.5/weather'
        params = {
            'appid': 'f343b053f04b7509fab23b2fcb4bfeb3',
            'lang': 'ru',
            'units': 'metric',
            'lat': f'{city.lat}',
            'lon': f'{city.lon}',
        }

        response = requests.get(url, params=params).json()

        # Температура
        if int(response['main']['temp']) >= 0:
            temp = '+ ' + str(round(int(response['main']['temp']), 1))
        else:
            temp = str(int(response['main']['temp']))

        # Ветер
        wind_direction = ("С", "С-В", "В", "Ю-В", "Ю", "Ю-З", "З", "С-З")
        direction = int((int(response['wind']['deg']) + 22.5) // 45 % 8)

        # Время заката/восхода
        sunrise = datetime.datetime.utcfromtimestamp(int(response['sys']['sunrise'])
                                                     + int(response['timezone']))
        sunset = datetime.datetime.utcfromtimestamp(int(response['sys']['sunset'])
                                                    + int(response['timezone']))
        current_time = datetime.datetime.now()
        sun_level = str(-100 + (current_time - sunrise) / (sunset - sunrise) * 195)

        # заставка

        if str(response['weather'][0]['id']) == '800':
            background = weather_background_dict['800']
        else:
            background = weather_background_dict[str(response['weather'][0]['id'])[0]]

        weather_response_dict = {
            'background': background,
            'date': current_time,
            'temp': temp,
            'sunrise': sunrise.strftime('%H:%M'),
            'sunset': sunset.strftime('%H:%M'),
            'humidity': response['main']['humidity'],
            'pres': int(int(response['main']['pressure']) * 0.75006375541921),
            'wind_speed': response['wind']['speed'],
            'wind_direction': wind_direction[direction],
            'sun_level': sun_level,
            'feels_like': int(response['main']['feels_like']),
            'weather_type': response['weather'][0]['description'].capitalize()
        }
        return weather_response_dict

    def five_by_day_weather(self, city):
        url = 'https://api.openweathermap.org/data/2.5/forecast'
        params = {
            'appid': 'f343b053f04b7509fab23b2fcb4bfeb3',
            'lang': 'ru',
            'units': 'metric',
            'lat': f'{city.lat}',
            'lon': f'{city.lon}',
        }

        response = requests.get(url, params=params).json()

        weather_list = response['list']

        date = datetime.datetime.utcfromtimestamp(int(response['list'][0]['dt']) + int(response['city']['timezone']))
        # Температура
        if int(response['list'][0]['main']['temp']) >= 0:
            temp = '+' + str(round(int(response['list'][0]['main']['temp']), 1))
        else:
            temp = str(response['main']['temp'])

        now = {
            'date': date.date(),
            'temp_day': temp,
            'ico': 'weatherforecast/images/{}.png'.format(str(response['list'][0]['weather'][0]['icon'])),
            'day_num': 0
        }
        new_weather_list = [now]
        num = 1
        for cnt in weather_list:
            new_date = datetime.datetime.utcfromtimestamp(int(cnt['dt']) + int(response['city']['timezone']))

            if new_date.date() > date.date() and str(new_date.time()) == '15:00:00':
                if int(cnt['main']['temp']) >= 0:
                    temp_d = '+' + str(round(int(cnt['main']['temp']), 1))
                else:
                    temp_d = str(response['main']['temp'])
                cur_weather = {
                    'day_num': num,
                    'date': new_date.date(),
                    'temp_day': temp_d,
                    'ico': 'weatherforecast/images/{}.png'.format(str(cnt['weather'][0]['icon']))
                }
                new_weather_list.append(cur_weather)
                num += 1

            if new_date.date() > date.date() and str(new_date.time()) == '00:00:00':
                if int(cnt['main']['temp']) >= 0:
                    temp_n = '+' + str(round(int(cnt['main']['temp']), 1))
                else:
                    temp_n = str(response['main']['temp'])
                new_weather_list[-1].update({'temp_night': temp_n})

        if len(new_weather_list) > 5:
            new_weather_list.pop(-1)

        return new_weather_list

    def five_by_hour_weather(self, city):
        url = 'https://api.openweathermap.org/data/2.5/forecast'
        params = {
            'appid': 'f343b053f04b7509fab23b2fcb4bfeb3',
            'lang': 'ru',
            'units': 'metric',
            'lat': f'{city.lat}',
            'lon': f'{city.lon}',
        }

        response = requests.get(url, params=params).json()

        weather_list = response['list']
        date = datetime.datetime.utcfromtimestamp(int(response['list'][0]['dt']) + int(response['city']['timezone']))
        new_weather_list = [list()]
        for cnt in weather_list:
            timedate = datetime.datetime.utcfromtimestamp(int(cnt['dt']) + int(response['city']['timezone']))
            if int(cnt['main']['temp']) >= 0:
                temp = '+' + str(round(int(cnt['main']['temp']), 1))
            else:
                temp = str(response['main']['temp'])
            cnt_weather_dict = {
                'time': timedate.time(),
                'date': timedate.date(),
                'humidity': cnt['main']['humidity'],
                'ico': 'weatherforecast/images/{}.png'.format(str(cnt['weather'][0]['icon'])),
                'temp': temp,
                'wind': round(float(cnt['wind']['speed']), 1),
            }
            new_weather_list[-1].append(cnt_weather_dict)
            if timedate.date() > date.date():
                new_weather_list.append(list())
            date = timedate

        return new_weather_list
