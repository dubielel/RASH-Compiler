from PyQt5.QtWidgets import QTreeWidget, QFileSystemModel, QVBoxLayout, QWidget, QMessageBox, QTabWidget, QFileDialog
from PyQt5.QtCore import Qt, QDir
import typing

class FileBrowser(QTreeView):
    def __init__(self, parent=None, root_path: str=None):
        super().__init__(parent)
        self.model = QFileSystemModel(self)
        self.setModel(self.model)
        self.setRootPath(root_path)

        self.setColumnHidden(1, True)  # Hide Size column
        self.setColumnHidden(2, True)  # Hide Type column
        self.setColumnHidden(3, True)  # Hide Date Modified column

    def change_directory(self, directory_path):
        self.setRootIndex(self.model.index(directory_path))
        self.browser_model.setRootPath(self.root_path)
        self.browser_tree.setRootIndex(self.browser_model.index(self.root_path))
        self.root_directory_label.setText(self.root_path.split('/')[-1])