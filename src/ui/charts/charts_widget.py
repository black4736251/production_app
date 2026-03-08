from PySide6.QtWidgets import QGridLayout, QWidget
from ui.charts.views.total_bought_by_mat_cat import TotalBoughtByMaterialCategory


class ChartsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.chart_layout = QGridLayout(self)

        self.total_by_category = TotalBoughtByMaterialCategory()

        self.chart_layout.addWidget(self.total_by_category, 0, 0)

    def refresh(self):
        self.total_by_category.refresh()
