import configparser

#Clase que escoge aleatoriamente diferentes strings para que el robot hable.
class Saludos:
	
	def __init__(self):
		config = configparser.RawConfigParser()
		config.read('list.cfg')
		

	def darSaludos(self,i):
		config = configparser.RawConfigParser()
		config.read('list.cfg')
		saludos = config.get('saludos','Saludo'+str(i))
		return saludos

	def verificarNombres(self,i):
		config = configparser.RawConfigParser()
		config.read('list.cfg')
		verificarNombres = config.get('verificarNombres','VerificarN'+str(i))
		return verificarNombres

	def verificarPedidos(self,i):
		config = configparser.RawConfigParser()
		config.read('list.cfg')
		verificarPedidos = config.get('verificarPedidos','verificarP'+str(i))
		return verificarPedidos

	def disculparNombres(self,i):
		config = configparser.RawConfigParser()
		config.read('list.cfg')
		disculparNombre = config.get('disculparNombre','disculpaN'+str(i))
		return disculparNombre

	def verificarFinal(self,i):
		config = configparser.RawConfigParser()
		config.read('list.cfg')
		verificacionFinal = config.get('verificacionFinal','verificarF'+str(i))
		return verificacionFinal

	def disculparPedidos(self,i):
		config = configparser.RawConfigParser()
		config.read('list.cfg')
		disculparPedidos = config.get('disculparPedido','disculpaP'+str(i))
		return disculparPedidos

	def solicitarPedidos(self,i):
		config = configparser.RawConfigParser()
		config.read('list.cfg')
		solicitarPedido = config.get('solicitarPedido','solicitarP'+str(i))
		return solicitarPedido

	def disculparRuidos(self,i):
		config = configparser.RawConfigParser()
		config.read('list.cfg')
		disculpaRuido = config.get('disculparRuido','disculpaR'+str(i))
		return disculpaRuido

	def confirmarPedidos(self,i):
		config = configparser.RawConfigParser()
		config.read('list.cfg')
		confirmarPedido = config.get('confirmarPedido','confirmarP'+str(i))
		return confirmarPedido

	def masClientes(self,i):
		config = configparser.RawConfigParser()
		config.read('list.cfg')
		masClientes = config.get('masClientes','masClientesP'+str(i))
		return masClientes

	def noMasClientes(self,i):
		config = configparser.RawConfigParser()
		config.read('list.cfg')
		noMasClientes = config.get('noMasClientes','noMasClientesP'+str(i))
		return noMasClientes