from core.appstate import AppState
from models.production_line_model import ProductionLineRecord


class ProductionLineService:
    def __init__(self) -> None:
        self.appstate = AppState()
        self.materials = self.appstate.materials
        self.product_materials = list(self.appstate.product_materials.values())

    # checks if the materials' quantities are above 0 after production
    def is_production_valid(self, record) -> bool:
        if not isinstance(record, ProductionLineRecord):
            return True

        product_materials = [
            pm for pm in self.product_materials if pm.pro_code == record.pro_code
        ]
        materials = [self.materials[pm.mat_code] for pm in product_materials]

        needed_quantity = {}
        for pm, m in zip(product_materials, materials):
            needed_quantity[m] = pm.quantity * int(record.quantity)

        for m, q in needed_quantity.items():
            if m.quantity < q:
                return False

        return True
