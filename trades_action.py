from audioop import avg
import datetime
from locale import currency
import time
import random

import requests
from jose import jws
from jose.constants import ALGORITHMS

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
            raise e
    return wrapper



proxies = {
    'https': 'http://CMg6mg:fHoqJx@185.168.248.24:8000'
}

@catch_error
def authorization(key, email_bz):
    dt = datetime.datetime.now()
    ts = time.mktime(dt.timetuple())
    claims = {
        "email": email_bz,
        "aud": "usr",
        "iat": int(ts),
        "jti": hex(random.getrandbits(64))
    }
    token = jws.sign(claims, key, headers={"kid": "1"}, algorithm=ALGORITHMS.ES256)
    # print ({'Authorization': "Bearer " + token})
    return {'Authorization': "Bearer " + token}

@catch_error
def get_all_trades(key, email):
    headers = authorization(key, email)
    url = 'https://bitzlato.com/api/p2p/trade/'
    r = requests.get(url, headers=headers, proxies=proxies)
    if (r.status_code == 200):
        return r.json()['data']
        # return r.json()
    else:
        return []

@catch_error
def synchron(trade_id, key, email, proxy):

    url = f'https://bitzlato.bz/api/p2p/trade/{trade_id}'
    url_db = 'http://194.58.92.160:8000/api/update/trade/'

    headers = authorization(key, email)
    
    get_trade = requests.get(url, headers=headers, proxies=proxy)

    # print(get_trade.text)

    if (get_trade.status_code == 200):
        changes_db = {
            'id': trade_id,
            'status' : get_trade.json()['status']
        }
        r_db = requests.post(url_db, json=changes_db)
    else:
        print ('[ERROR] 179 line')

    


@catch_error
def check_trades(key, bz_id, email, proxy):
    # print(proxy)
    for adv in get_all_trades(key, email):
        header = authorization(key=key, email_bz=email)
        id = adv['id']
        adv_info = requests.get(f'https://bitzlato.bz/api/p2p/trade/{id}', headers=header, proxies=proxy).json()
        cryptocurrency = adv['cryptocurrency']['code']
        cryptocurrency_amount = adv['cryptocurrency']['amount']
        currency = adv['currency']['code']
        currency_amount = adv['currency']['amount']
        paymethod = adv['paymethod']
        details = adv_info['details']
        counterDetails = adv_info['counterDetails']
        status = adv_info['status']
        partner = adv_info['partner']
        exists_trades = requests.get('http://194.58.92.160:8000/api/get/trades/').json()
        if not str(id) in exists_trades:
            data = {
                'id' : id,
                'bzuser_id': bz_id,
                'cryptocurrency' :  cryptocurrency,
                'cryptocurrency_amount' : cryptocurrency_amount,
                'currency':currency,
                'currency_amount': currency_amount,
                'paymethod':paymethod,
                'details': str(details),
                'counterDetails' : str(counterDetails),
                'status':status,
                'partner' : partner
            }
            add_trade = requests.post('http://194.58.92.160:8000/api/create/trade/', json=data)
            # print(add_trade.status_code)
        synchron(email=email, key=key, trade_id=id, proxy=proxy)