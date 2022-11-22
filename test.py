from audioop import avg
import datetime
from locale import currency
import time
import random
from log import logger
import requests
from jose import jws
from jose.constants import ALGORITHMS


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


proxy = {"https": "http://vkY9ug:huCqxg@193.41.122.170:8000"}
key = {"d": "eGjueiOVTWmvl7gfk3hcnPpWn1Apb2BUsXrAeLA8Tr4", "x": "yl31Sm28W2IS9UKEKmVoewQYYFp3ToyrRlZn-hiMhDU", "y": "9mWeLBzW0pwgM41gpgKq_p5zm2Lok5QBWbOfJhWCzwM", "alg": "ES256", "crv": "P-256", "kty": "EC"}
email = 'skill834092@gmail.com'


headers = authorization(key, email)
#onlyClosed=false&dateFrom=1664582400000
url = 'https://bitzlato.bz/api/p2p/trade/?onlyClosed=false&dateFrom=1664582400000&type=purchase'
r = requests.get(url, headers=headers, proxies=proxy)
print(r.status_code, r.elapsed.total_seconds())
print(r.json())