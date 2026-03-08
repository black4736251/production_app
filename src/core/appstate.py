from models import (
    ProductView,
    Client,
    Supplier,
    MaterialView,
    MovementInView,
    MovementOutView,
    ProductionLineView,
    ProductMaterials,
)


class AppState:
    products: dict[str, ProductView] = {}
    clients: dict[str, Client] = {}
    suppliers: dict[str, Supplier] = {}
    materials: dict[str, MaterialView] = {}
    movements_in: dict[str, MovementInView] = {}
    movements_out: dict[str, MovementOutView] = {}
    production_line: dict[str, ProductionLineView] = {}
    product_materials: dict[str, ProductMaterials] = {}
