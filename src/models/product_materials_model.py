from dataclasses import dataclass, field
from itertools import count

_id_counter = count(1)


@dataclass(frozen=True)
class ProductMaterials:
    pro_code: str
    mat_code: str
    quantity: int
    nr: int = field(default_factory=lambda: next(_id_counter))
