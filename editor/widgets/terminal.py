import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPlainTextEdit
from PyQt5.QtCore import Qt, QProcess


class TerminalWidget(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create a QPlainTextEdit widget to display the terminal output
        self.output_widget = QPlainTextEdit(self)
        self.output_widget.setReadOnly(True)

        # Redirect the standard output and error to the QPlainTextEdit widget
        sys.stdout = self.output_widget
        sys.stderr = self.output_widget

        # Create a QProcess to execute terminal commands
        self.process = QProcess()
        self.process.readyReadStandardOutput.connect(self.update_output)
        self.process.readyReadStandardError.connect(self.update_output)

        # Create a command prompt to input terminal commands
        self.command_prompt = QPlainTextEdit(self)
        self.command_prompt.setFixedHeight(30)
        self.command_prompt.setFocusPolicy(Qt.StrongFocus)
        self.command_prompt.installEventFilter(self)

        # Set the central widget and layout
        self.setCentralWidget(self.output_widget)

    def eventFilter(self, obj, event):
        if obj == self.command_prompt and event.type() == event.KeyPress:
            if event.key() == Qt.Key_Return:
                command = self.command_prompt.toPlainText()
                self.execute_command(command)
                self.command_prompt.clear()
                return True
        return super().eventFilter(obj, event)

    def execute_command(self, command):
        # Execute the terminal command using QProcess
        self.process.start(command)

    def update_output(self):
        # Update the output widget with the terminal command output
        data = self.process.readAllStandardOutput().data().decode()
        self.output_widget.appendPlainText(data)

        error = self.process.readAllStandardError().data().decode()
        self.output_widget.appendPlainText(error)
