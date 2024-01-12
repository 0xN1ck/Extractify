from widgets.Ui_MainWindow import Ui_MainWindow
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setFont(QFont("Arial", 14))

        self.ui.tree_files.root_path = ''
        self.files = {}
        self.label_status = QLabel(self)
        self.ui.statusbar.addWidget(self.label_status)

        self.ui.pb_gen.clicked.connect(self.generate_report)

        self.load_path_files()

    def load_path_files(self):
        self.ui.tree_files.invisibleRootItem()

    def view_main_dir(self, path_main_dir):
        self.ui.tree_files.clear()
        self.ui.tree_files.root_path = path_main_dir
        self.ui.tree_files.populate_tree(root_path=path_main_dir)

    def generate_report(self):
        save_path, _ = QFileDialog.getSaveFileName(self, 'Save Report', '', 'Text Files (*.txt)')

        if save_path:
            save_path = save_path if save_path.endswith('.txt') else f"{save_path}.txt"

            with open(save_path, 'w', encoding='utf-8') as report_file:
                for file_path in self.ui.tree_files.checked_items:
                    report_file.write(f"\n\n----- {file_path} -----\n\n")
                    try:
                        with open(file_path, 'r', encoding='utf-8') as source_file:
                            content = source_file.read()
                            report_file.write(content)
                    except Exception as e:
                        report_file.write(f"Error reading file: {e}\n")

                    clickable_save_path = f"<a href='file:///{save_path}'>{save_path}</a>"

                    self.label_status.setText(f"Report generated and saved to: {clickable_save_path}")
                    self.label_status.setOpenExternalLinks(True)

                    # Open file manager when the link is clicked
                    self.label_status.linkActivated.connect(lambda url: QDesktopServices.openUrl(QUrl(url)))


