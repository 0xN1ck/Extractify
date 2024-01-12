from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import os


class TreeFiles(QTreeWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setHeaderLabels(['Files и directories'])
        self.icon_provider = QFileIconProvider()
        self.root_path = ''
        self.checked_items = {}
        self.itemExpanded.connect(self.load_child_items)
        # self.populate_tree(self.root_path)
        self.itemChanged.connect(self.update_child_check_state)
        self.setFont(QFont("Arial", 14))

    def populate_tree(self, root_path, parent_item=None, state=Qt.Unchecked):
        if parent_item is None:
            parent_item = self.invisibleRootItem()

        try:
            items = os.listdir(root_path)
        except PermissionError as e:
            print(f"PermissionError: {e}")
            return

        for item_name in items:
            item_path = os.path.join(root_path, item_name)
            item = QTreeWidgetItem(parent_item, [item_name])
            item.setCheckState(0, state)

            if state == Qt.Checked and not os.path.isdir(item_path):
                self.checked_items[item_path] = item_name  # добавляем элемент в словарь

            try:
                if os.path.isdir(item_path):
                    item.setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)
                    item.setIcon(0, self.icon_provider.icon(QFileIconProvider.Folder))
                else:
                    item.setIcon(0, self.icon_provider.icon(QFileIconProvider.File))
            except PermissionError as e:
                print(f"PermissionError: {e}")


    def load_child_items(self, item: QTreeWidgetItem):
        if item.childCount() > 0:
            return
        item_path = self.get_item_path(item)
        self.populate_tree(item_path, item, state=item.checkState(0))

    def get_item_path(self, item):
        path = []
        while item is not None:
            path.insert(0, item.text(0))
            item = item.parent()
        return os.path.join(self.root_path, *path)

    def update_child_check_state(self, item: QTreeWidgetItem, column):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        state = item.checkState(column)
        item_path = self.get_item_path(item)
        for i in range(item.childCount()):
            child_item = item.child(i)
            child_item.setCheckState(column, state)

        if item.childIndicatorPolicy() == QTreeWidgetItem.ShowIndicator and state == Qt.Checked:
            self.load_child_items(item)

        if state == Qt.Checked and not os.path.isdir(item_path):
            self.checked_items[item_path] = item.text(0)  # добавляем элемент в словарь
        elif state == Qt.Unchecked and item_path in self.checked_items:
            del self.checked_items[item_path]  # удаляем элемент из словаря

        self.update_parent_check_state(item, column)
        QApplication.restoreOverrideCursor()

    def update_parent_check_state(self, item: QTreeWidgetItem, column):
        parent_item = item.parent()
        self.itemChanged.disconnect(self.update_child_check_state)
        while parent_item is not None and item.checkState(column) == Qt.Checked:
            parent_item.setCheckState(column, item.checkState(column))
            parent_item = parent_item.parent()

        while parent_item is not None and item.checkState(0) == Qt.Unchecked:
            if not Qt.Checked in [parent_item.child(i).checkState(column) for i in range(parent_item.childCount())]:
                parent_item.setCheckState(column, Qt.Unchecked)
            parent_item = parent_item.parent()

        self.itemChanged.connect(self.update_child_check_state)
