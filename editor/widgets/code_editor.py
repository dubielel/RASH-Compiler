from PyQt5.QtWidgets import QTextEdit, QVBoxLayout, QWidget, QMessageBox, QTabWidget, QFileDialog
from PyQt5.QtCore import Qt, QDir


class CodeEditor(QTabWidget):
    def __init__(self):
        super().__init__()

        # Create a QTabWidget for managing the tabs
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.close_tab)

        # Add an initial empty tab
        self.add_tab()


    def add_tab(self, file_path=None):
        # Create a new text editor widget
        text_editor = QTextEdit()
        text_editor.textChanged.connect(lambda: self.mark_tab_as_unsaved(file_path))

        # Add the text editor to a new tab
        tab_index = self.addTab(text_editor, "Untitled")
        self.setCurrentIndex(tab_index)

        # Set the file path as the tab data
        if file_path:
            self.setTabToolTip(tab_index, file_path)

    def mark_tab_as_unsaved(self, path: str):
        current_tab_index = self.currentIndex()
        current_tab_widget = self.widget(current_tab_index)
        current_tab_text = self.tabText(current_tab_index)

        if current_tab_text.endswith("*"):
            return

        if current_tab_widget.toPlainText().strip() != self.get_file_content(path).strip():
            self.setTabText(current_tab_index, current_tab_text + "*")

    def close_tab(self, index):
        current_tab_widget = self.widget(index)
        current_tab_text = self.tabText(index)

        if current_tab_text.endswith("*"):
            response = self.prompt_to_save_changes(current_tab_text)
            if response == QMessageBox.Save:
                self.save_current_tab()
            elif response == QMessageBox.Cancel:
                return

        self.removeTab(index)

    def prompt_to_save_changes(self, tab_text):
        message_box = QMessageBox()
        message_box.setWindowTitle("Unsaved Changes")
        message_box.setIcon(QMessageBox.Warning)
        message_box.setText(f"The file {tab_text[:-1]} has unsaved changes. Do you want to save the changes?")
        message_box.setStandardButtons(QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
        return message_box.exec()

    def save_current_tab(self):
        if (current_index := self.currentIndex()) >= 0:
            file_path = self.tabData(current_index)
            if file_path:
                self._save_file(current_index, file_path)
            else:
                self.save_as_current_tab()

    def save_as_current_tab(self):
        if (current_index := self.currentIndex()) >= 0:
            file_dialog = QFileDialog(self)
            file_dialog.setAcceptMode(QFileDialog.AcceptSave)
            file_dialog.setDefaultSuffix("txt")
            file_path, _ = file_dialog.getSaveFileName(self, "Save File")
            if file_path:
                self._save_file(current_index, file_path)

    def open_file(self):
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getOpenFileName(self, "Open File")
        if file_path:
            self.add_tab(file_path)
            with open(file_path, "r") as file:
                content = file.read()
                current_index = self.currentIndex()
                current_tab_widget = self.widget(current_index)
                current_tab_widget.setPlainText(content)
                self.setTabText(current_index, QDir.toNativeSeparators(file_path))
    
    def _save_file(self, current_index: int, file_name: str):
        current_tab_widget = self.widget(current_index)
        content = current_tab_widget.toPlainText()
        try:
            with open(file_name, "w") as file:
                file.write(content)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to save file: {str(e)}")
        else:
            self.setTabText(current_index, QDir.toNativeSeparators(file_name))
            self.setTabData(current_index, file_name)
            QMessageBox.information(self, "Success", "File saved successfully.")

        tab_index = self.indexOf(file_name)
        self.setTabText(tab_index, file_name[:-1])
    
    def get_file_content(self, file_path: str):
        with open(file_path, "r") as file:
            content = file.read()
        return content
