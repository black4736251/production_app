from PySide6.QtWidgets import QApplication
import sys

from core import data_manager
from repos.base_repo import Base
from ui.main_window import MainWindow

app = QApplication(sys.argv)

with open("src/main.qss") as style:
    app.setStyleSheet(style.read())

base = Base("test.db")
data_manager = data_manager.DataManager()
data_manager.refresh_all()

main_window = MainWindow()
main_window.show()

app.exec()
