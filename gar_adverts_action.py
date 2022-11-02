from garantexAPI.adds import *
from garantexAPI.auth import *
from setting import URL_DJANGO

user = {
    'id': 'SNCE99027726',
    'private_key': 'LS0tLS1CRUdJTiBSU0EgUFJJVkFURSBLRVktLS0tLQpNSUlFcEFJQkFBS0NBUUVBd0M3aWFWWFdTdmR2TVAwRnpzK0NjY0pRdUpuelBaUE5VbGlLUjdLYVE5VWhiY1Z6CmZwTDV0ZGlJemllV2tMT0lSTzNBbFp4RHRSdUJnZTQ0S0RVdVhtZ0svZyt5aE1zSXRILzhXODJiV1g0RVJGdzYKVE1sTlYvRE1PMEFJSllYZHVzcGlmd3E3NzROVTVxeFdqcER2ZVA5SnlDSUQvM2hQTG82KzdBVlFiMVhLS3I0ZgppVnZSa2xhNjl0dHQ5T1pOUWkxdWpSbFBsYjVrVnRsS05vV0RmcFJKaFQ4SjlWc1crQjRSZ3ZRYnBmakFlSWNQCnNISUE2c2pGR3RvaGNtOFIxM2VuVDlzbW40MW9XZDBUMnVhUGRyNlg3RHR0OTBZdUVPUEcvaGZJcGZhYmhqSlUKdEFjK2RCQWFMMTZGZ0N6TGFWc01BYmZMTVM4OGhkTm40OUgrQ3dJREFRQUJBb0lCQVFDYmlKWW1KNWpoWFBUNQpFWjBVcmEzbFFSeXcrYTc0dzloa2IxR2lDdko4T1UzdmwrQUxyUWs0MlVDR2oxVjBVRWZWZVJEbVErd3I4MUhSCmhLaWdLY0lZRjEzbUZYQWx0bWVhSlFab2liTFRMNEJtanJtRUVWcHQ5R3hrKzBKY2s4VkorYWJUS0MzRy9tUEUKdCs3cFBIVUNXS0V1dmhDOFBYTGZ2Qmpaek1jM0FpK1gyWWk0dWRUbWQ1OUUwUjhFM1pRWW44UWxyVng1TXNmTApBRVFZajJIOTdIQW1CdXZBcDJBcGc4L2VtTmVJVVM1RFRwK2crc3NnaGdYSFR4aTZCZ2Q1YkNYZDFMSnRTbEw2CndabW9aMm5VVzYxZUd5SG9uSmg2ZzZBMk93WXFBako4UzMxcTJ1SFNvVDJ5ZFp1bFN6SGZteCtkQU5WZjNiT0QKVEFHcmRicXhBb0dCQVBPN2gzSVpXTk5CRE1iQ20yak9hM3FoaVlLYkxnbXdFMG4wd3BNZWx4eW1KRkJqbkl3aApVMFZyeXRCZytCbHMrS2tHR0I0dzAydDlEdUVJZ2c2N0hYam1GK1ZtQmpGN1pIajRTNVlQSTFjYnkrSWlQS2d6CkdjLzFwMFVtNC8xNHhrNEFteHRwV2JaR2F6K2lpai9BMzlIemR2L1VjR1RZMWo1aUo2YUtaTGZwQW9HQkFNbmIKSlc4WnE0NU42R0FFOTJudmRVTTkycTBYSTcwMzg1K1NDQXZ0WXhCUDRVNmRIQU5JTUJHYVhIZDBYeVd0cVZ2awpKUWlLOUlmM01WOXkxRUN0K0lGRlZ3MjhNcmYxZDkwZ1c0KzJZQnFoRFhOMUpuRk5KOWwwbE93LzFuenZ3MTQ1CmRkV2liTGR5cWlDdGdrV3ZXK3YzV0pjcUFsVm5zaXI0R21wdDBvSFRBb0dBYjQwMTJhL21LcElNTWZBaHh0OHEKNis2QkRFalAwbGxIQ3NNK1JxMXFoZzg0Y1o2VnFNRWI1cHNHTVVjZ1ppcXN5RmRrdEhTdVh2VFcyWUhXWEwyaApLSk5PL293cWEzMUpKK0NrWDZMQUR2OUcybEhISjBoMEdPMGF5SmliSW9pallsSCtxNVlWSEVxd2pXaHNFKy9ICndNVElneUNNN0dzZDYyRnJPbHIrNi9rQ2dZQTRHWVhQMk15TElpL2c3OEJyV3JlMlZteCtDcDVPS2t5MUhucksKQmRHd2FPTHZYRTY2d3NkSlBTTlJ0Ni94NHMvYzBBMVMwSHVoaGh2Y3NTYzRTcUYwRy9kVHcrZzhwQ1lKK01JNQpzTEFJOXBXc2J2U2VMSmxVb0VmN1dNcWRzbTBUdE5pQTVVRmR3cXB4cG9jOElyNWpXRHp3MWlZTDRtUHIrVVF1CkxCT0RMUUtCZ1FEenFXeHBPc0VwOTNkTDRNUGtVaHFkLzd1SnlHV0RzdlFDRlR2YUZFcDRsZndRR1d0blFkR0UKNFlGWndGZjA5WDhBN0k1L2x0Qi9obnBKWHZXU2ozMmZOUFNOb2U0Rk4yOEhBUXo1Nzh0ak1XTXNHaTAyQm0xVgp3Q1NQY2U2WmxaOVQyQzIyWElhM0tEREMrWkU4NTk5bXFyd0orOFI3clVWdWltWWlBUi9Ga1E9PQotLS0tLUVORCBSU0EgUFJJVkFURSBLRVktLS0tLQo=',
    'uid': 'b5e94c7f-3f35-450f-a87a-4a3f1f40a0a0',
}


