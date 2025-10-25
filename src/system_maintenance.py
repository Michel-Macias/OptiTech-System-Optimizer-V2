# src/system_maintenance.py

import logging
import os
import subprocess
import datetime
from src import utils

APP_LOGGER_NAME = 'OptiTechOptimizer'
logger = logging.getLogger(APP_LOGGER_NAME)

def backup_registry():
    """Crea un backup completo del registro de Windows."""
    logger.info("Iniciando el proceso de backup del registro.")
    
    backup_dir = utils.get_backup_dir()
    if not backup_dir:
        logger.error("No se pudo obtener el directorio de backups. Abortando backup del registro.")
        return False

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = os.path.join(backup_dir, f"registry_backup_{timestamp}.reg")

    try:
        print(f"Creando backup del registro en: {backup_filename}")
        command = ["reg", "export", "HKEY_CURRENT_USER", backup_filename, "/y"]

        result = subprocess.run(command, capture_output=True, text=True, check=True)

        if result.returncode == 0:
            logger.info(f"Backup del registro creado con éxito en {backup_filename}")
            print("Backup del registro completado con éxito.")
            return True
        else:
            logger.error(f"Error al crear el backup del registro. Stderr: {result.stderr}")
            print(f"Error al crear el backup del registro: {result.stderr}")
            return False

    except FileNotFoundError:
        logger.error("El comando 'reg' no se encontró. Asegúrese de que está en el PATH del sistema.")
        print("Error: El comando 'reg' no se encontró.")
        return False
    except subprocess.CalledProcessError as e:
        logger.error(f"El comando de backup del registro falló. Stderr: {e.stderr}")
        print(f"Error durante el backup del registro: {e.stderr}")
        return False
    except Exception as e:
        logger.error(f"Error inesperado durante el backup del registro: {e}", exc_info=True)
        print(f"Ocurrió un error inesperado: {e}")
        return False

def restore_registry(backup_path):
    """Restaura el registro de Windows desde un archivo .reg."""
    logger.info(f"Iniciando la restauración del registro desde: {backup_path}")

    if not os.path.exists(backup_path):
        logger.error(f"El archivo de backup no existe: {backup_path}")
        print(f"Error: El archivo de backup no fue encontrado en '{backup_path}'.")
        return False

    try:
        print(f"Restaurando el registro desde: {backup_path}")
        command = ["reg", "import", backup_path]

        result = subprocess.run(command, capture_output=True, text=True, check=True)

        if result.returncode == 0:
            logger.info(f"Restauración del registro completada con éxito desde {backup_path}")
            print("Restauración del registro completada con éxito.")
            return True
        else:
            logger.error(f"Error al restaurar el registro. Stderr: {result.stderr}")
            print(f"Error al restaurar el registro: {result.stderr}")
            return False

    except FileNotFoundError:
        logger.error("El comando 'reg' no se encontró. Asegúrese de que está en el PATH del sistema.")
        print("Error: El comando 'reg' no se encontró.")
        return False
    except subprocess.CalledProcessError as e:
        logger.error(f"El comando de restauración del registro falló. Stderr: {e.stderr}")
        print(f"Error durante la restauración del registro: {e.stderr}")
        return False
    except Exception as e:
        logger.error(f"Error inesperado durante la restauración del registro: {e}", exc_info=True)
        print(f"Ocurrió un error inesperado: {e}")
        return False

def create_system_restore_point(description):
    """Crea un punto de restauración del sistema."""
    logger.info(f"Creando punto de restauración del sistema con descripción: {description}")
    try:
        command = [
            "powershell.exe",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-Command",
            f"Checkpoint-Computer -Description '{description}' -RestorePointType 'MODIFY_SETTINGS'"
        ]
        
        print(f"Creando punto de restauración del sistema: '{description}'")
        result = subprocess.run(command, capture_output=True, text=True, check=True)

        if result.returncode == 0:
            logger.info("Punto de restauración del sistema creado con éxito.")
            print("Punto de restauración del sistema creado con éxito.")
            return True
        else:
            logger.error(f"Error al crear el punto de restauración. Stderr: {result.stderr}")
            print(f"Error al crear el punto de restauración: {result.stderr}")
            return False

    except FileNotFoundError:
        logger.error("El comando 'powershell.exe' no se encontró. Asegúrese de que está en el PATH del sistema.")
        print("Error: El comando 'powershell.exe' no se encontró.")
        return False
    except subprocess.CalledProcessError as e:
        logger.error(f"El comando de creación de punto de restauración falló. Stderr: {e.stderr}")
        print(f"Error durante la creación del punto de restauración: {e.stderr}")
        return False
    except Exception as e:
        logger.error(f"Error inesperado durante la creación del punto de restauración: {e}", exc_info=True)
        print(f"Ocurrió un error inesperado: {e}")
        return False

