from audioop import avg
import datetime
from locale import currency
import time
import random
from log import logger
import requests
from jose import jws
from jose.constants import ALGORITHMS

from setting import URL_DJANGO

url_error = URL_DJANGO + 'error/'


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
def get_all_trades(key, email, proxy):
    headers = authorization(key, email)
    url = 'https://bitzlato.bz/api/p2p/trade/'
    r = requests.get(url, headers=headers, proxies=proxy)
    print(r.status_code, r.elapsed.total_seconds())
    if r.status_code == 200:
        return r.json()['data']
    else:
        return []


@catch_error
def get_more_time(key, email, proxy, trade_id):
    header = authorization(key=key, email_bz=email)
    data_timeout = {
        "timeout": 10,
    }
    get_more_time_req = requests.post(f'https://bitzlato.bz/api/p2p/trade/{trade_id}/timeout', headers=header,
                                      proxies=proxy, json=data_timeout)
    return get_more_time_req.status_code


@catch_error
def cancel_bz_trade(key, email, proxy, trade_id):
    header = authorization(key=key, email_bz=email)
    data_cancel = {
        'type': "cancel"
    }
    adv_requests = requests.post(f'https://bitzlato.bz/api/p2p/trade/{trade_id}', headers=header,
                                 proxies=proxy, json=data_cancel)
    print('cancel', adv_requests.status_code)


@catch_error
def synchron(trade_id, cur_trade):
    date_created = 0
    date_closed = 0
    for i in cur_trade['history']:
        if i['status'] == 'trade_created':
            date_created = i['date'] // 1000
        if i['status'] == 'confirm_payment' or i['status'] == 'cancel':
            date_closed = i['date'] // 1000

    changes_db = {
        'id': trade_id,
        'status': cur_trade['status'],
        'date_closed': date_closed,
        'date_created': date_created,
        'need_prolong': False
    }
    r_db = requests.post(URL_DJANGO + 'update/bz/trade/', json=changes_db)


def check_trades(key, bz_id, email, proxy):
    print('check_trades')
    exists_trades = requests.get(URL_DJANGO + 'get/trades/').json()
    all_ids = [i['id'] for i in exists_trades]
    for trade in get_all_trades(key, email, proxy):
        if not str(trade["id"]) in all_ids:
            header = authorization(key=key, email_bz=email)
            adv_requests = requests.get(f'https://bitzlato.bz/api/p2p/trade/{trade["id"]}', headers=header,
                                        proxies=proxy)
            if adv_requests.status_code == 200:
                date_created = 0
                date_closed = 0
                adv_info = adv_requests.json()
                for i in adv_info['history']:
                    if i['status'] == 'trade_created':
                        date_created = i['date'] // 1000
                    if i['status'] == 'confirm_payment' or i['status'] == 'cancel':
                        date_closed = i['date'] // 1000
                data = {
                    'id': trade["id"],
                    'bzuser_id': bz_id,
                    'cryptocurrency': trade['cryptocurrency']['code'],
                    'cryptocurrency_amount': trade['cryptocurrency']['amount'],
                    'currency': trade['currency']['code'],
                    'amount': trade['currency']['amount'],
                    'paymethod': trade['paymethod'],
                    'card_number': str(adv_info['counterDetails']),
                    'counterDetails': str(adv_info['details']),
                    'status': adv_info['status'],
                    'partner': adv_info['partner'],
                    'date_created': date_created if date_created else None,
                    'date_closed': date_closed if date_closed else None,
                }
                print('добавляем в дб')
                print(adv_info['status'])
                add_trade = requests.post(URL_DJANGO + 'create/trade/', json=data)
        elif trade['status'] != 'cancel' and trade['status'] != 'confirm_payment':
            print(trade)

            cur_trade = requests.get(URL_DJANGO + f'bz/trade/detail/{str(trade["id"])}/').json()
            flag = False
            if cur_trade['bz']['need_prolong']:
                more_time = get_more_time(key, email, proxy, trade["id"])
                print(more_time)
                if more_time == 200:
                    flag = True
            time_now = datetime.datetime.now().timestamp()
            time_create = trade['date'] // 1000
            limit_close = cur_trade['bz']['time_close'] * 60
            print(time_now - time_create)

            if time_now - time_create > limit_close and not cur_trade['bz']['agent']:
                cancel_bz_trade(key, email, proxy, trade["id"])

            header = authorization(key=key, email_bz=email)
            adv_requests = requests.get(f'https://bitzlato.bz/api/p2p/trade/{trade["id"]}', headers=header,
                                        proxies=proxy)
            synchron(trade_id=str(trade["id"]), cur_trade=adv_requests.json())
            print(111111111111111111)
