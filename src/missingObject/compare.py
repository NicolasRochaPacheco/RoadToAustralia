# Script para comparar los objetos existentes con el pedido
# Desarrollado por Uniandes Pepper Team
# Universidad de Los Andes
# Bogota, Colombia
# Octubre de 2018

# Direccion del archivo .csv a leer
csv_file_path = "../../data/request.csv"

# Arreglo en el cual se guardan las bebidas solicitadas.



# Se importa la libreria para manejar archivos .csv
import csv

# El formato .csv es leido por el programa
with open( csv_file_path ) as csvfile:

	# Se crea un lector para el archivo .csv
	csv_reader = csv.reader( csvfile , delimiter=',' )

	# Un contador de linea es inicializado
	line_count = 0

	# Se hace un recorrido del lector del archivo.
	for row in csv_reader:
		
		# Si el contador de linea esta en cero, se obvia la linea
		if line_count == 0:
			#print("Los nombres de las columnas son: %s" % " ".join(row) )
			line_count += 1
		# Si el contador de linea no esta en cero, se procede a leer la linea.
		else:
			print("%s quiere %s." % ( row[0] , str( row[1] ) ) )
			line_count += 1

# El archivo es cerrado para que otros scripts puedan trabajar con el.
csvfile.close()


