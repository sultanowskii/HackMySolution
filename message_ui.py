# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'message_ui.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 170)
        Form.setMinimumSize(QtCore.QSize(400, 170))
        Form.setMaximumSize(QtCore.QSize(400, 170))
        self.btn_ok = QtWidgets.QPushButton(Form)
        self.btn_ok.setGeometry(QtCore.QRect(150, 130, 111, 31))
        font = QtGui.QFont()
        font.setFamily("JetBrains Mono")
        font.setPointSize(11)
        self.btn_ok.setFont(font)
        self.btn_ok.setObjectName("btn_ok")
        self.label_text = QtWidgets.QLabel(Form)
        self.label_text.setGeometry(QtCore.QRect(10, 10, 381, 101))
        font = QtGui.QFont()
        font.setFamily("JetBrains Mono")
        font.setPointSize(10)
        self.label_text.setFont(font)
        self.label_text.setText("")
        self.label_text.setObjectName("label_text")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.btn_ok.setText(_translate("Form", "Ок"))
