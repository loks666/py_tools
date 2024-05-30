import sys

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget

from main_win import main_logic


class Worker(QThread):
    log_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._is_running = True

    def run(self):
        main_logic(self.log_signal, self.is_running)

    def stop(self):
        self._is_running = False

    def is_running(self):
        return self._is_running


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.worker = None

    def initUI(self):
        self.setWindowTitle("CAN Monitor")
        self.setGeometry(100, 100, 800, 600)

        self.textEdit = QTextEdit()
        self.textEdit.setReadOnly(True)

        self.startButton = QPushButton("Start")
        self.stopButton = QPushButton("Stop")
        self.startButton.clicked.connect(self.startThread)
        self.stopButton.clicked.connect(self.stopThread)

        layout = QVBoxLayout()
        layout.addWidget(self.textEdit)
        layout.addWidget(self.startButton)
        layout.addWidget(self.stopButton)

        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

    def startThread(self):
        if self.worker is None or not self.worker.isRunning():
            self.worker = Worker()
            self.worker.log_signal.connect(self.updateTextEdit)
            self.worker.start()

    def stopThread(self):
        if self.worker is not None:
            self.worker.stop()
            self.worker.wait()  # 等待线程安全结束
            self.updateTextEdit("程序已停止")  # 更新文本编辑框
            self.worker = None

    def updateTextEdit(self, message):
        self.textEdit.append(message)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
