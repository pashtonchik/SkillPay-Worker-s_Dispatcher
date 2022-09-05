import datetime
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
            func(*args, **kwargs)
        except Exception as e:
            data = {
                'error_class': str(type(e)),
                'target': func.__name__,
                'text': str(e),
            }
            r = requests.post(url_error, json=data)
            # raise e
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
    return {'Authorization': "Bearer " + token}


@catch_error
def get_amounts(min_amount, key, email, asset='BTC', fiat='RUB'):
    headers = authorization(key, email)
    url = f'https://bitzlato.bz/api2/p2p/exchange/dsa/?lang=ru&limit=10&skip=0&'\
    f'type=selling&currency={fiat}&cryptocurrency={asset}&' \
    f'isOwnerVerificated=false&isOwnerTrusted=false&isOwnerActive=false&'\
    f'amount={min_amount}&paymethod=443&amountType=currency&paymethodSlug=tinkoff'
    r = requests.get(url, headers=headers, proxies=proxies)

    return r.json()['data']


@catch_error
def parse_average_amount(amounts_info):
    sum_amounts = 0
    for amount in amounts_info:
        sum_amounts += float(amount['rate'])
    return sum_amounts / 10


@catch_error
def get_all_adverts(key, email):
    headers = authorization(key, email)

    url = 'https://bitzlato.com/api/p2p/dsa/all'
    r = requests.get(url, headers=headers, proxies=proxies)

    exists_advert_id = requests.get('http://194.58.92.160:8000/api/adverts/').json()

    for advert in r.json():
        if not str(advert['id']) in exists_advert_id:
            add_advert = {
                'advert_id': advert['id'],
                'amount': float(advert['rateValue']),
                'limit_min': advert['minAmount'],
                'limit_max': advert['maxAmount'],
                'is_active': True if (advert['status'] == 'active') else False,
            }
            r1 = requests.post('http://194.58.92.160:8000/api/create/advert/', json=add_advert)
    return r.json()


@catch_error
def edit_rate_value_advert(advert_id, average_price, key, email):
    
    url = f'https://bitzlato.com/api/p2p/dsa/{advert_id}'
    
    changes = {
        'rateValue': average_price,
    }

    headers = authorization(key, email)
    r = requests.put(url, headers=headers, proxies=proxies, json=changes)
    
    advert = {
        'advert_id' : advert_id
    }

    get_price_garantex = 'http://194.58.92.160:8000/api/get_exchange_garantex/'
    price_garantex = requests.get(get_price_garantex).json()['btc-rub']
    
    headers = authorization(key, email)
    get_adv = requests.get(url, headers=headers, proxies=proxies)

    advert_info = requests.post('http://194.58.92.160:8000/api/get_advert_info/', json=advert)

    if (advert_info.json()['revenue_percentage'] != None):
    
        percent = float(advert_info.json()['revenue_percentage'])
    
        side_percent = ( (float(price_garantex) * 1.002) / (float(get_adv.json()['rateValue']) * 0.995)- 1) * 100
    
        if side_percent < percent:
    
            # print(float(price_garantex) * 1.002, float(get_adv.json()['rateValue']) * 0.995)
    
            stop_advert(advert_id=advert_id, key=key, email=email)
    
        else:
    
            run_advert(advert_id=advert_id, key=key, email=email)

    return r.json()


@catch_error
def stop_advert(advert_id, key, email):
    headers = authorization(key, email)
    url = f'https://bitzlato.com/api/p2p/dsa/{advert_id}'
    
    changes = {
        'status': 'pause',
    }
    r = requests.put(url, headers=headers, proxies=proxies, json=changes)
    return r.json()


@catch_error
def run_advert(advert_id, key, email):
    headers = authorization(key, email)
    url = f'https://bitzlato.com/api/p2p/dsa/{advert_id}'

    changes = {
        'status': 'active',
    }

    r = requests.put(url, headers=headers, proxies=proxies, json=changes)
    return r.json()

@catch_error
def synchron(advert_id, key, email):

    url = f'https://bitzlato.com/api/p2p/dsa/{advert_id}'
    url_db = 'http://194.58.92.160:8000/api/update/advert/'

    headers = authorization(key, email)
    
    get_ads = requests.get(url, headers=headers, proxies=proxies)

    changes_db = {
        'advert_id': advert_id,
        'amount': get_ads.json()['rateValue'],
        'is_active': True if get_ads.json()['status'] == 'active' else False    
    }
    
    r_db = requests.post(url_db, json=changes_db)
    

    


@catch_error
def check_advert(key, bz_id, email):
    for adv in get_all_adverts(key, email):
        limit_min = adv['minAmount']
        adv_id = adv['id']
        average_amount = parse_average_amount(get_amounts(limit_min, key=key, email=email))
        edit_rate_value_advert(adv_id, average_amount, key, email)
        # print('[YES]')
        synchron(adv_id, key, email)
        # print('ok')
        
