from PyQt5 import uic, QtWidgets
#Core.T2S.
from T2SThread import T2SThread
from PyQt5.QtWidgets import QApplication
import sys



class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.fn_init_ui()
        self.t2sThread = T2SThread()

        self.t2sThread.start()


    def fn_init_ui(self):
        uic.loadUi("t2sUi.ui", self)
        self.btnSpeak.clicked.connect(self.robot_speak)

    def robot_speak(self):
        self.t2sThread.say_something(self.leText.text())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
