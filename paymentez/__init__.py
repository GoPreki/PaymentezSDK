from paymentez.utils.requests import Keys


def init(server_application_code, secret_key, test: bool):
    Keys.SERVER_APPLICATION_CODE = server_application_code
    Keys.SECRET_KEY = secret_key
    Keys.TEST = test
