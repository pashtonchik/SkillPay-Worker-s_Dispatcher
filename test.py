import datetime
import time
import random

import requests
from jose import jws
from jose.constants import ALGORITHMS


proxies = {
    'https': 'http://CMg6mg:fHoqJx@185.168.248.24:8000'
}


def authorization(key, email_bz):
    print('1111111111111')
    dt = datetime.datetime.now()
    ts = time.mktime(dt.timetuple())
    claims = {
        "email": email_bz,
        "aud": "usr",
        "iat": int(ts),
        "jti": hex(random.getrandbits(64))
    }
    token = jws.sign(claims, key, headers={
                     "kid": "1"}, algorithm=ALGORITHMS.ES256)
    return {'Authorization': "Bearer " + token}


if __name__ == '__main__':

    key = {"kty":"EC","alg":"ES256","crv":"P-256","x":"EMhj-c0DymACAdAR_b6FrZmSiYe7cXURDMSx18goIcY","y":"fUWCMJ9a4xpCmoDtU4fQENLm-h8VO1cpLhLk2rLgK18","d":"ysOqmzM6Y2rME_fmQEOnp0ix6gumffXp4OXTi7Q5lBg"}
    email = 'alex@lbnv.net'

    headers = authorization(key, email)

    url = 'https://bitzlato.com/api/p2p/dsa/all'

    r = requests.get(url, headers=headers, proxies=proxies)

    print(r.text)
