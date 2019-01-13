"""

=====================================================

Use this simple tool to toggle Maya outliner and wireframe color on the fly!

Copyright 2019 Yinglei Yang www.ying-lei.com

=====================================================

Usage: run following commands in Maya Python

import colorTaggingTool as ctool
reload(ctool)
ctool.run()


"""


from PySide import QtGui, QtCore, QtUiTools
from shiboken import wrapInstance


import os
import functools
import maya.cmds as mc
import pymel.core as pm
import maya.OpenMayaUI as omui


import logging
_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)





def getMayaWindow():
	""" pointer to the maya main window
	"""

	ptr = omui.MQtUtil.mainWindow()

	if ptr:
		return wrapInstance(long(ptr), QtGui.QMainWindow)


def run():
	""" builds UI
	"""
	global win
	win = ColorTaggingUI(parent=getMayaWindow())



class ColorTaggingUI(QtGui.QDialog):
	""" Main UI
	"""


	def __init__(self, parent = None):
		super(ColorTaggingUI, self).__init__(parent)

		# close window if window existed
		for widget in parent.findChildren(QtGui.QDialog):
			if widget is not self:
				if widget.objectName() == self.objectName():
					widget.close()


		self.scaleVal = 1.0

		# index color mapping to rgb for qPixMap widgets
		self.colorMapDict = {
		            0:None,
		            1:(0,0,0),
		            2:(64,64,64),
		            3:(128,128,128),
		            4:(155,0,40),
		            5:(0,4,96),
		            6:(0,0,255),
		            7:(0,70,25),
		            8:(38,0,67),
		            9:(200,0,200),
		            10:(138,72,51),
		            11:(63,35,31),
		            12:(153,38,0),
		            13:(255,0,0),
		            14:(0,255,0),
		            15:(0,65,153),
		            16:(255,255,255),
		            17:(255,255,0),
		            18:(100,220,255),
		            19:(67,255,163),
		            20:(255,176,176),
		            21:(228,172,121),
		            22:(255,255,99),
		            23:(0,153,84),
		            24:(165,108,49),
		            25:(158,160,48),
		            26:(104,160,48),
		            27:(48,161,94),
		            28:(48,162,162),
		            29:(48,102,160),
		            30:(112,48,162),
		            31:(162,48,106)
		        }



		# Topmost layout
		self.gridLayout = QtGui.QGridLayout()
		self.verticalLayout = QtGui.QVBoxLayout()
	
		# Label
		self.outlinerLabel = QtGui.QLabel("Choose Outliner Color")
		self.verticalLayout.addWidget(self.outlinerLabel)

		# button grid 01
		self.buttonGridLayout_1 = QtGui.QGridLayout()
		self.buttonGridLayout_1.setHorizontalSpacing(1)
		self.buttonGridLayout_1.setVerticalSpacing(1)

		self.outlinerButtonGrp = QtGui.QButtonGroup()

		# adding buttons to grid
		outlinerBtnNum = 0
		for i in range(32):
			self.colorButton = QtGui.QPushButton("")
			self.colorButton.setMinimumSize(20,20)
			self.colorButton.setMaximumSize(20,20)
			self.colorButton.setCheckable(1)

			if outlinerBtnNum == 0:
				self.colorButton.setMinimumSize(60,20)
				self.colorButton.setMaximumSize(60,20)
				self.colorButton.setText("Disable")


			else:
				bColor = self.colorMapDict.get(outlinerBtnNum)
				#_logger.debug("bColor: {0}".format(bColor))

				self.colorButton.setStyleSheet('QPushButton {background-color: rgb(%d,%d,%d); color: white}' % (bColor))


			self.outlinerButtonGrp.addButton(self.colorButton, outlinerBtnNum)

			# adding button to the grid
			self.buttonGridLayout_1.addWidget(self.colorButton, 0, i)
			outlinerBtnNum += 1
	
		self.verticalLayout.addLayout(self.buttonGridLayout_1)

		# Lable
		self.wireframeLabel = QtGui.QLabel("Choose Wireframe Color")
		self.verticalLayout.addWidget(self.wireframeLabel)



		# button grid 02
		self.buttonGridLayout_2 = QtGui.QGridLayout()
		self.buttonGridLayout_2.setHorizontalSpacing(1)
		self.buttonGridLayout_2.setVerticalSpacing(1)

		self.wireframeButtonGrp = QtGui.QButtonGroup()

		# adding buttons to grid
		wireframeBtnNum = 0
		for i in range(32):
			self.colorButton = QtGui.QPushButton("")
			self.colorButton.setMinimumSize(20,20)
			self.colorButton.setMaximumSize(20,20)
			self.colorButton.setCheckable(1)

			if wireframeBtnNum == 0:
				self.colorButton.setMinimumSize(60,20)
				self.colorButton.setMaximumSize(60,20)
				self.colorButton.setText("Disable")


			else:
				bColor = self.colorMapDict.get(wireframeBtnNum)
				_logger.debug("bColor: {0}".format(bColor))

				self.colorButton.setStyleSheet('QPushButton {background-color: rgb(%d,%d,%d); color: white}' % (bColor))


			self.wireframeButtonGrp.addButton(self.colorButton, wireframeBtnNum)

			# adding button to the grid
			self.buttonGridLayout_2.addWidget(self.colorButton, 0, i)
			wireframeBtnNum += 1
	
		self.verticalLayout.addLayout(self.buttonGridLayout_2)


		self.emptySpace = QtGui.QLabel("")
		self.verticalLayout.addWidget(self.emptySpace)

		# Disable All Btn
		self.disableAllBtn = QtGui.QPushButton("Disable All On Selections")
		self.disableAllBtn.setStyleSheet('QPushButton {background-color: rgb(50,0,0); color: white}' )
		self.verticalLayout.addWidget(self.disableAllBtn)

		self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)



		# THINGS YOU HAVE TO ADD
		self.makeConnections()
		self.setWindowTitle("COLOR TAGGING TOOL")
		self.setLayout(self.gridLayout)

		self.setFixedSize(740, 175)

		#self.initUIState();
		self.show();




	def initUIState(self):
		""" sets up init state of UI
		"""

		self.initButtonGroup(self.outlinerButtonGrp)
		self.initButtonGroup(self.wireframeButtonGrp)



	def initButtonGroup(self, buttonGrp=None):
		""" set buttonGrp back to initial state
		"""
		
		checkedButton = buttonGrp.checkedButton()
	
		buttonGrp.setExclusive(False)
		try:
			checkedButton.setChecked(False)
		except:
			pass

		buttonGrp.setExclusive(True)

		_logger.debug("checkedButton: {0}".format(checkedButton))
		_logger.debug(buttonGrp.checkedId())



	def makeConnections(self):
		""" connect events in UI"""

		# self.conListWidget.itemDoubleClicked.connect(self.doubleClickedItem)
		# self.scaleSlider.valueChanged[int].connect(self.sliderEvent)
		# self.scaleValLineEdit.editingFinished.connect(self.manualScaleEnteredEvent)
		
		self.outlinerButtonGrp.buttonClicked.connect(self.outlinerButtonClicked)
		self.wireframeButtonGrp.buttonClicked.connect(self.wireframeButtonClicked)

		
		self.disableAllBtn.clicked.connect(self.initUIState)


	def outlinerButtonClicked(self):
		_logger.debug("outlinerButtonClicked: {0}".format(self.outlinerButtonGrp.checkedId())) 



	def wireframeButtonClicked(self):
		_logger.debug("wireframeButtonClicked: {0}".format(self.wireframeButtonGrp.checkedId()))



