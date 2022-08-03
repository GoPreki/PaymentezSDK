from enum import Enum
from dataclasses import dataclass
from paymentez.models.country import Country
from typing import Optional, Union
from paymentez.utils import optional_dict
from paymentez.utils.dates import isoformat_to_timestamp


class PaymentStatus(Enum):
    PENDING = 'pending'
    APPROVED = 'approved'
    FAILURE = 'failure'
    CANCELLED = 'cancelled'


class BankStatus(Enum):
    PENDING = 'PENDING'
    APPROVED = 'APPROVED'
    FAILURE = 'FAILURE'


class PaymentMethod(Enum):
    PSE = 'PSE'


@dataclass
class Order:
    country: Country
    amount: Union[int, float]
    description: str
    dev_reference: Optional[str]
    vat: Optional[Union[int, float]]

    def to_dict(self) -> dict:
        return optional_dict(country=self.country.country,
                             currency=self.country.currency,
                             dev_reference=self.dev_reference,
                             amount=self.amount,
                             vat=self.vat,
                             description=self.description)

    @staticmethod
    def from_dict(res: dict) -> 'Order':
        return Order(
            country=Country(res.get('country'), res.get('currency')),
            dev_reference=res.get('dev_reference'),
            amount=res.get('amount'),
            vat=res.get('vat'),
            description=res['description'],
        )


@dataclass
class Transaction(Order):
    paid_date: float
    status: PaymentStatus
    id: str
    bank_url: str
    status_bank: BankStatus
    trazability_code: str
    ticket_id: int

    def to_dict(self) -> dict:
        return {
            **super().to_dict(),
            **optional_dict(paid_date=self.paid_date,
                            status=self.status,
                            id=self.id,
                            bank_url=self.bank_url,
                            status_bank=self.status_bank,
                            trazability_code=self.trazability_code,
                            ticket_id=self.ticket_id)
        }

    @staticmethod
    def from_dict(res: dict) -> 'Transaction':
        order = Order.from_dict(res)
        return Transaction(
            country=order.country,
            amount=order.amount,
            description=order.description,
            dev_reference=order.dev_reference,
            vat=order.vat,
            paid_date=isoformat_to_timestamp(res['paid_date']) if res.get('paid_date') else '',
            status=res.get('status'),
            id=res.get('id'),
            bank_url=res.get('bank_url'),
            status_bank=res.get('status_bank'),
            trazability_code=res.get('trazability_code'),
            ticket_id=res.get('ticket_id'),
        )
