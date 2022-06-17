from dataclasses import dataclass
from enum import Enum
from paymentez.models.order import PaymentStatus
from paymentez.utils.exceptions import PaymentezErrorCode, PaymentezException
from paymentez.utils.requests import Keys
import hashlib

class WebHookPaymentStatus(Enum):
    PENDING = '0'
    APPROVED = '1'
    CANCELLED = '2'
    REJECTED = '4'
    EXPIRED = '5'

WEBHOOK_PAYMENT_STATUS = {
    WebHookPaymentStatus.PENDING.value: PaymentStatus.PENDING,
    WebHookPaymentStatus.APPROVED.value: PaymentStatus.APPROVED,
    WebHookPaymentStatus.CANCELLED.value: PaymentStatus.CANCELLED,
    WebHookPaymentStatus.REJECTED.value: PaymentStatus.FAILURE,
    WebHookPaymentStatus.EXPIRED.value: PaymentStatus.FAILURE,
}

@dataclass
class Event:
    status: PaymentStatus
    id: str
    order_description: str
    authorization_code: str
    status_detail: str
    date: str
    message: str
    carrier_code: str
    amount: str
    paid_date: str
    stoken: str
    application_code: str
    user_id: str
    user_email: str


    def validate(self) -> bool:
        if not Keys.SECRET_KEY:
            raise PaymentezException(code=PaymentezErrorCode.MISSING_KEYS.value,
                                    message='Keys were not correctly initialized')

        for_md5 = f'{self.id}_{self.application_code}_{self.user_id}_{Keys.SECRET_KEY}'

        m = hashlib.sha256()
        m.update(bytes(for_md5, 'utf-8'))

        return m.hexdigest() == self.stoken

    @staticmethod
    def from_dict(res: dict) -> 'Event':
        return Event(
            status=WEBHOOK_PAYMENT_STATUS[res['transaction']['status']],
            id=res['transaction']['id'],
            order_description=res['transaction']['order_description'],
            authorization_code=res['transaction']['authorization_code'],
            status_detail=res['transaction']['status_detail'],
            date=res['transaction']['date'],
            message=res['transaction']['message'],
            carrier_code=res['transaction']['carrier_code'],
            amount=res['transaction']['amount'],
            paid_date=res['transaction']['paid_date'],
            stoken=res['transaction']['stoken'],
            application_code=res['transaction']['application_code'],
            user_id=res['user']['id'],
            user_email=res['user']['email']
        )
