# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mwin.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(850, 571)
        self.pltxt = QtWidgets.QPlainTextEdit(Dialog)
        self.pltxt.setGeometry(QtCore.QRect(30, 80, 481, 241))
        self.pltxt.setObjectName("pltxt")
        self.intxt = QtWidgets.QPlainTextEdit(Dialog)
        self.intxt.setGeometry(QtCore.QRect(30, 360, 481, 31))
        self.intxt.setObjectName("intxt")
        self.outtxt = QtWidgets.QPlainTextEdit(Dialog)
        self.outtxt.setGeometry(QtCore.QRect(30, 430, 481, 101))
        self.outtxt.setObjectName("outtxt")
        self.brbt = QtWidgets.QPushButton(Dialog)
        self.brbt.setGeometry(QtCore.QRect(150, 20, 81, 41))
        self.brbt.setObjectName("brbt")
        self.cpbt = QtWidgets.QPushButton(Dialog)
        self.cpbt.setGeometry(QtCore.QRect(290, 20, 81, 41))
        self.cpbt.setObjectName("cpbt")
        self.itbt = QtWidgets.QPushButton(Dialog)
        self.itbt.setGeometry(QtCore.QRect(430, 20, 81, 41))
        self.itbt.setObjectName("itbt")
        self.pctable = QtWidgets.QTableWidget(Dialog)
        self.pctable.setGeometry(QtCore.QRect(560, 80, 251, 451))
        self.pctable.setObjectName("pctable")
        self.pctable.setColumnCount(0)
        self.pctable.setRowCount(0)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(40, 50, 91, 31))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(30, 330, 211, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(30, 400, 54, 12))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(570, 60, 54, 12))
        self.label_4.setObjectName("label_4")

        self.retranslateUi(Dialog)
        self.brbt.clicked.connect(Dialog.br)
        self.cpbt.clicked.connect(Dialog.compile)
        self.itbt.clicked.connect(Dialog.inte)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.brbt.setText(_translate("Dialog", "浏览"))
        self.cpbt.setText(_translate("Dialog", "编译"))
        self.itbt.setText(_translate("Dialog", "解释"))
        self.label.setText(_translate("Dialog", "PL0代码"))
        self.label_2.setText(_translate("Dialog", "输入（解释前请先输入数据）"))
        self.label_3.setText(_translate("Dialog", "输出"))
        self.label_4.setText(_translate("Dialog", "PCode"))

