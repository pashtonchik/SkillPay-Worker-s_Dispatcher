from garantexAPI.trades import *
from garantexAPI.auth import *
from setting import URL_DJANGO
import datetime

user = {
    'id': 'SNCE99027726',
    'private_key': 'LS0tLS1CRUdJTiBSU0EgUFJJVkFURSBLRVktLS0tLQpNSUlFcEFJQkFBS0NBUUVBd0M3aWFWWFdTdmR2TVAwRnpzK0NjY0pRdUpuelBaUE5VbGlLUjdLYVE5VWhiY1Z6CmZwTDV0ZGlJemllV2tMT0lSTzNBbFp4RHRSdUJnZTQ0S0RVdVhtZ0svZyt5aE1zSXRILzhXODJiV1g0RVJGdzYKVE1sTlYvRE1PMEFJSllYZHVzcGlmd3E3NzROVTVxeFdqcER2ZVA5SnlDSUQvM2hQTG82KzdBVlFiMVhLS3I0ZgppVnZSa2xhNjl0dHQ5T1pOUWkxdWpSbFBsYjVrVnRsS05vV0RmcFJKaFQ4SjlWc1crQjRSZ3ZRYnBmakFlSWNQCnNISUE2c2pGR3RvaGNtOFIxM2VuVDlzbW40MW9XZDBUMnVhUGRyNlg3RHR0OTBZdUVPUEcvaGZJcGZhYmhqSlUKdEFjK2RCQWFMMTZGZ0N6TGFWc01BYmZMTVM4OGhkTm40OUgrQ3dJREFRQUJBb0lCQVFDYmlKWW1KNWpoWFBUNQpFWjBVcmEzbFFSeXcrYTc0dzloa2IxR2lDdko4T1UzdmwrQUxyUWs0MlVDR2oxVjBVRWZWZVJEbVErd3I4MUhSCmhLaWdLY0lZRjEzbUZYQWx0bWVhSlFab2liTFRMNEJtanJtRUVWcHQ5R3hrKzBKY2s4VkorYWJUS0MzRy9tUEUKdCs3cFBIVUNXS0V1dmhDOFBYTGZ2Qmpaek1jM0FpK1gyWWk0dWRUbWQ1OUUwUjhFM1pRWW44UWxyVng1TXNmTApBRVFZajJIOTdIQW1CdXZBcDJBcGc4L2VtTmVJVVM1RFRwK2crc3NnaGdYSFR4aTZCZ2Q1YkNYZDFMSnRTbEw2CndabW9aMm5VVzYxZUd5SG9uSmg2ZzZBMk93WXFBako4UzMxcTJ1SFNvVDJ5ZFp1bFN6SGZteCtkQU5WZjNiT0QKVEFHcmRicXhBb0dCQVBPN2gzSVpXTk5CRE1iQ20yak9hM3FoaVlLYkxnbXdFMG4wd3BNZWx4eW1KRkJqbkl3aApVMFZyeXRCZytCbHMrS2tHR0I0dzAydDlEdUVJZ2c2N0hYam1GK1ZtQmpGN1pIajRTNVlQSTFjYnkrSWlQS2d6CkdjLzFwMFVtNC8xNHhrNEFteHRwV2JaR2F6K2lpai9BMzlIemR2L1VjR1RZMWo1aUo2YUtaTGZwQW9HQkFNbmIKSlc4WnE0NU42R0FFOTJudmRVTTkycTBYSTcwMzg1K1NDQXZ0WXhCUDRVNmRIQU5JTUJHYVhIZDBYeVd0cVZ2awpKUWlLOUlmM01WOXkxRUN0K0lGRlZ3MjhNcmYxZDkwZ1c0KzJZQnFoRFhOMUpuRk5KOWwwbE93LzFuenZ3MTQ1CmRkV2liTGR5cWlDdGdrV3ZXK3YzV0pjcUFsVm5zaXI0R21wdDBvSFRBb0dBYjQwMTJhL21LcElNTWZBaHh0OHEKNis2QkRFalAwbGxIQ3NNK1JxMXFoZzg0Y1o2VnFNRWI1cHNHTVVjZ1ppcXN5RmRrdEhTdVh2VFcyWUhXWEwyaApLSk5PL293cWEzMUpKK0NrWDZMQUR2OUcybEhISjBoMEdPMGF5SmliSW9pallsSCtxNVlWSEVxd2pXaHNFKy9ICndNVElneUNNN0dzZDYyRnJPbHIrNi9rQ2dZQTRHWVhQMk15TElpL2c3OEJyV3JlMlZteCtDcDVPS2t5MUhucksKQmRHd2FPTHZYRTY2d3NkSlBTTlJ0Ni94NHMvYzBBMVMwSHVoaGh2Y3NTYzRTcUYwRy9kVHcrZzhwQ1lKK01JNQpzTEFJOXBXc2J2U2VMSmxVb0VmN1dNcWRzbTBUdE5pQTVVRmR3cXB4cG9jOElyNWpXRHp3MWlZTDRtUHIrVVF1CkxCT0RMUUtCZ1FEenFXeHBPc0VwOTNkTDRNUGtVaHFkLzd1SnlHV0RzdlFDRlR2YUZFcDRsZndRR1d0blFkR0UKNFlGWndGZjA5WDhBN0k1L2x0Qi9obnBKWHZXU2ozMmZOUFNOb2U0Rk4yOEhBUXo1Nzh0ak1XTXNHaTAyQm0xVgp3Q1NQY2U2WmxaOVQyQzIyWElhM0tEREMrWkU4NTk5bXFyd0orOFI3clVWdWltWWlBUi9Ga1E9PQotLS0tLUVORCBSU0EgUFJJVkFURSBLRVktLS0tLQo=',
    'uid': 'b5e94c7f-3f35-450f-a87a-4a3f1f40a0a0',
}

