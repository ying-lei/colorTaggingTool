"""

=====================================================

File: colorTaggingTool.py
Use this simple tool to toggle Maya outliner and wireframe color on the fly!

* Works in Maya 2016, 2018
* Only toggle override on transform node, not shape node
* Only using index color as wireframe color

* v005

Copyright (C) 2019 Yinglei Yang www.ying-lei.com

=====================================================

Usage:
* run following commands in Maya Python

import colorTaggingTool as ctool
ctool.run()


"""


try:
	from PySide import QtCore, QtUiTools
	from PySide import QtGui as qtToolInstance
except:
	from PySide2 import QtCore, QtUiTools
	from PySide2 import QtWidgets as qtToolInstance


try:
	from shiboken import wrapInstance
except:
	from shiboken2 import wrapInstance


import os
import functools
import maya.cmds as mc
import pymel.core as pm
import maya.OpenMayaUI as omui
import maya.mel as mel

import logging
_logger = logging.getLogger(__name__)
_logger.setLevel(logging.ERROR)




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


# UI var
win = None

# ==================== MAIN UI ====================


def getMayaWindow():
	""" pointer to the maya main window
	"""

	ptr = omui.MQtUtil.mainWindow()

	if ptr:
		return wrapInstance(long(ptr), qtToolInstance.QMainWindow)



def run():
	""" builds UI
	"""
	global win

	# close window if window exist
	if win:
		win.close()

	win = ColorTaggingUI(parent=getMayaWindow())



class ColorTaggingUI(qtToolInstance.QDialog):
	""" Main UI
	"""


	def __init__(self, parent = None):
		super(ColorTaggingUI, self).__init__(parent)


		# UI variables
		self.outlinerEnable = 0
		self.wireframeEnable = 0

		# self.counter = 0

		# topmost layout
		self.gridLayout = qtToolInstance.QGridLayout()
		self.verticalLayout = qtToolInstance.QVBoxLayout()
	
		# label
		self.taggingLabel = qtToolInstance.QLabel("Tagging color for...")
		self.verticalLayout.addWidget(self.taggingLabel)
		
		# checkbox
		self.outlinerCheckbox = qtToolInstance.QCheckBox("Outliner")
		self.outlinerCheckbox.setChecked(True)
		self.verticalLayout.addWidget(self.outlinerCheckbox)
		
		self.wireframeCheckbox = qtToolInstance.QCheckBox("Wireframe")
		self.verticalLayout.addWidget(self.wireframeCheckbox)

		# button grid
		self.buttonGridLayout_1 = qtToolInstance.QGridLayout()
		self.buttonGridLayout_1.setHorizontalSpacing(1)
		self.buttonGridLayout_1.setVerticalSpacing(1)

		self.taggingButtonGrp = qtToolInstance.QButtonGroup()

		# adding buttons to grid
		outlinerBtnNum = 0
		for i in range(4):
			for j in range(8):
				self.colorButton = qtToolInstance.QPushButton("")
				self.colorButton.setMinimumSize(20,20)
				self.colorButton.setMaximumSize(20,20)
				self.colorButton.setCheckable(1)
	
				if outlinerBtnNum == 0:
					self.colorButton.setText("X")
	
	
				else:
					bColor = colorMapDict.get(outlinerBtnNum)
					#_logger.debug("bColor: {0}".format(bColor))
	
					self.colorButton.setStyleSheet('QPushButton {background-color: rgb(%d,%d,%d); color: white}' % (bColor))
	
	
				self.taggingButtonGrp.addButton(self.colorButton, outlinerBtnNum)
	
				# adding button to the grid
				self.buttonGridLayout_1.addWidget(self.colorButton, i, j)
				outlinerBtnNum += 1
	
		self.verticalLayout.addLayout(self.buttonGridLayout_1)



		# disable all btn
		self.disableAllBtn = qtToolInstance.QPushButton("Disable All On Selections")
		self.disableAllBtn.setStyleSheet('QPushButton {background-color: rgb(50,0,0); color: white}' )
		self.verticalLayout.addWidget(self.disableAllBtn)

		self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)



		# calling UI
		self.makeConnections()
		self.setWindowTitle("COLOR TAGGING TOOL")
		self.setLayout(self.gridLayout)

		self.setFixedSize(230, 200)

		self.initUIState();
		self.show();




	# ==================== UI FUNCTIONS ====================
	
	def initUIState(self, colorIndex = 0):
		""" sets up init state of UI
		"""
		self.initButtonGroup(self.taggingButtonGrp)
		
		self.outlinerCheckboxToggled()
		self.wireframeCheckboxToggled()




	def makeConnections(self):
		""" connect events in UI"""
	
		self.taggingButtonGrp.buttonClicked.connect(self.taggingButtonClicked)
		self.disableAllBtn.clicked.connect(self.disableAllBtnClicked)

		self.outlinerCheckbox.stateChanged.connect(self.outlinerCheckboxToggled)
		self.wireframeCheckbox.stateChanged.connect(self.wireframeCheckboxToggled)



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

		if not len(disableList) == 0:
			outlinerOverrideOff(disableList)
			wireframeOverrideOff(disableList)

		else:
			_logger.error("Nothing selected")

		self.initUIState()
		refreshMayaUI()




	def taggingButtonClicked(self):
		""" tagging color based on selected color index
		"""

		colorIndex = self.taggingButtonGrp.checkedId()
		_logger.debug("colorIndex: {0}".format(colorIndex)) 

		colorOnList = getSelection()		
		_logger.debug("colorOnList: {0}".format(colorOnList)) 


		# tag outliner color
		if self.outlinerEnable == 1:

			if not len(colorOnList) == 0:

				if colorIndex == 0:
					outlinerOverrideOff(colorOnList)
					_logger.debug("Disable outliner color") 
				
				else:
					outlinerOverrideOn(colorOnList, colorIndex)
					_logger.debug("Enable outliner color") 

			else:
				_logger.error("Nothing selected")

		else:
			pass


		# tag wireframe color
		if self.wireframeEnable == 1:

			if not len(colorOnList) == 0:

				if colorIndex == 0:
					wireframeOverrideOff(colorOnList)
					_logger.debug("Disable outliner color") 
				
				else:
					wireframeOverrideOn(colorOnList, colorIndex)
					_logger.debug("Enable outliner color") 

			else:
				_logger.error("Nothing selected")

		else:
			pass



		self.initUIState()
		refreshMayaUI()




	def outlinerCheckboxToggled(self):
		""" check if outliner checkbox is enable
		"""
		self.outlinerEnable = self.outlinerCheckbox.isChecked() 
		_logger.debug("outlinerEnable: {0}".format(self.outlinerEnable))




	def wireframeCheckboxToggled(self):
		""" check if wireframe checkbox is enable
		"""
		self.wireframeEnable = self.wireframeCheckbox.isChecked() 
		_logger.debug("wireframeEnable: {0}".format(self.wireframeEnable))




	def toggleWireframeColor(self, colorIndex = None):
		""" toggle wireframe color based on colorIndex
		"""

		buttonToToggle = self.wireframeButtonGrp.button(colorIndex)
		buttonToToggle.setChecked(True)




	def toggleOutlinerColor(self, colorIndex = None):
		""" toggle outliner color based on colorIndex
		"""

		buttonToToggle = self.taggingButtonGrp.button(colorIndex)
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
	""" refresh UI after updates
	"""
	mel.eval('autoUpdateAttrEd')
	mc.refresh()

	if int(mel.eval('exists AEdagNodeCommonRefreshOutliners')) == 1:
		mel.eval('AEdagNodeCommonRefreshOutliners()')
	else:
		pass

