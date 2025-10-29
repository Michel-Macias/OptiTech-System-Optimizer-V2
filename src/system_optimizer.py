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
            print(utils.colored_text(f"Éxito: Configuración '{description}' aplicada.", utils.Colors.GREEN))
            changes_applied += 1
        else:
            print(utils.colored_text(f"Error al aplicar '{description}': {message}", utils.Colors.RED))
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
        print(utils.colored_text("No se encontraron configuraciones para la optimización de servicios.", utils.Colors.YELLOW))
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
            print(utils.colored_text(f"Información: El servicio '{service_name}' no se encontró en el sistema.", utils.Colors.YELLOW))
            logger.warning(f"Servicio no encontrado: {service_name}. Omitiendo.")
            continue

        if status.get('startup') == 'DISABLED':
            print(utils.colored_text(f"El servicio '{service_name}' ya se encuentra deshabilitado.", utils.Colors.YELLOW))
            logger.info(f"El servicio '{service_name}' ya está deshabilitado. Omitiendo.")
            continue
        
        logger.info(f"Intentando deshabilitar el servicio '{service_name}'.")
        success = utils.set_service_startup_type(service_name, 'disabled')

        if success:
            print(utils.colored_text(f"Éxito: El servicio '{service_name}' ha sido configurado como deshabilitado.", utils.Colors.GREEN))
            logger.info(f"Servicio '{service_name}' deshabilitado con éxito.")
            changes_applied += 1
        else:
            print(utils.colored_text(f"Error al deshabilitar el servicio '{service_name}'.", utils.Colors.RED))
            logger.error(f"Fallo al cambiar el tipo de inicio para el servicio '{service_name}'.")

    print(f"\nOptimización de servicios completada. Se intentaron {changes_applied} cambios.")
    logger.info(f"Finalizada la optimización de servicios. Cambios intentados: {changes_applied}")

