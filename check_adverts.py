import datetime
import time
import random

import requests
from jose import jws
from jose.constants import ALGORITHMS

proxies = {
    'https': 'http://CMg6mg:fHoqJx@185.168.248.24:8000'

}


def authorization():
    key = {"kty": "EC", "alg": "ES256", "crv": "P-256", "x": "yl31Sm28W2IS9UKEKmVoewQYYFp3ToyrRlZn-hiMhDU",
           "y": "9mWeLBzW0pwgM41gpgKq_p5zm2Lok5QBWbOfJhWCzwM", "d": "eGjueiOVTWmvl7gfk3hcnPpWn1Apb2BUsXrAeLA8Tr4"}
    dt = datetime.datetime.now()
    ts = time.mktime(dt.timetuple())
    claims = {
        "email": 'skill834092@gmail.com',
        "aud": "usr",
        "iat": int(ts),
        "jti": hex(random.getrandbits(64))
    }
    token = jws.sign(claims, key, headers={"kid": "1"}, algorithm=ALGORITHMS.ES256)
    return {'Authorization': "Bearer " + token}


def get_amounts(min_amount, fiat='BTC', asset='RUB'):
    headers = authorization()
    url = f'https://bitzlato.com/api/p2p/public/exchange/dsa/?amount={min_amount}&amountType' \
          f'=currency%20%2F%20cryptocurrency&cryptocurrency={fiat}&currency={asset}&isOwnerActive=false' \
          f'&isOwnerVerificated=false&lang=en&limit=10&paymethod=443&skip=0&slug=rub-tinkoff&type=purchase'
    r = requests.get(url, headers=headers, proxies=proxies)
    return r.json()['data']


def parse_average_amount(amounts_info):
    sum_amounts = 0
    for amount in amounts_info:
        sum_amounts += float(amount['rate'])
    return sum_amounts / 10


def get_all_adverts():
    headers = authorization()
    url = 'https://bitzlato.com/api/p2p/dsa/all'
    r = requests.get(url, headers=headers, proxies=proxies)
    exists_advert_id = requests.get('http://127.0.0.1:8000/api/adverts/')
    exists_advert_id = exists_advert_id.json()
    for advert in r.json():
        if not str(advert['id']) in exists_advert_id:
            add_advert = {
                'advert_id': advert['id'],
                'amount': float(advert['rateValue']),
                'limit_min': advert['minAmount'],
                'limit_max': advert['maxAmount'],
                'is_active': True if (advert['status'] == 'active') else False,
            }
            r1 = requests.post('http://127.0.0.1:8000/api/create/advert/', json=add_advert)
    return r.json()


def edit_rate_value_advert(advert_id, good_price):
    headers = authorization()
    url = f'https://bitzlato.com/api/p2p/dsa/{advert_id}'
    url_db = 'http://127.0.0.1:8000/api/update/advert'
    changes = {
        'rateValue': good_price,
    }
    changes_db = {
        'advert_id': advert_id,
        'amount': good_price,
    }
    r = requests.put(url, headers=headers, proxies=proxies, json=changes)
    r_db = requests.post(url_db, json=changes_db)
    print(r.text)
    return r.json()


def stop_advert(advert_id):
    headers = authorization()
    url = f'https://bitzlato.com/api/p2p/dsa/{advert_id}'
    url_db = 'http://127.0.0.1:8000/api/update/advert'
    changes = {
        'status': 'pause',
    }
    changes_db = {
        'advert_id': advert_id,
        'is_active': False,
    }
    r = requests.put(url, headers=headers, proxies=proxies, json=changes)
    r_db = requests.post(url_db, json=changes_db)
    return r.json()


def run_advert(advert_id):
    headers = authorization()
    url = f'https://bitzlato.com/api/p2p/dsa/{advert_id}'
    url_db = 'http://127.0.0.1:8000/api/update/advert'
    changes = {
        'status': 'active',
    }
    changes_db = {
        'advert_id': advert_id,
        'is_active': True,
    }
    r = requests.put(url, headers=headers, proxies=proxies, json=changes)
    r_db = requests.post(url_db, json=changes_db)
    return r.json()


while True:
    for adv in get_all_adverts():
        limit_min = adv['minAmount']
        adv_id = adv['id']
        average_amount = parse_average_amount(get_amounts(limit_min)) - 100000
        edit_rate_value_advert(adv_id, average_amount)
        print('ok')
        time.sleep(30)






