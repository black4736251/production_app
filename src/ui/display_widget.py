from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QMessageBox,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
)
import json

from core.data_manager import DataManager
from ui.containers.inputs_container import InputsContainer
from ui.views.list_widget import ListWidget
from ui.views.table_widget import TableWidget
from core.settings import Settings
from core.appstate import AppState
from repos import (
    ClientRepo,
    SupplierRepo,
    ProductionLineRepo,
    ProductMaterialsRepo,
    ProductRepo,
    MaterialRepo,
    MovementInRepo,
    MovementOutRepo,
)


class DisplayWidget(QWidget):
    data_changed = Signal()
    MAPPING = {
        "clients": (ClientRepo),
        "suppliers": (SupplierRepo),
        "materials": (MaterialRepo),
        "products": (ProductRepo),
        "movements_in": (MovementInRepo),
        "movements_out": (MovementOutRepo),
        "production_line": (ProductionLineRepo),
        "product_materials": (ProductMaterialsRepo),
    }

    def __init__(self, table_name):
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.TABLE_NAME = table_name
        self.data_manager = DataManager()

        self.column_info = self.get_column_names()
        self.COLUMN_NAMES = list(self.column_info.keys())

        self.table = TableWidget(self)
        self.list = ListWidget(self)
        self.inputs = InputsContainer(self)

        self.table.updated.connect(self.data_changed.emit)
        self.list.updated.connect(self.data_changed.emit)
        self.inputs.data_inserted.connect(self.table.load)

        self.add_btn = QPushButton("Adicionar")
        self.delete_btn = QPushButton("Remover")

        self.add_btn.clicked.connect(self.insert_values)
        self.delete_btn.clicked.connect(self.delete_values)

        self.switch_to_list = QPushButton("Vista de lista")
        self.switch_to_list.clicked.connect(self.toggle_view)
        self.switch_to_list.setFixedWidth(100)

        self.switch_to_table = QPushButton("Vista de tabela")
        self.switch_to_table.setDisabled(True)
        self.switch_to_table.clicked.connect(self.toggle_view)
        self.switch_to_table.setFixedWidth(100)

        self.master_layout = QVBoxLayout()
        self.toggle_layout = QHBoxLayout()
        self.buttons_layout = QHBoxLayout()

        self.toggle_layout.addWidget(self.switch_to_table)
        self.toggle_layout.addWidget(self.switch_to_list)
        self.toggle_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.buttons_layout.addWidget(self.add_btn)
        self.buttons_layout.addWidget(self.delete_btn)

        self.master_layout.addLayout(self.toggle_layout)
        self.master_layout.addWidget(self.inputs)
        self.master_layout.addLayout(self.buttons_layout)

        self.master_layout.addWidget(self.table)
        self.master_layout.addWidget(self.list)
        self.list.hide()

        self.setLayout(self.master_layout)

        self.table.load()
        self.inputs.update_combos()

    def update_views(self):
        self.table.load()
        self.list.load()

    def insert_values(self):
        self.inputs.insert_data()

        self.table.load()
        self.list.load()
        self.data_changed.emit()

    def delete_values(self):
        id = ""
        if not self.switch_to_table.isEnabled():
            selection = self.table.selectionModel()
            if not selection.hasSelection():
                QMessageBox.warning(
                    self,
                    "A seleção está vazia",
                    "Selecione alguma linha para a eliminar.",
                )
                return

            rows = selection.selectedRows()
            for index in rows:
                row = index.row()
                id = self.table.model().index(row, 0).data()
        else:
            selection = self.list.selectionModel()
            if not selection.hasSelection():
                QMessageBox.warning(
                    self,
                    "A seleção está vazia",
                    "Selecione alguma linha para a eliminar.",
                )
                return

            items = self.list.selectedItems()
            for item in items:
                id = item.data(Qt.ItemDataRole.UserRole)

        table_attr = getattr(AppState, self.TABLE_NAME, None)

        if table_attr is not None:
            record = table_attr[id]
        else:
            raise Exception("Failed to get data")

        if record is not None:
            repo_class = self.MAPPING[self.TABLE_NAME]
            repo = repo_class(Settings.DB_PATH)
            repo.delete(record)

        self.data_manager.refresh_all()
        self.table.load()
        self.list.load()
        self.data_changed.emit()

    def toggle_view(self):
        if self.switch_to_table.isEnabled():
            self.switch_to_table.setDisabled(True)
            self.list.hide()
            self.switch_to_list.setDisabled(False)
            self.table.show()
        else:
            self.switch_to_list.setDisabled(True)
            self.table.hide()
            self.switch_to_table.setDisabled(False)
            self.list.show()

    def get_column_names(self):
        with open("src/table_info.json", encoding="utf-8") as f:
            map = json.load(f)
        return map[self.TABLE_NAME]["columns"]
