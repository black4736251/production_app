from PySide6.QtSql import QSqlQuery
from PySide6.QtWidgets import QLineEdit, QComboBox
from PySide6.QtCore import QRegularExpression
from PySide6.QtGui import QRegularExpressionValidator, QDoubleValidator

from models import ClientType, SupplierType, ProductCategory, MaterialCategory, BaseUnit


class InputFactory:
    @staticmethod
    def create_widget(field_conf: dict):
        itype = field_conf.get("input_type")

        match itype:
            case "line_edit":
                w = QLineEdit()
                match field_conf.get("data_type"):
                    case "uppercase":
                        w.textChanged.connect(lambda: w.setText(w.text().upper()))
                    case "string":
                        regex = QRegularExpression(r"[A-Za-z\-\ \á\à\ã\â]+")
                        w.setValidator(QRegularExpressionValidator(regex))
                    case "integer":
                        regex = QRegularExpression(r"\d+")
                        w.setValidator(QRegularExpressionValidator(regex))
                    case "float":
                        w.setValidator(QDoubleValidator(bottom=0, decimals=2))
                    case "uppercase_only":
                        regex = QRegularExpression(r"[A-Z0-9]+")
                        w.setValidator(QRegularExpressionValidator(regex))
                w.setMaxLength(field_conf.get("max_len", 0))
                return w

            case "combo_box":
                w = QComboBox()
                items = []
                match field_conf.get("enum"):
                    case "client_type":
                        items = [item.value for item in ClientType]
                    case "supplier_type":
                        items = [item.value for item in SupplierType]
                    case "material_category":
                        items = [item.value for item in MaterialCategory]
                    case "product_category":
                        items = [item.value for item in ProductCategory]
                    case "base_unit":
                        items = [item.value for item in BaseUnit]
                    case _:
                        items = []

                w.addItems(items)
                return w

        return QLineEdit()
