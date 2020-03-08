import sys
from PyQt5.QtWidgets import QApplication, QWidget
from message_ui import Ui_Form


class Message(QWidget, Ui_Form):
    def __init__(self, text):
        super().__init__()
        self.setupUi(self)
        self.label_text.setText(text)
        self.btn_ok.clicked.connect(self.close_mes)

    def close_mes(self):
        self.close()
