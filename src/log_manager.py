# src/log_manager.py
import os

def view_logs(log_dir):
    """Muestra el contenido del archivo de log principal."""
    log_file_path = os.path.join(log_dir, 'OptiTech_System_Optimizer.log')

    try:
        if os.path.exists(log_file_path):
            with open(log_file_path, 'r', encoding='utf-8') as f:
                log_content = f.read()
            print(f"--- Mostrando contenido del log: {os.path.basename(log_file_path)} ---")
            print(log_content)
            print("--- Fin del log ---")
        else:
            print(f"El archivo de log no se encontró en {log_file_path}")
    except Exception as e:
        print(f"Ocurrió un error al leer el archivo de log: {e}")
