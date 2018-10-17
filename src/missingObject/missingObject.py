# Script para la identificacion de objetos a partir de una imagen con text to speech.
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
img_file_path = "../../data/"


#------------------------
#	LIBRERIAS
#------------------------

# Libreria de OpenCV para capturar la imagen de la camara web.
import cv2

# Libreria de Lightnet para identificar los objetos.
import lightnet

#------------------------
#	VARIABLES
#------------------------

# Objeto de VideoCapture para tomar las imagenes.
cap = cv2.VideoCapture( camera_port )

# Modelo de la red neuronal para identificar objetos de las imagenes.
model = lightnet.load('yolo')

#------------------------
#	ALGORITMO
#------------------------

# Se captura la imagen de la camara
ret, frame = cap.read()

# La idea es meter el frame en la red neuronal.





# El VideoCapture es cerrado
cap.release()
# Las instancias de OpenCV son destruidas
cv2.destroyAllWindows()
