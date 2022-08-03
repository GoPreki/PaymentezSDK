from paymentez.utils import requests


def list_banks():
    return requests.get('/banks/PSE')