'''
	def saveControllerEvent(self):
		""" saves selected curve
		"""

		sel = pm.selected()

		if sel and len(sel) == 1:

			try:
				crvShape = sel[0].getShape()

				if not crvShape.nodeType() == 'nurbsCurve':
					_logger.error("Selected is not a curve")
				else:
					_logger.debug("Selected a curve")

			except:	
				_logger.error("Error placeholder")

		elif sel and len(sel) > 1:
			_logger.error("Too many selected")
		else:
			_logger.debug("Nothing selected")


		curveName = self.conNameLineEdit.text()
		if not curveName:
			_logger.error("No valid name entered")


		# SAVE THE CURVE!
		conGenApi.saveCon(con=sel[0], conName=curveName, debug=True)
		self.updateListWidget()



	def manualScaleEnteredEvent(self):
		""" when a manual scale is entered update slider and self.scaleVal
		"""
		tempScale = float(self.scaleValLineEdit.text()) 

		if tempScale < 1:
			self.scaleVal = 1
		elif tempScale > 10.0:
			self.scaleVal = 10.0
		else:
			self.scaleVal = tempScale

		self.scaleSlider.setValue(self.scaleVal * 10)


	def sliderEvent(self,value):
		""" gets slider value
		"""
		# slider = self.sender()
		# value = slider.value()

		print("value: {0}".format(value))


		floatVal = float(value) / 10.0
		self.scaleValLineEdit.setText(str(floatVal))

		self.scaleVal = floatVal



	def doubleClickedItem(self):
		""" for when an item is double-clicked
		"""

		theListWidget = self.sender()
		curItem = theListWidget.currentItem()
		curItemText = curItem.text()

		# print("sender: {0}".format(self.sender()))
		print("current Item: {0}".format(curItemText))

		# get color
		# curBtn = self.buttonGrp.checkedButton()
		curBtn = self.buttonGrp.checkedId()


		# tenery
		color = int(curBtn) if (curBtn >= 0)  else 0


		conGenApi.generateCon(conName=curItemText, scale=self.scaleVal, color=color)



	def updateListWidget(self):
		""" updates the list widget
		"""

		# returns sorted list
		conList = conGenApi.conList()

		# empty list widget
		self.conListWidget.clear()

		for con in conList:
			item = QtGui.QListWidgetItem(con)
			self.conListWidget.addItem(item)






	def radioChange(self,geomType):
		self.geomType = geomType
		print("geomtype: {0}".format(geomType))


	def createGeometry(self):
		print("create geometry pressed: {0}".format(self.geomType))

		finalName = self.geomType

		if self.customNameCheckBox.isChecked():
			# get a custom name
			customName = self.customNameLineEdit.text()

			if customName != "nameOfGeometryHere":
				finalName = customName

		# retrieve scale
		print("scale value:{0}".format(self.scaleLcdNumber.value()))
		scaleValue = self.scaleLcdNumber.value()

		retName = None

		if self.geomType == 'pCube1':
			retName = mc.polyCube( n=finalName, w=scaleValue, h=scaleValue, d=scaleValue, ch=0)
		elif self.geomType == 'pSphere1':
			retName = mc.polySphere( n=finalName, r=scaleValue, ch=0)
		elif self.geomType == 'pCone1':
			retName = mc.polyCone( n=finalName, r=scaleValue, h=scaleValue*2.0, ch=0)
		else:
			print("BROKEN LOGIC")

		appendedName = retName[0]

		# Adding text to text edit
		self.textEdit.append(appendedName)
'''