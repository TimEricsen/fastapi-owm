import os

from dotenv import load_dotenv

load_dotenv()


def get_parameters():
    parameters = {
        'appid': os.getenv('API'),
        'units': 'metric',
        'lang': 'en'
    }
    return parameters

