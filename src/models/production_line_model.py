from dataclasses import dataclass, field
import datetime
from decimal import Decimal
from itertools import count

_id_counter = count(1)


@dataclass(frozen=True)
class ProductionLineRecord:
    nr: int
    pro_code: str
    quantity: int
    nr: int = field(default_factory=lambda: next(_id_counter))
    created_at: datetime.date = field(default_factory=datetime.date.today)
    updated_at: datetime.date = field(default_factory=datetime.date.today)


@dataclass(frozen=True)
class ProductionLineView(ProductionLineRecord):
    total_cost: Decimal = Decimal("0.00")
