
import datetime
import time
import random

import requests
from jose import jws
from jose.constants import ALGORITHMS



proxies = {
    'https': 'http://rp3R2E:fAfUYW@193.41.123.50:8000'
}


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



if __name__ == '__main__':
    key = {"kty":"EC","alg":"ES256","crv":"P-256","x":"hSBO76-0UpdvKlR9PQCo1tyGnSXSnEFPhVCsXEk2mJM","y":"TNM6EP34Ag2cFq2OfkRx_XMoqr-oxfrU2NkHWp7L0Vw","d":"IELsNynt0o3t6qPxSMlY-yiZNKQGiq7Tkz4lvxicugc"}
    email = 'alex@lbnv.net'
    headers = authorization(key, email)
    data = {
        'advertId' : '654602',
        'amount' : '10',
        'rate' : '1197339',
        'amountType' : 'RUB',
        'counterDetails' : 'Оплата на номер 939393993 лаллала'
    }
    url = 'https://bitzlato.com/api/p2p/trade'


    r = requests.post(url, headers=headers, proxies=proxies, json=data)
    print(r.text, r.status_code)