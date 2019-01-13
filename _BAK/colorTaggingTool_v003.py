"""

=====================================================

Use this simple tool to toggle Maya outliner and wireframe color on the fly!

* Only toggle override on transform node, not shape node
* Only using index color

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
import maya.mel as mel

import logging
_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)


# ==================== VARIABLES ==================== 

# index color mapping to rgb for qPixMap widgets
colorMapDict = {
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

# ==================== MAIN UI ====================


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


		# variables
		self.syncColor = 0
		self.counter = 0

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
				bColor = colorMapDict.get(outlinerBtnNum)
				#_logger.debug("bColor: {0}".format(bColor))

				self.colorButton.setStyleSheet('QPushButton {background-color: rgb(%d,%d,%d); color: white}' % (bColor))


			self.outlinerButtonGrp.addButton(self.colorButton, outlinerBtnNum)

			# adding button to the grid
			self.buttonGridLayout_1.addWidget(self.colorButton, 0, i)
			outlinerBtnNum += 1
	
		self.verticalLayout.addLayout(self.buttonGridLayout_1)


		self.emptySpace_1 = QtGui.QLabel("")
		self.verticalLayout.addWidget(self.emptySpace_1)


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
				bColor = colorMapDict.get(wireframeBtnNum)
				_logger.debug("bColor: {0}".format(bColor))

				self.colorButton.setStyleSheet('QPushButton {background-color: rgb(%d,%d,%d); color: white}' % (bColor))


			self.wireframeButtonGrp.addButton(self.colorButton, wireframeBtnNum)

			# adding button to the grid
			self.buttonGridLayout_2.addWidget(self.colorButton, 0, i)
			wireframeBtnNum += 1
	
		self.verticalLayout.addLayout(self.buttonGridLayout_2)

		# sync checkbox
		self.syncColorCheckBox = QtGui.QCheckBox("Sync outliner color and wireframe color")
		self.verticalLayout.addWidget(self.syncColorCheckBox)



		self.emptySpace_2 = QtGui.QLabel("")
		self.verticalLayout.addWidget(self.emptySpace_2)


		# Disable All Btn
		self.disableAllBtn = QtGui.QPushButton("Disable All On Selections")
		self.disableAllBtn.setStyleSheet('QPushButton {background-color: rgb(50,0,0); color: white}' )
		self.verticalLayout.addWidget(self.disableAllBtn)

		self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)



		# THINGS YOU HAVE TO ADD
		self.makeConnections()
		self.setWindowTitle("COLOR TAGGING TOOL")
		self.setLayout(self.gridLayout)

		self.setFixedSize(740, 200)

		self.initUIState();
		self.show();




	def initUIState(self, colorIndex = 0):
		""" sets up init state of UI
		"""
		self.initButtonGroup(self.outlinerButtonGrp)
		self.initButtonGroup(self.wireframeButtonGrp)




	def makeConnections(self):
		""" connect events in UI"""
	
		self.outlinerButtonGrp.buttonClicked.connect(self.outlinerButtonClicked)
		self.wireframeButtonGrp.buttonClicked.connect(self.wireframeButtonClicked)

		self.disableAllBtn.clicked.connect(self.disableAllBtnClicked)

		self.syncColorCheckBox.stateChanged.connect(self.syncColorCheckBoxToggled)


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



	def disableAllBtnClicked(self):

		disableList = getSelection()

		_logger.debug("disableList: {0}".format(disableList)) 

		outlinerOverrideOff(disableList)
		wireframeOverrideOff(disableList)

		self.initUIState()
		refreshMayaUI()



	def outlinerButtonClicked(self):
		outlinerColorIndex = self.outlinerButtonGrp.checkedId()
		_logger.debug("outlinerColorIndex: {0}".format(outlinerColorIndex)) 

		outlinerOnList = getSelection()		
		_logger.debug("outlinerOnList: {0}".format(outlinerOnList)) 

		if not len(outlinerOnList) == 0:

			if outlinerColorIndex == 0:
				outlinerOverrideOff(outlinerOnList)
				_logger.debug("Disable outliner color") 
			
			else:
				outlinerOverrideOn(outlinerOnList, outlinerColorIndex)
				_logger.debug("Enable outliner color") 

		else:
			_logger.error("Nothing selected")

		
		# check if need to sync color
		if self.syncColor == 1:
			self.toggleWireframeColor(outlinerColorIndex)
			self.counter += 1

			if self.counter < 2:
				self.wireframeButtonClicked()

			else:
				self.counter = 0
				pass
			
		else:
			pass


		self.initUIState()
		refreshMayaUI()



	def wireframeButtonClicked(self):
		wireframeColorIndex = self.wireframeButtonGrp.checkedId()
		_logger.debug("wireframeColorIndex: {0}".format(wireframeColorIndex))

		wireframeOnList = getSelection()
		_logger.debug("wireframeOnList: {0}".format(wireframeOnList)) 

		if not len(wireframeOnList) == 0:

			if wireframeColorIndex == 0:
				wireframeOverrideOff(wireframeOnList)
				_logger.debug("Disable outliner color") 
			
			else:
				wireframeOverrideOn(wireframeOnList, wireframeColorIndex)
				_logger.debug("Enable outliner color") 

		else:
			_logger.error("Nothing selected")


		# check if need to sync color
		if self.syncColor == 1:
			self.toggleOutlinerColor(wireframeColorIndex)
			self.counter += 1
	
			if self.counter < 2:
				self.outlinerButtonClicked()

			else:
				self.counter = 0
				pass

			_logger.debug("counter: {0}".format(self.counter))

		else:
			pass


		self.initUIState()
		refreshMayaUI()



	def syncColorCheckBoxToggled(self):
		""" check if syncColor checkbox is enable
		"""
		self.syncColor = self.syncColorCheckBox.isChecked() 
		_logger.debug("syncColor: {0}".format(self.syncColor))



	def toggleWireframeColor(self, colorIndex = None):
		""" toggle wireframe color based on colorIndex
		"""

		buttonToToggle = self.wireframeButtonGrp.button(colorIndex)
		buttonToToggle.setChecked(True)



	def toggleOutlinerColor(self, colorIndex = None):
		""" toggle outliner color based on colorIndex
		"""

		buttonToToggle = self.outlinerButtonGrp.button(colorIndex)
		buttonToToggle.setChecked(True)








# ==================== FUNCTIONS ====================

def getSelection():
	"""
	make sure override only happen in transform
	"""

	transformList = pm.selected(typ = 'transform')
	
	_logger.debug("filterdSelection: {0}".format(transformList))
	return transformList



def outlinerOverrideOn(list=None, colorIndex=0):
	""" toggle outliner color on
	"""

	tempClr = colorMapDict.get(colorIndex)
	outLnrClr = map(lambda x: float(x)/255, tempClr)
	_logger.debug("colorIndex: {0}". format(outLnrClr))

	for item in list:
		item.useOutlinerColor.set(1)
		item.outlinerColor.set(outLnrClr)



def outlinerOverrideOff(list=None):
	""" toggle outliner color off
	"""
	for item in list:
		item.outlinerColor.set(0,0,0)
		item.useOutlinerColor.set(0)



def wireframeOverrideOn(list=None, colorIndex=0):
	""" toggle wireframe color on
	"""
	for item in list:
		item.overrideEnabled.set(1)
		item.overrideRGBColors.set(0)		# make sure it's overridng index color
		item.overrideColor.set(colorIndex)




def wireframeOverrideOff(list=None):
	""" toggle wireframe color off
	"""
	for item in list:
		item.overrideColor.set(1)
		item.overrideRGBColors.set(0)		# make sure it's overridng index color
		item.overrideEnabled.set(0)



def refreshMayaUI():
	mel.eval('AEdagNodeCommonRefreshOutliners()')
	mel.eval('autoUpdateAttrEd')
	mc.refresh()
