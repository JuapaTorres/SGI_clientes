import json
import csv
import os
from src.tipos_cliente import ClienteRegular, ClientePremium, ClienteCorporativo

class Persistencia:
    ARCHIVO_JSON = "clientes.json"
    ARCHIVO_CSV = "reporte_clientes.csv"

    @staticmethod
    def guardar(lista_clientes):
        datos_para_guardar = []
        
        for c in lista_clientes:
            info = {
                "id": c.get_id(),
                "nombre": c.get_nombre(),
                "email": c.get_email()
            }
            
            if isinstance(c, ClienteRegular):
                info["tipo"] = "Regular"
                info["puntos"] = c.get_puntos()
            elif isinstance(c, ClientePremium):
                info["tipo"] = "Premium"
            elif isinstance(c, ClienteCorporativo):
                info["tipo"] = "Corporativo"
                info["empresa"] = c.get_empresa()
            
            datos_para_guardar.append(info)

        with open(Persistencia.ARCHIVO_JSON, "w", encoding="utf-8") as archivo:
            json.dump(datos_para_guardar, archivo, indent=4)

    @staticmethod
    def cargar():
        try:
            if not os.path.exists(Persistencia.ARCHIVO_JSON):
                return []

            with open(Persistencia.ARCHIVO_JSON, "r", encoding="utf-8") as archivo:
                lista_diccionarios = json.load(archivo)
                lista_objetos = []
                
                for d in lista_diccionarios:
                    if d["tipo"] == "Regular":
                        obj = ClienteRegular(d["id"], d["nombre"], d["email"], d["puntos"])
                    elif d["tipo"] == "Premium":
                        obj = ClientePremium(d["id"], d["nombre"], d["email"])
                    elif d["tipo"] == "Corporativo":
                        obj = ClienteCorporativo(d["id"], d["nombre"], d["email"], d["empresa"])
                    
                    lista_objetos.append(obj)
                return lista_objetos
        except (FileNotFoundError, json.JSONDecodeError):
            return []
        
    @staticmethod
    def exportar_csv(lista_clientes, nombre_archivo=None):
        if nombre_archivo is None:
            nombre_archivo = Persistencia.ARCHIVO_CSV
            
        try:
            with open(nombre_archivo, "w", newline="", encoding="utf-8") as archivo:
                escritor = csv.writer(archivo)
                escritor.writerow(["ID", "Nombre", "Email", "Tipo", "Dato Extra"])
                
                for c in lista_clientes:
                    tipo = c.__class__.__name__.replace("Cliente", "")
                    extra = ""
                    if isinstance(c, ClienteRegular): extra = f"{c.get_puntos()} puntos"
                    if isinstance(c, ClienteCorporativo): extra = c.get_empresa()
                    
                    escritor.writerow([c.get_id(), c.get_nombre(), c.get_email(), tipo, extra])
            return True
        except Exception as e:
            print(f"Error al exportar: {e}")
            return False