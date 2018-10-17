# Script para comentar las bebidas faltantes de los invitados
# Desarrollado por Sinfonia Pepper Team Uniandes
# Universidad de Los Andes
# Bogota, Colombia
# Octubre de 2018 

# Se importa la libreria de espeak
from espeak import espeak

# El espeak se configura en espanhol
espeak.set_voice("es")

# Charla de prueba
espeak.synth( "Hola a todos." )

while espeak.is_playing:
	pass




