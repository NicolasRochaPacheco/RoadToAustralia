# Script para comparar los objetos existentes con el pedido
# Desarrollado por Uniandes Pepper Team
# Universidad de Los Andes
# Bogota, Colombia
# Octubre de 2018

#-----------------------
#	CONFIGS
#-----------------------

# Direccion del archivo .csv con los pedidos a leer.
csv_request_file_path = "../../data/request.csv"

# Direccion del archivo .csv con las bebidas identificadas a leer.
csv_identified_file_path = "../../data/identified.csv"

#-----------------------
#	VARIABLES
#-----------------------

# Arreglo en el cual se guardan los pedidos.
pedidos = [ ['nombre' , 'bebida' , 'estado'] ]

# Arreglo en el cual se guardan las bebidas disponibles.
identificadas = []

# Arreglo donde se guarda el estado de los pedidos.
estado = []

#-----------------------
#	LIBRERIAS
#-----------------------

# Se importa la libreria para manejar archivos .csv
import csv

# El formato .csv es leido por el programa
with open( csv_request_file_path ) as csvfile:

	# Se crea un lector para el archivo .csv
	csv_reader = csv.reader( csvfile , delimiter=',' )

	# Un contador de linea es inicializado
	line_count = 0

	# Se hace un recorrido del lector del archivo.
	for row in csv_reader:
		# Si el contador de linea esta en cero, se obvia la linea
		if line_count == 0:
			line_count += 1
		# Si el contador de linea no esta en cero, se procede a leer la linea.
		else:
			nombre = row[0]
			bebida = row[1]
			estado = row[2]
			pedidos.append( [ nombre , bebida , estado ] )
			line_count += 1

# El archivo es cerrado para que otros scripts puedan trabajar con el.
csvfile.close()

# Ahora se lee el archivo de bebidas identificadas.
with open( csv_identified_file_path ) as csvfile:
	# Se crea el lector para el archivo .csv
	csv_reader = csv.reader( csvfile , delimiter=',' )
	# El contador de lineas es reinicializado
	line_count = 0
	# Se recorre el archivo para extraer los datos
	for row in csv_reader:
		# Si el contador de linea esta en cero, la linea se obvia
		if line_count == 0:
			line_count += 1
		# Si el contador de linea no esta en cero, se lee la linea
		else:
			bebida = row[0]
			identificadas.append( bebida )

#El archivo es cerrado para evitar problemas.
csvfile.close()

# Se procede a realizar la comparacion entre el pedido y los objetos identificados
for i in pedidos:
	for j in identificadas:
		if i[2] != 'estado':
			if i[1] == j:
				i[2] = 'esta listo'
				break
			else:
				i[2] = 'no esta listo'

# Se abre el archivo de pedidos nuevamente para ser escrito.
with open( csv_request_file_path , 'w' ) as csvfile:
	# Se crea el lector de archivos .csv
	csv_writer = csv.writer( csvfile )

	# Se escribe el arreglo con los datos de los pedidos
	csv_writer.writerows( pedidos )
