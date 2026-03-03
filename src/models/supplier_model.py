from dataclasses import dataclass, field
from typing import Optional
import datetime


@dataclass(frozen=True)
class Supplier:
    code: str
    first_name: str
    last_name: str
    sup_type: str
    company_name: Optional[str]
    country: str
    city: str
    phone: str
    email: str
    date_of_birth: datetime.date
    tax_id: str
    created_at: datetime.date = field(default_factory=datetime.date.today)
    updated_at: datetime.date = field(default_factory=datetime.date.today)
