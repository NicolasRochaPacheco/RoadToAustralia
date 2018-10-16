from PyQt5.QtWidgets import QApplication
#Core.S2T.
from MicThread import MicThread
from S2TThread import S2TThread
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5 import uic, QtWidgets
import sys


class MainWindow(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.fn_init_ui()

        self.micThread = MicThread()
        self.s2tThread = S2TThread()

        #self.s2tThread.wsReadySignal.connect(self.micThread.slot_ws_ready)
        self.s2tThread.sendSTTSignal.connect(self.slot_receive_text)
        self.s2tThread.stoppedSpeakingSignal.connect(self.slot_receive_text_silent)
        self.micThread.audioSignal.connect(self.s2tThread.slot_receive_stream)

        self.s2tThread.start()
        self.micThread.start()

    def fn_init_ui(self):
        uic.loadUi("S2TUi.ui", self)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(p)

    def mousePressEvent(self, QMouseEvent):
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.red)
        self.setPalette(p)

        self.micThread.slot_on_speaking(True)

    def mouseReleaseEvent(self, QMouseEvent):
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(p)

        self.micThread.slot_on_speaking(False)

    @pyqtSlot(str)
    def slot_receive_text(self, text):
        self.lblS2T.setText(text)

    @pyqtSlot(str)
    def slot_receive_text_silent(self, text):
        print("S2TWidget: Send TA = ", text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    w = 200; h = 200
    mainWindow.resize(w, h)
    mainWindow.show()
    sys.exit(app.exec_())
