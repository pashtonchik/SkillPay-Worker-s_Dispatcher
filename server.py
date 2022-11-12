import subprocess
from telnetlib import STATUS
from flask import Flask, request
import sys
import requests
import json
import threading
import adverts_action
import gar_adverts_action
import gar_trades_action
import trades_action
from parse_garantex import parse_garantex
import connector
from log import logger
from setting import URL_DJANGO
app = Flask(__name__)

# URL_DJANGO = 'http://194.58.92.160:8000/'


@app.route('/check_bz_adverts', methods=['POST', 'GET'])
def bz_adverts():
    data = request.get_json()
    id = data['id']
    key = data['key']
    command = 'check_adverts'
    email = data['email']
    proxy = data['proxy']
    if command == 'check_adverts':
        th = threading.Thread(target=adverts_action.check_scripts, args=(key, id, email, proxy))
        th.start()
    return "OK", 200, {'Content-Type': 'text/plain'}


@app.route('/check_bz_trades', methods=['POST', 'GET'])
def bz_trades():
    data = request.get_json()
    id = data['id']
    key = data['key']
    command = 'check_adverts'
    email = data['email']
    proxy = data['proxy']
    if command == 'check_adverts':
        th = threading.Thread(target=trades_action.check_trades, args=(key, id, email, proxy))
        th.start()
    return "OK", 200, {'Content-Type': 'text/plain'}


@app.route('/check_garantex_adverts', methods=['POST', 'GET'])
def gar_adverts():
    data = request.get_json()
    user_id = data['id']
    uid = data['uid']
    private_key = data['private_key']
    command = 'check_garantex_adverts'
    if command == 'check_garantex_adverts':
        th = threading.Thread(target=gar_adverts_action.update_adverts_garantex, args=(private_key, uid, user_id))
        th.start()
    return "OK", 200, {'Content-Type': 'text/plain'}


@app.route('/check_garantex_trades', methods=['POST', 'GET'])
def gar_trades():
    data = request.get_json()
    command = 'check_garantex_adverts'
    uid = data['uid']
    private_key = data['private_key']
    if command == 'check_garantex_adverts':
        th = threading.Thread(target=gar_trades_action.update_trades_garantex, args=(private_key, uid))
        th.start()
    return "OK", 200, {'Content-Type': 'text/plain'}


if __name__ == '__main__':
    threading.Thread(target=parse_garantex, args=()).start()
    threading.Thread(target=connector.connector, args=()).start()
    app.run(host="0.0.0.0", port=int("5001"))
   

