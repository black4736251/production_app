from dataclasses import dataclass, field
from decimal import Decimal
import datetime


@dataclass(frozen=True)
class ProductRecord:
    code: str
    name: str
    category: str
    base_unit: str
    unit_price: Decimal
    created_at: datetime.date = field(default_factory=datetime.date.today)
    updated_at: datetime.date = field(default_factory=datetime.date.today)


@dataclass(frozen=True)
class ProductView(ProductRecord):
    quantity: int = 0
    production_cost: Decimal = Decimal("0.00")
