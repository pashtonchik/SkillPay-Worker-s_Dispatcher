import subprocess
from telnetlib import STATUS
from flask import Flask, request
import sys
import requests
import json
import threading
import adverts_action 
from parse_garantex import parse_garantex
import connector

app = Flask(__name__)
          
@app.route('/check_adverts', methods=['POST', 'GET'])
def add_worker():

    data = request.get_json()
    id = data['id']
    key = data['key']
    command = 'check_adverts'
    email = data['email']
    print(data)
    
    if (command == 'check_adverts'):
        th = threading.Thread(target=adverts_action.check_advert, args=(key, id, email))
        th.start()
    return "OK", 200, {'Content-Type': 'text/plain'}

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
   