def run_sfc():
    """Ejecuta el System File Checker (SFC) para escanear y reparar archivos del sistema."""
    logger.info("Iniciando escaneo SFC (System File Checker).")
    try:
        print("Ejecutando SFC /scannow. Esto puede tardar varios minutos...")
        command = ["sfc", "/scannow"]
        result = subprocess.run(command, capture_output=True, text=True, check=True)

        if result.returncode == 0:
            logger.info("Escaneo SFC completado con éxito.")
            print("Escaneo SFC completado con éxito.")
            return True
        else:
            logger.error(f"Error durante el escaneo SFC. Stderr: {result.stderr}")
            print(f"Error durante el escaneo SFC: {result.stderr}")
            return False

    except FileNotFoundError:
        logger.error("El comando 'sfc' no se encontró. Asegúrese de que está en el PATH del sistema.")
        print("Error: El comando 'sfc' no se encontró.")
        return False
    except subprocess.CalledProcessError as e:
        logger.error(f"El comando SFC falló. Stderr: {e.stderr}")
        print(f"Error durante el escaneo SFC: {e.stderr}")
        return False
    except Exception as e:
        logger.error(f"Error inesperado durante el escaneo SFC: {e}", exc_info=True)
        print(f"Ocurrió un error inesperado: {e}")
        return False

def run_dism():
    """Ejecuta DISM para reparar la imagen de Windows."""
    logger.info("Iniciando DISM /Online /Cleanup-Image /RestoreHealth.")
    try:
        print("Ejecutando DISM. Esto puede tardar varios minutos...")
        command = ["DISM", "/Online", "/Cleanup-Image", "/RestoreHealth"]
        result = subprocess.run(command, capture_output=True, text=True, check=True)

        if result.returncode == 0:
            logger.info("DISM completado con éxito.")
            print("DISM completado con éxito.")
            return True
        else:
            logger.error(f"Error durante la ejecución de DISM. Stderr: {result.stderr}")
            print(f"Error durante la ejecución de DISM: {result.stderr}")
            return False

    except FileNotFoundError:
        logger.error("El comando 'DISM' no se encontró. Asegúrese de que está en el PATH del sistema.")
        print("Error: El comando 'DISM' no se encontró.")
        return False
    except subprocess.CalledProcessError as e:
        logger.error(f"El comando DISM falló. Stderr: {e.stderr}")
        print(f"Error durante la ejecución de DISM: {e.stderr}")
        return False
    except Exception as e:
        logger.error(f"Error inesperado durante la ejecución de DISM: {e}", exc_info=True)
        print(f"Ocurrió un error inesperado: {e}")
        return False

def run_chkdsk(drive):
    """Ejecuta CHKDSK en una unidad específica."""
    logger.info(f"Iniciando CHKDSK en la unidad {drive}.")
    try:
        print(f"Ejecutando CHKDSK en la unidad {drive}. Esto puede tardar varios minutos...")
        command = ["chkdsk", drive, "/F", "/R"]
        result = subprocess.run(command, capture_output=True, text=True, check=True)

        if result.returncode == 0:
            logger.info(f"CHKDSK en la unidad {drive} completado con éxito.")
            print(f"CHKDSK en la unidad {drive} completado con éxito.")
            return True
        else:
            logger.error(f"Error durante la ejecución de CHKDSK en la unidad {drive}. Stderr: {result.stderr}")
            print(f"Error durante la ejecución de CHKDSK en la unidad {drive}: {result.stderr}")
            return False

    except FileNotFoundError:
        logger.error("El comando 'chkdsk' no se encontró. Asegúrese de que está en el PATH del sistema.")
        print("Error: El comando 'chkdsk' no se encontró.")
        return False
    except subprocess.CalledProcessError as e:
        logger.error(f"El comando CHKDSK falló. Stderr: {e.stderr}")
        print(f"Error durante la ejecución de CHKDSK: {e.stderr}")
        return False
    except Exception as e:
        logger.error(f"Error inesperado durante la ejecución de CHKDSK: {e}", exc_info=True)
        print(f"Ocurrió un error inesperado: {e}")
        return False

