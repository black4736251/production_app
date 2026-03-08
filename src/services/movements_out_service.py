from core.appstate import AppState
from models.movement_out_model import MovementOutRecord


class MovementsOutService:
    def __init__(self) -> None:
        self.appstate = AppState()
        self.products = self.appstate.products

    # checks if the quantity after the movement is above 0
    def is_movement_allowed(self, record) -> bool:
        if not isinstance(record, MovementOutRecord):
            return True

        product = self.products[record.pro_code]
        resulting_quantity = product.quantity - int(record.quantity)
        if resulting_quantity < 0:
            return False

        return True
