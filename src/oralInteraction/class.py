from OralInteraction import OralInteraction
DictionaryStates = {'start' : 1, 'introduction' : 2, 'waitingPerson' : 3,'requestName':4, 'listeningName':5, 'verifyName' : 6, 'requestDrink' : 7, 'linsteningDrink':8,...
... 'verifyDrink':9, 'requestNewPerson':10, 'waitingNewPerson':11, 'exit':12, 'apology' : 13}

state = start
missunderstoodName = False
missunderstoodDrink = False
OralInteraction = OralInteraction()

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
		self.name = OralInteraction.listeningName()
		state = verifyName
		
	if state == verifyName:
		missunderstoodName = self.verifyName(name)
		if missunderstoodName == False
			state = requestDrink
		else:
			state = apology

	if state == requestDrink:
		OralInteraction.solicitarPedido()
		state = linsteningDrink

	if state == linsteningDrink:
		OralInteraction.askForDrink()
		state = verifyDrink
		
	if state == verifyDrink:
		missunderstoodDrink = OralInteraction.verifyDrink(name)
		if missunderstoodDrink == False
			state = requestDrink
		else:
			state = apology
		
	if state == requestNewPerson:
		OralInteraction.requestNewPerson()
		state = waitingPerson

	if state == waitingNewPerson:
		input("Press Enter to state waitingPerson")
		
	if state == exit:
		OralInteraction.exit()

	if state == apology
		if missunderstoodName == True
			OralInteraction.apologizeName()
			missunderstoodName = False
			state = askForName
		elif missunderstoodDrink == True:
			OralInteraction.apologizeDrink()
			missunderstoodDrink =False
			state = askForDrink
