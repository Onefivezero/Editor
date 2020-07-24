from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *
from datetime import datetime
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys
import os


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        #grafik widgeti ve menu olustur
        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)
        file_menu = self.menuBar().addMenu("&File")

        #Dosya acma menuye ekle
        open_file_action = QAction(QIcon(os.path.join('images', 'blue-folder-open-document.png')), "Open file...", self)
        open_file_action.triggered.connect(self.file_open)
        file_menu.addAction(open_file_action)
        # plot data: x, y values
        #self.graphWidget.plot(x, y)
            
    #Dosya ac
    def file_open(self):
        fname, _ = QFileDialog.getOpenFileName(self, "Open file", "", "Text documents (*.txt);All files (*.*)")
        if fname:
            f = open(fname, "r")
            datas = []
            for x in f:
                indx = x.find(": ")
                x.rstrip();
                y = int(x[indx+2:])
                datas.append(y)
            self.graphWidget.plot(range(len(datas)), datas)

#Main
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
