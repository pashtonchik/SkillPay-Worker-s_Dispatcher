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

    # key = {"kty":"EC","alg":"ES256","crv":"P-256","x":"SkcQ2TUWCEygFEhSOBhThRu8jUCc7NmLtJPOOOu52ec","y":"aNLV7Bg5CHqtiTcm5EVHmrjPNME_2mxrWp4AJGZfl80","d":"nqHmOQD-LwlkFby0slQZAXd-tqo9TbIy7hoVTAh76VA"}

    # email = 'superfast385903@gmail.com'

    key = {'d': 'nqHmOQD-LwlkFby0slQZAXd-tqo9TbIy7hoVTAh76VA', 'x': 'SkcQ2TUWCEygFEhSOBhThRu8jUCc7NmLtJPOOOu52ec', 'y': 'aNLV7Bg5CHqtiTcm5EVHmrjPNME_2mxrWp4AJGZfl80', 'alg': 'ES256', 'crv': 'P-256', 'kty': 'EC'}
    email = 'protraderz2000@gmail.com'
    
    # with open("my_image.png", "rb") as f:
    #     png_encoded = base64.b64encode(f.read())

    # print(type(png_encoded))
    headers = authorization(key, email)

    # url = 'https://bitzlato.bz/api/p2p/trade/17268092/chat/sendfile/'
    # data_message = {
    #     'message' : '11',
    #     'payload' : {
    #         'message' : 'string'
        # }
    # }
    # data = {
        # 'mime_type': 'image/png',
        # 'name': 'Снимок экрана от 2022-09-06 15-41-47.png'
    # }
    # files = {'file': open('img.png', 'rb')}
    
    # r = requests.post(url, headers=headers, proxies=proxies, files=files)

    # send_message = f'https://bitzlato.bz/api/p2p/trade/17268092/chat/'
    # headers = authorization(key, email)
    # data_message = {
        # 'message' : 'Оплатил.',
        # 'payload' : {
            # 'message' : 'string'
        # }
    # }
    # r = requests.post(send_message, headers=headers, proxies=proxies, json=data_message)

    # url = 'https://bitzlato.bz/api/p2p/trade/17248185'

    # data = {

    # }
    # r = requests.get(url, headers=headers, proxies=proxies)

    # url = 'https://bitzlato.bz/api/p2p/trade/17248661'

    # r = requests.get(url, headers=headers, proxies=proxies)

    # data = {
        # 'type': 'cancel'
    # }
    # url = 'https://bitzlato.com/api/p2p/trade/17260396'

    # r = requests.get(url, headers=headers, proxies=proxies)

    url = 'https://bitzlato.bz/api/auth/whoami'

    r = requests.get(url, headers=headers, proxies=proxies)


    print(r.status_code, r.text)
