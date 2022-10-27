from dataclasses import dataclass
from typing import Optional


@dataclass
class Country:
    country: Optional[str]
    currency: Optional[str]