def optimize_power_plan():
    """Busca dinámicamente y activa el plan de energía de alto rendimiento de Windows."""
    if not utils.confirm_operation("¿Está seguro de que desea activar el plan de energía de alto rendimiento?"):
        logger.info("Operación de optimización del plan de energía cancelada por el usuario.")
        return

    utils.show_header("Módulo de Optimización de Plan de Energía")
    logger.info("Iniciando la optimización del plan de energía.")

    try:
        logger.info("Buscando dinámicamente el GUID del plan de 'Alto rendimiento'.")
        result = subprocess.run(["powercfg", "/list"], capture_output=True, text=True, encoding='oem', errors='replace')

        if result.returncode != 0:
            print(utils.colored_text(f"Error al listar los planes de energía: {result.stderr}", utils.Colors.RED))
            logger.error(f"Fallo al ejecutar 'powercfg /list'. Salida: {result.stderr}")
            return False

        high_performance_guid = None
        for line in result.stdout.splitlines():
            normalized_line = line.lower()
            # Buscar tanto en español como en inglés
            if "(alto rendimiento)" in normalized_line or "(high performance)" in normalized_line:
                # Formato esperado: 'GUID de plan de energía: XXXXX-XXXX-.... (Alto rendimiento)'
                parts = line.split(':')
                if len(parts) > 1:
                    guid_part = parts[1].strip()
                    high_performance_guid = guid_part.split()[0]
                    logger.info(f"GUID de 'Alto rendimiento' encontrado: {high_performance_guid}")
                    break
        
        if not high_performance_guid:
            print(utils.colored_text("No se pudo encontrar el plan de energía de 'Alto rendimiento' en este sistema.", utils.Colors.YELLOW))
            logger.error("El plan de energía de 'Alto rendimiento' no fue encontrado tras listar los planes.")
            return False

        # Activar el plan de energía encontrado
        cmd = ["powercfg", "/setactive", high_performance_guid]
        activation_result = subprocess.run(cmd, capture_output=True, text=True, encoding='oem', errors='replace')

        if activation_result.returncode == 0:
            print(utils.colored_text("Éxito: Plan de energía de alto rendimiento activado.", utils.Colors.GREEN))
            logger.info(f"Plan de energía de alto rendimiento ({high_performance_guid}) activado con éxito.")
            return True
        else:
            print(utils.colored_text(f"Error al activar el plan de energía: {activation_result.stderr}", utils.Colors.RED))
            logger.error(f"Fallo al activar el plan de energía. Salida: {activation_result.stderr}")
            return False

    except FileNotFoundError:
        print(utils.colored_text("Error: El comando 'powercfg' no se encontró. Asegúrese de que está en el PATH.", utils.Colors.RED))
        logger.error("El comando 'powercfg' no se encontró. Asegúrese de que está en el PATH del sistema.")
        return False
    except Exception as e:
        print(utils.colored_text(f"Ocurrió un error inesperado: {e}", utils.Colors.RED))
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
        "Reiniciando Pila IP": ["netsh", "int", "ip", "reset", "reset.log"]
    }

    all_successful = True
    results_summary = [] # Lista para almacenar el resumen de cada comando
    for description, command in commands.items():
        print(f"\n--- Ejecutando: {description} ---")
        logger.info(f"Ejecutando comando de red: {' '.join(command)}")
        
        is_reset_command = "reset" in command and "ip" in command
        check_status = not is_reset_command
        
        # Seleccionar codificación dinámicamente
        encoding = 'utf-8' if command[0] == 'netsh' else 'oem'

        try:
            result = subprocess.run(
                command, 
                capture_output=True, 
                text=True, 
                check=check_status, 
                encoding=encoding, 
                errors='replace'
            )
            if result.returncode != 0:
                all_successful = False
                if is_reset_command: # Manejo especial para netsh int ip reset
                    critical_messages_log = [] # Para registrar detalles completos
                    restart_needed = False
                    successful_resets_count = 0

                    print(utils.colored_text("Comando ejecutado con advertencias/errores. Detalles:", utils.Colors.YELLOW))
                    for line in result.stdout.splitlines():
                        stripped_line = line.strip()
                        if not stripped_line: # Ignorar líneas vacías
                            continue
                        
                        if "se restableció correctamente" in stripped_line:
                            # Solo imprimir si hay texto descriptivo antes de "se restableció correctamente"
                            if len(stripped_line.replace("se restableció correctamente.", "").strip()) > 0:
                                print(utils.colored_text(f"  ✓ {stripped_line}", utils.Colors.GREEN))
                                successful_resets_count += 1
                            else:
                                # Ignorar mensajes genéricos "se restableció correctamente." sin descripción específica
                                pass
                        elif "Error" in stripped_line or "Acceso denegado" in stripped_line:
                            print(utils.colored_text(f"  ✗ {stripped_line}", utils.Colors.RED))
                            critical_messages_log.append(stripped_line)
                        elif "Reinicie el equipo" in stripped_line:
                            print(utils.colored_text(f"  ! {stripped_line}", utils.Colors.YELLOW + utils.Colors.BOLD))
                            critical_messages_log.append(stripped_line)
                            restart_needed = True
                        else:
                            # Imprimir otras líneas no críticas que no estén vacías o sean mensajes de éxito genéricos
                            print(stripped_line)

                    if successful_resets_count > 0:
                        print(utils.colored_text(f"  ({successful_resets_count} elementos restablecidos correctamente)", utils.Colors.GREEN))

                    if critical_messages_log:
                        if not restart_needed:
                            print(utils.colored_text("Algunas partes no se pudieron restablecer. Revise los logs para más detalles.", utils.Colors.YELLOW))
                        results_summary.append({'description': description, 'status': 'Advertencia', 'details': '; '.join(critical_messages_log)})
                else:
                    # Comandos que no son netsh int ip reset
                    print(utils.colored_text(f"Comando ejecutado con advertencias. Salida:\n{result.stdout}", utils.Colors.YELLOW))
                    logger.warning(f"El comando '{' '.join(command)}' finalizó con código {result.returncode}. Salida:\n{result.stdout}")
                    results_summary.append({'description': description, 'status': 'Advertencia', 'details': result.stdout})
            else:
                logger.info(f"Comando '{' '.join(command)}' ejecutado con éxito. Salida:\n{result.stdout}")
                print(utils.colored_text("Comando ejecutado con éxito.", utils.Colors.GREEN))
                results_summary.append({'description': description, 'status': 'Éxito'})
        except FileNotFoundError:
            logger.error(f"Error: El comando '{command[0]}' no se encontró.")
            print(utils.colored_text(f"Error: El comando '{command[0]}' no se encontró. No se puede continuar.", utils.Colors.RED))
            all_successful = False
            results_summary.append({'description': description, 'status': 'Error', 'details': f"Comando '{command[0]}' no encontrado."})
            break
        except subprocess.CalledProcessError as e:
            all_successful = False
            logger.error(f"El comando '{' '.join(command)}' falló. Salida:\n{e.stderr}")
            print(utils.colored_text(f"Error al ejecutar el comando. Detalles: {e.stderr}", utils.Colors.RED))
            results_summary.append({'description': description, 'status': 'Error', 'details': e.stderr})

    print("\n--- Resumen de Optimización de Red ---")
    for result in results_summary:
        status = result['status']
        description = result['description']
        details = result.get('details', '')

        if status == 'Éxito':
            print(utils.colored_text(f"  ✓ {description}: Éxito", utils.Colors.GREEN))
        elif status == 'Advertencia':
            print(utils.colored_text(f"  ! {description}: Advertencia - {details}", utils.Colors.YELLOW))
        elif status == 'Error':
            print(utils.colored_text(f"  ✗ {description}: Error - {details}", utils.Colors.RED))

    if all_successful:
        print(utils.colored_text("\nOptimización de red completada con éxito.", utils.Colors.GREEN))
    else:
        print(utils.colored_text("\nOptimización de red completada con advertencias. Algunas acciones no se completaron.", utils.Colors.YELLOW))
