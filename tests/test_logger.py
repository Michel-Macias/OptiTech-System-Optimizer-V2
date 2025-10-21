# tests/test_logger.py

import unittest
import os
import logging
from unittest.mock import patch, MagicMock
import io
import datetime

# Mock para el módulo config_manager
class MockConfigManager:
    def get_log_path(self):
        return "/mock/appdata/OptiTechOptimizer/logs"

    def get_default_encoding(self):
        return "utf-8"

# Mock para simular os.makedirs y os.path.exists
class MockOs:
    def __init__(self):
        self.dirs_created = []
        self.files = {}

    def makedirs(self, name, exist_ok=False):
        self.dirs_created.append(name)

    def path_exists(self, path):
        return path in self.files or path in self.dirs_created

    def path_getsize(self, path):
        return len(self.files.get(path, "").encode('utf-8'))

    def rename(self, src, dst):
        if src in self.files:
            self.files[dst] = self.files.pop(src)

    def open(self, file, mode='a', encoding=None):
        # Simular la escritura en el archivo
        mock_file = io.StringIO()
        if file in self.files and mode == 'a':
            mock_file.write(self.files[file])
        self.files[file] = mock_file
        return mock_file


class TestLogger(unittest.TestCase):

    @patch('src.logger.config_manager', new=MockConfigManager())
    @patch('os.makedirs', new=MockOs().makedirs)
    @patch('os.path.exists', new=MockOs().path_exists)
    @patch('os.path.getsize', new=MockOs().path_getsize)
    @patch('os.rename', new=MockOs().rename)
    def setUp(self):
        # Limpiar cualquier configuración de logging existente
        logging.shutdown()
        self.mock_os = MockOs()
        # Re-patch os.makedirs, os.path.exists, etc. para cada test si es necesario
        # Para este caso, los parches a nivel de clase son suficientes si MockOs se reinicia

        # Importar el módulo logger *después* de configurar los mocks
        from src import logger
        self.logger_module = logger

        # Capturar la salida de la consola
        self.held_stdout = io.StringIO()
        self.original_stdout = sys.stdout
        sys.stdout = self.held_stdout

        # Configurar el logger para usar un archivo de log mock
        self.log_file_path = os.path.join(MockConfigManager().get_log_path(), "app.log")
        self.logger_module.setup_logging(log_file=self.log_file_path, max_bytes=1024, backup_count=5)
        self.app_logger = logging.getLogger('OptiTechOptimizer')
        self.app_logger.setLevel(logging.DEBUG) # Asegurarse de que todos los niveles se procesen

    def tearDown(self):
        sys.stdout = self.original_stdout # Restaurar stdout
        # Limpiar handlers para evitar que se acumulen entre tests
        for handler in self.app_logger.handlers[:]:
            self.app_logger.removeHandler(handler)
            handler.close()

    def test_log_file_creation_and_message_format(self):
        message = "This is a test info message."
        self.app_logger.info(message)

        # Simular la lectura del archivo de log (usando el mock de os.open)
        with patch('builtins.open', new=self.mock_os.open):
            with open(self.log_file_path, 'r', encoding='utf-8') as f:
                log_content = f.read()

        self.assertIn(message, log_content)
        # Verificar el formato: YYYY-MM-DD HH:MM:SS,ms - LEVEL - MODULE - MESSAGE
        # Usamos un regex simple para la fecha y hora, y luego verificamos el resto
        # Esto fallará inicialmente porque el logger no está implementado
        expected_format_regex = r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3} - INFO - OptiTechOptimizer - This is a test info message\."
        self.assertRegex(log_content.strip(), expected_format_regex)

    def test_log_levels(self):
        self.app_logger.debug("Debug message")
        self.app_logger.info("Info message")
        self.app_logger.warning("Warning message")
        self.app_logger.error("Error message")
        self.app_logger.critical("Critical message")

        with patch('builtins.open', new=self.mock_os.open):
            with open(self.log_file_path, 'r', encoding='utf-8') as f:
                log_content = f.read()

        self.assertIn("Debug message", log_content)
        self.assertIn("Info message", log_content)
        self.assertIn("Warning message", log_content)
        self.assertIn("Error message", log_content)
        self.assertIn("Critical message", log_content)

    def test_console_output(self):
        message = "Console info message."
        self.app_logger.info(message)
        self.assertIn(message, self.held_stdout.getvalue())

        self.held_stdout.seek(0) # Reset StringIO
        self.held_stdout.truncate(0)
        self.app_logger.debug("Console debug message.") # DEBUG no debería aparecer en consola por defecto
        self.assertEqual(self.held_stdout.getvalue(), "")

    # Test de rotación de logs (esto es más complejo de mockear completamente en un unit test)
    # Nos centraremos en que el RotatingFileHandler esté configurado correctamente
    def test_log_rotation_handler_configured(self):
        # Verificar que un handler de tipo RotatingFileHandler está presente
        found_rotating_handler = False
        for handler in self.app_logger.handlers:
            if isinstance(handler, logging.handlers.RotatingFileHandler):
                found_rotating_handler = True
                self.assertEqual(handler.baseFilename, self.log_file_path)
                self.assertEqual(handler.maxBytes, 1024)
                self.assertEqual(handler.backupCount, 5)
                break
        self.assertTrue(found_rotating_handler, "RotatingFileHandler not found in logger handlers")

if __name__ == '__main__':
    unittest.main()
