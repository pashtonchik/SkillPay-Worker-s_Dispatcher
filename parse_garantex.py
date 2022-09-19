import time
import requests

from django import URL_DJANGO


def parse_garantex():
    while True:
        garantex_resp = requests.get('https://garantex.io/api/v2/depth?market=btcrub')
        if (garantex_resp.status_code == 200):
            garantex_resp = garantex_resp.json()
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

            server_resp = requests.post(URL_DJANGO + 'api/update/garantex', json=exchange_info)
            if (server_resp.status_code != 200):
                print(f'[ERROR] {server_resp.status_code}')
            else:
                print(f'[POLLING]')
        else:
            print(f'[ERROR Garantex]')
            continue
        time.sleep(15)

if __name__ == '__main__':
    parse_garantex()