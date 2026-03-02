from dataclasses import astuple
from PySide6.QtCore import Signal
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QAbstractItemView, QTableWidget, QTableWidgetItem

from ui.containers.popup_container import PopupContainer
from core.appstate import AppState


class TableWidget(QTableWidget):
    updated = Signal()

    def __init__(self, master):
        super().__init__()

        self.master = master
        self.COLUMN_NAMES = self.master.COLUMN_NAMES
        self.TABLE_NAME = self.master.TABLE_NAME
        self.column_info = self.master.column_info

        self.setColumnCount(len(self.COLUMN_NAMES))
        self.setHorizontalHeaderLabels(self.COLUMN_NAMES)
        self.horizontalHeader().setSectionsClickable(True)
        self.verticalHeader().setVisible(False)
        self.setAlternatingRowColors(True)
        self.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_popup)

    def load(self):
        self.setRowCount(0)
        table_attr = getattr(AppState, self.TABLE_NAME, None)

        if table_attr is not None:
            data = list(table_attr.values())
        else:
            raise Exception("Failed to get data")

        row = 0
        for record in data:
            self.insertRow(row)
            record_tuple = astuple(record)
            for col in range(len(record_tuple)):
                self.setItem(row, col, QTableWidgetItem(str(record_tuple[col])))

            row += 1
        self.resizeColumnsToContents()

    def show_popup(self, pos):
        row = self.rowAt(pos.y())
        if row < 0:
            return

        global_pos = self.viewport().mapToGlobal(pos)

        self.popup = PopupContainer(self, row=row)
        self.popup.move(global_pos)
        self.popup.updated.connect(self.on_update)

        self.popup.show()

    def on_update(self):
        self.master.update_views()
        self.updated.emit()
