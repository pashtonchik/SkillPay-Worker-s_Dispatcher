import subprocess
from telnetlib import STATUS
from flask import Flask, request
import sys
import requests
import json
import threading
import adverts_action 
import trades_action
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
    # print(data['key'])    
    proxy = data['proxy']
    # print(proxy)
    if (command == 'check_adverts'):
        th = threading.Thread(target=adverts_action.check_advert, args=(key, id, email, proxy))
        th.start()
    return "OK", 200, {'Content-Type': 'text/plain'}

@app.route('/check_trades', methods=['POST', 'GET'])
def check():
    
    data = request.get_json()
    # print(data)
    id = data['id']
    key = data['key']
    command = 'check_adverts'
    email = data['email']
    proxy = data['proxy']
    # print(data['key'])    
    if (command == 'check_adverts'):
        th = threading.Thread(target=trades_action.check_trades, args=(key, id, email, proxy))
        th.start()
    return "OK", 200, {'Content-Type': 'text/plain'}






if __name__ == '__main__':
    threading.Thread(target=parse_garantex, args=()).start()
    threading.Thread(target=connector.connector, args=()).start()
    app.run()
   

