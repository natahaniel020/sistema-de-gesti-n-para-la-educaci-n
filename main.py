"""
Punto de entrada principal - Sistema de Gestión Académica MVC
"""

import tkinter as tk
import sys
import os

# Ajustar el path para que Python encuentre tus módulos si ejecutas desde la raíz
# Esto permite importar correctamente los paquetes del proyecto
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importaciones principales del sistema
from views.main_window import MainWindow
from config.database import DatabaseConnection


def main():
    """
    Función principal que arranca toda la aplicación.
    Controla la inicialización de la base de datos y la interfaz gráfica.
    """
    try:
        # 1. Inicializar la conexión a la base de datos
        # Se crea una instancia de la clase que maneja MySQL
        db = DatabaseConnection()
        
        # Verificar que la conexión funcione antes de continuar
        if not db.test_connection():
            print("ERROR: No se pudo establecer conexión con el servidor MySQL.")
            print("Verifica que el servicio esté activo y los datos en config/database.py sean correctos.")
            sys.exit(1)  # Termina el programa si falla la conexión

        # 2. Crear la ventana raíz de Tkinter (contenedor principal)
        root = tk.Tk()
        
        # 3. Instanciar la ventana principal del sistema
        # Aquí se construye toda la arquitectura MVC internamente
        app = MainWindow(root, db)

        # 4. Configurar el evento de cierre de la ventana
        # Se delega al método de MainWindow para cerrar correctamente la BD
        root.protocol("WM_DELETE_WINDOW", app._on_closing)

        # 5. Iniciar el loop principal de la interfaz gráfica
        print("Sistema Académico iniciado correctamente...")
        root.mainloop()

    # Manejo de error si faltan módulos o rutas mal configuradas
    except ImportError as ie:
        print(f"Error de importación: {ie}")
        print("Asegúrate de que las carpetas y archivos existan en la ruta especificada.")

    # Manejo de errores críticos generales
    except Exception as e:
        print(f"Error crítico al iniciar la aplicación: {e}")
        sys.exit(1)


# Punto de entrada del programa
# Solo ejecuta main() si el archivo se ejecuta directamente
if __name__ == "__main__":
    main()