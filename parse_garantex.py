import time
import requests

while True:
    garantex_resp = requests.get('https://garantex.io/api/v2/depth?market=btcrub').json()

    orders = garantex_resp['bids']
    for order in orders:
        if float(order['volume']) >= 0.5:
            actually_price = order['price']
            break

    exchange_info = {
        'fiat': 'BTC',
        'asset': 'RUB',
        'price': actually_price,
    }

    server_resp = requests.post('http://127.0.0.1:8000/api/update/', json=exchange_info)
    time.sleep(15)

