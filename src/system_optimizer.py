# src/system_optimizer.py

import os
import json
import subprocess
import logging
from src import utils
from src import config_manager

APP_LOGGER_NAME = 'OptiTechOptimizer'
logger = logging.getLogger(APP_LOGGER_NAME)

def run_optimizer():
    """Muestra un menú interactivo para que el usuario elija las optimizaciones a aplicar."""
    utils.show_header("Módulo de Optimización del Sistema")
    logger.info("Iniciando el módulo interactivo de optimización.")

    while True:
        print("\nPor favor, elija una opción de optimización:")
        print("  1. Optimizar Efectos Visuales (Recomendado)")
        print("  2. Optimizar Servicios No Esenciales")
        print("  3. Activar Plan de Máximo Rendimiento")
        print("  4. Optimizar y Reiniciar Red")
        print("  5. Volver al Menú Principal")

        choice = input("Seleccione una opción: ").strip()

        if choice == '1':
            optimize_visual_effects()
        elif choice == '2':
            optimize_services()
        elif choice == '3':
            optimize_power_plan()
        elif choice == '4':
            optimize_network()
        elif choice == '5':
            print("Volviendo al menú principal...")
            logger.info("Saliendo del módulo de optimización.")
            break
        else:
            print("Opción no válida. Por favor, intente de nuevo.")
            logger.warning(f"Opción de optimización no válida seleccionada: {choice}")

CONFIG_FILE_PATH = os.path.join(os.path.dirname(__file__), '..', 'config', 'services_to_optimize.json')

