# Widget para probar el thread del objeto perdido.
# Desarrollado por Sinfonia Pepper Team
# Universidad de Los Andes
# Bogota, Colombia
# Octubre de 2018

from PyQt5 import uic, QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
import sys
from PyQt5.QtCore import pyqtSlot
#from missingObject.missingObjectThread import MissingObjectThread

class MainWindow( QtWidgets.QMainWindow ):

	def __init__(self):
		super(MainWindow, self).__init__()

		self.bt_widget = ButtonWidget(self)
		self.setCentralWidget(self.bt_widget)
		#self.missingObjectThread = MissingObjectThread()
		#self.missingObjectThread.objectSignal.connect('')
		#self.missingObjectThread.start()

class ButtonWidget(QWidget):

	def __init__(self, parent):
		super(ButtonWidget, self).__init__(parent)
		self.layout = QVBoxLayout(self)
		self.layout.addWidget(QPushButton("Inicial"))
		self.layout.addWidget(QPushButton('Palal'))
		self.setLayout( self.layout )


if __name__ == '__main__':
	app = QApplication(sys.argv)	
	window = MainWindow()
	window.show()	
	sys.exit(app.exec_())