def adds_bd():
    return requests.get(URL_DJANGO + 'get/ids/gar/adverts/').json()


def create_bd_gar_add(user, info_trade):
    body_create_advert = {
        'advert_id': info_trade['id'],
        'price': float(info_trade['price']),
        'paymethod': 443 if info_trade['payment_method'] == 'Тинькофф' else 3547,
        'is_active': info_trade['active'],
        'user': user['id'],
        'description': info_trade['description'],
        'direction': info_trade['direction'],
        'date_created': datetime.datetime.strptime(info_trade['created_at'].split('+')[0], '%Y-%m-%dT%H:%M:%S').timestamp(),
        'date_edited': datetime.datetime.strptime(info_trade['edited_at'].split('+')[0], '%Y-%m-%dT%H:%M:%S').timestamp(),
    }

    a = requests.post(URL_DJANGO + 'create/garantex/advert/', json=body_create_advert)


def update_bd_gar_advert(info_trade):
    body_update_advert = {
        'advert_id': info_trade['id'],
        'price': float(info_trade['price']),
        'paymethod': 443 if info_trade['payment_method'] == 'Тинькофф' else 3547,
        'is_active': info_trade['active'],
        'description': info_trade['description'],
        'direction': info_trade['direction'],
        'date_created': datetime.datetime.strptime(info_trade['created_at'].split('+')[0], '%Y-%m-%dT%H:%M:%S').timestamp(),
        'date_edited': datetime.datetime.strptime(info_trade['edited_at'].split('+')[0], '%Y-%m-%dT%H:%M:%S').timestamp(),
    }

    a = requests.post(URL_DJANGO + 'update/garantex/advert/', json=body_update_advert)


def update_adverts_garantex(garantex_user):
    JWT = get_jwt(garantex_user['private_key'], garantex_user['uid'])
    adds_from_garantex = get_adds(JWT)
    adds_from_bd = adds_bd()
    for gar_add in adds_from_garantex:
        if str(gar_add['id']) not in adds_from_bd:
            create_bd_gar_add(garantex_user, gar_add)
        else:
            update_bd_gar_advert(gar_add)


update_adverts_garantex(user)




