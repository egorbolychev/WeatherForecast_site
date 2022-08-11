import pandas as pd
from transliterate import translit

import sqlite3

conn = sqlite3.connect("../weather/db.sqlite3")  # или :memory: чтобы сохранить в RAM
cursor = conn.cursor()

type_dict = {
    'Респ': 'Республика',
    'край': 'Край',
    'обл': 'Область',
    'Аобл': 'Автономная область',
    'г': 'Город',
    'АО': 'Автономный округ',
    'Чувашия': 'Республика'
}

city_table = pd.read_csv('cities.csv')
k = 0
for i, row in city_table.iterrows():
    reg_name = row['Регион']
    reg_type = type_dict[row['Тип региона']]
    reg_slug = str(translit(str(reg_name), language_code='ru', reversed=True))\
        .strip().replace(' ', '').replace('/', '').replace('-', '').replace('\'', '')
    city_name = row['Город']
    city_slug = translit(str(city_name), language_code='ru', reversed=True)\
        .strip().replace(' ', '').replace('/', '').replace('-', '').replace('\'', '')
    lat = row['Широта']
    lon = row['Долгота']

    cursor.execute(f"""SELECT EXISTS(SELECT cityName FROM weatherforecast_citiesmodel WHERE cityName = '{city_name}')""")
    x = cursor.fetchall()
    if int(x[0][0]) == 0:
        k += 1
        print(k)
    cursor.execute(f"""INSERT OR IGNORE INTO weatherforecast_citiesmodel
                        VALUES ({k}, '{city_name}', '{city_slug}', '{lat}', '{lon}',
                        (
                        SELECT id FROM weatherforecast_regionsmodel WHERE regName = '{reg_name}'
                        ))""")
conn.commit()

