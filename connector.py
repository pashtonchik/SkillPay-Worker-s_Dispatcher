import requests
import time 

URL_DJANGO = 'http://194.58.92.160:8000/'
URL_FLASK = 'http://127.0.0.1:5000/'
def connector():
    while True:
        req_django = requests.get(URL_DJANGO + 'api/tasks').json()
        for i in req_django:
            req_flask = requests.post(URL_FLASK + 'check_adverts', json=i['user'])
        time.sleep(15)
