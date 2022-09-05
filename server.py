import subprocess
from flask import Flask, request
import sys
import requests
import json
import threading
import adverts_action 
from parse_garantex import parse_garantex
import connector


URL = 'http://194.58.92.160:8000/api/'

key = {"kty": "EC", "alg": "ES256", "crv": "P-256", "x": "yl31Sm28W2IS9UKEKmVoewQYYFp3ToyrRlZn-hiMhDU",
           "y": "9mWeLBzW0pwgM41gpgKq_p5zm2Lok5QBWbOfJhWCzwM", "d": "eGjueiOVTWmvl7gfk3hcnPpWn1Apb2BUsXrAeLA8Tr4"}
    

app = Flask(__name__)

# def queue(add=None, comands=[]):
#     if comands == []:
#         r = requests.get(URL + 'tasks/')
#         if (r.status_code == 200):
#             data = json.loads(r.text)
#             for i in data['ads']:
                
@app.route('/check_adverts', methods=['POST', 'GET'])
def add_worker():

    data = request.get_json()
    id = data[0]['id']
    key = data[0]['key']
    command = 'check_adverts'
    email = data[0]['email']
    
    
    if (command == 'check_adverts'):
        th = threading.Thread(target=adverts_action.check_advert, args=(key, id, email))
        th.start()
    return "1"

@app.route('/check_trades', methods=['POST', 'GET'])
def check():
    # data = request.get_json()
    data = {
        'account_id': '123',
        'email': '', 
        'account_key': {''},
        'command' : 'check_adverts'
    }

    # if (data['command'] == 'check_trades'):
    #     th = threading.Thread(target=adverts_action.check_advert, args=('', '123', 'skill834092@gmail.com'))
    #     th.start()
    return "1"





if __name__ == '__main__':
    threading.Thread(target=parse_garantex, args=()).start()
    threading.Thread(target=connector.connector, args=()).start()
    app.run()
   

