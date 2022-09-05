import datetime
import time
import random

import requests
from jose import jws
from jose.constants import ALGORITHMS

proxies = {
    'https': 'http://CMg6mg:fHoqJx@185.168.248.24:8000'
}
email = 'skill834092@gmail.com'

key_bz = {"kty": "EC", "alg": "ES256", "crv": "P-256", "x": "yl31Sm28W2IS9UKEKmVoewQYYFp3ToyrRlZn-hiMhDU", "y": "9mWeLBzW0pwgM41gpgKq_p5zm2Lok5QBWbOfJhWCzwM", "d": "eGjueiOVTWmvl7gfk3hcnPpWn1Apb2BUsXrAeLA8Tr4"}


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


def get_amounts(min_amount, key, email, asset='BTC', fiat='RUB'):
    headers = authorization(key, email)
    url = f'https://bitzlato.bz/api2/p2p/exchange/dsa/?lang=ru&limit=10&skip=0&'\
    f'type=selling&currency={fiat}&cryptocurrency={asset}&' \
    f'isOwnerVerificated=false&isOwnerTrusted=false&isOwnerActive=false&'\
    f'amount={min_amount}&paymethod=443&amountType=currency&paymethodSlug=tinkoff'
    # print(url)
    r = requests.get(url, headers=headers, proxies=proxies)

    # print(r.text)
    return r.json()['data']


def parse_average_amount(amounts_info):
    # print(amounts_info)
    sum_amounts = 0
    for amount in amounts_info:
        sum_amounts += float(amount['rate'])
        # print(amount['rate'])
    return sum_amounts / 10


def get_all_adverts(key, email):
    headers = authorization(key, email)
    url = 'https://bitzlato.com/api/p2p/dsa/all'
    r = requests.get(url, headers=headers, proxies=proxies)
    # print(r.text)
    exists_advert_id = requests.get('http://194.58.92.160:8000/api/adverts/')
    exists_advert_id = exists_advert_id.json()
    # print(exists_advert_id)
    # print(r.json())
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


def edit_rate_value_advert(advert_id, average_price, key, email):
    headers = authorization(key, email)
    
    url = f'https://bitzlato.com/api/p2p/dsa/{advert_id}'
    
    url_db = 'http://194.58.92.160:8000/api/update/advert/'
    
    changes = {
        'rateValue': average_price,
    }
    
    r = requests.put(url, headers=headers, proxies=proxies, json=changes)
    
    # print(r.json())
    headers = authorization(key, email)
    get_ads = requests.get(url, headers=headers, proxies=proxies)
    print(get_ads.text)
    changes_db = {
        'advert_id': advert_id,
        'amount': average_price,
        'is_active': True if get_ads.json()['status'] == 'active' else False    
    }

    # print(r.json())
    r_db = requests.post(url_db, json=changes_db)
    print(r_db.status_code, r_db.text)
    # print(r.text)
    return r.json()


def stop_advert(advert_id, key, email):
    headers = authorization(key, email)
    url = f'https://bitzlato.com/api/p2p/dsa/{advert_id}'
    url_db = 'http://194.58.92.160:8000/api/update/advert'
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


def run_advert(advert_id, key, email):
    headers = authorization(key, email)
    url = f'https://bitzlato.com/api/p2p/dsa/{advert_id}'
    url_db = 'http://194.58.92.160:8000/api/update/advert'
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


def check_advert(key, bz_id, email):
    for adv in get_all_adverts(key, email):
        limit_min = adv['minAmount']
        adv_id = adv['id']
        average_amount = parse_average_amount(get_amounts(limit_min, key=key, email=email))
        edit_rate_value_advert(adv_id, average_amount, key, email)
        print('ok')
        
