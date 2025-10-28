# src/utils.py

import sys
import time
import winreg
import os
import subprocess



def set_registry_value(hive, key, value_name, value, value_type):
    """
    Modifica un valor en el Registro de Windows.

    Args:
        hive (str): El hive del registro (ej. "HKEY_CURRENT_USER").
        key (str): La ruta de la clave del registro.
        value_name (str): El nombre del valor a modificar.
        value (any): El nuevo valor a establecer.
        value_type (str): El tipo de valor del registro (ej. "REG_SZ", "REG_DWORD").

    Returns:
        tuple[bool, str]: Una tupla con un booleano de éxito y un mensaje de error (si lo hay).
    """
    hive_map = {
        "HKEY_CURRENT_USER": winreg.HKEY_CURRENT_USER,
        "HKEY_LOCAL_MACHINE": winreg.HKEY_LOCAL_MACHINE,
        "HKEY_CLASSES_ROOT": winreg.HKEY_CLASSES_ROOT,
        "HKEY_USERS": winreg.HKEY_USERS,
        "HKEY_CURRENT_CONFIG": winreg.HKEY_CURRENT_CONFIG
    }

    type_map = {
        "REG_SZ": winreg.REG_SZ,
        "REG_EXPAND_SZ": winreg.REG_EXPAND_SZ,
        "REG_BINARY": winreg.REG_BINARY,
        "REG_DWORD": winreg.REG_DWORD,
        "REG_MULTI_SZ": winreg.REG_MULTI_SZ,
        "REG_QWORD": winreg.REG_QWORD
    }

    try:
        reg_hive = hive_map[hive]
        reg_type = type_map[value_type]

        # Para REG_BINARY, el valor debe ser convertido de una cadena hexadecimal a bytes
        if reg_type == winreg.REG_BINARY and isinstance(value, str):
            processed_value = bytes.fromhex(value.replace(' ', ''))
        else:
            processed_value = value

        with winreg.OpenKeyEx(reg_hive, key, 0, winreg.KEY_ALL_ACCESS) as reg_key:
            winreg.SetValueEx(reg_key, value_name, 0, reg_type, processed_value)
        
        return True, ""
    except FileNotFoundError:
        return False, f"La clave de registro no fue encontrada: {key}"
    except PermissionError:
        return False, f"Permiso denegado para acceder a la clave: {key}"
    except Exception as e:
        return False, str(e)

def show_header(text, screen_width=80):
    """
    Displays a centered header with a decorative border.

    Args:
        text (str): The text to display in the header.
        screen_width (int): The width of the header in characters.
    """
    print("=" * screen_width)
    print(text.center(screen_width))
    print("=" * screen_width)
    print() # Add a blank line for spacing

def confirm_operation(prompt):
    """
    Asks the user for confirmation (Y/N) and returns a boolean.

    Args:
        prompt (str): The question to ask the user.

    Returns:
        bool: True if the user confirms, False otherwise.
    """
    while True:
        response = input(f"{prompt} [y/n]: ").lower().strip()
        if response in ['y', 'yes']:
            return True
        elif response in ['n', 'no']:
            return False
        else:
            print("Invalid input. Please enter 'y' or 'n'.")

def show_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=50, fill='█'):
    """
    Displays a progress bar in the console.

    Args:
        iteration (int): current iteration.
        total (int): total iterations.
        prefix (str): prefix string.
        suffix (str): suffix string.
        decimals (int): positive number of decimals in percent complete.
        length (int): character length of bar.
        fill (str): bar fill character.
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // float(total))
    bar = fill * filled_length + '-' * (length - filled_length)
    sys.stdout.write(f'\r{prefix} |{bar}| {percent}% {suffix}')
    sys.stdout.flush()
    if iteration == total:
        sys.stdout.write('\n')
        sys.stdout.flush()


def get_service_status(service_name):
    """
    Obtiene el estado y el tipo de inicio de un servicio de Windows de forma robusta.
    Es compatible con sistemas en inglés y español.

    Args:
        service_name (str): El nombre del servicio.

    Returns:
        dict: Un diccionario con 'state' y 'startup', o None si el servicio no existe o hay un error.
    """
    status_info = {'state': 'UNKNOWN', 'startup': 'UNKNOWN'}

    try:
        # 1. Verificar existencia y obtener START_TYPE con 'sc qc'
        qc_cmd = ["sc.exe", "qc", service_name]
        qc_result = subprocess.run(qc_cmd, capture_output=True, text=True, encoding='utf-8', errors='replace', check=False)

        if qc_result.returncode != 0:
            return {'state': 'NOT_FOUND', 'startup': 'NOT_FOUND'}

        for line in qc_result.stdout.splitlines():
            if "START_TYPE" in line or "TIPO_INICIO" in line:
                startup_raw = line.split(':')[1].strip()
                if "AUTO_START" in startup_raw or "AUTOMATICO" in startup_raw:
                    status_info['startup'] = 'AUTO_START'
                elif "DEMAND_START" in startup_raw or "A_PETICION" in startup_raw:
                    status_info['startup'] = 'DEMAND_START'
                elif "DISABLED" in startup_raw or "DESHABILITADO" in startup_raw:
                    status_info['startup'] = 'DISABLED'
                break
        
        # 2. Obtener el estado (STATE) con 'sc query'
        query_cmd = ["sc.exe", "query", service_name]
        query_result = subprocess.run(query_cmd, capture_output=True, text=True, encoding='utf-8', errors='replace', check=False)

        if query_result.returncode == 0:
            for line in query_result.stdout.splitlines():
                if "STATE" in line or "ESTADO" in line:
                    state_raw = line.split(':')[1].strip()
                    if "RUNNING" in state_raw or "EN_EJECUCION" in state_raw:
                        status_info['state'] = 'RUNNING'
                    elif "STOPPED" in state_raw or "DETENIDO" in state_raw:
                        status_info['state'] = 'STOPPED'
                    break
        else:
            if status_info['startup'] == 'DISABLED':
                status_info['state'] = 'STOPPED'

    except FileNotFoundError:
        return None
    except Exception:
        return None

    return status_info

def set_service_startup_type(service_name, startup_type):
    """
    Cambia el tipo de inicio de un servicio de Windows.

    Args:
        service_name (str): El nombre del servicio.
        startup_type (str): El nuevo tipo de inicio ('auto', 'demand', 'disabled').

    Returns:
        bool: True si la operación fue exitosa, False en caso contrario.
    """

    valid_startup_types = {
        "automatic": "auto",
        "manual": "demand",
        "disabled": "disabled"
    }
    sc_startup_type = valid_startup_types.get(startup_type, startup_type)

    try:
        cmd = ["sc.exe", "config", service_name, "start=", sc_startup_type]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True, encoding='utf-8', errors='replace')
        return True
    except FileNotFoundError:
        # log_manager.error("El comando 'sc.exe' no se encontró.")
        return False
    except subprocess.CalledProcessError:
        # log_manager.error(f"Error al cambiar tipo de inicio de '{service_name}': {e.stderr}")
        return False
    except Exception:
        # log_manager.error(f"Error inesperado al cambiar tipo de inicio de '{service_name}': {e}", exc_info=True)
        return False


