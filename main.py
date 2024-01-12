import locale
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from modules.MainWindow import MainWindow


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(":/images/icon.png"))
    locale.setlocale(locale.LC_ALL, 'ru_RU.utf8')

    window = MainWindow()

    window.show()
    sys.exit(app.exec_())

