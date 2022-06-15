from dataclasses import dataclass
from enum import Enum


class TypeUser(Enum):
    NATURAL = 'N'
    LEGAL = 'J'


class TypeFiscalNumber(Enum):
    CC = 'CC'
    CE = 'CE'
    NIT = 'NIT'
    TI = 'TI'
    PP = 'PP'
    IDC = 'IDC'
    CEL = 'CEL'
    RC = 'RC'
    DE = 'DE'


@dataclass
class BaseUser:
    id: str
    email: str
    name: str

    @staticmethod
    def from_dict(res: dict) -> 'BaseUser':
        return BaseUser(
            id=res['id'],
            email=res['email'],
            name=res['name'],
        )


@dataclass
class BankUser(BaseUser):
    fiscal_number: str
    type: TypeUser
    type_fis_number: TypeFiscalNumber
    ip_address: str
