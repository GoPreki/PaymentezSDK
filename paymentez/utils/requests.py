import requests
import time
import hashlib
from base64 import b64encode

from urllib.parse import quote
from paymentez.utils.exceptions import PaymentezErrorCode, PaymentezException


class Keys:
    SERVER_APPLICATION_CODE = None
    SECRET_KEY = None

    TEST: bool = True


def get_base_url():
    _prefix = '-stg' if Keys.TEST else ''
    return f'https://noccapi{_prefix}.paymentez.com'


def form_headers() -> dict:
    if not Keys.SERVER_APPLICATION_CODE or not Keys.SECRET_KEY:
        raise PaymentezException(code=PaymentezErrorCode.MISSING_KEYS.value,
                                 message='Keys were not correctly initialized')

    return {
        'Content-Type': 'application/json',
        'User-Agent': 'Preki API',
        'Auth-Token': generate_token(),
    }


def generate_token():
    if not Keys.SERVER_APPLICATION_CODE or not Keys.SECRET_KEY:
        raise PaymentezException(code=PaymentezErrorCode.MISSING_KEYS.value,
                                 message='Keys were not correctly initialized')

    unix_timestamp = str(int(time.time()))
    uniq_token_string = Keys.SECRET_KEY + unix_timestamp
    uniq_token_hash = hashlib.sha256(uniq_token_string).hexdigest()
    auth_token = b64encode('%s;%s;%s' % (
        Keys.SERVER_APPLICATION_CODE, unix_timestamp, uniq_token_hash))

    return auth_token


def generate_stoken(transaction_id: str, app_code: str, user_id: str):
    if not Keys.SECRET_KEY:
        raise PaymentezException(code=PaymentezErrorCode.MISSING_KEYS.value,
                                 message='Keys were not correctly initialized')

    for_md5 = f'{transaction_id}_{app_code}_{user_id}_{Keys.SECRET_KEY}'
    return hashlib.md5(for_md5).hexdigest()


def check_for_errors(req, res):
    if req.status_code >= 400:
        raise PaymentezException(code=req.status_code,
                                 message=res.get('help', 'Unknown Paymentez error occured'),
                                 type=res.get('type'),
                                 description=res.get('description'))


def post(path='', body=None):
    req = requests.post(url=f'{get_base_url()}{path}',
                        json=body, headers=form_headers())
    res = req.json()
    check_for_errors(req, res)
    return res


def delete(path='', body=None):
    req = requests.delete(
        url=f'{get_base_url()}{path}', json=body, headers=form_headers())
    res = req.json()
    check_for_errors(req, res)
    return res


def get(path='', path_params={}, query_params={}):
    for key, value in path_params.items():
        value = quote(value)
        path = path.replace(f'/{{{key}}}', f'/{value}')

    req = requests.get(url=f'{get_base_url()}{path}',
                       headers=form_headers(), params=query_params)
    res = req.json()
    check_for_errors(req, res)
    return res
