from PyQt5 import uic, QtWidgets
#from T2S import T2S
from T2SThread import T2SThread
from Cliente import Cliente
import os 
import speech_recognition as sr
import csv
import time
import os 
import sys
from ListasEntendimiento import ListasEntendimiento
import random
from gtts import gTTS
import playsound
from Saludos import Saludos

class OralInteraction():
    def __init__(self):
        #super(MainWindow, self).__init__()
        self.t2sThread = T2SThread()
        #self.t2sThread = T2S()
        self.t2sThread.start()
        self.saludos = Saludos()    

        #Declaración de Strings necesarios
        self.ListasEntendimiento = ListasEntendimiento()
        self.clientes = []
        self.listaNombres = self.ListasEntendimiento.darListaNombres()
        self.listaPedidos = self.ListasEntendimiento.darListaPedidos()
        self.listaAfirmaciones = self.ListasEntendimiento.darListaAfirmaciones()
        self.listaNegaciones = self.ListasEntendimiento.darListaNegaciones()
        self.listaBartender = self.ListasEntendimiento.darListaBartender()
        self.listaAlternativas = self.ListasEntendimiento.darListaAlternativas()
        self.totalClientes = 1
        self.alternativas = ""
        self.alternativaReemplazo = ""
        self.clienteFaltante = Cliente("", "", "no esta listo")


    #Métodos que definen qué dice el robot
    #Saludo al cliente
    def greet(self):
        string = self.saludos.darSaludos(random.randint(1,3))
        self.t2sThread.say_something(string)
        time.sleep(8)

    #Disculparse por comprender mal el nombre
    def apologize(self):
        string = self.saludos.disculpar(random.randint(1,3))
        self.t2sThread.say_something(string)
        time.sleep(4)

    #Asks the client for name
    def askForName(self):
        string = self.saludos.solicitarNombre(random.randint(1,3))
        self.t2sThread.say_something(string)
        time.sleep(2)

    #Asks the client for drink
    def askForDrink(self):
        string = self.saludos.solicitarPedidos(random.randint(1,3))
        self.t2sThread.say_something(string)
        time.sleep(2)
    
    #Asks the client for newPerson
    def askForNewPerson(self):
        string = self.saludos.masClientes(random.randint(1,3))
        self.t2sThread.say_something(string)
        time.sleep(2)

    #Confirms the understood name
    def verifyName(self, pName):
        verificacionInicial = self.saludos.verificarNombres(random.randint(1,3))
        verificacionFinal = self.saludos.verificarFinal(random.randint(1,3))
        string = verificacionInicial + pName + verificacionFinal
        self.t2sThread.say_something(string)
        time.sleep(2)

    #Confirms the understood drink
    def verifyDrink(self, pDrink):
        string = self.saludos.confirmarPedidos(random.randint(1,3)) + pDrink
        self.t2sThread.say_something(string)
        time.sleep(6)

    #Confirms the understood newPerson
    def verifyNewPerson(self, pNewPerson):
        string = "Comprendí que " + pNewPerson + " hay una nueva persona. Estoy en lo correcto?"
        self.t2sThread.say_something(string)
        time.sleep(2)

    #If there are no more clients
    def exit(self):
        string = self.saludos.noMasClientes(random.randint(1,3))
        self.t2sThread.say_something(string)
        time.sleep(3)

    #Builds the bartender string with the requests    
    def stingBartender(self, nombre, pedido):
        string = nombre + "me pidió" + pedido
        self.t2sThread.say_something(string)    
        time.sleep(4)

    #Asks  the bartender for alternatives
    def askForAlternatives(self, clienteFaltante):
        string = "Veo que falta el pedido de " + clienteFaltante.darNombre() + " Qué alternativas tienes?"
        self.t2sThread.say_something(string)
        time.sleep(6)

    #Informs the client the available alternatives
    def informAlternativas(self, alternativas, clienteFaltante):
        string = "Lo siento" + clienteFaltante.darNombre() + " . No tengo " + clienteFaltante.darPedido() + ". Podría ofrecerte: " + self.alternativas + ". ¿Que te gustaría?"
        self.t2sThread.say_something(string)
        time.sleep(5)

    #Obtains the name upon a string
    def listeningName(self, string):
        palabras = string.split()
        nombre =""
        for i in palabras:
            if i in self.listaNombres:
                auxNombre = palabras[(palabras.index(i)+1):(len(palabras))]
                nombre = self.buildString(auxNombre)
                print(nombre)
            elif len(palabras)<=2:
                nombre = string
        print(nombre)
        return nombre

    #Obtains the drink upon a string
    def listeningDrink(self, string):
        palabras = string.split()
        pedido = ""
        for i in palabras:
            if i in self.listaPedidos:
                auxPedido = palabras[(palabras.index(i)):(len(palabras))]
                if "por" in auxPedido:
                    auxPedido.remove("por")
                if "porfavor" in auxPedido:
                    auxPedido.remove("porfavor")
                if "favor" in auxPedido:
                    auxPedido.remove("favor")
                if "gracias" in auxPedido:
                    auxPedido.remove("gracias")
                if "y" in auxPedido:
                    auxPedido.remove("y")
                pedido = self.buildString(auxPedido)
                print(pedido)
        return pedido


    #comprensionBartender
    #Returns true when the bartender is ready with the drinks
    def listeningBartender(self, string):
        palabras = string.split()
        entendido = False
        for i in palabras:
            if i in self.listaBartender:
                entendido = True               
        return entendido
    
    #comprensionAlternativas
    #Obtains the avilable alternativs upon a string
    def listeningAlternativesBartender(self, string):
        opciones = string.split()
        listado = []
        for i in opciones:
            if i == "son":
                listado = opciones[opciones.index(i)+1:len(opciones)]
        self.alternativas = self.buildString(listado)
        return self.alternativas

    #compresionAlternativaCliente
    #obtains the chosen alternative from the client upon a string
    def listeningAlternativesClient(self,string):
        palabras = string.split()
        auxAlternativas =[]
        for i in palabras:
            if i in self.listaAlternativas:
                auxAlternativas = palabras[(palabras.index(i)+1):(len(palabras))]
            else: 
                auxAlternativas = palabras
        alternativa = self.buildString(auxAlternativas)
        return alternativa 

    #verificarAlternativas
    #verifies the understood avilable alternatives
    def verifyAlternativesBartender(self):
        verificacionInicial = "Comprendí las alternativas son "
        verificacionFinal = self.saludos.verificarFinal(random.randint(1,3))
        string = verificacionInicial + self.alternativas + verificacionFinal
        self.t2sThread.say_something(string)
        time.sleep(5)


    #Métodos adicionales
    #Reconstruccion de strings
    def buildString(self,lista):   
        reconstruido = ""
        for i in lista:
            reconstruido +=i
            reconstruido +=" "
        return reconstruido    

    #Encuentra el cliente que pidio el objeto faltante
    def objetoFaltante(self): 
        self.csvfile_reader()
        self.clienteFaltante =  Cliente("","","")
        for i in self.clientes:
            if i.darEstadoPedido() == "no esta listo":
                self.clienteFaltante = self.clientes[self.clientes.index(i)]
        return self.clienteFaltante
    
    #"Una bolella de agua" -> "botella de agua"
    #Quitar el articulo en el pedido
    def ajustePedido(self,pPedido):
        separado = pPedido.split()
        final = self.buildString(separado[1:len(separado)])
        return final

    #Afirmacion no negacion
    def affirmationCheck(self, string):
        palabras = string.split()
        afirmacion = False
        nonegacion = False
        for i in palabras:
            if i in self.listaAfirmaciones:
                afirmacion = True
            if ~(i in self.listaNegaciones):
                nonegacion = True
        return afirmacion and nonegacion


    #Métodos de captura de audio
    #Captura de audio
    def captureAudio(self):
        r = sr.Recognizer()
        with sr.Microphone(device_index = 5, sample_rate = 44100, chunk_size = 512) as source:
            r.adjust_for_ambient_noise(source, duration=2)
            print("Recording")
            audio = r.listen(source, phrase_time_limit=3.5)
        #try:
        #    audio1 =r.recognize_ibm(audio, language='es-ES', username="0d53ad4a-5068-4a73-bcbb-8e119e6c9ff6", password="GKNXDhqEfvAb")
        #    print(audio1)
        #except sr.UnknownValueError:
        #    audio1 = "IBM Speech to Text could not understand audio"
        #except sr.RequestError as e:
        #    audio1 = "Could not request results from IBM Speech to xText service"
        try:
            audio1 = r.recognize_google(audio, language='es-ES')
            print(audio1)
        except sr.UnknownValueError:
            audio1 = "Google Speech Recognition could not understand audio"
        except sr.RequestError as e:
            audio1 = "Could not request results from Google Speech Recognition service"
        return audio1


    #Método para obtener los pedidos    
    def pedidos(self):
        x=0
        self.continuar = 0
        while x < self.totalClientes:
            clienteActual = Cliente("","","no esta listo")
            self.saludar()
            print("Nombre")
            #while self.audioDefinitivo() == 0:
                #self.disculpaRuido()
            #print(self.capturarAudio())
            self.nombre = self.comprensionNombre(self.capturarAudio())
            while ((self.nombre == "") or (self.nombre==" ")):
                print("Ruido")
                self.disculpaRuido()
                self.nombre = self.comprensionNombre(self.capturarAudio())

            self.noComprendio = 0
            while self.continuar == 0:
                if self.noComprendio == 1:
                    self.disculparNombre()
                    print("Nombre equivocado")
                    self.nombre = self.comprensionNombre(self.capturarAudio())
                    clienteActual.cambiarNombre(self.nombre)
                self.verificarNombre(self.nombre)
                self.continuar = self.afirmacionCheck(self.capturarAudio())
                self.noComprendio = 1
            print("Nombre: " + str(self.nombre))
            clienteActual.cambiarNombre(self.nombre)

            self.continuar = 0

            self.solicitarPedido()
            print("Pedido")
            
            self.pedido = self.comprensionPedido(self.capturarAudio())
            while ((self.pedido == "") or (self.pedido==" ")):
                print("Ruido")
                self.disculpaRuido()
                print(self.pedido)
                self.pedido = self.comprensionPedido(self.capturarAudio())
                print(self.pedido)

            self.noComprendio = 0
            while self.continuar == 0:
                if self.noComprendio == 1:
                    self.disculparPedido()
                    print("No entendido el pedido")
                    self.pedido = self.comprensionPedido(self.capturarAudio())
                    clienteActual.cambiarPedido(self.ajustePedido(self.pedido))
                self.verificarPedido(self.pedido)
                self.continuar = self.afirmacionCheck(self.capturarAudio())
                self.noComprendio = 1
            print("Pedido: " + str(self.ajustePedido(self.pedido)))
            clienteActual.cambiarPedido(self.ajustePedido(self.pedido))
            
            self.confirmarPedido(self.pedido)
            self.continuar = 0

            self.clientes.append(clienteActual)
            
            self.masClientes()
            if (self.afirmacionCheck(self.capturarAudio()) == 1):
                self.totalClientes += 1
            else:
                self.noMasClientes()
            x+=1
        self.csvfile_writer()

    #Informar al bartender los pedidos obtenidos
    def bartender(self):
        self.csvfile_reader()
        time.sleep(5)
        self.t2sThread.say_something("Hola, Héctor, los pedidos que recibí son los siguientes:")
        time.sleep(5)
        x = 0
        while x < self.totalClientes:
            self.stingBartender(self.clientes[x].darNombre(), self.clientes[x].darPedido())
            time.sleep(5)
            x+=1
        self.t2sThread.say_something("Me los podrías alistar?")

    #Escuchar al bartender las alternativas disponibles
    def alternativasProductoFaltante(self):
        self.continuar = 0
        self.noComprendio = 0
        self.objetoFaltante()
        self.pedidoAlternativas(self.clienteFaltante)
        self.comprensionAlterntivas(self.capturarAudio())
        while self.continuar == 0:
        	if self.noComprendio == 1:
        		self.disculparAlternativas()
        		print("No entendido las alternativas")
        		self.comprensionAlterntivas(self.capturarAudio())
        	self.verificarAlternativas()
        	time.sleep(5)
        	self.continuar = self.afirmacionCheck(self.capturarAudio())
        	self.noComprendio = 1


       	
    #Informar al cliente de las alternativas dispinibles, escucha y verifica la respeusta
    def clienteAlternativaReemplazo(self):
        self.informarAlternativas(self.alternativas, self.clienteFaltante)
        time.sleep(10)
        self.alternativaReemplazo = self.compresionAlternativaCliente(self.capturarAudio())
        self.verificarPedido(alternativaReemplazo)

    #Le infroma al bartender de la alternativa reemplzao
    def bartenderAlternativaReemplazo(self):
        self.stingBartender(self.clienteFaltante.darNombre(),self.clienteFaltante.darPedido())
        time.sleep(10)

    def todosLosMetodos(self):
    	self.pedidos()
    	self.bartender()
    	self.alternativasProductoFaltante()
    	self.clienteAlternativaReemplazo()
    	self.bartenderAlternativaReemplazo()