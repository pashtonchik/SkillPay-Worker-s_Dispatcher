import requests
import time 




import requests
from log import logger
from server import URL_DJANGO

URL_FLASK = 'http://127.0.0.1:5001/'
url_error = URL_DJANGO + 'api/error/'


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


@catch_error
@logger.catch
def connector():
    while True:
        try:
            req_django = requests.get(URL_DJANGO + 'tasks/').json()
            for i in req_django:
                if i['type'] == 'bz':
                    req_check_adv = requests.post(URL_FLASK + 'check_bz_adverts', json=i['user'])
                    req_chech_trades = requests.post(URL_FLASK + 'check_bz_trades', json=i['user'])
                if i['type'] == 'gar':
                    print('gar')
                    req_check__gar_adv = requests.post(URL_FLASK + 'check_garantex_adverts', json=i['user'])
                    req_chech_gar_trades = requests.post(URL_FLASK + 'check_garantex_trades', json=i['user'])
        except Exception as e:
            print(e)
            pass
        time.sleep(15)
