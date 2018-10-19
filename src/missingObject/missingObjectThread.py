# Clase para la identificacion de objetos a partir de una imagen con text to speech.
# Desarrollado por Sinfonia Pepper Team
# Universidad de Los Andes
# Bogota, Colombia
# Octubre de 2018


import cv2
import lightnet
import numpy as np
import csv
from gtts import gTTS
import os

from PyQt5 import QtCore
from PyQt5.QtCore import QThread


class MissingObjectThread( QThread ):

	objectSignal = QtCore.pyqtSignal(str)

	def __init__(self):
		super( MissingObjectThread , self ).__init__()

		self.camera_port = 0
		self.csv_request_file_path = "../../data/request.csv"
		self.img_file_path = "../../data/img.jpg"
		self.objetos_validos = []
		self.pedidos = []
		self.discurso = []
		self.texto = [ 'Hola, ' , ' tu pedido de ' , ' ' ]
		self.beverage_list = [ 'bottle' , 'vase' , 'cup' ]
		self.class_dict = { 	"person":"persona",
					"bottle":"botella",
					"cell phone":"celular",
					"vase":"vaso",
					"cup":"taza" }
		self.running = False
		self.model = lightnet.load('yolo')
		self.cap = cv2.VideoCapture( self.camera_port )

	def run(self):
		self.running = True
		while self.running:
			ret, frame = self.cap.read()
			cv2.imwrite( self.img_file_path , frame )
			self.cap.release()
			cv2.destroyAllWindows()
			image = lightnet.Image.from_bytes( open( self.img_file_path , 'rb' ).read() )
			boxes = self.model( image )
			for objeto in boxes:
				if objeto[1] in self.beverage_list:
					self.objetos_validos.append( self.class_dict[ objeto[1] ] )
			self.leerArchivoCSV()
			self.compararObjetos()
			self.escribirArchivoCSV()
			self.textToSpeech()

	def stop(self):
		self.running = False


	def leerArchivoCSV(self):
		with open( self.csv_request_file_path ) as csvfile:
			csv_reader = csv.reader( csvfile , delimiter=',' )
			for row in csv_reader:
				self.pedidos.append( [ row[0] , row[1] , row[2] ] )

	def compararObjetos(self):
		for pedido in self.pedidos:
			for objeto in self.objetos_validos:
				if pedido[1] == objeto:
					pedido[2] = 'esta listo'
				else:
					pedido[2] = 'no esta listo'

	def escribirArchivoCSV(self):
		with open( self.csv_request_file_path , 'w' ) as csvfile:
			csv_writer = csv.writer( csvfile )
			csv_writer.writerows( self.pedidos )

	def textToSpeech(self):
		for pedido in self.pedidos:
			linea = self.texto[0] + pedido[0] + self.texto[1] + pedido[1] + self.texto[2] + pedido[2]
			self.discurso.append(linea)
		for linea in self.discurso:
			tts = gTTS( text=linea , lang='es' )
			tts.save("speak.mp3")
			os.system("mpg321 speak.mp3")





