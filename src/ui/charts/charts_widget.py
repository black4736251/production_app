from PySide6.QtWidgets import QGridLayout, QWidget
from ui.charts.views.total_bought_by_mat_cat import TotalBoughtByMaterialCategory
from ui.charts.views.total_sold_by_prod_cat import TotalSoldByProductCategory


class ChartsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.chart_layout = QGridLayout(self)

        self.total_bought_by_mat_cat = TotalBoughtByMaterialCategory()
        self.total_sold_by_pro_cat = TotalSoldByProductCategory()

        self.chart_layout.addWidget(self.total_bought_by_mat_cat, 0, 0)
        self.chart_layout.addWidget(self.total_sold_by_pro_cat, 0, 1)

    def refresh(self):
        self.total_bought_by_mat_cat.refresh()
        self.total_sold_by_pro_cat.refresh()
