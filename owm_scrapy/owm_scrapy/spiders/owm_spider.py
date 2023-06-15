import json
import os

import scrapy
import psycopg2

from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

parameters = {
    'appid': os.getenv('API'),
    'units': 'metric',
    'lang': 'en'
}


class OpenweathermapSpider(scrapy.Spider):
    name = 'openweathermap'
    start_urls = ['https://api.openweathermap.org/data/2.5/weather']

    def start_requests(self):
        db_conn = psycopg2.connect(
            dbname='postgres',
            host='db',
            user='postgres',
            password='postgres'
        )
        cursor = db_conn.cursor()

        try:
            cursor.execute(
            'SELECT city FROM openweather_city'
            )
            cities = cursor.fetchall()

            for city in cities:
                parameters['q'] = city[0]
                yield scrapy.FormRequest(url=self.start_urls[0], method='GET',
                                         formdata=parameters, callback=self.parse)

        except:
            raise Exception

    def parse(self, response, **kwargs):
        data = json.loads(response.body)
        db_conn = psycopg2.connect(
            dbname='postgres',
            host='db',
            user='postgres',
            password='postgres'
        )
        cursor = db_conn.cursor()

        try:
            cursor.execute(f'INSERT INTO '
                           f'openweather_info(temperature, atm_pressure, wind_speed, record_time, city_name)'
                           f'VALUES (%s, %s, %s, %s, %s)',
                           (str(data['main']['temp']), str(data['main']['pressure']),
                            str(data['wind']['speed']), datetime.now(),
                            data['name']))
            db_conn.commit()
        except Exception as exc:
            print(exc)



