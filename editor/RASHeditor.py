import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QFileSystemModel, \
    QTreeView, QWidget, QPlainTextEdit, QSplitter, QMessageBox, QAction, QFileDialog
from PyQt5.QtCore import QDir, Qt, QProcess
from widgets.code_editor import CodeEditor
from widgets.popup_window import PopupWindow


class RashEditor(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("RashEdit")
        self.setGeometry(100, 100, 1980, 1080)
        self.root_path = QDir.currentPath()

        self.create_widgets()
        self.create_layout()
        self.browser_tree.doubleClicked.connect(self.open_file_from_browser)

        self.create_menu()

    def create_menu(self):
        self.save_action = QAction("Save", self)
        self.save_action.setShortcut("Ctrl+S")
        self.save_action.triggered.connect(self.save_file)

        self.open_action = QAction("Open", self)
        self.open_action.setShortcut("Ctrl+O")
        self.open_action.triggered.connect(self.open_file_dialog)

        self.open_directory_action = QAction("Open Directory", self)
        self.open_directory_action.setShortcut("Ctrl+Shift+O")
        self.open_directory_action.triggered.connect(self.open_directory_dialog)

        self.new_file_action = QAction("New File", self)
        self.new_file_action.setShortcut("Ctrl+N")
        self.new_file_action.triggered.connect(self.create_new_file)

        self.new_directory_action = QAction("New Directory", self)
        self.new_directory_action.setShortcut("Ctrl+Shift+N")
        self.new_directory_action.triggered.connect(self.create_new_directory)

        file_menu = self.menuBar().addMenu("File")
        file_menu.addAction(self.save_action)
        file_menu.addAction(self.open_action)
        file_menu.addAction(self.open_directory_action)
        file_menu.addAction(self.new_file_action)
        file_menu.addAction(self.new_directory_action)

        self.run_action = QAction("Run", self)
        self.run_action.setShortcut("Ctrl+R")
        self.run_action.triggered.connect(self.run_code)

        run_menu = self.menuBar().addMenu("Run")
        run_menu.addAction(self.run_action)



    def create_widgets(self):
        self.create_file_browser()

        # Code Editor
        self.code_editor = CodeEditor()

        # Terminal
        self.terminal_output = QPlainTextEdit()
        self.terminal_output.setPlaceholderText("Terminal...")
        self.terminal_output.setReadOnly(True)

        # Terminal Execute Button
        # self.execute_button = QPushButton("Execute")
        # self.execute_button.clicked.connect(self.execute_command

    def create_layout(self):
        # Browser Widget
        browser_widget = QWidget()
        self.root_directory_label = QLabel(self.root_path.split('/')[-1])
        self.root_directory_label.setStyleSheet("font-weight: bold; font-size: 12px;")
        browser_layout = QVBoxLayout()
        browser_layout.addWidget(self.root_directory_label)
        browser_layout.addWidget(self.browser_tree)
        browser_widget.setLayout(browser_layout)

        # Text Editor Widget
        editor_widget = QWidget()
        editor_layout = QVBoxLayout()
        editor_layout.addWidget(self.code_editor)
        editor_widget.setLayout(editor_layout)

        # Terminal Widget
        terminal_widget = QWidget()
        terminal_layout = QVBoxLayout()
        terminal_layout.addWidget(self.terminal_output)
        terminal_widget.setLayout(terminal_layout)

        # Splitter for Text Editor and Terminal
        splitterEditorTerminal = QSplitter()
        splitterEditorTerminal.setOrientation(Qt.Orientation.Vertical)
        # splitter.addWidget(file_widget)
        splitterEditorTerminal.addWidget(self.code_editor)
        splitterEditorTerminal.addWidget(terminal_widget)
        splitterEditorTerminal.setStyleSheet("QSplitter::handle { background-color: gray; width: 2px; }")
        splitterEditorTerminal.handle(1).setStyleSheet("QSplitterHandle { background-color: transparent; }")
        splitterEditorTerminal.setStretchFactor(0, 10)
        splitterEditorTerminal.setStretchFactor(1, 1)
        

        splitter = QSplitter()
        splitter.addWidget(browser_widget)
        splitter.addWidget(splitterEditorTerminal)
        splitter.setStyleSheet("QSplitter::handle { background-color: gray; width: 2px; }")
        splitter.handle(1).setStyleSheet("QSplitterHandle { background-color: transparent; }")
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 10)
        self.setCentralWidget(splitter)

    def create_file_browser(self):
        self.browser_model = QFileSystemModel(self)
        self.browser_model.setRootPath(self.root_path)
        self.browser_tree = QTreeView()
        self.browser_tree.setModel(self.browser_model)
        self.browser_tree.setRootIndex(self.browser_model.index(self.root_path))

        self.browser_tree.setColumnHidden(1, True)  # Hide Size column
        self.browser_tree.setColumnHidden(2, True)  # Hide Type column
        self.browser_tree.setColumnHidden(3, True)  # Hide Date Modified column

    def open_file_from_browser(self, index):
        path = self.browser_model.filePath(index)
        if os.path.isfile(path):
            self.code_editor.add_tab(path)
        else:
            QMessageBox.warning(self, "Warning", "Selected item is not a file.")

    def save_file(self):
        # Get the current file path
        file_path = self.browser_model.filePath(self.browser_tree.currentIndex())
        if not file_path:
            QMessageBox.warning(self, "Warning", "No file selected.")
            return

        self.code_editor.save_current_tab()

    def open_file_dialog(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.ExistingFile)
        file_path, _ = dialog.getOpenFileName(self, "Open File", self.root_path, "All Files (*)")

        if os.path.isfile(file_path):
            self.code_editor.add_tab(file_path)
        else:
            QMessageBox.warning(self, "Warning", "Selected item is not a file.")
    
    def open_directory_dialog(self):
        directory_dialog = QFileDialog(self)
        directory_dialog.setFileMode(QFileDialog.Directory)
        file_path = directory_dialog.getExistingDirectory(self, "Open Directory", self.root_path)

        if os.path.isdir(file_path):
            self.root_path = file_path
            self.browser_model.setRootPath(self.root_path)
            self.browser_tree.setRootIndex(self.browser_model.index(self.root_path))
            self.root_directory_label.setText(self.root_path.split('/')[-1])
            self.code_editor.clear()
        else:
            QMessageBox.warning(self, "Warning", "Selected item is not a file.")

    def create_file_or_directory(self):
        new_file_dialog = PopupWindow()

    def create_new_file(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.AnyFile)
        file_dialog.setAcceptMode(QFileDialog.AcceptSave)
        if file_dialog.exec_() == QFileDialog.Accepted:
            file_path = file_dialog.selectedFiles()[0]
            directory = os.path.dirname(file_path)
        else:
            return

        if os.path.exists(file_path):
            QMessageBox.warning(self, "Error", "The specified file or directory already exists.")
            return

        if not os.path.exists(directory):
            os.makedirs(directory)

        open(file_path, 'w').close()
        QMessageBox.information(self, "Success", "File created successfully!")

    def create_new_directory(self):
        dir_dialog = QFileDialog()
        dir_dialog.setFileMode(QFileDialog.Directory)
        if dir_dialog.exec_() == QFileDialog.Accepted:
            directory_path = dir_dialog.selectedFiles()[0]
        else:
            return

        if os.path.exists(directory_path):
            QMessageBox.warning(self, "Error", "The specified file or directory already exists.")
            return

        os.makedirs(directory_path)
        QMessageBox.information(self, "Success", "Directory created successfully!")

    def execute_command(self):
        command = self.terminal_input.toPlainText().strip()
        if command:
            self.terminal_input.clear()
            process = QProcess()
            process.setProcessChannelMode(QProcess.MergedChannels)
            process.readyReadStandardOutput.connect(lambda: self.handle_output(process))
            process.start(command)
        
    def run_code(self):
        filename = self.code_editor.get_current_tab_name()
        if not filename:
            return
        
        # command = f"bash rash.sh -f {filename}".strip()
        # print(command)
        # process_compile = QProcess()
        # process_compile.setProcessChannelMode(QProcess.MergedChannels)
        # process_compile.readyReadStandardOutput.connect(lambda: self.handle_std_output(process_compile))
        # process_compile.readyReadStandardError.connect(lambda: self.handle_std_error(process_compile))
        # process_compile.start(command)

        command = f"bash rash.sh -r {filename}"
        process_run = QProcess()
        process_run.setProcessChannelMode(QProcess.MergedChannels)
        process_run.readyReadStandardOutput.connect(lambda: self.handle_std_output(process_run))
        process_run.readyReadStandardError.connect(lambda: self.handle_std_error(process_run))
        process_run.start(command)

    def handle_std_output(self, process):
        output = process.readAllStandardOutput().data().decode()
        self.terminal_output.appendPlainText(output)

    def handle_std_error(self, process):
        output = process.readAllStandardError().data().decode()
        self.terminal_output.appendPlainText(output)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    editor = RashEditor()
    editor.show()
    sys.exit(app.exec_())
