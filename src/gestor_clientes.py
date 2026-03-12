from src.cliente import Cliente
from src.excepciones import ErrorCliente

class GestorClientes:
    def __init__(self):
        self.__clientes = []

    def agregar(self, cliente):
        if not isinstance(cliente, Cliente):
            raise TypeError("Solo se pueden agregar objetos que sean instancias de Cliente")
        
        if self.existe_id(cliente.get_id()):
            from src.excepciones import IdDuplicadoError
            raise IdDuplicadoError(cliente.get_id())
            
        self.__clientes.append(cliente)

    def get_clientes(self):
        return self.__clientes

    def set_clientes(self, lista):
        if all(isinstance(c, Cliente) for c in lista):
            self.__clientes = lista
        else:
            print("Error: La lista contiene elementos que no son Clientes")

    def eliminar(self, id_cliente):
        self.__clientes = [c for c in self.__clientes if c.get_id() != id_cliente]

    def existe_id(self, id_cliente):
        return any(c.get_id() == id_cliente for c in self.__clientes)
    
    def listar(self):
        for c in self.__clientes:
            print(f"ID: {c.get_id()} | Nombre: {c.get_nombre()} | Tipo: {type(c).__name__}")