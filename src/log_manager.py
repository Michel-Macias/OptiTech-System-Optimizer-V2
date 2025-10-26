# src/log_manager.py

import os
import re
from src import config_manager

class LogManager:
    """Gestiona las operaciones sobre los archivos de log, como ver y eliminar."""

    def __init__(self):
        """Inicializa el gestor de logs, obteniendo la ruta desde ConfigManager."""
        self._log_path = config_manager.get_log_path()

    def get_log_files(self):
        """Devuelve una lista de nombres de archivos de log en el directorio de logs."""
        try:
            all_files = os.listdir(self._log_path)
            # Filtra para incluir solo 'app.log' y sus rotaciones (ej. 'app.log.1')
            log_pattern = re.compile(r'^app\.log(\.\d+)?$')
            return sorted([f for f in all_files if log_pattern.match(f)])
        except FileNotFoundError:
            return []

    def view_log_content(self, filename):
        """Devuelve el contenido de un archivo de log específico."""
        # Seguridad: Prevenir path traversal. Solo permitir nombres de archivo.
        if os.path.basename(filename) != filename:
            return None

        log_file_path = os.path.join(self._log_path, filename)
        
        try:
            with open(log_file_path, 'r', encoding=config_manager.get_default_encoding()) as f:
                return f.read()
        except FileNotFoundError:
            return None

    def delete_log_file(self, filename):
        """Elimina un archivo de log específico."""
        # Seguridad: Prevenir path traversal.
        if os.path.basename(filename) != filename:
            return False

        log_file_path = os.path.join(self._log_path, filename)

        if not os.path.exists(log_file_path):
            return False

        try:
            os.remove(log_file_path)
            return True
        except OSError:
            # Podríamos loggear el error específico si tuviéramos un logger aquí
            return False