def load_optimization_profiles(file_path=CONFIG_FILE_PATH):
    """Carga los perfiles de optimización de servicios desde un archivo JSON."""
    logger.info(f"Cargando perfiles de optimización desde: {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            profiles = json.load(f)
        logger.info("Perfiles de optimización cargados con éxito.")
        return profiles.get('services', [])
    except FileNotFoundError:
        logger.error(f"El archivo de configuración de optimización no se encontró en {file_path}")
        return []
    except json.JSONDecodeError:
        logger.error(f"Error al decodificar el archivo JSON: {file_path}")
        return []
    except Exception as e:
        logger.error(f"Error inesperado al cargar los perfiles de optimización: {e}", exc_info=True)
        return []

def optimize_visual_effects():
    """Orquesta la optimización de los efectos visuales de Windows."""
    if not utils.confirm_operation("¿Está seguro de que desea optimizar los efectos visuales? Esta acción modificará el registro de Windows."):
        logger.info("Operación de optimización de efectos visuales cancelada por el usuario.")
        return

    utils.show_header("Módulo de Optimización de Efectos Visuales")
    logger.info("Iniciando la optimización de efectos visuales.")

    settings = config_manager.load_config('visual_effects_settings.json')

    if not settings:
        print("No se encontraron configuraciones para la optimización de efectos visuales.")
        logger.warning("El archivo 'visual_effects_settings.json' no se encontró o está vacío.")
        return

    changes_applied = 0
    for i, setting in enumerate(settings, 1):
        description = setting.get('description', 'Sin descripción')
        print(f"\n--- {i}. Aplicando: {description} ---")
        
        success, message = utils.set_registry_value(
            hive=setting['hive'],
            key=setting['key'],
            value_name=setting['value_name'],
            value=setting['optimized_value'],
            value_type=setting['value_type']
        )

        if success:
            print(f"Éxito: Configuración '{description}' aplicada.")
            changes_applied += 1
        else:
            print(f"Error al aplicar '{description}': {message}")
            logger.error(f"Fallo al establecer el valor del registro para '{description}': {message}")

    print(f"\nOptimización de efectos visuales completada. Se aplicaron {changes_applied} cambios.")
    logger.info(f"Finalizada la optimización de efectos visuales. Cambios aplicados: {changes_applied}")

def optimize_services():
    """Orquesta la desactivación de servicios no esenciales de Windows."""
    if not utils.confirm_operation("¿Está seguro de que desea optimizar los servicios? Esto desactivará servicios que pueden no ser necesarios."):
        logger.info("Operación de optimización de servicios cancelada por el usuario.")
        return

    utils.show_header("Módulo de Optimización de Servicios")
    logger.info("Iniciando la optimización de servicios.")

    config = config_manager.load_config('services_to_optimize.json')
    services_to_disable = config.get('services', [])

    if not services_to_disable:
        print("No se encontraron configuraciones para la optimización de servicios.")
        logger.warning("El archivo 'services_to_optimize.json' no se encontró o está vacío.")
        return

    changes_applied = 0
    for i, service in enumerate(services_to_disable, 1):
        service_name = service.get('name', 'SinNombre')
        description = service.get('description', 'Sin descripción')
        print(f"\n--- {i}. Deshabilitando: {service_name} ---")
        print(f"Descripción: {description}")

        logger.info(f"Procesando servicio: {service_name}")
        status = utils.get_service_status(service_name)
        logger.info(f"Estado obtenido para {service_name}: {status}")

        if not status or status.get('startup') == 'NOT_FOUND':
            print(f"Información: El servicio '{service_name}' no se encontró en el sistema.")
            logger.warning(f"Servicio no encontrado: {service_name}. Omitiendo.")
            continue

        if status.get('startup') == 'DISABLED':
            print(f"El servicio '{service_name}' ya se encuentra deshabilitado.")
            logger.info(f"El servicio '{service_name}' ya está deshabilitado. Omitiendo.")
            continue
        
        logger.info(f"Intentando deshabilitar el servicio '{service_name}'.")
        success = utils.set_service_startup_type(service_name, 'disabled')

        if success:
            print(f"Éxito: El servicio '{service_name}' ha sido configurado como deshabilitado.")
            logger.info(f"Servicio '{service_name}' deshabilitado con éxito.")
            changes_applied += 1
        else:
            print(f"Error al deshabilitar el servicio '{service_name}'.")
            logger.error(f"Fallo al cambiar el tipo de inicio para el servicio '{service_name}'.")

    print(f"\nOptimización de servicios completada. Se intentaron {changes_applied} cambios.")
    logger.info(f"Finalizada la optimización de servicios. Cambios intentados: {changes_applied}")

def optimize_power_plan():
    """Activa el plan de energía de alto rendimiento de Windows."""
    if not utils.confirm_operation("¿Está seguro de que desea activar el plan de energía de alto rendimiento?"):
        logger.info("Operación de optimización del plan de energía cancelada por el usuario.")
        return

    utils.show_header("Módulo de Optimización de Plan de Energía")
    logger.info("Iniciando la optimización del plan de energía.")

    config = config_manager.load_config('power_plan_settings.json')
    high_performance_guid = config.get('high_performance_guid')

    if not high_performance_guid:
        print("No se encontró el GUID del plan de energía de alto rendimiento en la configuración.")
        logger.error("GUID del plan de energía de alto rendimiento no encontrado en 'power_plan_settings.json'.")
        return False

    try:
        cmd = ["powercfg", "/setactive", high_performance_guid]
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')

        if result.returncode == 0:
            print("Éxito: Plan de energía de alto rendimiento activado.")
            logger.info("Plan de energía de alto rendimiento activado con éxito.")
            return True
        else:
            print(f"Error al activar el plan de energía: {result.stderr}")
            logger.error(f"Fallo al activar el plan de energía. Salida: {result.stderr}")
            return False
    except FileNotFoundError:
        logger.error("El comando 'powercfg' no se encontró. Asegúrese de que está en el PATH del sistema.")
        return False
    except Exception as e:
        logger.error(f"Error inesperado al activar el plan de energía: {e}", exc_info=True)
        return False

def optimize_network():
    """Ejecuta una serie de comandos para reiniciar la configuración de red de Windows."""
    if not utils.confirm_operation("¿Está seguro de que desea optimizar la red? Esto reiniciará la configuración de red."):
        logger.info("Operación de optimización de red cancelada por el usuario.")
        return

    utils.show_header("Módulo de Optimización de Red")
    logger.info("Iniciando la optimización de red.")

    commands = {
        "Liberando IP actual": ["ipconfig", "/release"],
        "Renovando IP": ["ipconfig", "/renew"],
        "Limpiando caché DNS": ["ipconfig", "/flushdns"],
        "Reiniciando Winsock": ["netsh", "winsock", "reset"],
        "Reiniciando Pila IP": ["netsh", "int", "ip", "reset"]
    }

    all_successful = True
    for description, command in commands.items():
        print(f"\n--- Ejecutando: {description} ---")
        logger.info(f"Ejecutando comando de red: {' '.join(command)}")
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            logger.info(f"Comando '{' '.join(command)}' ejecutado con éxito. Salida:\n{result.stdout}")
            print("Comando ejecutado con éxito.")
        except FileNotFoundError:
            logger.error(f"Error: El comando '{command[0]}' no se encontró.")
            print(f"Error: El comando '{command[0]}' no se encontró. No se puede continuar.")
            all_successful = False
            break
        except subprocess.CalledProcessError as e:
            logger.error(f"El comando '{' '.join(command)}' falló. Salida:\n{e.stderr}")
            print(f"Error al ejecutar el comando. Detalles: {e.stderr}")
            all_successful = False
        except Exception as e:
            logger.error(f"Error inesperado al ejecutar '{' '.join(command)}': {e}", exc_info=True)
            print(f"Ocurrió un error inesperado: {e}")
            all_successful = False

    if all_successful:
        print("\nOptimización de red completada con éxito.")
        logger.info("Todos los comandos de optimización de red se ejecutaron correctamente.")
    else:
        print("\nOptimización de red completada con errores.")
        logger.warning("Algunos comandos de optimización de red no se pudieron completar.")

    print("Es posible que necesites reiniciar el equipo para que todos los cambios surtan efecto.")
    return all_successful
