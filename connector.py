import requests
import time 

import requests
url_error = 'http://194.58.92.160:8000/api/error/'
import json


def catch_error(func):
    def wrapper(*args, **kwargs):
        try:
            res = func(*args, **kwargs)
            return res
        except Exception as e:
            data = {
                'error_class': str(type(e)),
                'target': func.__name__,
                'text': str(e),
            }
            r = requests.post(url_error, json=data)
            pass
    return wrapper


URL_DJANGO = 'http://194.58.92.160:8000/'
URL_FLASK = 'http://127.0.0.1:5000/'


@catch_error
def connector():
    while True:
        try:
            req_django = requests.get(URL_DJANGO + 'api/tasks').json()
            for i in req_django:
                req_check_adv = requests.post(URL_FLASK + 'check_adverts', json=i['user'])
                req_chech_trades = requests.post(URL_FLASK + 'check_trades', json=i['user'])
        except Exception as e:
            print(e)
            pass
        time.sleep(15)
