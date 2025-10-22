# src/main.py

import sys
import logging
from src import privileges
from src import logger
from src import config_manager
from src import system_cleaner
from src import system_analysis
from src import utils

APP_LOGGER_NAME = 'OptiTechOptimizer'

def main():
    # 1. Asegurar privilegios de administrador
    privileges.elevate()
    # Si el script se reinicia con privilegios, el código anterior a esta línea se ejecuta de nuevo.
    # Si ya tiene privilegios, o si se reinició, continúa aquí.

    # 2. Configurar el sistema de logging
    logger.setup_logging()
    app_logger = logging.getLogger(APP_LOGGER_NAME)
    app_logger.info("Aplicación iniciada.")

    # 3. Mostrar menú principal
    while True:
        utils.show_header("Menú Principal - OptiTech System Optimizer")
        print("\nSeleccione una opción:")
        print("  1. Ejecutar Análisis del Sistema")
        print("  2. Ejecutar Limpiador del Sistema")
        print("  0. Salir")

        opcion = input("Ingrese su opción: ").strip()

        if opcion == '1':
            system_analysis.run_system_analysis()
        elif opcion == '2':
            system_cleaner.ejecutar_limpiador()
        elif opcion == '0':
            app_logger.info("Aplicación finalizada.")
            break
        else:
            print("Opción no válida. Por favor, intente de nuevo.")
            app_logger.warning(f"Opción de menú principal no válida seleccionada: {opcion}")

if __name__ == "__main__":
    main()
