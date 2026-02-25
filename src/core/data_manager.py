from core.appstate import AppState
from repos.client_repo import ClientRepo
from repos.product_repo import ProductRepo
from repos.production_line_repo import ProductionLineRepo
from repos.supplier_repo import SupplierRepo
from repos.material_repo import MaterialRepo
from repos.movement_out_repo import MovementOutRepo
from repos.movement_in_repo import MovementInRepo
from repos.product_materials_repo import ProductMaterialsRepo
from core.settings import Settings


class DataManager:
    def __init__(self, state: AppState):
        self.state = state

        self.client_repo = ClientRepo(Settings.DB_PATH)
        self.supplier_repo = SupplierRepo(Settings.DB_PATH)
        self.material_repo = MaterialRepo(Settings.DB_PATH)
        self.product_repo = ProductRepo(Settings.DB_PATH)
        self.movement_in_repo = MovementInRepo(Settings.DB_PATH)
        self.movement_out_repo = MovementOutRepo(Settings.DB_PATH)
        self.production_line_repo = ProductionLineRepo(Settings.DB_PATH)
        self.product_materials_repo = ProductMaterialsRepo(Settings.DB_PATH)

    def refresh_all(self):
        self.state.clients = self.client_repo.get_all()
        self.state.suppliers = self.supplier_repo.get_all()
        self.state.materials = self.material_repo.get_all()
        self.state.products = self.product_repo.get_all()
        self.state.movements_in = self.movement_in_repo.get_all()
        self.state.movements_out = self.movement_out_repo.get_all()
        self.state.production_line = self.production_line_repo.get_all()
        self.state.product_materials = self.product_materials_repo.get_all()
