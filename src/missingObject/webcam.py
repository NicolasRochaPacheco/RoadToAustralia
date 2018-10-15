# Codigo para capturar una imagen de una camara web.
# Desarrollado por Uniandes Pepper Team
# Universidad de Los Andes
# Bogota, Colombia
# Octubre de 2018

# La camara se encuentra en el puerto 0 del computador.
camera_port = 0
data_dir = "../outputData/"


# Se importa la libreria de numpy y matplotlib.
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

# Se importa la libreria de OpenCV.
import cv2

#Se crea el objeto de Video Capture.
cap = cv2.VideoCapture( camera_port )

# Recorrido para probar multiples tomas de la camara web.
for i in range( 0 , 10 ):
	# Se imprime el numero de la iteracion
	print( i )

	# Se captura la imagen de la cara web
	ret, frame = cap.read()

	# Si la imagen fue capturada adecuadamente, se guarda en un archivo
	if( ret ):
		# Se crea la figura para guardar la imagen
		fig = plt.figure()

		#Se imprime la imagen en la figura
		plt.imshow( frame )

		# Se guarda la figura con el numero de iteracion
		fig.savefig( data_dir + "frame" + str(i) + ".png" )

# Se liberan los componentes para usarlos despues.
cap.release()
cv2.destroyAllWindows()
