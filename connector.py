import requests
import time 

URL_DJANGO = 'http://194.58.92.160:8000/'
URL_FLASK = 'http://127.0.0.1:5000/'
def connector():
    while True:
        req_django = requests.get(URL_DJANGO + 'api/tasks').json()
        req_flask = requests.post(URL_FLASK + 'check_adverts', json=req_django['BZ_users'])
        print(req_flask.status_code)
        time.sleep(3)