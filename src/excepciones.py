class ErrorCliente(Exception):
    pass

class IdDuplicadoError(ErrorCliente):
    def __init__(self, id_cliente):
        self.mensaje = f"Error: El ID {id_cliente} ya está registrado."
        super().__init__(self.mensaje)

class DatoVacioError(ErrorCliente):
    def __init__(self, campo):
        self.mensaje = f"Error: El campo '{campo}' no puede estar vacío." #Aplicamos para campos obligatorios
        super().__init__(self.mensaje)

class FormatoInvalidoError(ErrorCliente):
    def __init__(self, valor):
        self.mensaje = f"Error: '{valor}' no es un número válido."
        super().__init__(self.mensaje)

class EmailInvalidoError(ErrorCliente):
    def __init__(self, email):
        self.mensaje = f"Error: '{email}' no es un correo electrónico válido."
        super().__init__(self.mensaje)