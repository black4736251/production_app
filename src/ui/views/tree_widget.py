from PySide6.QtWidgets import QAbstractItemView, QTreeWidget, QTreeWidgetItem

from core.appstate import AppState


class TreeWidget(QTreeWidget):
    def __init__(self):
        super().__init__()
        self.setColumnCount(2)
        self.setHeaderLabels(("Name", "Quantity"))
        self.setColumnWidth(0, 500)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)

        self.load()

    def load(self):
        self.clear()

        data = sorted(AppState.product_materials.values(), key=lambda x: x.pro_code)

        items = []
        current_product = None
        item = QTreeWidgetItem()

        for record in data:
            product = str(record.pro_code)
            material = str(record.mat_code)
            quantity = str(record.quantity)

            if product != current_product:
                if item.childCount() > 0:
                    items.append(item)

                current_product = product
                item = QTreeWidgetItem([product])

            item.addChild(QTreeWidgetItem([material, quantity]))

        # append last item
        if item is not None:
            items.append(item)

        self.insertTopLevelItems(0, items)
