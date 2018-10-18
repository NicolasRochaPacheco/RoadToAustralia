class Cliente:
	def __init__(self, n, p, e):
		self.nombre = n
		self.pedido = p
		self.estadoPedido = e
	def darNombre(self):
		return self.nombre
	def darPedido(self):
		return self.pedido
	def darEstadoPedido(self):
		return self.estadoPedido
	def cambiarNombre(self, pNombre):
		self.nombre = pNombre
	def cambiarPedido(self, pPedido):
		self.pedido = pPedido
	def cambiarEstadoPedido(self, pEstadoPedido):
		self.estadoPedido = pEstadoPedido