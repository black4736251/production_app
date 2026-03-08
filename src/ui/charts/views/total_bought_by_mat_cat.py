from PySide6.QtCharts import QChart, QChartView, QPieSeries
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter

from core.appstate import AppState
from models import MaterialCategory


class TotalBoughtByMaterialCategory(QChartView):
    def __init__(self):
        super().__init__()
        self.appstate = AppState()
        self.materials = self.appstate.materials
        self.movements_in = list(self.appstate.movements_in.values())
        self.series = QPieSeries()
        self.categories = [cat.value for cat in MaterialCategory]

        self._build_chart()

    def get_total_by_category(self) -> dict[str, int]:
        total_by_category = {cat: 0 for cat in self.categories}

        for mi in self.movements_in:
            mat = self.materials[mi.mat_code]
            total_by_category[mat.category] += mi.quantity

        return total_by_category

    def _build_chart(self):
        totals = self.get_total_by_category()

        for cat, total in totals.items():
            if total > 0:
                self.series.append(cat, total)

        for slc in self.series.slices():
            slc.setLabelVisible(True)
            slc.setLabel(f"{slc.label()}  {slc.percentage()*100:.1f}%")

        chart = QChart()
        chart.addSeries(self.series)
        chart.setTitle("Total Bought by Material Category")
        chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        chart.legend().setAlignment(Qt.AlignmentFlag.AlignBottom)

        self.setChart(chart)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)

    def refresh(self):
        self.appstate = AppState()
        self.materials = self.appstate.materials
        self.movements_in = list(self.appstate.movements_in.values())

        self.series = QPieSeries()
        self._build_chart()
