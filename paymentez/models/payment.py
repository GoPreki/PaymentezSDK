from dataclasses import dataclass
from paymentez.models.user import BaseUser
from paymentez.models.order import Transaction


@dataclass
class Payment:
    application_code: str
    commerce_merchant_id: str
    user: BaseUser
    transaction: Transaction

    @staticmethod
    def from_dict(res: dict) -> 'Payment':
        return Payment(
            application_code=res['application']['code'],
            commerce_merchant_id=res['commerce']['merchant_id'],
            user=BaseUser.from_dict(res['user']),
            transaction=Transaction.from_dict(res['transaction']),
        )
