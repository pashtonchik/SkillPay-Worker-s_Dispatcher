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
from log import logger
from setting import URL_DJANGO
app = Flask(__name__)

# URL_DJANGO = 'http://194.58.92.160:8000/'


@logger.catch          
@app.route('/check_bz_adverts', methods=['POST', 'GET'])
def bz_adverts():
    data = request.get_json()
    id = data['id']
    key = data['key']
    command = 'check_adverts'
    email = data['email']
    # print(data['key'])    
    proxy = data['proxy']
    # print(proxy)
    if command == 'check_adverts':
        th = threading.Thread(target=adverts_action.check_scripts, args=(key, id, email, proxy))
        th.start()
    return "OK", 200, {'Content-Type': 'text/plain'}


@logger.catch
@app.route('/check_bz_trades', methods=['POST', 'GET'])
def bz_trades():
    data = request.get_json()
    # print(data)
    id = data['id']
    key = data['key']
    command = 'check_adverts'
    email = data['email']
    proxy = data['proxy']
    # print(data['key'])    
    if command == 'check_adverts':
        th = threading.Thread(target=trades_action.check_trades, args=(key, id, email, proxy))
        th.start()
    return "OK", 200, {'Content-Type': 'text/plain'}


if __name__ == '__main__':
    threading.Thread(target=parse_garantex, args=()).start()
    threading.Thread(target=connector.connector, args=()).start()
    app.run(host="0.0.0.0", port=int("5001"))
   

