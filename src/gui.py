import tkinter as tk
from tkinter import messagebox
from src.gestor_clientes import GestorClientes
from src.persistencia import Persistencia
from src.tipos_cliente import ClienteRegular, ClientePremium, ClienteCorporativo
from src.excepciones import IdDuplicadoError, DatoVacioError, FormatoInvalidoError, ErrorCliente, EmailInvalidoError

class InterfazCliente:
    def __init__(self, ventana):
        self.gestor = GestorClientes()
        #Cargamos los datos apenas abre la aplicación
        self.gestor.set_clientes(Persistencia.cargar())
        
        self.ventana = ventana
        self.ventana.title("SolutionTech - Sistema de Gestión")
        self.ventana.geometry("500x850") 

        #SECCIÓN DE REGISTRO
        tk.Label(ventana, text="--- REGISTRO DE CLIENTE ---", font=("Arial", 12, "bold")).pack(pady=10)
        
        tk.Label(ventana, text="ID:").pack()
        self.txt_id = tk.Entry(ventana)
        self.txt_id.pack()

        tk.Label(ventana, text="Nombre:").pack()
        self.txt_nombre = tk.Entry(ventana)
        self.txt_nombre.pack()

        tk.Label(ventana, text="Email:").pack()
        self.txt_email = tk.Entry(ventana)
        self.txt_email.pack()

        tk.Label(ventana, text="Tipo de Cliente:").pack()
        self.tipo_var = tk.StringVar(ventana)
        self.tipo_var.set("Regular")
        tk.OptionMenu(ventana, self.tipo_var, "Regular", "Premium", "Corporativo").pack()

        tk.Label(ventana, text="Dato Extra (Puntos o Empresa):").pack()
        self.txt_extra = tk.Entry(ventana)
        self.txt_extra.pack()

        tk.Button(ventana, text="Agregar Cliente", command=self.agregar_cliente, bg="#ADD8E6", font=("Arial", 9, "bold")).pack(pady=15)

        #SECCIÓN DE BÚSQUEDA
        tk.Label(ventana, text="--- BÚSQUEDA ---", font=("Arial", 10, "bold")).pack(pady=5)
        self.txt_buscar = tk.Entry(ventana)
        self.txt_buscar.pack(pady=5)
        
        frame_busqueda = tk.Frame(ventana)
        frame_busqueda.pack(pady=5)
        tk.Button(frame_busqueda, text="Buscar", command=self.buscar_cliente, bg="#FFFFE0").pack(side=tk.LEFT, padx=5)
        tk.Button(frame_busqueda, text="Ver Todos", command=self.actualizar_lista_visual, bg="white").pack(side=tk.LEFT, padx=5)
        
        #LISTADO
        tk.Label(ventana, text="--- CLIENTES REGISTRADOS ---", font=("Arial", 10, "bold")).pack(pady=10)
        self.lista_visual = tk.Listbox(ventana, width=60, height=12, font=("Courier", 9))
        self.lista_visual.pack(padx=10)

        #ACCIONES FINALES
        tk.Button(ventana, text="Eliminar Seleccionado", command=self.eliminar_cliente, bg="#FA8072").pack(pady=5)
        tk.Button(ventana, text="GUARDAR DATOS (JSON)", command=self.guardar_datos, bg="#90EE90", font=("Arial", 9, "bold")).pack(pady=10)
        tk.Button(ventana, text="Exportar reporte (CSV)", command=self.exportar_a_csv, bg="#FFA500").pack(pady=5)
        
        self.actualizar_lista_visual()

    def agregar_cliente(self):
        try:
            if not self.txt_id.get().strip(): raise DatoVacioError("ID")
            if not self.txt_nombre.get().strip(): raise DatoVacioError("Nombre")
            
            try:
                id_c = int(self.txt_id.get())
            except ValueError:
                raise FormatoInvalidoError("El ID debe ser un número entero")

            nom = self.txt_nombre.get()
            mail = self.txt_email.get()
            tipo = self.tipo_var.get()
            extra = self.txt_extra.get()

            if tipo == "Regular":
                try:
                    pts = int(extra) if extra else 0
                except ValueError:
                    raise FormatoInvalidoError("Los Puntos deben ser un número")
                nuevo = ClienteRegular(id_c, nom, mail, pts)
                
            elif tipo == "Premium":
                nuevo = ClientePremium(id_c, nom, mail)
                
            elif tipo == "Corporativo":
                if not extra.strip(): raise DatoVacioError("Nombre de Empresa")
                nuevo = ClienteCorporativo(id_c, nom, mail, extra)

            self.gestor.agregar(nuevo)
            self.actualizar_lista_visual()
            self.limpiar_campos()
            messagebox.showinfo("SolutionTech", f"Cliente {tipo} registrado con éxito.")

        except ErrorCliente as e:
            #Captura todas nuestras excepciones personalizadas (Email, ID duplicado, etc.)
            messagebox.showerror("Error de Validación", str(e))
        except Exception as e:
            messagebox.showerror("Error del Sistema", f"Algo salió mal: {str(e)}")

    def buscar_cliente(self):
        criterio = self.txt_buscar.get().lower()
        if not criterio:
            messagebox.showwarning("Atención", "Ingresa un dato para buscar.")
            return

        self.lista_visual.delete(0, tk.END)
        for c in self.gestor.get_clientes():
            if criterio == str(c.get_id()) or criterio in c.get_nombre().lower():
                self.insertar_en_lista(c)
        
        if self.lista_visual.size() == 0:
            messagebox.showinfo("Búsqueda", "No hay coincidencias.")
            self.actualizar_lista_visual()

    def guardar_datos(self):
        Persistencia.guardar(self.gestor.get_clientes())
        messagebox.showinfo("Persistencia", "Datos guardados en 'clientes.json'.")

    def exportar_a_csv(self):
        if Persistencia.exportar_csv(self.gestor.get_clientes()):
            messagebox.showinfo("Exportar", "Reporte 'reporte_clientes.csv' generado.")
        else:
            messagebox.showerror("Error", "No se pudo generar el reporte.")

    def eliminar_cliente(self):
        seleccion = self.lista_visual.curselection()
        if not seleccion:
            messagebox.showwarning("Atención", "Selecciona un cliente de la lista.")
            return
            
        linea = self.lista_visual.get(seleccion[0])
        #Extraemos el ID de la cadena formateada
        id_a_borrar = int(linea.split("|")[0].replace("ID:", "").strip())
        
        self.gestor.eliminar(id_a_borrar)
        self.actualizar_lista_visual()
        messagebox.showinfo("Eliminado", f"Cliente {id_a_borrar} quitado de la sesión.")

    def actualizar_lista_visual(self):
        self.lista_visual.delete(0, tk.END)
        for c in self.gestor.get_clientes():
            self.insertar_en_lista(c)

    def insertar_en_lista(self, c):
        info = f"ID: {c.get_id():<4} | {c.get_nombre():<15} | Desc: ${c.calcular_descuento()}"
        self.lista_visual.insert(tk.END, info)

    def limpiar_campos(self):
        self.txt_id.delete(0, tk.END)
        self.txt_nombre.delete(0, tk.END)
        self.txt_email.delete(0, tk.END)
        self.txt_extra.delete(0, tk.END)