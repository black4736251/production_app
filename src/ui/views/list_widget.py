from PySide6.QtCore import Signal
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QAbstractItemView, QListWidget, QListWidgetItem
from dataclasses import astuple

from ui.containers.data_container import DataContainer
from ui.containers.popup_container import PopupContainer
from core.appstate import AppState


class ListWidget(QListWidget):
    updated = Signal()

    def __init__(self, master):
        super().__init__()
        self.master = master
        self.TABLE_NAME = self.master.TABLE_NAME
        self.COLUMN_NAMES = self.master.COLUMN_NAMES
        self.column_info = self.master.column_info

        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_popup)

        self.load()

    def load(self):
        self.clear()

        table_attr = getattr(AppState, self.TABLE_NAME, None)

        if table_attr is not None:
            data = list(table_attr.values())
        else:
            raise Exception("Failed to get data")

        for record in data:
            record_tuple = astuple(record)
            item = QListWidgetItem(self)
            item.setData(Qt.ItemDataRole.UserRole, record_tuple[0])
            container = DataContainer(self, record_tuple)

            item.setSizeHint(container.sizeHint())
            self.setItemWidget(item, container)

    def show_popup(self, pos):
        item = self.itemAt(pos)
        if not item:
            return

        global_pos = self.viewport().mapToGlobal(pos)

        self.popup = PopupContainer(self, item=item)
        self.popup.move(global_pos)
        self.popup.updated.connect(self.on_update)

        self.popup.show()

    def on_update(self):
        self.master.update_views()
        self.updated.emit()