url_error = URL_DJANGO + 'api/error/'


def catch_error(func):
    def wrapper(*args, **kwargs):
        try:
            res = func(*args, **kwargs)
            return res
        except Exception as e:
            data = {
                'error_class': str(type(e)),
                'target': func.__name__,
                'text': str(e),
            }
            r = requests.post(url_error, json=data)
            pass
    return wrapper


@catch_error
def adds_bd():
    return requests.get(URL_DJANGO + 'get/ids/gar/trades/').json()


@catch_error
def create_bd_gar_trade(jwt, info_trade):
    trade_detail = get_trade_detail(jwt, info_trade['id'])
    body_create_trade = {
        'id': str(info_trade['id']),
        'gar_advert': trade_detail['ad']['id'],
        'cryptocurrency': 'RUB',
        'cryptocurrency_amount': str(info_trade['amount']),
        'currency': 'RUB',
        'currency_amount': str(info_trade['volume']),
        'card_number': 'aaaaaaaa',
        'paymethod': 443 if 'Тинькофф' in trade_detail['ad']['payment_method'] else 3547,
        'partner': info_trade['seller'],
        'status': info_trade['state'], ###########################################################################
        'date_created': datetime.datetime.strptime(info_trade['created_at'].split('+')[0],
                                                   '%Y-%m-%dT%H:%M:%S').timestamp(),
        'date_closed': None if not info_trade['completed_at'] else datetime.datetime.strptime(
            info_trade['completed_at'].split('+')[0], '%Y-%m-%dT%H:%M:%S').timestamp(),
    }

    a = requests.post(URL_DJANGO + 'create/garantex/trade/', json=body_create_trade)


@catch_error
def update_bd_gar_trade(info_trade):
    body_update_trade = {
        'id': str(info_trade['id']),
        'card_number': info_trade['payment_details'] if info_trade['payment_details'] else 'no payment details',
        'status': info_trade['state'],
        'date_closed': None if not info_trade['completed_at'] else datetime.datetime.strptime(
            info_trade['completed_at'].split('+')[0], '%Y-%m-%dT%H:%M:%S').timestamp(),
    }
    print(body_update_trade)
    a = requests.post(URL_DJANGO + 'update/gar/trade/', json=body_update_trade)


def update_trades_garantex(private_key, uid):
    print(datetime.datetime.now(), '   update_trades_garantex')
    JWT = get_jwt(private_key, uid)
    trades_from_garantex = get_trades(JWT)
    trades_from_bd = adds_bd()
    for gar_trade in trades_from_garantex:
        print(gar_trade)
        if gar_trade['state'] == 'waiting':
            accept_trade(JWT, gar_trade['id'])
        if str(gar_trade['id']) not in trades_from_bd:
            create_bd_gar_trade(JWT, gar_trade)
        time_create_gar_trade = datetime.datetime.strptime(gar_trade['created_at'].split('+')[0],
                                                           "%Y-%m-%dT%H:%M:%S").timestamp()
        time_now = datetime.datetime.now().timestamp()
        if time_now - time_create_gar_trade < 7200:
            req_trade_info_from_bd = requests.get(URL_DJANGO + f'gar/trade/detail/{gar_trade["id"]}/')
            if req_trade_info_from_bd.status_code == 200:
                trade_info_from_bd = req_trade_info_from_bd.json()
                limit_close = trade_info_from_bd['gar_trade']['time_close'] * 60
                if time_now - time_create_gar_trade > limit_close and gar_trade['state'] == 'pending' and not \
                        trade_info_from_bd['gar_trade']['agent']:
                    cancel_trade_flag = cancel_trade(JWT, gar_trade['id'])
                    body_update_trade = {
                        'id': str(gar_trade['id']),
                        'status': 'time_cancel',
                    }
                    if cancel_trade_flag:
                        req_update_cancel = requests.post(URL_DJANGO + 'update/gar/trade/', json=body_update_trade)
                    print(gar_trade)
            update_bd_gar_trade(gar_trade)
