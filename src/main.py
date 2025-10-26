# src/main.py

import sys
import logging
import argparse
from src import privileges
from src import logger
from src import config_manager
from src import system_cleaner
from src import system_analysis
from src import system_optimizer
from src import utils
from src.log_manager import LogManager

APP_LOGGER_NAME = 'OptiTechOptimizer'

def handle_log_management():
    """Gestiona el submenú para ver y eliminar archivos de log."""
    log_manager = LogManager()
    app_logger = logging.getLogger(APP_LOGGER_NAME)

    while True:
        utils.show_header("Gestión de Logs")
        print("\nSeleccione una opción:")
        print("  1. Ver archivos de log")
        print("  2. Eliminar un archivo de log")
        print("  0. Volver al Menú Principal")

        opcion = input("Ingrese su opción: ").strip()

        if opcion == '1':
            app_logger.info("Usuario seleccionó ver archivos de log.")
            logs = log_manager.get_log_files()
            if not logs:
                print("\nNo se encontraron archivos de log.")
                continue
            
            print("\nArchivos de log disponibles:")
            for i, log_file in enumerate(logs, 1):
                print(f"  {i}. {log_file}")
            
            try:
                choice = int(input("\nSeleccione un log para ver (0 para cancelar): ").strip())
                if 0 < choice <= len(logs):
                    filename = logs[choice - 1]
                    app_logger.info(f"Usuario seleccionó ver el log: {filename}")
                    content = log_manager.view_log_content(filename)
                    print(f"--- Contenido de {filename} ---\n")
                    print(content)
                    print("--- Fin del contenido ---")
                elif choice != 0:
                    print("Selección no válida.")
            except ValueError:
                print("Entrada no válida. Por favor, ingrese un número.")

        elif opcion == '2':
            app_logger.info("Usuario seleccionó eliminar un archivo de log.")
            logs = log_manager.get_log_files()
            if not logs:
                print("\nNo se encontraron archivos de log para eliminar.")
                continue

            print("\nArchivos de log disponibles para eliminar:")
            for i, log_file in enumerate(logs, 1):
                print(f"  {i}. {log_file}")

            try:
                choice = int(input("\nSeleccione un log para eliminar (0 para cancelar): ").strip())
                if 0 < choice <= len(logs):
                    filename = logs[choice - 1]
                    if utils.confirm_operation(f"¿Está seguro de que desea eliminar '{filename}'? Esta acción es irreversible."):
                        app_logger.warning(f"Usuario confirmó la eliminación del log: {filename}")
                        if log_manager.delete_log_file(filename):
                            print(f"El archivo '{filename}' ha sido eliminado.")
                            app_logger.info(f"Log eliminado exitosamente: {filename}")
                        else:
                            print(f"Error al intentar eliminar '{filename}'.")
                            app_logger.error(f"Fallo al eliminar el log: {filename}")
                elif choice != 0:
                    print("Selección no válida.")
            except ValueError:
                print("Entrada no válida. Por favor, ingrese un número.")

        elif opcion == '0':
            app_logger.info("Usuario salió de la gestión de logs.")
            break
        else:
            print("Opción no válida. Por favor, intente de nuevo.")
            app_logger.warning(f"Opción de menú de logs no válida: {opcion}")

def main():
    # Parse minimal CLI args
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--no-elevate', action='store_true', help='No intentar elevar privilegios (útil para pruebas).')
    args, _ = parser.parse_known_args()

    # Force UTF-8 output in Python (helps avoid mojibake in Windows consoles)
    try:
        import os
        os.environ.setdefault('PYTHONUTF8', '1')
        # Reconfigure stdout/stderr to utf-8 if supported (Python 3.7+)
        import sys
        try:
            sys.stdout.reconfigure(encoding='utf-8', errors='replace')
            sys.stderr.reconfigure(encoding='utf-8', errors='replace')
        except Exception:
            # Not all environments support reconfigure; ignore if unavailable
            pass
    except Exception:
        pass

    # 1. Asegurar privilegios de administrador (saltear si --no-elevate)
    if not args.no_elevate:
        # Use module invocation to ensure the elevated process runs the module the same way
        # This prevents launching a separate Python window that can close immediately
        privileges.elevate(cmd_args=['-m', 'src.main'])
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
        print("  3. Ejecutar Optimizador del Sistema")
        print("  4. Gestión de Logs")
        print("  0. Salir")

        opcion = input("Ingrese su opción: ").strip()

        if opcion == '1':
            system_analysis.run_system_analysis()
        elif opcion == '2':
            system_cleaner.ejecutar_limpiador()
        elif opcion == '3':
            system_optimizer.run_optimizer()
        elif opcion == '4':
            handle_log_management()
        elif opcion == '0':
            app_logger.info("Aplicación finalizada.")
            break
        else:
            print("Opción no válida. Por favor, intente de nuevo.")
            app_logger.warning(f"Opción de menú principal no válida seleccionada: {opcion}")

if __name__ == "__main__":
    main()
