from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class LineEditMainDir(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.folder_path = ""

        self.setReadOnly(True)
        self.mousePressEvent = self.open_folder_dialog

    def open_folder_dialog(self, event):
        folder_dialog = QFileDialog()
        folder_dialog.setWindowIcon(QIcon(":/ui/icon.png"))
        folder_dialog.setFileMode(QFileDialog.Directory)

        if folder_dialog.exec_() == QFileDialog.Rejected:
            return

        self.folder_path = folder_dialog.selectedFiles()[0]
        self.setText(self.folder_path)
        self.parent().parent().view_main_dir(self.folder_path)