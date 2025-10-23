# src/system_optimizer.py

import os
import json
import subprocess
import logging
from src import utils
from src import config_manager

APP_LOGGER_NAME = 'OptiTechOptimizer'
logger = logging.getLogger(APP_LOGGER_NAME)

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

def get_service_status(service_name):
    """Obtiene el estado y el tipo de inicio de un servicio de Windows."""
    logger.info(f"Obteniendo estado para el servicio: {service_name}")
    status_info = {'state': 'NOT_FOUND', 'startup': 'NOT_FOUND'}

    try:
        # Obtener el estado (STATE)
        query_cmd = ["sc.exe", "query", service_name]
        query_result = subprocess.run(query_cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')

        if query_result.returncode == 0:
            for line in query_result.stdout.splitlines():
                if "STATE" in line:
                    # La línea es como '        STATE              : 4  RUNNING'
                    status_info['state'] = line.split(':')[1].strip().split()[-1]
                    break
        else:
            logger.warning(f"El comando 'sc query' falló para el servicio {service_name}. Salida: {query_result.stderr}")
            # Si query falla, es probable que el servicio no exista.
            return status_info

        # Obtener el tipo de inicio (START_TYPE)
        qc_cmd = ["sc.exe", "qc", service_name]
        qc_result = subprocess.run(qc_cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')

        if qc_result.returncode == 0:
            for line in qc_result.stdout.splitlines():
                if "START_TYPE" in line:
                    # La línea es como '        START_TYPE         : 2   AUTO_START'
                    status_info['startup'] = line.split(':')[1].strip().split()[-1]
                    break
        else:
            logger.warning(f"El comando 'sc qc' falló para el servicio {service_name}. Salida: {qc_result.stderr}")

    except FileNotFoundError:
        logger.error("El comando 'sc.exe' no se encontró. Asegúrese de que está en el PATH del sistema.")
        return None # Error crítico, no podemos continuar
    except Exception as e:
        logger.error(f"Error inesperado al obtener el estado del servicio {service_name}: {e}", exc_info=True)
        return None

    logger.info(f"Estado para {service_name}: {status_info}")
    return status_info

def set_service_startup_type(service_name, startup_type):
    """Cambia el tipo de inicio de un servicio de Windows."""
    logger.info(f"Cambiando el tipo de inicio del servicio '{service_name}' a '{startup_type}'")
    # Los tipos de inicio válidos para 'sc.exe config' son: boot, system, auto, demand, disabled
    # Hacemos un mapeo por si usamos términos más amigables
    valid_startup_types = {
        "automatic": "auto",
        "manual": "demand",
        "disabled": "disabled"
    }
    
    sc_startup_type = valid_startup_types.get(startup_type, startup_type) # Usar el valor mapeado o el original

    try:
        cmd = ["sc.exe", "config", service_name, "start=", sc_startup_type]
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')

        if result.returncode == 0:
            logger.info(f"El tipo de inicio del servicio '{service_name}' se cambió a '{sc_startup_type}' con éxito.")
            return True
        else:
            logger.error(f"Error al cambiar el tipo de inicio del servicio '{service_name}'. Salida: {result.stderr}")
            return False
            
    except FileNotFoundError:
        logger.error("El comando 'sc.exe' no se encontró. Asegúrese de que está en el PATH del sistema.")
        return False
    except Exception as e:
        logger.error(f"Error inesperado al cambiar el tipo de inicio del servicio {service_name}: {e}", exc_info=True)
        return False

def run_optimizer():
    """Función principal que orquesta la optimización de servicios."""
    utils.show_header("Módulo de Optimización del Sistema")
    logger.info("Iniciando módulo de optimización del sistema.")

    services_to_optimize = load_optimization_profiles()

    if not services_to_optimize:
        print("No se encontraron perfiles de optimización o el archivo de configuración está vacío.")
        return

    print("Se analizarán los siguientes servicios para su posible optimización:")
    optimizations_applied = 0

    for i, service in enumerate(services_to_optimize, 1):
        service_name = service['name']
        print(f"\n--- {i}. Analizando '{service_name}' ---")
        print(f"Descripción: {service['description']}")

        status = get_service_status(service_name)
        if not status or status['state'] == 'NOT_FOUND':
            print(f"El servicio '{service_name}' no se encontró en el sistema. Omitiendo.")
            logger.warning(f"Servicio '{service_name}' del perfil de optimización no encontrado.")
            continue

        print(f"Estado actual: {status['state']} | Inicio: {status['startup']}")

        if status['startup'] == 'DISABLED':
            print(f"El servicio '{service_name}' ya está deshabilitado. No se requiere acción.")
            continue

        prompt = f"¿Desea deshabilitar el servicio '{service_name}'?"
        if utils.confirm_operation(prompt):
            if set_service_startup_type(service_name, 'disabled'):
                print(f"Éxito: El servicio '{service_name}' ha sido deshabilitado.")
                optimizations_applied += 1
            else:
                print(f"Error: No se pudo deshabilitar el servicio '{service_name}'.")
        else:
            print(f"Operación cancelada para el servicio '{service_name}'.")

    print(f"\nOptimización completada. Se aplicaron {optimizations_applied} cambios.")
    logger.info(f"Módulo de optimización finalizado. Cambios aplicados: {optimizations_applied}")

def optimize_visual_effects():
    """Orquesta la optimización de los efectos visuales de Windows."""
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

        status = get_service_status(service_name)

        if status and status.get('startup', '').upper() == 'DISABLED':
            print(f"El servicio '{service_name}' ya se encuentra deshabilitado.")
            continue
        
        success = set_service_startup_type(service_name, 'disabled')

        if success:
            print(f"Éxito: El servicio '{service_name}' ha sido configurado como deshabilitado.")
            changes_applied += 1
        else:
            print(f"Error al deshabilitar el servicio '{service_name}'.")
            logger.error(f"Fallo al cambiar el tipo de inicio para el servicio '{service_name}'.")

    print(f"\nOptimización de servicios completada. Se intentaron {changes_applied} cambios.")
    logger.info(f"Finalizada la optimización de servicios. Cambios intentados: {changes_applied}")

def optimize_power_plan():
    """Activa el plan de energía de alto rendimiento de Windows."""
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
