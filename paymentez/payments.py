from paymentez.models.order import PaymentMethod, Order
from paymentez.models.user import BankUser
from paymentez.models.payment import Payment
from paymentez.utils.requests import get, post


def create_bank_payment(id: PaymentMethod, bank_code: str, response_url: str, user: BankUser, order: Order):
    body = {
        'carrier': {
            'id': id.value,
            'extra_params': {
                'bank_code': bank_code,
                'response_url': response_url,
                'user': {
                    'name': user.name,
                    'fiscal_number': user.fiscal_number,
                    'type': user.type.value,
                    'type_fis_number': user.type_fis_number.value,
                    'ip_address': user.ip_address,
                }
            }
        },
        'user': {
            'id': user.id,
            'email': user.email,
        },
        'order': order.to_dict(),
    }

    return post(path='/order/', body=body)


def get_payment(order_id: str) -> Payment:
    res = get(path='/order/{order_id}', path_params={'order_id': order_id})

    return Payment.from_dict(res)
