from dataclasses import astuple, asdict
from PySide6.QtCore import QDate, Qt, Signal
from PySide6.QtWidgets import (
    QComboBox,
    QDateEdit,
    QLabel,
    QLineEdit,
    QVBoxLayout,
    QPushButton,
    QHBoxLayout,
    QWidget,
)
from core.data_manager import DataManager
from core.settings import Settings
from models import (
    Client,
    Supplier,
    MaterialView,
    ProductView,
    MovementInView,
    MovementOutView,
    ProductionLineView,
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

from core.appstate import AppState
from ui.containers.inputs_container import InputsContainer


class PopupContainer(QWidget):
    updated = Signal()

    MAPPING = {
        "clients": (ClientRepo, Client),
        "suppliers": (SupplierRepo, Supplier),
        "materials": (MaterialRepo, MaterialView),
        "products": (ProductRepo, ProductView),
        "movements_in": (MovementInRepo, MovementInView),
        "movements_out": (MovementOutRepo, MovementOutView),
        "production_line": (ProductionLineRepo, ProductionLineView),
        "product_materials": (ProductMaterialsRepo, ProductMaterials),
    }

    def __init__(self, master, row=None, item=None):
        super().__init__()
        self.row = row
        self.item = item
        self.master = master
        self.TABLE_NAME = self.master.TABLE_NAME
        self.COLUMN_NAMES = self.master.COLUMN_NAMES
        self.column_info = self.master.column_info
        self.setWindowFlags(Qt.WindowType.Popup)
        self.hasNr = False
        self.record_old = None
        self.data_manager = DataManager()

        self.inputs_container = InputsContainer(master)
        self.inputs_container.update_combos()

        self.title = QLabel("Edit")
        self.title.setStyleSheet("font: bold 20px")
        self.name_mapping = {
            k[0].text(): v
            for k, v in zip(self.inputs_container.inputs, self.column_info)
        }

        self.start = 0
        if self.TABLE_NAME in ("movements_in", "movements_out", "production_line"):
            self.start = 1
            self.hasNr = True

        if row is not None:
            for i in range(self.start, len(self.inputs_container.inputs) + self.start):
                value = self.master.model().index(row, i).data()
                input_widget = self.inputs_container.inputs[i - self.start][1]

                if isinstance(input_widget, QLineEdit):
                    input_widget.setText(value)
                elif isinstance(input_widget, QComboBox):
                    input_widget.setCurrentText(value)
                elif isinstance(input_widget, QDateEdit):
                    date_ints = value.split(sep="/")
                    d, m, y = date_ints

                    date = QDate()
                    date.setDate(int(y), int(m), int(d))
                    input_widget.setDate(date)

        elif item is not None:
            id = item.data(Qt.ItemDataRole.UserRole)
            self.id = id

            table_attr = getattr(AppState, self.TABLE_NAME)
            self.record_old = astuple(table_attr[id])

            for i in range(self.start, len(self.record_old) - 2 + self.start):
                value = self.record_old[i - self.start]
                input_widget = self.inputs_container.inputs[i - self.start][1]

                if isinstance(input_widget, QLineEdit):
                    input_widget.setText(value)
                elif isinstance(input_widget, QComboBox):
                    input_widget.setCurrentText(value)
                elif isinstance(input_widget, QDateEdit):
                    date_ints = value.split(sep="/")
                    d, m, y = date_ints

                    date = QDate()
                    date.setDate(int(y), int(m), int(d))
                    input_widget.setDate(date)

        self.confirm_btn = QPushButton("Confirm")
        self.cancel_btn = QPushButton("Cancel")

        self.confirm_btn.clicked.connect(self.confirm)
        self.cancel_btn.clicked.connect(lambda: self.hide())

        self.popup_layout = QVBoxLayout()
        self.buttons_layout = QHBoxLayout()

        self.buttons_layout.addWidget(self.confirm_btn)
        self.buttons_layout.addWidget(self.cancel_btn)

        self.popup_layout.addWidget(self.title)
        self.popup_layout.addWidget(self.inputs_container)
        self.popup_layout.addLayout(self.buttons_layout)

        self.setLayout(self.popup_layout)

    def confirm(self):
        col_val = ""
        values = []
        code = ""
        if self.row is not None:
            code = self.master.model().index(self.row, 0).data()
        elif self.item:
            code = self.id

        table_attr = getattr(AppState, self.TABLE_NAME)
        self.record_old = asdict(table_attr[code])

        try:
            values.append(self.record_old["nr"])
        except KeyError:
            pass

        for i in range(len(self.inputs_container.inputs)):
            input_field = self.inputs_container.inputs[i][1]
            col_name = self.name_mapping[self.inputs_container.inputs[i][0].text()]
            value = ""

            if isinstance(input_field, QLineEdit):
                value = input_field.text()
            elif isinstance(input_field, QComboBox):
                value = input_field.currentText()
            elif isinstance(input_field, QDateEdit):
                value = input_field.date().toString("dd/MM/yyyy")

            values.append(value)

            col_val += col_name + " = ?"
            if i < len(self.inputs_container.inputs) - 1:
                col_val += ", "

        table_attr = getattr(AppState, self.master.TABLE_NAME)
        repo_class, record_class = self.MAPPING[self.master.TABLE_NAME]
        record_new = None
        if self.record_old:
            record_new = record_class(created_at=self.record_old["created_at"], *values)

            repo = repo_class(Settings.DB_PATH)
            repo.delete(record_class(**self.record_old))
            repo.save(record_new)

        self.data_manager.refresh_all()
        self.updated.emit()

        self.hide()
