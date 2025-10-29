# src/main.py

import sys
import logging
import argparse
import colorama # Importar colorama
from src import privileges
from src import logger
from src import config_manager
from src import system_cleaner
from src import system_analysis
from src import system_optimizer
from src import system_maintenance
from src import utils
from src import log_manager

APP_LOGGER_NAME = 'OptiTechOptimizer'

def main():
    # Parse minimal CLI args
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--no-elevate', action='store_true', help='No intentar elevar privilegios (útil para pruebas).')
    args, _ = parser.parse_known_args()



    # 1. Asegurar privilegios de administrador (saltear si --no-elevate)
    if not args.no_elevate:
        # Use module invocation to ensure the elevated process runs the module the same way
        # This prevents launching a separate Python window that can close immediately
        privileges.elevate(cmd_args=['-m', 'src.main'])
    # Si el script se reinicia con privilegios, el código anterior a esta línea se ejecuta de nuevo.
    # Si ya tiene privilegios, o si se reinició, continúa aquí.

    # Force UTF-8 output and enable ANSI colors on Windows
    try:
        import os
        if sys.platform == 'win32':
            os.system('') # Enables ANSI escape codes in many Windows terminals
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

    # Inicializar Colorama para asegurar colores en todas las consolas
    colorama.init()

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
        print("  4. Ejecutar Mantenimiento del Sistema")
        print("  5. Ver Logs del Sistema")
        print("  0. Salir")

        opcion = input("Ingrese su opción: ").strip()

        if opcion == '1':
            system_analysis.run_system_analysis()
        elif opcion == '2':
            system_cleaner.ejecutar_limpiador()
        elif opcion == '3':
            system_optimizer.run_optimizer()
        elif opcion == '4':
            system_maintenance.run_maintenance()
        elif opcion == '5':
            log_manager.view_logs(config_manager.get_log_path())
        elif opcion == '0':
            app_logger.info("Aplicación finalizada.")
            print(utils.colored_text("Saliendo de OptiTech System Optimizer. ¡Hasta pronto!", utils.Colors.GREEN))
            break
        else:
            print(utils.colored_text("Opción no válida. Por favor, intente de nuevo.", utils.Colors.YELLOW))
            app_logger.warning(f"Opción de menú principal no válida seleccionada: {opcion}")

if __name__ == "__main__":
    main()
