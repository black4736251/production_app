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
from core.appstate import AppState
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
from ui.components.input_factory import InputFactory


class InputsContainer(QWidget):
    MAPPING = {
        "clients": (ClientRepo, Client),
        "suppliers": (SupplierRepo, Supplier),
        "materials": (MaterialRepo, MaterialRecord),
        "products": (ProductRepo, ProductRecord),
        "movements_in": (MovementInRepo, MovementInRecord),
        "movements_out": (MovementOutRepo, MovementOutRecord),
        "production_line": (ProductionLineRepo, ProductionLineRecord),
        "product_materials": (ProductMaterialsRepo, ProductMaterials),
    }
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

            input_reference = self.master.column_info.get(col_name).get("reference")
            if input_reference and isinstance(input_widget, QComboBox):
                self.relational_combos.append((input_reference, input_widget))
            self.inputs.append(
                (
                    QLabel(self.master.column_info.get(col_name).get("name")),
                    input_widget,
                )
            )

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
        for table, input_widget in self.relational_combos:
            input_widget.clear()

            table_attr = getattr(AppState, table)
            if table_attr:
                input_widget.addItems(tuple(table_attr.keys()))

    def insert_data(self):
        data = []
        table_attr = getattr(AppState, self.master.TABLE_NAME)
        repo_class, record_class = self.MAPPING[self.master.TABLE_NAME]
        if repo_class in (
            ProductMaterialsRepo,
            ProductionLineRepo,
            MovementOutRepo,
            MovementInRepo,
        ):
            data.append(int(list(table_attr.keys())[-1]) + 1)

        for _, input_field in self.inputs:
            value = ""
            if isinstance(input_field, QLineEdit):
                value = input_field.text()
            elif isinstance(input_field, QComboBox):
                value = input_field.currentText()
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

        repo = repo_class(Settings.DB_PATH)
        repo.save(record_class(*data))

        self.data_manager.refresh_all()
        self.data_inserted.emit()
