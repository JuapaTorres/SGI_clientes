## Gestor Inteligente de Clientes (GIC)

Sistema integral de gestión de clientes desarrollado en Python como parte del Bootcamp de Desarrollo de Aplicaciones Full Stack. El proyecto aplica principios avanzados de Programación Orientada a Objetos (POO) y una interfaz gráfica funcional.



## Características Principales

- Gestión Completa (CRUD) Registro, búsqueda y eliminación de clientes.
- Tipos de Clientes: Diferenciación entre Clientes Regulares, Premium y Corporativos mediante Herencia.
- Lógica de Descuentos: Aplicación de Polimorfismo para calcular beneficios según el tipo de cliente.
- Validaciones Inteligentes: Control de errores mediante Excepciones Personalizadas (email válido, ID único, campos obligatorios).
- Persistencia de Datos: Almacenamiento local en formato JSON y exportación de reportes a CSV.
- Interfaz Gráfica: Desarrollada íntegramente con la librería Tkinter.

## Arquitectura del Proyecto (POO)

El sistema se basa en una estructura modular para asegurar la escalabilidad (Clean Code):

* **cliente.py:** Clase base con Encapsulamiento (atributos privados).
* **tipos_cliente.py:** Subclases que implementan herencia y el método super().
* **gestor_clientes.py:** Lógica de negocio y validación con isinstance.
* **persistencia.py:** Manejo de lectura/escritura de archivos.
* **excepciones.py:** Definición de errores específicos del sistema.
* **gui.py:** Capa de presentación (Interfaz de Usuario).



## Instalación y Uso

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/JuapaTorres/SGI_clientes](https://github.com/JuapaTorres/SGI_clientes)