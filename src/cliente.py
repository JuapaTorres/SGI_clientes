from src.excepciones import EmailInvalidoError

class Cliente:
    def __init__(self, cliente_id, nombre, email):
        self.__id = cliente_id
        self.__nombre = nombre
        self.set_email(email) 

    def get_id(self):
        return self.__id
    
    def get_nombre(self):
        return self.__nombre
    
    def set_nombre(self, nombre):
        self.__nombre = nombre

    def get_email(self):
        return self.__email

    def set_email(self, email):
        if "@" in email and "." in email:
            self.__email = email
        else:
            raise EmailInvalidoError(email)
        
    def calcular_descuento(self):
        return 0