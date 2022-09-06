import datetime
import json
import time
import random
import base64

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
    token = jws.sign(claims, key, headers={
                     "kid": "1"}, algorithm=ALGORITHMS.ES256)
    return {'Authorization': "Bearer " + token}


if __name__ == '__main__':

    key = {"kty": "EC", "alg": "ES256", "crv": "P-256", "x": "yl31Sm28W2IS9UKEKmVoewQYYFp3ToyrRlZn-hiMhDU", "y": "9mWeLBzW0pwgM41gpgKq_p5zm2Lok5QBWbOfJhWCzwM", "d": "eGjueiOVTWmvl7gfk3hcnPpWn1Apb2BUsXrAeLA8Tr4"}

    email = 'skill834092@gmail.com'

    headers = authorization(key, email)
    
    # with open("my_image.png", "rb") as f:
    #     png_encoded = base64.b64encode(f.read())

    # print(type(png_encoded))
    # url = 'https://bitzlato.bz/api2/p2p/trade/17247229/chat/sendfile'
    # data = {
    #     'mime_type': 'image/png',
    #     'name': 'Снимок экрана от 2022-09-06 15-41-47.png'
    # }
    # files = {'file': open('Снимок экрана от 2022-09-02 22-54-50.png', 'rb')}
    
    # r = requests.post(url, headers=headers, proxies=proxies, files=files)

    # url = 'https://bitzlato.bz/api/p2p/trade/17248185'

    # data = {

    # }
    # r = requests.get(url, headers=headers, proxies=proxies)

    # url = 'https://bitzlato.bz/api/p2p/trade/17248661'

    # r = requests.get(url, headers=headers, proxies=proxies)

    # data = {
    #     'type': 'cancel'
    # }
    url = 'https://bitzlato.com/api/p2p/trade/'

    # r = requests.get(url, headers=headers, proxies=proxies)

    url = 'https://bitzlato.bz/api/auth/whoami'

    r = requests.get(url, headers=headers, proxies=proxies)


    print(r.status_code, r.text)
