from PyQt5.QtCore import QThread
from gtts import gTTS
import playsound

class T2S(QThread):
	def __init__(self):
		super(T2S, self).__init__()
		self.running = False

	def say_something(self,text):
		self.running = True
		grabacion = gTTS(text = text, lang = 'es')
		grabacion.save('output.mp3')
		playsound.playsound('output.mp3',True)