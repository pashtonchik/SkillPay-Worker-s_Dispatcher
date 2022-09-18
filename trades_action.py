from audioop import avg
import datetime
from locale import currency
import time
import random
from log import logger
import requests
from jose import jws
from jose.constants import ALGORITHMS


URL_DJANGO = 'http://194.58.92.160:8001/'
url_error = URL_DJANGO + 'api/error/'
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



proxies = {
    'https': 'http://CMg6mg:fHoqJx@185.168.248.24:8000'
}

@catch_error
@logger.catch
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
@logger.catch
def get_all_trades(key, email):
    # logger.debug("target: get_all_trades; action: start;")
    headers = authorization(key, email)
    url = 'https://bitzlato.com/api/p2p/trade/'
    r = requests.get(url, headers=headers, proxies=proxies)
    # logger.debug(f"target: get_all_trades; action: GET {url}; code: {r.status_code}; data: {r.text}")
    if r.status_code == 200:
        return r.json()['data']
    else:
        return []

@catch_error
@logger.catch
def synchron(trade_id, key, email, proxy):
    #logger.debug("target: synchron; action: start;")
    url = f'https://bitzlato.bz/api/p2p/trade/{trade_id}'
    url_db = URL_DJANGO + 'api/update/trade/'

    headers = authorization(key, email)
    
    get_trade = requests.get(url, headers=headers, proxies=proxy)
    #logger.debug(f"target: synchron; action: GET {url} status:{get_trade.status_code}")

    if (get_trade.status_code == 200):
        date_created = 0
        date_closed = 0 
        for i in get_trade.json()['history']:
            if i['status'] == 'trade_created':
                date_created = i['date'] // 1000
                #logger.debug(f"target: synchron; action: date_created = {date_created}")
                
            if i['status'] == 'confirm_payment':
                date_closed = i['date'] // 1000
                #logger.debug(f"target: synchron; action: date_closed = {date_created}")

            if i['status'] == 'cancel':
                date_closed = i['date'] // 1000
                #logger.debug(f"target: synchron; action: date_closed = {date_created}")
        changes_db = {
            'id': trade_id,
            'status': get_trade.json()['status'],
            'date_closed' : date_closed, 
            'date_created' : date_created
        }
        # print(changes_db['date_closed'])
        r_db = requests.post(url_db, json=changes_db)
        # logger.debug(f"target: synchron; action: POST {url}, data: {changes_db} status:{r_db.status_code}")
    else:
        pass
        # logger.debug(f"target: synchron; ERROR 93 line. get_trade status code != 200")

    


@catch_error
@logger.catch
def check_trades(key, bz_id, email, proxy):
    #logger.debug(f"target: check_trades; action: start")
    for adv in get_all_trades(key, email):
        # print(adv, email)
        header = authorization(key=key, email_bz=email)
        id = adv['id']
        adv_requests = requests.get(f'https://bitzlato.bz/api/p2p/trade/{id}', headers=header, proxies=proxy)
        # logger.debug(f"target: check_trades; GET {f'https://bitzlato.bz/api/p2p/trade/{id}'}: status:{adv_requests.status_code}; \
         #   data: {adv_requests.text}")
        if (adv_requests.status_code == 200):
            date_created = 0
            date_closed = 0 
            adv_info = adv_requests.json()
            for i in adv_info['history']:
                if i['status'] == 'trade_created':
                    date_created = i['date'] // 1000
                if i['status'] == 'confirm_payment':
                    date_closed = i['date'] // 1000
            cryptocurrency = adv['cryptocurrency']['code']
            cryptocurrency_amount = adv['cryptocurrency']['amount']
            currency = adv['currency']['code']
            currency_amount = adv['currency']['amount']
            paymethod = adv['paymethod']
            details = adv_info['details']
            counterDetails = adv_info['counterDetails']
            status = adv_info['status']
            partner = adv_info['partner']
            exists_trades = requests.get(URL_DJANGO + 'api/get/trades/').json()
            #  logger.debug(f'target: check_trades; action: GET http://194.58.92.160:8001/api/get/trades/; data:{exists_trades}')
            all_ids = []
            for i in exists_trades:
                all_ids.append(i['id'])
            if not str(id) in all_ids:
                data = {
                    'id': id,
                    'bzuser_id': bz_id,
                    'cryptocurrency':  cryptocurrency,
                    'cryptocurrency_amount': cryptocurrency_amount,
                    'currency': currency,
                    'currency_amount': currency_amount,
                    'paymethod': paymethod,
                    'details': str(details),
                    'counterDetails': str(counterDetails),
                    'status': status,
                    'partner': partner,
                    'date_created': date_created if date_created else None,
                    'date_closed':  date_closed if date_closed else None,
                }
                add_trade = requests.post(URL_DJANGO + 'api/create/trade/', json=data)
                # logger.debug(f'target: check_trades; action: POST http://194.58.92.160:8001/api/create/trade/;\
                #      status:{add_trade.status_code}; data: {data}')
        synchron(email=email, key=key, trade_id=id, proxy=proxy)