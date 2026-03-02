from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QComboBox,
    QDateEdit,
    QHBoxLayout,
    QGridLayout,
    QMessageBox,
)
from PySide6.QtSql import QSqlQuery
from core.data_manager import DataManager
from core.settings import Settings
from models import (
    Client,
    Supplier,
    MaterialRecord,
    ProductRecord,
    MovementInRecord,
    MovementOutRecord,
    ProductionLineRecord,
    ProductMaterials,
)
from repos import (
    ClientRepo,
    SupplierRepo,
    MaterialRepo,
    ProductRepo,
    MovementInRepo,
    MovementOutRepo,
    ProductMaterialsRepo,
    ProductionLineRepo,
)
from models.enums import ClientType, SupplierType, MaterialCategory, ProductCategory
from ui.components.input_factory import InputFactory


class InputsContainer(QWidget):
    data_inserted = Signal()

    def __init__(self, master):
        super().__init__()
        self.master = master
        self.data_manager = DataManager()

        self.inputs: list[tuple] = []
        self.relational_combos: list[tuple[str, QComboBox]] = []
        for col_name in self.master.COLUMN_NAMES:
            if self.master.column_info.get(col_name).get("input_type") == "defaulted":
                continue
            input_widget = InputFactory.create_widget(
                self.master.column_info.get(col_name)
            )

            self.inputs.append((QLabel(col_name), input_widget))

        self.grid = QGridLayout()
        row = 0
        col = 0
        for i in range(len(self.inputs)):
            widget = QWidget()

            h_layout = QHBoxLayout()
            h_layout.addWidget(self.inputs[i][0])
            h_layout.addWidget(self.inputs[i][1])
            h_layout.setStretch(0, 1)
            h_layout.setStretch(1, 3)

            widget.setLayout(h_layout)
            self.grid.addWidget(widget, row, col)

            col += 1

            if col >= 3:
                col = 0
                row += 1

        self.setLayout(self.grid)

    def update_combos(self):
        for col_name, input_widget in self.relational_combos:
            input_widget.clear()

            query_str = self.master.column_info[col_name]["values"][1]
            query = QSqlQuery()
            query.exec(query_str)

            values = []
            while query.next():
                values.append(query.value(0))

            input_widget.addItems(values)

    def insert_data(self):
        data = []
        for _, input_field in self.inputs:
            value = ""
            if isinstance(input_field, QLineEdit):
                value = input_field.text()
            elif isinstance(input_field, QComboBox):
                match self.master.TABLE_NAME:
                    case "clients":
                        value = ClientType(input_field.currentText())
                    case "suppliers":
                        value = SupplierType(input_field.currentText())
                    case "materials":
                        value = MaterialCategory(input_field.currentText())
                    case "products":
                        value = ProductCategory(input_field.currentText())
            elif isinstance(input_field, QDateEdit):
                value = input_field.date().toString("dd/MM/yyyy")

            if value != "":
                data.append(value)
            else:
                QMessageBox.warning(
                    self,
                    "Valor vazio",
                    "Confirme que preencheu todos os campos",
                )
                return

        path = Settings.DB_PATH
        match self.master.TABLE_NAME:
            case "clients":
                repo = ClientRepo(path)
                repo.save(Client(*data))
            case "suppliers":
                repo = SupplierRepo(path)
                repo.save(Supplier(*data))
            case "materials":
                repo = MaterialRepo(path)
                repo.save(MaterialRecord(*data))
            case "products":
                repo = ProductRepo(path)
                repo.save(ProductRecord(*data))
            case "movements_in":
                repo = MovementInRepo(path)
                repo.save(MovementInRecord(*data))
            case "movements_out":
                repo = MovementOutRepo(path)
                repo.save(MovementOutRecord(*data))
            case "production_line":
                repo = ProductionLineRepo(path)
                repo.save(ProductionLineRecord(*data))
            case "product_materials":
                repo = ProductMaterialsRepo(path)
                repo.save(ProductMaterials(*data))

        self.data_manager.refresh_all()
        self.data_inserted.emit()
