# Script para crear el texto que va a ser hablado
# Desarrollado por Sinfonia Pepper Team Uniandes
# Universidad de Los Andes
# Bogota, Colombia
# Octubre de 2018

#-----------------------
#	CONFIGS
#-----------------------

# Direccion del archivo .csv con los pedidos.
csv_request_file_path = "../../data/request.csv"

#-----------------------
#	VARIABLES
#-----------------------

# Arreglo en el cual se guardan los pedidos.
pedidos = []

# Arreglo con el discurso del robot.
discurso = []

# Variables de formatos de texto
text0 = 'Hola '
text1 = ', tu pedido de '
text2 = ' '

#-----------------------
#	LIBRERIAS
#-----------------------

# Se importa la libreria para manejar archivos .csv
import csv

# Se importa la libreria para que el robot hable
from gtts import gTTS
from pygame import mixer
import os


with open( csv_request_file_path ) as csvfile:
	csv_reader = csv.reader( csvfile , delimiter=',' )
	line_count = 0
	for row in csv_reader:
		if line_count == 0:
			line_count += 1
		else:
			nombre = row[0]
			bebida = row[1]
			estado = row[2]
			pedidos.append( [ nombre , bebida , estado ] )
			line_count += 1

csvfile.close()

for pedido in pedidos:
	linea = text0 + pedido[0] + text1 + pedido[1] + text2 + pedido[2]
	discurso.append(linea)

for linea in discurso:
	tts = gTTS( text=linea , lang='es' )
	tts.save("joda.mp3")
	os.system("mpg321 joda.mp3")

