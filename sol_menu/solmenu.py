from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import sys	, json
	
#Custom textbox to accept input

class textboxdrag(QPlainTextEdit):

	def __init__(self,parent):
		super(textboxdrag,self).__init__(parent)
		self.setAcceptDrops(True)

	def dragEnterEvent(self, e):
		index = self.parent().treeView.selectedIndexes()[0]
		item = self.parent().model.itemFromIndex(index).text()
		e.mimeData().setText(item)
		e.accept()
	
	def dropEvent(self, e):
		self.setPlainText(e.mimeData().text())

class MainWindow(QWidget):
	def __init__(self):
	
		super(MainWindow, self).__init__()
		self.text1 = textboxdrag(self)
		self.treeView = QTreeView()
		self.treeView.setDragEnabled(True)
		self.treeView.setSelectionMode(QAbstractItemView.SingleSelection)
		self.treeView.setDropIndicatorShown(True)
		self.model = QStandardItemModel()
		self.addItems(self.model, raw_data)
		self.treeView.setModel(self.model)
		
		
		self.model.setHorizontalHeaderLabels([self.tr("Object")])
		
		layout = QHBoxLayout()
		layout.addWidget(self.treeView)
		layout.addWidget(self.text1)
		self.setLayout(layout)
	
	#Treeview item ekleme
	def addItems(self, parent, elements):
		for x in elements:
			if type(elements[x]) == dict:
				item = QStandardItem(x)
				parent.appendRow(item)
				self.addItems(item, elements[x])
			else:
				item = QStandardItem(elements[x])
				parent.appendRow(item)
	
	#Treeview item ekleme(eski, tuple icin)
	def addItems_old(self, parent, elements):
		
		for text, children in elements:
			item = QStandardItem(text)
			parent.appendRow(item)
			if children:
				self.addItems(item, children)
	
if __name__ == "__main__":
	file = open("solmenu.json", "r")
	raw_data = json.load(file)
	file.close()
	app = QApplication(sys.argv)
	window = MainWindow()
	window.show()
	sys.exit(app.exec_())