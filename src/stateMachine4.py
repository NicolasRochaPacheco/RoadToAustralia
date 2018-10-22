from OralInteraction import OralInteraction
from Cliente import Cliente
import time
DictionaryStates = {'start' : 1, 'waitForBarman' : 2, 'informNewChoice' : 3, 'waitForBarmanResponse':5, 'verifyBarmanResponse':7, 'returnToClients':8}

OralInteraction= OralInteraction()
# Arreglo de clientes inventado para la máquina de estados
clients = [Cliente("Adelaida ","un cóctel","no esta listo"), Cliente("Juan José","una gaseosa","esta listo"), Cliente("Pedro","un cafe con leche","esta listo")]
# String con el nuevo pedido del cliente al que le falto la bebida
newOrder = "una cerveza"

state = 'start'
while True:
	print(state)
	if state == 'start':
		state = 'waitForBarman'

	if state == 'waitForBarman':
		input("Press enter if barman is ready to listen")
		state = 'informNewChoice'

	if state == 'informNewChoice':
		#Dice el nuevo pedido del cliente faltante
		OralInteraction.informNewChoice(clients, newOrder)
		state = 'waitForBarmanResponse'
	
	if state == 'waitForBarmanResponse':
		if (OralInteraction.waitingBarmanResponse() == 1):
			state = 'returnToClients'
		else:
			state = 'waitingBarmanResponse'

	if state == 'returnToClients':
		OralInteraction.returnToClients(clients)