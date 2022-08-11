import requests
import json

url = 'https://api.openweathermap.org/data/2.5/forecast'

params = {
    'appid': 'f343b053f04b7509fab23b2fcb4bfeb3',
    'lang': 'ru',
    'units': 'metric',
    'lat': '34',
    'lon': '118'
}

response = requests.get(url, params=params).json()
print(response['list'])
dict_json = dict(response)
print(json.dumps(dict_json, indent=3, sort_keys=True,  ensure_ascii=False))
with open('data.json', 'w', encoding='utf-8') as data:
    json.dump(dict_json, data, indent=4, sort_keys=True,  ensure_ascii=False)
