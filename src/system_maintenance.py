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
