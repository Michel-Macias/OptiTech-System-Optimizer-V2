# src/system_optimizer.py

import os
import json
import subprocess
import logging
from src import utils
from src import config_manager

APP_LOGGER_NAME = 'OptiTechOptimizer'
logger = logging.getLogger(APP_LOGGER_NAME)

_original_service_states = [] # Lista global para almacenar los estados originales de los servicios

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
        print("  5. Restaurar Servicios a Estado Original")
        print("  6. Volver al Menú Principal")

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
            restore_services_to_original_state()
        elif choice == '6':
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

    global _original_service_states
    _original_service_states = [] # Limpiar la lista al inicio de cada ejecución

    services_to_optimize = config_manager.config_manager_instance.load_services_to_optimize_config()

    if not services_to_optimize:
        print("No se encontraron configuraciones para la optimización de servicios. Asegúrese de que 'services_to_optimize.json' esté configurado correctamente.")
        logger.warning("El archivo 'services_to_optimize.json' no se encontró o está vacío/mal formado.")
        return

    changes_applied = 0
    for i, service_config in enumerate(services_to_optimize, 1):
        service_name = service_config.get('name', 'SinNombre')
        description = service_config.get('description', 'Sin descripción')
        recommended_startup_type = service_config.get('recommended_startup_type', 'disabled')
        risk_level = service_config.get('risk_level', 'desconocido')

        print(f"\n--- {i}. Procesando servicio: {service_name} ---")
        print(f"Descripción: {description}")
        print(f"Tipo de inicio recomendado: {recommended_startup_type.capitalize()}")
        print(f"Nivel de riesgo: {risk_level.capitalize()}")

        status = get_service_status(service_name)

        if status is None: # Error crítico al obtener el estado
            print(f"Error crítico: No se pudo obtener el estado del servicio '{service_name}'. Saltando.")
            logger.error(f"Error crítico al obtener el estado del servicio '{service_name}'.")
            continue

        current_startup = status.get('startup', '').lower()
        current_state = status.get('state', '').lower()

        if current_startup == 'not_found':
            print(f"Advertencia: El servicio '{service_name}' no se encontró en el sistema. Saltando.")
            logger.warning(f"El servicio '{service_name}' no se encontró en el sistema.")
            continue

        if current_startup == recommended_startup_type.lower():
            print(f"El servicio '{service_name}' ya está configurado como '{recommended_startup_type}'.")
            logger.info(f"El servicio '{service_name}' ya está en el estado deseado: '{recommended_startup_type}'.")
            continue
        
        print(f"Estado actual: Inicio: {current_startup.capitalize()}, Estado: {current_state.capitalize()}")
        logger.info(f"Cambiando el tipo de inicio del servicio '{service_name}' de '{current_startup}' a '{recommended_startup_type}'.")

        # Almacenar el estado original antes de modificar
        _original_service_states.append({
            'name': service_name,
            'original_startup_type': current_startup
        })

        success = set_service_startup_type(service_name, recommended_startup_type)

        if success:
            print(f"Éxito: El servicio '{service_name}' ha sido configurado como '{recommended_startup_type}'.")
            changes_applied += 1
        else:
            print(f"Error al configurar el servicio '{service_name}' a '{recommended_startup_type}'.")
            logger.error(f"Fallo al cambiar el tipo de inicio para el servicio '{service_name}' a '{recommended_startup_type}'.")

    print(f"\nOptimización de servicios completada. Se aplicaron {changes_applied} cambios.")
    logger.info(f"Finalizada la optimización de servicios. Cambios aplicados: {changes_applied}")

def restore_services_to_original_state():
    """Restaura los servicios a su tipo de inicio original antes de la última optimización."""
    global _original_service_states

    if not _original_service_states:
        print("No hay estados de servicios originales guardados para restaurar.")
        logger.info("Intento de restaurar servicios sin estados originales guardados.")
        return

    if not utils.confirm_operation("¿Está seguro de que desea restaurar los servicios a su estado original?"):
        logger.info("Operación de restauración de servicios cancelada por el usuario.")
        return

    utils.show_header("Módulo de Restauración de Servicios")
    logger.info("Iniciando la restauración de servicios.")

    restored_count = 0
    for i, service_data in enumerate(_original_service_states, 1):
        service_name = service_data['name']
        original_startup_type = service_data['original_startup_type']

        print(f"\n--- {i}. Restaurando servicio: {service_name} ---")
        print(f"Restaurando a tipo de inicio: {original_startup_type.capitalize()}")

        status = get_service_status(service_name)
        if status is None:
            print(f"Error crítico: No se pudo obtener el estado del servicio '{service_name}'. Saltando restauración.")
            logger.error(f"Error crítico al obtener el estado del servicio '{service_name}' durante la restauración.")
            continue

        current_startup = status.get('startup', '').lower()

        if current_startup == 'not_found':
            print(f"Advertencia: El servicio '{service_name}' no se encontró en el sistema. No se puede restaurar.")
            logger.warning(f"El servicio '{service_name}' no se encontró en el sistema durante la restauración.")
            continue

        if current_startup == original_startup_type.lower():
            print(f"El servicio '{service_name}' ya está en su estado original '{original_startup_type}'.")
            logger.info(f"El servicio '{service_name}' ya está en su estado original '{original_startup_type}'.")
            continue

        success = set_service_startup_type(service_name, original_startup_type)

        if success:
            print(f"Éxito: El servicio '{service_name}' ha sido restaurado a '{original_startup_type}'.")
            restored_count += 1
        else:
            print(f"Error al restaurar el servicio '{service_name}' a '{original_startup_type}'.")
            logger.error(f"Fallo al restaurar el tipo de inicio para el servicio '{service_name}' a '{original_startup_type}'.")

    print(f"\nRestauración de servicios completada. Se restauraron {restored_count} servicios.")
    logger.info(f"Finalizada la restauración de servicios. Servicios restaurados: {restored_count}")
    _original_service_states = [] # Limpiar la lista después de la restauración

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
