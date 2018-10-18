from PyQt5 import uic, QtWidgets
#from T2S import T2S
from T2SThread import T2SThread
from PyQt5.QtWidgets import QApplication
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

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.fn_init_ui()
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
        self.clienteFaltante = Cliente("", "", "no esta listo")
        
    #Arranque
    def fn_init_ui(self):
        uic.loadUi("t2sUi.ui", self)
        self.btnSpeak.clicked.connect(self.pedidos)

    #Metodo para hablar
    def robot_speak(self):
        self.t2sThread.say_something(self.leText.text())

    #Métodos que definen qué dice el robot
    #Saludo al cliente
    def saludar(self):
        string = self.saludos.darSaludos(random.randint(1,3))
        self.t2sThread.say_something(string)
        time.sleep(5)

    #Disculparse por comprender mal el nombre
    def disculparNombre(self):
        string = self.saludos.disculparNombres(random.randint(1,3))
        self.t2sThread.say_something(string)
        time.sleep(5)

    #Disculparse por comprender mal el pedido
    def disculparPedido(self):
        string = self.saludos.disculparPedidos(random.randint(1,3))
        self.t2sThread.say_something(string)
        time.sleep(7)

    #Pregunta que desea ordenar
    def solicitarPedido(self):
        string = self.saludos.solicitarPedidos(random.randint(1,3))
        self.t2sThread.say_something(string)
        time.sleep(1)

    #Se disculpa por no escuchar por el ruido
    def disculpaRuido(self):
        string = self.saludos.disculparRuidos(random.randint(1,3))
        self.t2sThread.say_something(string)
        time.sleep(4)

    #Confirma el pedido
    def confirmarPedido(self,pPedido):
        string = self.saludos.confirmarPedidos(random.randint(1,3)) + pPedido
        self.t2sThread.say_something(string)
        time.sleep(6)
    
    #Pregunta si hay más clientes
    def masClientes(self):
        string = self.saludos.masClientes(random.randint(1,3))
        print(string)
        self.t2sThread.say_something(string)
        time.sleep(10)

    #Si no hay más clientes
    def noMasClientes(self):
        string = self.saludos.noMasClientes(random.randint(1,3))
        self.t2sThread.say_something(string)
        time.sleep(3)

    #Le informa al bartender el pedido    
    def stingBartender(self, nombre, pedido):
        string = nombre + "me pidió" + pedido
        self.t2sThread.say_something(string)    
        time.sleep(4)

    #Pregunta al bartender por las altervativas disponibles
    def pedidoAlternativas(self, clienteFaltante):
        string = "Veo que falta el pedido de " + clienteFaltante.darNombre() + " Qué alternativas tienes?"
        self.t2sThread.say_something(string)
        time.sleep(6)

    #Informa al cliente las alternativas disponibles
    def informarAlternativas(self, alternativas, clienteFaltante):
        string = "Lo siento" + clienteFaltante.darNombre() + " . No tengo " + clienteFaltante.darPedido() + ". Podría ofrecerte: " + self.alternativas
        self.t2sThread.say_something(string)
        time.sleep(10)


    #Métodos de entendimiento de lo que escucha el robot
    #Comprension del nombre del cliente
    def comprensionNombre(self, string):
        palabras = string.split()
        nombre =""
        for i in palabras:
            if i in self.listaNombres:
                auxNombre = palabras[(palabras.index(i)+1):(len(palabras))]
                nombre = self.reconstruirString(auxNombre)
                print(nombre)
            elif len(palabras)<=2:
                nombre = string
        print(nombre)
        return nombre

    #Comprension del pedido del cliente
    def comprensionPedido(self, string):
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
                pedido = self.reconstruirString(auxPedido)
                print(pedido)
        return pedido

    #Comprension del pedido del cliente
    def comprensionBartender(self, string):
        palabras = string.split()
        entendido = 0
        for i in palabras:
            if i in self.listaBartender:
                entendido = 1               
        return entendido
    
    #Comprende las alternativas que le ofrece el bartender
    def comprensionAlterntivas(self, string):
        opciones = string.split()
        listado = []
        for i in opciones:
            if i == "son":
                listado = opciones[opciones.index(i)+1:len(opciones)]
        self.alternativas = self.reconstruirString(listado)
        return self.alternativas

    #Comprende la alternativa escogida por el cliente
    def compresionAlternativaCliente(self,string):
        palabras = string.split()
        auxAlternativas =[]
        for i in palbaras:
            if i in self.listaAlternativas:
                auxAlternativas = palabras[(palabras.index(i)+1):(len(palabras))]
            else: 
                auxAlternativas = palabras
        alternativa = self.reconstruirString(auxAlternativas)
        return alternativa 


    #Métodos para verificar la comprension
    #Verifica el nombre del cliente segun el número
    def verificarNombre(self, pNombre):
        verificacionInicial = self.saludos.verificarNombres(random.randint(1,3))
        verificacionFinal = self.saludos.verificarFinal(random.randint(1,3))
        string = verificacionInicial + pNombre + verificacionFinal
        self.t2sThread.say_something(string)

    #Veriica el pedido segun el numero
    def verificarPedido(self, pPedido):
        verificacionInicial = self.saludos.verificarPedidos(random.randint(1,3))
        verificacionFinal = self.saludos.verificarFinal(random.randint(1,3))
        string = verificacionInicial + pPedido + verificacionFinal
        self.t2sThread.say_something(string)

    #Verifica las alternativas del bartender
    def verificarAlternativas(self):
        verificacionInicial = "Comprendí las alternativas son"
        verificacionFinal = self.saludos.verificarFinal(random.randint(1,3))
        string = verificacionIncial + self.altervativas + verificacionFinal
        self.t2sThread.say_something(string)


    #Métodos adicionales
    #Reconstruccion de strings
    def reconstruirString(self,lista):   
        reconstruido = ""
        for i in lista:
            reconstruido +=i
            reconstruido +=" "
        return reconstruido    

    #Encuentra el cliente que pidio el objeto faltante
    def objetoFaltante(self): 
        self.clienteFaltante =  Cliente("","","")
        for i in self.clientes:
            if i.darEstadoPedido() == "no esta listo":
                self.clienteFaltante = self.clientes[self.clientes.index(i)]
        return self.clienteFaltante
    
    #"Una bolella de agua" -> "botella de agua"
    #Quitar el articulo en el pedido
    def ajustePedido(self,pPedido):
        separado = pPedido.split()
        final = self.reconstruirString(separado[1:len(separado)])
        return final

    #Afirmacion no negacion
    def afirmacionCheck(self, string):
        palabras = string.split()
        afirmacion = 0
        nonegacion = 0
        for i in palabras:
            if i in self.listaAfirmaciones:
                afirmacion = 1
            if ~(i in self.listaNegaciones):
                nonegacion = 1
        return afirmacion*nonegacion


    #Métodos para archivos .csv
    #Escribe el archivo
    def csvfile_writer(self):
        with open('pedidos_file.csv', mode='w',newline='') as pedidos_file:
            pedidos_file = csv.writer(pedidos_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            i=0
            for i in range(self.totalClientes):
                pedidos_file.writerow([self.clientes[i].darNombre(),self.clientes[i].darPedido(),self.clientes[i].darEstadoPedido()])
    
    #Lee el archivo      
    def csvfile_reader(self):
        with open('pedidos_file.csv') as csv_file:
            pedido_bartender = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in pedido_bartender:
                clienteNuevo = Cliente("","","")
                clienteNuevo.cambiarNombre(row[0])
                clienteNuevo.cambiarPedido(row[1])
                clienteNuevo.cambiarEstadoPedido(row[2])
                self.clientes.append(clienteNuevo)
                #print(clienteNuevo.darNombre())
                #print(clienteNuevo.darPedido())
                #print(clienteNuevo.darEstadoPedido())
                line_count += 1 

    #Métodos de captura de audio
    #Captura de audio
    def capturarAudio(self):
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

    #Informar al bartender los pedidos obtenidos
    def bartender(self):
        self.t2sThread.say_something("Hola, Héctor, los pedidos que recibí son los siguientes:")
        time.sleep(10)
        x = 0
        self.csvfile_reader()
        while x <= 2:
            self.sting_bartender(self.clientes[x].darNombre(), self.clientes[x].darPedido())
            time.sleep(6)
            x+=1
        self.t2sThread.say_something("Me los podrías alistar?")

    #Escuchar al bartender las alternativas disponibles
    def alternativasProductoFaltante(self):
        self.objetoFaltante()
        self.pedidoAlternativas(self.clienteFaltante)
        time.sleep(10)
        self.comprensionAlterntivas(self.capturarAudio())
        self.verificarAlternativas()
        time.sleep(10)

    #Informar al cliente de las alternativas dispinibles, escucha y verifica la respeusta
    def clienteAlternativaReemplazo(self):
        self.informarAlternativas()
        time.sleep(10)
        self.alternativaReemplazo = self.compresionAlternativaCliente(self.capturarAudio())
        self.verificarPedido(alternativaReemplazo)

    #Le infroma al bartender de la alternativa reemplzao
    def bartenderAlternativaReemplazo(self):
        self.stingBartender(self.clienteFaltante.darNombre(),self.clienteFaltante.darPedido())
        time.sleep(10)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())