def run_maintenance():
    """Muestra un menú interactivo para que el usuario elija las tareas de mantenimiento a aplicar."""
    utils.show_header("Módulo de Mantenimiento del Sistema")
    logger.info("Iniciando el módulo interactivo de mantenimiento.")

    while True:
        print("\nPor favor, elija una opción de mantenimiento:")
        print("  1. Backup del Registro")
        print("  2. Restaurar Registro")
        print("  3. Crear Punto de Restauración del Sistema")
        print("  4. Ejecutar SFC (System File Checker)")
        print("  5. Ejecutar DISM (Deployment Image Servicing and Management)")
        print("  6. Ejecutar CHKDSK (Check Disk)")
        print("  7. Volver al Menú Principal")

        choice = input("Seleccione una opción: ").strip()

        if choice == '1':
            if utils.confirm_operation("¿Está seguro de que desea hacer un backup del registro?"):
                backup_registry()
        elif choice == '2':
            backup_files = [f for f in os.listdir(utils.get_backup_dir()) if f.startswith("registry_backup_") and f.endswith(".reg")]
            if not backup_files:
                print("No se encontraron archivos de backup del registro.")
                logger.warning("Intento de restauración de registro sin archivos de backup disponibles.")
                continue
            
            print("\nArchivos de backup del registro disponibles:")
            for i, f in enumerate(backup_files, 1):
                print(f"  {i}. {f}")
            
            file_choice = input("Seleccione el número del archivo de backup a restaurar: ").strip()
            try:
                selected_file = backup_files[int(file_choice) - 1]
                full_path = os.path.join(utils.get_backup_dir(), selected_file)
                if utils.confirm_operation(f"¿Está seguro de que desea restaurar el registro desde {selected_file}? Esta operación es crítica."):
                    restore_registry(full_path)
            except (ValueError, IndexError):
                print("Selección no válida.")
                logger.warning(f"Selección de archivo de backup no válida: {file_choice}")

        elif choice == '3':
            if utils.confirm_operation("¿Está seguro de que desea crear un punto de restauración del sistema?"):
                description = input("Ingrese una descripción para el punto de restauración: ").strip()
                if description:
                    create_system_restore_point(description)
                else:
                    print("La descripción no puede estar vacía.")
                    logger.warning("Intento de crear punto de restauración con descripción vacía.")
        elif choice == '4':
            if utils.confirm_operation("¿Está seguro de que desea ejecutar SFC /scannow? Esto puede tardar un tiempo."):
                run_sfc()
        elif choice == '5':
            if utils.confirm_operation("¿Está seguro de que desea ejecutar DISM /RestoreHealth? Esto puede tardar un tiempo."):
                run_dism()
        elif choice == '6':
            drive = input("Ingrese la letra de la unidad para CHKDSK (ej. C): ").strip().upper()
            if drive and len(drive) == 1 and drive.isalpha():
                if utils.confirm_operation(f"¿Está seguro de que desea ejecutar CHKDSK en la unidad {drive}:? Esto puede requerir un reinicio."):
                    run_chkdsk(f"{drive}:")
            else:
                print("Entrada de unidad no válida.")
                logger.warning(f"Entrada de unidad CHKDSK no válida: {drive}")
        elif choice == '7':
            print("Volviendo al menú principal...")
            logger.info("Saliendo del módulo de mantenimiento.")
            break
        else:
            print("Opción no válida. Por favor, intente de nuevo.")
            logger.warning(f"Opción de mantenimiento no válida seleccionada: {choice}")
