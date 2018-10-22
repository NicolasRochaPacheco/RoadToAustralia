#Maquina de estados vuelta al cliente 
from OralInteraction import OralInteraction
#from missingDrink import MissingDrink
from Cliente import Cliente 
DictionaryStates = {'arriveToClient' : 1, 'requestClients' : 2, 'clientArrived' : 3,'identifyClient':4,'informOrderState':5, 'apology':6, 'listingAlternatives': 9, 'listenChoice':10,'confirmOrder':11, 'returnToBar':13, 'exit':14, 'arrivedNewClient':15}
clients = [Cliente("Adelaida","un guarito","no esta listo"),Cliente("Juan","un cafe","esta listo"),Cliente("José","un milo","esta listo")]
OralInteraction= OralInteraction()
#missingDrink= MissingDrink() 
beverageFound= False
# Variable para la nueva orden
newOrder= " "
# Numero de clientes totales
totalClients = len(clients)
# Variable de iteración
i = 0
# Alternativas dadas por el bartender previamente
alternatives = " agua, gaseosa o cerveza"

state = 'arriveToClient'
while 1:
	if state == 'arriveToClient':
		input("Press Enter to state arriveToClient")
		state='requestClients'

	if state == 'requestClients':
 		OralInteraction.requestClients()
 		state='clientArrived'
	
	while i < totalClients:
		print(state)
		print(i)
		if state == 'clientArrived':
 			input("Press Enter to state clientArrived ")
 			state='identifyClient'

		if state == 'identifyClient':
 			input("Press Enter to state identifyClient")
 			state='informOrderState'
	
		if state == 'informOrderState':
 			beverageFound = OralInteraction.informOrderState(clients[i])
 			if beverageFound== True:
 				if i==totalClients:
 					state='returnToBar'
 				else:
 					i = i + 1
 					state='arrivedNewClient'
 			elif beverageFound==False:
 				state= 'apology'
		
		if state == 'arrivedNewClient':
			input("Press Enter to state arrivedNewClient")
			state='identifyClient'

		if state == 'apology':
 			if beverageFound == False:
 				OralInteraction.apologizeClient()
 				state = 'listingAlternatives'

		if state == 'listingAlternatives':
 			OralInteraction.listingAlternatives(alternatives)
 			state='listenChoice'
 			#retornar lista 

		if state == 'listenChoice':
 			newOrder = OralInteraction.listenChoice()
 			state='confirmOrder'

		if state == 'confirmOrder':
 			OralInteraction.confirmOrder(newOrder)
 			i += 1
 			state='arrivedNewClient'
 			#mandar como parámetro el nuevo order 
	
	if state == 'returnToBar':
 		input("Press Enter to state returnToBar")