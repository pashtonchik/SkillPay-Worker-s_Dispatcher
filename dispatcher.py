import time
import requests

from adverts_action import check_scripts
from gar_adverts_action import update_adverts_garantex
from gar_trades_action import update_trades_garantex
from log import logger
from setting import URL_FLASK, URL_DJANGO
from trades_action import check_trades

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


while True:
    try:
        req_django = requests.get(URL_DJANGO + 'tasks/').json()
        for i in req_django:
            if i['type'] == 'bz':
                id = i['user']['id']
                key = i['user']['key']
                email = i['user']['email']
                proxy = i['user']['proxy']
                # req_check_adv = requests.post(URL_FLASK + 'check_bz_adverts', json=i['user'])
                # req_chech_trades = requests.post(URL_FLASK + 'check_bz_trades', json=i['user'])
                check_trades(key, id, email, proxy)
                check_scripts(key, id, email, proxy)
            if i['type'] == 'gar':
                user_id = i['user']['id']
                uid = i['user']['uid']
                private_key = i['user']['private_key']
                update_trades_garantex(private_key, uid)
                update_adverts_garantex(private_key, uid, user_id)
                # req_check__gar_adv = requests.post(URL_FLASK + 'check_garantex_adverts', json=i['user'])
                # req_chech_gar_trades = requests.post(URL_FLASK + 'check_garantex_trades', json=i['user'])
    except Exception as e:
        print(e)
        pass
    time.sleep(5)

