import datetime
import time
import random
import requests
from log import logger
from jose import jws
from jose.constants import ALGORITHMS

from setting import URL_DJANGO


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
            r = requests.post(URL_DJANGO + 'api/error/', json=data)
            pass
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
def get_amounts(paymethod, min_amount, down, up, key, email, proxy, asset='BTC', fiat='RUB'):
    headers = authorization(key, email)
    limit = up - down + 1
    skip = down - 1
    url = f'https://bitzlato.bz/api/p2p/exchange/dsa/?lang=ru&limit={limit}&skip={skip}&'\
    f'type=selling&currency={fiat}&cryptocurrency={asset}&' \
    f'isOwnerVerificated=false&isOwnerTrusted=false&isOwnerActive=false&'\
    f'amount={min_amount}&paymethod={str(paymethod)}&amountType=currency'
    r = requests.get(url, headers=headers, proxies=proxy)
    if r.status_code == 200:
        return r.json()['data']
    else:
        return []


@catch_error
def parse_average_amount(amounts_info, count):
    sum_amounts = 0
    if amounts_info:
        for amount in amounts_info:
            sum_amounts += float(amount['rate'])
    return sum_amounts / count


@catch_error
def get_all_scripts():
    req_scripts = requests.get(URL_DJANGO + 'api/get/scripts/')
    if req_scripts.status_code == 200:
        data_scripts = req_scripts.json()
    else:
        data_scripts = []
    return data_scripts


@catch_error
def get_all_adverts(key, email, proxy):
    headers = authorization(key, email)
    url = 'https://bitzlato.com/api/p2p/dsa/all'
    r = requests.get(url, headers=headers, proxies=proxy)
    headers = authorization(key, email)
    url = 'https://bitzlato.com/api/auth/whoami'
    user_id = requests.get(url, headers=headers, proxies=proxy).json()
    if r.status_code == 200:
        exists_advert_id = requests.get(URL_DJANGO + 'api/adverts/').json()
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
                r1 = requests.post(URL_DJANGO + 'api/create/advert/', json=add_advert)
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
        if r.status_code == 200:
            advert = {
                'advert_id' : advert_id
            }

            get_price_garantex = URL_DJANGO + 'api/get_exchange_garantex/'
            price_garantex = requests.get(get_price_garantex).json()['btc-rub']
            
            headers = authorization(key, email)
            get_adv = requests.get(url, headers=headers, proxies=proxy)
            if get_adv.status_code == 200:
                advert_info = requests.post(URL_DJANGO + 'api/get_advert_info/', json=advert)
                if advert_info.json()['revenue_percentage'] != None:
                
                    percent = float(advert_info.json()['revenue_percentage'])
                
                    side_percent = ( (float(price_garantex) * 0.998) / (float(get_adv.json()['rateValue']) * 1.005)- 1) * 100
                
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
    if r.status_code == 200:
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
    if r.status_code == 200:
        return r.json() 
    else:
        print('[ERROR] 164 line')


@catch_error
def stop_script(script_id):
    changes = {
        'is_active': False,
    }

    r = requests.post(URL_DJANGO + f'api/update/script/{script_id}/', json=changes)
    if r.status_code == 200:
        return True
    else:
        print('[ERROR] 164 line')


@catch_error
def start_script(script_id):
    changes = {
        'is_active': True,
    }

    r = requests.post(URL_DJANGO + f'api/update/script/{script_id}/', json=changes)
    if r.status_code == 200:
        return True
    else:
        print('[ERROR] 164 line')


@catch_error
def edit_amount_script(script_id, average_amount):
    changes = {
        'average_price': average_amount,
    }
    r = requests.post(URL_DJANGO + f'api/update/script/{script_id}/', json=changes)
    if r.status_code == 200:
        return r.json()
    else:
        return {}


@catch_error
def synchron(advert_id, key, email, proxy):
    url = f'https://bitzlato.com/api/p2p/dsa/{advert_id}'
    url_db = URL_DJANGO + f'api/get/advert_info/{advert_id}/'

    advert_info_db = requests.get(url_db).json()
    changes_bz = {
        'rateValue': advert_info_db['amount'],
        'status': 'active' if advert_info_db['is_active'] else 'pause',
    }

    headers = authorization(key, email)
    r = requests.put(url, headers=headers, proxies=proxy, json=changes_bz)



@catch_error
def check_scripts(key, bz_id, email, proxy):
    all_adverts = get_all_adverts(key, email, proxy)
    for script in get_all_scripts():
        limit_min = script['script']['amount']
        paymethod = script['script']['paymethod']
        up = script['script']['upper_target']
        down = script['script']['bottom_target']
        count = up - down + 1
        average_amount = parse_average_amount(get_amounts(paymethod, limit_min,
                                                          key=key, email=email, proxy=proxy, up=up, down=down), count)
        updated_script = edit_amount_script(script['script']['id'], average_amount)
        if (updated_script.get('revenue_percentage', None) and updated_script.get('actual_percentage', None)) \
         and (updated_script.get('revenue_percentage', None) > updated_script.get('actual_percentage', None)):
            stop_script(updated_script['id'])
        else:
            start_script(updated_script['id'])
        for advert_id in script['adverts']:
            synchron(advert_id, key, email, proxy)   
        if average_amount == 0:
            try_updated_script = edit_amount_script(script['script']['id'], average_amount)
            if  (try_updated_script.get('revenue_percentage', None) and try_updated_script.get('actual_percentage', None)) \
                and (try_updated_script.get('revenue_percentage', None) > try_updated_script.get('actual_percentage', None)):
                stop_script(try_updated_script['id'])
            else:
                start_script(try_updated_script['id'])
            for advert_id in script['adverts']:
                synchron(advert_id, key, email, proxy)
