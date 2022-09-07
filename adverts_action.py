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
def get_amounts(min_amount, key, email, proxy, asset='BTC', fiat='RUB'):
    headers = authorization(key, email)
    url = f'https://bitzlato.bz/api2/p2p/exchange/dsa/?lang=ru&limit=10&skip=0&'\
    f'type=selling&currency={fiat}&cryptocurrency={asset}&' \
    f'isOwnerVerificated=false&isOwnerTrusted=false&isOwnerActive=false&'\
    f'amount={min_amount}&paymethod=443&amountType=currency&paymethodSlug=tinkoff'
    r = requests.get(url, headers=headers, proxies=proxy)
    if (r.status_code == 200):
        return r.json()['data']
    else:
        return []


@catch_error
def parse_average_amount(amounts_info):
    sum_amounts = 0
    for amount in amounts_info:
        sum_amounts += float(amount['rate'])
    return sum_amounts / 10


@catch_error
def get_all_adverts(key, email, proxy):
    headers = authorization(key, email)
    url = 'https://bitzlato.com/api/p2p/dsa/all'
    r = requests.get(url, headers=headers, proxies=proxy)

    headers = authorization(key, email)
    url = 'https://bitzlato.com/api/auth/whoami'
    user_id = requests.get(url, headers=headers, proxies=proxy).json()
    if (r.status_code == 200):
        exists_advert_id = requests.get('http://194.58.92.160:8000/api/adverts/').json()
        for advert in r.json():
            if not str(advert['id']) in exists_advert_id:
                add_advert = {
                    'advert_id': advert['id'],
                    'amount': float(advert['rateValue']),
                    'limit_min': advert['minAmount'],
                    'limit_max': advert['maxAmount'],
                    'paymethod': advert['paymethod'],
                    'paymethod_description': advert['paymethod_description'],
                    'is_active': True if (advert['status'] == 'active') else False,
                    'user': user_id['userId']
                }
                r1 = requests.post('http://194.58.92.160:8000/api/create/advert/', json=add_advert)
        return r.json()
    else:
        return []


@catch_error
def edit_rate_value_advert(advert_id, average_price, key, email, proxy):
    if (average_price != 0):
        url = f'https://bitzlato.com/api/p2p/dsa/{advert_id}'
        
        changes = {
            'rateValue': average_price,
        }

        headers = authorization(key, email)
        r = requests.put(url, headers=headers, proxies=proxy, json=changes)
        if (r.status_code == 200):
            advert = {
                'advert_id' : advert_id
            }

            get_price_garantex = 'http://194.58.92.160:8000/api/get_exchange_garantex/'
            price_garantex = requests.get(get_price_garantex).json()['btc-rub']
            
            headers = authorization(key, email)
            get_adv = requests.get(url, headers=headers, proxies=proxy)
            if (get_adv.status_code == 200):
                advert_info = requests.post('http://194.58.92.160:8000/api/get_advert_info/', json=advert)
                if (advert_info.json()['revenue_percentage'] != None):
                
                    percent = float(advert_info.json()['revenue_percentage'])
                
                    side_percent = ( (float(price_garantex) * 1.002) / (float(get_adv.json()['rateValue']) * 0.995)- 1) * 100
                
                    if side_percent < percent:
                
                
                        stop_advert(advert_id=advert_id, key=key, email=email, proxy=proxy)
                
                    else:
                
                        run_advert(advert_id=advert_id, key=key, email=email, proxy=proxy)
                return r.json()
            else:
                print('[ERROR] 131 line')
    else:
        return '[ERROR] 135 line'


@catch_error
def stop_advert(advert_id, key, email, proxy):
    headers = authorization(key, email)
    url = f'https://bitzlato.com/api/p2p/dsa/{advert_id}'
    
    changes = {
        'status': 'pause',
    }
    r = requests.put(url, headers=headers, proxies=proxy, json=changes)
    if (r.status_code == 200):
        return r.json()
    else:
        print('[ERROR] 149 line')


@catch_error
def run_advert(advert_id, key, email, proxy):
    headers = authorization(key, email)
    url = f'https://bitzlato.com/api/p2p/dsa/{advert_id}'
    changes = {
        'status': 'active',
    }

    r = requests.put(url, headers=headers, proxies=proxy, json=changes)
    if (r.status_code == 200):
        return r.json() 
    else:
        print('[ERROR] 164 line')


@catch_error
def synchron(advert_id, key, email, proxy):

    url = f'https://bitzlato.com/api/p2p/dsa/{advert_id}'
    url_db = 'http://194.58.92.160:8000/api/update/advert/'

    headers = authorization(key, email)
    
    get_ads = requests.get(url, headers=headers, proxies=proxy)
    if (get_ads.status_code == 200):
        changes_db = {
            'advert_id': advert_id,
            'amount': get_ads.json()['rateValue'],
            'is_active': True if get_ads.json()['status'] == 'active' else False    
        }
        
        r_db = requests.post(url_db, json=changes_db)
    else:
        print('[ERROR] 179 line')


@catch_error
def check_advert(key, bz_id, email, proxy):
    for adv in get_all_adverts(key, email, proxy):
        limit_min = adv['minAmount']
        adv_id = adv['id']
        average_amount = parse_average_amount(get_amounts(limit_min, key=key, email=email, proxy=proxy))
        edit_rate_value_advert(adv_id, average_amount, key, email, proxy=proxy)
        synchron(adv_id, key, email, proxy)
        
