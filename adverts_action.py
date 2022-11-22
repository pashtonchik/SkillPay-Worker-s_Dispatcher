import datetime
import time
import random
import requests
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
            r = requests.post(URL_DJANGO + 'error/', json=data)
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
    begin = datetime.datetime.now().timestamp()
    headers = authorization(key, email)
    limit = up - down + 1
    skip = down - 1
    url = f'https://bitzlato.net/api/p2p/exchange/dsa/?lang=ru&limit={limit}&skip={skip}&' \
          f'type=selling&currency={fiat}&cryptocurrency={asset}&' \
          f'isOwnerVerificated=false&isOwnerTrusted=false&isOwnerActive=false&' \
          f'amount={min_amount}&paymethod={str(paymethod)}&amountType=currency'
    r = requests.get(url, headers=headers, proxies=proxy)
    if r.status_code == 200:
        print('get_amounts', begin - datetime.datetime.now().timestamp())
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
    req_scripts = requests.get(URL_DJANGO + 'get/scripts/')
    if req_scripts.status_code == 200:
        data_scripts = req_scripts.json()
    else:
        data_scripts = []
    return data_scripts


@catch_error
def get_all_adverts(bz_user_id, key, email, proxy):
    headers = authorization(key, email)
    url = 'https://bitzlato.net/api/p2p/dsa/all'
    print(1111)
    r = requests.get(url, headers=headers, proxies=proxy)
    print(2222)
    if r.status_code == 200:
        print(33333)
        exists_advert_id = requests.get(URL_DJANGO + 'adverts/')
        print(4444)
        print(exists_advert_id)
        exists_advert_id = [advert['advert_id'] for advert in exists_advert_id.json()] if exists_advert_id.status_code == 200 else []
        print(exists_advert_id)
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
                    'user': bz_user_id
                }
                r1 = requests.post(URL_DJANGO + 'create/advert/', json=add_advert)
                print('r1', r1.status_code)
        return r.json()
    else:
        return []


@catch_error
def edit_amount_advert(advert_id, average_amount):
    changes = {
        'average_price': average_amount,
    }
    r = requests.post(URL_DJANGO + f'update/advert/{advert_id}/', json=changes)
    print('внесли среднюю цену')
    if r.status_code == 200:
        return r.json()
    else:
        return {}


@catch_error
def synchron(advert_id, key, email, proxy, advert_info_db):
    print('id', advert_id)
    begin = datetime.datetime.now().timestamp()
    url = f'https://bitzlato.net/api/p2p/dsa/{advert_id}'

    changes_bz = {
        'rateValue': advert_info_db['average_price'],
        'status': 'active' if advert_info_db['is_active'] else 'pause',
    }

    headers = authorization(key, email)
    r = requests.put(url, headers=headers, proxies=proxy, json=changes_bz)
    print('synchron', begin - datetime.datetime.now().timestamp())


def check_adverts(key, bz_id, email, proxy, adverts):
    ########### раскомментить в случае если нужно создавать объявления в БД #############
    all_adverts = get_all_adverts(bz_id, key, email, proxy)
    ####################################################################################
    for advert in adverts:
        limit_min = advert['script']['amount']
        paymethod = advert['script']['paymethod']
        up = advert['upper_target']
        down = advert['bottom_target']
        count = up - down + 1
        average_amount = parse_average_amount(get_amounts(paymethod, limit_min,
                                                          key=key, email=email, proxy=proxy, up=up, down=down), count)
        updated_advert = edit_amount_advert(advert['advert_id'], average_amount)
        synchron(advert['advert_id'], key, email, proxy, updated_advert)
