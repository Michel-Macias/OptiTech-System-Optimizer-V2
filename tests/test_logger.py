import unittest
import os
import logging
import logging.handlers
from unittest.mock import patch, MagicMock
import io
import tempfile
import shutil

# Mock para el módulo config_manager
class MockConfigManager:
    def __init__(self, temp_dir):
        self._temp_dir = temp_dir
    def get_log_path(self):
        return os.path.join(self._temp_dir, "logs")
    def get_default_encoding(self):
        return "utf-8"

class TestLogger(unittest.TestCase):

    def setUp(self):
        # Crear un directorio temporal para los logs de prueba
        self.temp_log_dir = tempfile.mkdtemp()
        self.mock_config_manager = MockConfigManager(self.temp_log_dir)

        # Limpiar cualquier configuración de logging existente
        logging.shutdown()

        # Parchear config_manager y os.makedirs antes de importar src.logger
        self.patcher_config = patch('src.logger.config_manager', new=self.mock_config_manager)
        self.patcher_makedirs = patch('os.makedirs')
        self.mock_makedirs = self.patcher_makedirs.start()
        self.patcher_config.start()

        # Importar el módulo logger *después* de configurar los mocks
        from src import logger
        self.logger_module = logger

        # Capturar la salida de la consola
        self.held_stdout = io.StringIO()
        self.original_stdout = sys.stdout
        sys.stdout = self.held_stdout

        # Configurar el logger para usar un archivo de log mock
        self.log_file_path = os.path.join(self.mock_config_manager.get_log_path(), "app.log")
        # Asegurarse de que el directorio mockeado exista para el RotatingFileHandler
        os.makedirs(os.path.dirname(self.log_file_path), exist_ok=True) # Esto llamará a nuestro mock_makedirs
        self.logger_module.setup_logging(log_file=self.log_file_path, max_bytes=1024, backup_count=5)
        self.app_logger = logging.getLogger('OptiTechOptimizer')
        self.app_logger.setLevel(logging.DEBUG) # Asegurarse de que todos los niveles se procesen

    def tearDown(self):
        sys.stdout = self.original_stdout # Restaurar stdout
        # Limpiar handlers para evitar que se acumulen entre tests
        for handler in self.app_logger.handlers[:]:
            self.app_logger.removeHandler(handler)
            handler.close()
        # Detener los parches
        self.patcher_config.stop()
        self.patcher_makedirs.stop()
        # Eliminar el directorio temporal
        shutil.rmtree(self.temp_log_dir)

    def test_log_file_creation_and_message_format(self):
        message = "This is a test info message."
        self.app_logger.info(message)

        # Verificar que os.makedirs fue llamado para el directorio del log
        self.mock_makedirs.assert_called_with(os.path.dirname(self.log_file_path), exist_ok=True)

        # Leer el contenido del archivo de log real (ya que estamos en un temp_dir)
        with open(self.log_file_path, 'r', encoding='utf-8') as f:
            log_content = f.read()

        self.assertIn(message, log_content)
        expected_format_regex = r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3} - INFO - OptiTechOptimizer - This is a test info message\.$"
        self.assertRegex(log_content.strip(), expected_format_regex)

    def test_log_levels(self):
        self.app_logger.debug("Debug message")
        self.app_logger.info("Info message")
        self.app_logger.warning("Warning message")
        self.app_logger.error("Error message")
        self.app_logger.critical("Critical message")

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