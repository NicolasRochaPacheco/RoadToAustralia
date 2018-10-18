# Clase para la identificacion de objetos a partir de una imagen con text to speech.
# Desarrollado por Sinfonia Pepper Team
# Universidad de Los Andes
# Bogota, Colombia
# Octubre de 2018

#------------------------
#	CONFIGS
#------------------------

# Puerto de la camara a usar por parte del programa.
camera_port = 0

# Direccion del archivo .csv con los datos de los pedidos.
csv_request_file_path = "../../data/request.csv"

# Direccion de salida de las imagenes
img_file_path = "../../data/img.jpg"


#------------------------
#	LIBRERIAS
#------------------------

# Libreria de OpenCV para capturar la imagen de la camara web.
import cv2

# Libreria de Lightnet para identificar los objetos.
import lightnet

# Libreria Numpy para el manejo de arreglos.
import numpy as np

# Libreria CSV para manejar archivos .csv
import csv

# Se importa la libreria para que el robot hable
from gtts import gTTS
import os


#------------------------
#	VARIABLES
#------------------------

# Objeto de VideoCapture para tomar las imagenes.
cap = cv2.VideoCapture( camera_port )
cap.set( 3 , 1280 )
cap.set( 4 , 1024 )

# Modelo de la red neuronal para identificar objetos de las imagenes.
model = lightnet.load('yolo')

# Arreglo en el cual se agregan los objetos validos.
objetos_validos = []

# Arreglo en el cual se guardan los pedidos.
pedidos = []

# Arreglo con el discurso del robot.
discurso = []

# Variables de formatos de texto
text0 = 'Hola, '
text1 = ', tu pedido de '
text2 = ' '

# Lista de los objetos considerados para la seleccion
beverage_list = [ 'bottle' , 'vase' , 'cup' ]

# Diccionario para las clases de los objetos
# TODO: Buscar la manera de traducir las clases de YOLOv2 y agregarlas al script.
class_dict = { "person":"persona" , "bottle":"botella" , "cell phone":"celular" , "vase":"vaso" , "cup":"taza"}


#------------------------
#	ALGORITMO
#------------------------

#---------------------------------------------------------------
#	TOMA DE LA CAMARA E IDENTIFICACION DE OBJETOS

# Se captura la imagen de la camara
ret, frame = cap.read()

# La imagen es guarda en una archivo .jpg
cv2.imwrite( img_file_path , frame )

# El archivo .jpg es leido como bytes y llevado al formato requerido.
# La idea es meter el frame en la red neuronal directamente.
image = lightnet.Image.from_bytes( open( img_file_path , 'rb' ).read() )

# Se pasa la imagen en la red neuronal para obtener los objetos identificados.
boxes = model( image )

print( boxes )

# Las clases de los boxes son leidos
for objeto in boxes:
	# Si un objeto identificado pertenece a la lista de bebidas, se agrega a los objetos validos
	if objeto[1] in beverage_list:
		objetos_validos.append( class_dict[ objeto[1] ] )

# El VideoCapture es cerrado
cap.release()
# Las instancias de OpenCV son destruidas
cv2.destroyAllWindows()


#---------------------------------------------------------------
#	LECTURA DEL CSV DE LOS PEDIDOS

#El formato .csv es leido por el programa
with open( csv_request_file_path ) as csvfile:

	# Se crea un lector para el archivo .csv
	csv_reader = csv.reader( csvfile , delimiter=',' )

	# Se hace un recorrido del lector del archivo.
	for row in csv_reader:
		# El pedido es agregado al vector de pedidos.
		pedidos.append( [ row[0] , row[1] , row[2] ] )


#---------------------------------------------------------------
#	COMPARACION ENTRE LOS OBJETOS VALIDOS Y LOS PEDIDOS

for pedido in pedidos:
	for objeto in objetos_validos:
		if pedido[1] == objeto:
			pedido[2] = 'esta listo'
		else:
			pedido[2] = 'no esta listo'

#---------------------------------------------------------------
#	ESCRITURA DELS ARCHIVO .CSV ACTUALIZADO

# Se abre el archivo de pedidos nuevamente para ser escrito.
with open( csv_request_file_path , 'w' ) as csvfile:
	# Se crea el lector de archivos .csv
	csv_writer = csv.writer( csvfile )

	# Se escribe el arreglo con los datos de los pedidos
	csv_writer.writerows( pedidos )

#---------------------------------------------------------------
#	TEXT TO SPEECH

for pedido in pedidos:
	linea = text0 + pedido[0] + text1 + pedido[1] + text2 + pedido[2]
	discurso.append(linea)

for linea in discurso:
	tts = gTTS( text=linea , lang='es' )
	tts.save("speak.mp3")
	os.system("mpg321 speak.mp3")





