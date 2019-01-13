# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:/scripts/tool/colorTaggingUI_v001.ui'
#
# Created: Sat Jan 12 23:04:25 2019
#      by: pyside-uic 0.2.14 running on PySide 1.2.0
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(401, 239)
        self.gridLayout_2 = QtGui.QGridLayout(Dialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setContentsMargins(5, 5, 5, -1)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.colTagLabel = QtGui.QLabel(Dialog)
        self.colTagLabel.setObjectName("colTagLabel")
        self.verticalLayout_2.addWidget(self.colTagLabel)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.setAllBtn = QtGui.QPushButton(Dialog)
        self.setAllBtn.setObjectName("setAllBtn")
        self.horizontalLayout_2.addWidget(self.setAllBtn)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.outlinerCheckBox = QtGui.QCheckBox(Dialog)
        self.outlinerCheckBox.setObjectName("outlinerCheckBox")
        self.horizontalLayout_3.addWidget(self.outlinerCheckBox)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.setOutlinerBtn = QtGui.QPushButton(Dialog)
        self.setOutlinerBtn.setObjectName("setOutlinerBtn")
        self.verticalLayout.addWidget(self.setOutlinerBtn)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.wireFrameCheckBox = QtGui.QCheckBox(Dialog)
        self.wireFrameCheckBox.setObjectName("wireFrameCheckBox")
        self.horizontalLayout_4.addWidget(self.wireFrameCheckBox)
        self.sameAsOutlinerCheckBox = QtGui.QCheckBox(Dialog)
        self.sameAsOutlinerCheckBox.setObjectName("sameAsOutlinerCheckBox")
        self.horizontalLayout_4.addWidget(self.sameAsOutlinerCheckBox)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.setWireframeBtn = QtGui.QPushButton(Dialog)
        self.setWireframeBtn.setObjectName("setWireframeBtn")
        self.verticalLayout.addWidget(self.setWireframeBtn)
        self.disableAllBtn = QtGui.QPushButton(Dialog)
        self.disableAllBtn.setObjectName("disableAllBtn")
        self.verticalLayout.addWidget(self.disableAllBtn)
        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.colTagLabel.setText(QtGui.QApplication.translate("Dialog", "COLOR TAGGING TOOL", None, QtGui.QApplication.UnicodeUTF8))
        self.setAllBtn.setText(QtGui.QApplication.translate("Dialog", "Propagate Selections", None, QtGui.QApplication.UnicodeUTF8))
        self.outlinerCheckBox.setText(QtGui.QApplication.translate("Dialog", "Use Outliner Color", None, QtGui.QApplication.UnicodeUTF8))
        self.setOutlinerBtn.setText(QtGui.QApplication.translate("Dialog", "Propagate Outliner Color", None, QtGui.QApplication.UnicodeUTF8))
        self.wireFrameCheckBox.setText(QtGui.QApplication.translate("Dialog", "Use Wireframe Color", None, QtGui.QApplication.UnicodeUTF8))
        self.sameAsOutlinerCheckBox.setText(QtGui.QApplication.translate("Dialog", "Wireframe color is the same as outliner color", None, QtGui.QApplication.UnicodeUTF8))
        self.setWireframeBtn.setText(QtGui.QApplication.translate("Dialog", "Propagate Wireframe Color", None, QtGui.QApplication.UnicodeUTF8))
        self.disableAllBtn.setText(QtGui.QApplication.translate("Dialog", "Disable All On Selections", None, QtGui.QApplication.UnicodeUTF8))

