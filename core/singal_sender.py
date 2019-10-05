# coding=utf-8

import sys
import time
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QWidget, QPushButton, QApplication
from PyQt5.QtGui import QIcon
import AssetIO.core.Td_TDC as Td_TDC


class Example(QMainWindow,QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        btn1 = QPushButton("GetFile", self)
        btn1.move(0, 50)

        btn2 = QPushButton("MakeZip", self)
        btn2.move(100, 50)

        btn3 = QPushButton("Update", self)
        btn3.move(0, 100)

        btn4 = QPushButton("Quit", self)
        btn4.move(100,100)

        btn1.clicked.connect(self.buttonClicked)
        btn2.clicked.connect(self.buttonClicked)
        btn3.clicked.connect(self.buttonClicked)
        btn4.clicked.connect(self.buttonClicked)

        self.statusBar()

        self.setGeometry(300, 300, 290, 150)
        self.setWindowTitle("信号发送")
        self.setWindowIcon(QIcon("1.jpg"))
        self.show()

    def buttonClicked(self):

        sender = self.sender()
        self.statusBar().showMessage("正在进行:   " + sender.text() + "。   请稍后...")

        reply = QMessageBox.question(self, "Message",
                                     self.exec_resault(sender.text()))

    def exec_resault(self, button):
        print(button)
        if button == "Quit":
            exit()
        self.a = Td_TDC.button(button)
        return self.a


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
