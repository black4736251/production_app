from PySide6.QtCharts import QChart, QChartView, QPieSeries, QPieSlice
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QFont, QColor

from core.appstate import AppState
from models.enums import ProductCategory


class TotalSoldByProductCategory(QChartView):
    def __init__(self):
        super().__init__()
        self.appstate = AppState()
        self.products = self.appstate.products
        self.movements_out = list(self.appstate.movements_out.values())
        self.series = QPieSeries()
        self.categories = [cat.value for cat in ProductCategory]

        self._build_chart()

    def get_total_by_category(self) -> dict[str, int]:
        total_by_category = {cat: 0 for cat in self.categories}

        for mo in self.movements_out:
            pro = self.products[mo.pro_code]
            total_by_category[pro.category] += mo.quantity

        return total_by_category

    def _build_chart(self):
        totals = {
            cat: total
            for cat, total in self.get_total_by_category().items()
            if total > 0
        }

        for cat, total in totals.items():
            self.series.append(cat, total)

        chart = QChart()
        chart.addSeries(self.series)
        chart.setTitle("Total Vendido por Categoria de Produto")
        chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        chart.legend().setAlignment(Qt.AlignmentFlag.AlignBottom)

        markers = chart.legend().markers(self.series)
        for marker, slc in zip(markers, self.series.slices()):
            marker.setLabel(f"{slc.label()}  {slc.percentage() * 100:.1f}%")

        for slc in self.series.slices():
            slc.setLabelVisible(True)
            if slc.percentage() < 0.05:
                slc.setLabelPosition(QPieSlice.LabelPosition.LabelOutside)
                slc.setLabelColor(QColor("black"))
            else:
                slc.setLabelPosition(QPieSlice.LabelPosition.LabelInsideHorizontal)
                slc.setLabelColor(QColor("white"))
            slc.setLabel(f"{slc.percentage() * 100:.1f}%")
            slc.setLabelFont(QFont("Arial", 10, QFont.Weight.Bold))

        self.setChart(chart)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)

    def refresh(self):
        self.appstate = AppState()
        self.products = self.appstate.products
        self.movements_out = list(self.appstate.movements_out.values())

        self.series = QPieSeries()
        self._build_chart()
