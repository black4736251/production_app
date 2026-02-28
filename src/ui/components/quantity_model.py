from typing import Any
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt
from ui.components.base_entity_model import BaseEntityModel


class StockQuantityModel(BaseEntityModel):
    def data(self, index, role: int = Qt.ItemDataRole.DisplayRole) -> Any:
        if role == Qt.ItemDataRole.DisplayRole:
            return super().data(index, role)

        if role == Qt.ItemDataRole.ForegroundRole:
            key = self._keys[index.column()]
            if key == "quantity":
                val = self._data[index.row()].get("quantity", 0)
                min_val = 10
                if val <= min_val:
                    return QColor("red")

        return super().data(index, role)
