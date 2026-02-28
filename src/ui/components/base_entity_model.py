from PySide6.QtCore import QPersistentModelIndex, Qt, QAbstractTableModel, QModelIndex


class BaseEntityModel(QAbstractTableModel):
    def __init__(self, data=None, headers=None):
        super().__init__()
        self._data = data or []
        self._headers = headers or {}
        self._keys = list(self._headers.keys())

    def rowCount(
        self, parent: QModelIndex | QPersistentModelIndex = QModelIndex()
    ) -> int:
        return len(self._data)

    def columnCount(
        self, parent: QModelIndex | QPersistentModelIndex = QModelIndex()
    ) -> int:
        return len(self._keys)

    def data(self, index, role: int = Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None

        item = self._data[index.row()]
        key = self._keys[index.column()]
        value = item.get(key)

        if role == Qt.ItemDataRole.DisplayRole:
            if isinstance(value, float):
                return f"{value:.2f}€".replace(".", ",")
            return str(value) if value is not None else ""

        return None

    def headerData(
        self,
        section: int,
        orientation: Qt.Orientation,
        role: int = Qt.ItemDataRole.DisplayRole,
    ):
        if (
            role == Qt.ItemDataRole.DisplayRole
            and orientation == Qt.Orientation.Horizontal
        ):
            return list(self._headers.values())[section]
        return None
