import json
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QHBoxLayout, QPushButton, QVBoxLayout, QWidget

from core.appstate import AppState
from core.data_manager import DataManager
from core.settings import Settings
from repos.product_materials_repo import ProductMaterialsRepo
from ui.containers.inputs_container import InputsContainer
from ui.views.tree_widget import TreeWidget


class ProdMatWidget(QWidget):
    data_changed = Signal()

    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.TABLE_NAME = "product_materials"
        self.data_manager = DataManager()

        self.column_info = self.get_column_names()
        self.COLUMN_NAMES = list(self.column_info.keys())

        self.tree = TreeWidget()
        self.inputs = InputsContainer(self)

        self.add_btn = QPushButton("Add")
        self.delete_btn = QPushButton("Delete")

        self.add_btn.clicked.connect(self.insert_values)
        self.delete_btn.clicked.connect(self.delete_values)

        self.master_layout = QVBoxLayout()
        self.buttons_layout = QHBoxLayout()

        self.buttons_layout.addWidget(self.add_btn)
        self.buttons_layout.addWidget(self.delete_btn)

        self.master_layout.addWidget(self.inputs)
        self.master_layout.addLayout(self.buttons_layout)
        self.master_layout.addWidget(self.tree)

        self.setLayout(self.master_layout)

        self.inputs.update_combos()

    def get_column_names(self):
        with open("src/table_info.json") as f:
            map = json.load(f)
        return map[self.TABLE_NAME]["columns"]

    def insert_values(self):
        self.inputs.insert_data()

        self.data_changed.emit()
        self.tree.load()

    def delete_values(self):
        items = self.tree.selectedItems()
        records_to_delete = []

        for item in items:
            parent = item.parent()

            if parent is not None:
                pro_code = parent.text(0)
                mat_code = item.text(0)
                records_to_delete = [
                    record
                    for record in list(AppState.product_materials.values())
                    if record.pro_code == pro_code and record.mat_code == mat_code
                ]
            else:
                pro_code = item.text(0)
                records_to_delete = [
                    record
                    for record in list(AppState.product_materials.values())
                    if record.pro_code == pro_code
                ]

        repo = ProductMaterialsRepo(Settings.DB_PATH)
        for record in records_to_delete:
            repo.delete(record)

        self.data_changed.emit()
        self.data_manager.refresh_all()
        self.tree.load()
