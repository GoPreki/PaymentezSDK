from dataclasses import dataclass
from paymentez.models.user import SimpleUser
from paymentez.models.order import Transaction


@dataclass
class Payment:
    application_code: str
    commerce_merchant_id: str
    user: SimpleUser
    transaction: Transaction

    @staticmethod
    def from_dict(res: dict) -> 'Payment':
        return Payment(
            application_code=res.get('application').get('code'),
            commerce_merchant_id=res.get('commerce').get('merchant_id'),
            user=SimpleUser.from_dict(res.get('user')),
            transaction=Transaction.from_dict(res.get('transaction')),
        )
