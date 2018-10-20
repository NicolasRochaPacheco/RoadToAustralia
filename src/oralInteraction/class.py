from OralInteraction import OralInteraction
from Cliente import Cliente
DictionaryStates = {'start' : 1, 'introduction' : 2, 'waitingPerson' : 3,'requestName':4, 'listeningName':5, 'verifyName' : 6, 'requestDrink' : 7, 'linsteningDrink':8,...
... 'verifyDrink':9, 'requestPerson':10, 'waitingNewPerson':11, 'exit':12, 'apology' : 13, 'listeningNewPerson' : 14, 'verifyNewPerson' : 15...
... 'affirmationNewPerson' : 16}

state = start
missunderstoodName = False
missunderstoodDrink = False
missunderstoodNewPerson = False
name = ""
drink = ""
newPerson = ""
OralInteraction = OralInteraction()
clientCount = 0
clients = []

while 1
	print(state)
	if state == start
		state = introduction

	if state == introduction:
		OralInteraction.greet()
		state = waitingPerson
		
	if state == waitingPerson:
		input("Press Enter to state requestName")
		state = requestName

	if state == requestName:
		OralInteraction.askForName()
		state = listeningName
		
	if state == listeningName:
		name = OralInteraction.listeningName(OralInteraction.capturarAudio())
		if name == ""
			missunderstoodName = True
			state = apology
		else:
			state = verifyName
		
	if state == verifyName:
		OralInteraction.verifyName(name)
		missunderstoodName = OralInteraction.affirmationCheck(OralInteraction.capturarAudio())
		if missunderstoodName == False
			state = requestDrink
			newClient = Cliente(name,"","no esta listo")
		else:
			state = apology

	if state == requestDrink:
		OralInteraction.askForDrink()
		state = linsteningDrink

	if state == linsteningDrink:
		drink = OralInteraction.listeningDrink(OralInteraction.capturarAudio())
		if drink == ""
			missunderstoodDrink = True
			state = apology
		else:
			state = verifyDrink
		
	if state == verifyDrink:
		OralInteraction.verifyDrink(drink)
		missunderstoodDrink = OralInteraction.affirmationCheck(OralInteraction.capturarAudio())
		if missunderstoodDrink == False
			state = requestNewPerson
			newClient.cambiarPedido(drink)
			clients.append(newClient)
		else:
			state = apology

	if state == requestNewPerson:
		OralInteraction.askForNewPerson()
		state = listeningNewPerson

	if state == listeningNewPerson
		newPerson = OralInteraction.listeningNewPerson(OralInteraction.capturarAudio())
		if newPerson == ""
			missunderstoodNewPerson = True
			state = apology
		else:
			state = verifyNewPerson

	if state == verifyNewPerson
		OralInteraction.verifyNewPerson(newPerson)
		missunderstoodNewPerson = OralInteraction.affirmationCheck(OralInteraction.capturarAudio())
		if missunderstoodNewPerson == False:
			state = affirmationNewPerson
		else:
			state = apology

	if state == affirmationNewPerson
		newPersonBoolean = OralInteraction.affirmationCheck(newPerson)
		if newPersonBoolean == True
			state = waitingPerson
		else:
			state = exit

	if state == exit:
		OralInteraction.exit()

	if state == apology:
		OralInteraction.apologize()
		if missunderstoodName == True
			missunderstoodName = False
			state = requestName
		elif missunderstoodDrink == True
			missunderstoodDrink =False
			state = requestDrink
		elif missunderstoodNewPerson == True
			missunderstoodNewPerson = False
			state = requestNewPerson