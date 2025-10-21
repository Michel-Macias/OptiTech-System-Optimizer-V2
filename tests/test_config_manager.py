# tests/test_config_manager.py

import unittest
import os
from unittest.mock import patch, MagicMock

# Mock para simular la función os.makedirs
class MockOs:
    def __init__(self):
        self.dirs_created = []

    def makedirs(self, name, exist_ok=False):
        self.dirs_created.append(name)

class TestConfigManager(unittest.TestCase):

    @patch('os.makedirs')
    @patch('os.path.exists')
    @patch('os.path.expandvars')
    def setUp(self, mock_expandvars, mock_exists, mock_makedirs):
        # Configurar mocks para simular el entorno de Windows
        mock_expandvars.side_effect = lambda x: x.replace('%LOCALAPPDATA%', 'C:\\Users\\testuser\\AppData\\Local')
        mock_exists.return_value = False # Simular que los directorios no existen inicialmente
        mock_makedirs.side_effect = MockOs().makedirs # Usar nuestro mock para makedirs

        # Importar el módulo de configuración *después* de configurar los mocks
        # para asegurar que el módulo usa los mocks al inicializarse
        # Esto fallará porque src.config_manager no existe aún, lo cual es el comportamiento esperado de un test que falla.
        try:
            from src import config_manager
            self.config_manager = config_manager
        except ImportError:
            self.config_manager = None # Para que las pruebas puedan fallar limpiamente si el módulo no existe

    def test_default_app_data_path(self):
        self.assertIsNotNone(self.config_manager, "config_manager module not found")
        expected_path = os.path.join('C:\\Users\\testuser\\AppData\\Local', 'OptiTechOptimizer')
        self.assertEqual(self.config_manager.get_app_data_path(), expected_path)

    def test_default_log_path(self):
        self.assertIsNotNone(self.config_manager, "config_manager module not found")
        expected_path = os.path.join('C:\\Users\\testuser\\AppData\\Local', 'OptiTechOptimizer', 'logs')
        self.assertEqual(self.config_manager.get_log_path(), expected_path)

    def test_default_backup_path(self):
        self.assertIsNotNone(self.config_manager, "config_manager module not found")
        expected_path = os.path.join('C:\\Users\\testuser\\AppData\\Local', 'OptiTechOptimizer', 'backups')
        self.assertEqual(self.config_manager.get_backup_path(), expected_path)

    def test_default_report_path(self):
        self.assertIsNotNone(self.config_manager, "config_manager module not found")
        expected_path = os.path.join('C:\\Users\\testuser\\AppData\\Local', 'OptiTechOptimizer', 'reports')
        self.assertEqual(self.config_manager.get_report_path(), expected_path)

    @patch('os.makedirs')
    @patch('os.path.exists')
    @patch('os.path.expandvars')
    def test_directories_are_created(self, mock_expandvars, mock_exists, mock_makedirs):
        # Re-configurar mocks para esta prueba específica si es necesario, o asegurar que los de setUp son suficientes
        mock_expandvars.side_effect = lambda x: x.replace('%LOCALAPPDATA%', 'C:\\Users\\testuser\\AppData\\Local')
        mock_exists.return_value = False
        # Crear una nueva instancia del config_manager para asegurar que makedirs se llama durante su inicialización
        from src import config_manager as fresh_config_manager
        _ = fresh_config_manager.ConfigManager() # Instanciar para que se llamen los métodos de creación de directorios

        expected_app_data_path = os.path.join('C:\\Users\\testuser\\AppData\\Local', 'OptiTechOptimizer')
        expected_log_path = os.path.join(expected_app_data_path, 'logs')
        expected_backup_path = os.path.join(expected_app_data_path, 'backups')
        expected_report_path = os.path.join(expected_app_data_path, 'reports')

        mock_makedirs.assert_any_call(expected_app_data_path, exist_ok=True)
        mock_makedirs.assert_any_call(expected_log_path, exist_ok=True)
        mock_makedirs.assert_any_call(expected_backup_path, exist_ok=True)
        mock_makedirs.assert_any_call(expected_report_path, exist_ok=True)

    def test_default_encoding_is_utf8(self):
        self.assertIsNotNone(self.config_manager, "config_manager module not found")
        self.assertEqual(self.config_manager.get_default_encoding(), 'utf-8')

if __name__ == '__main__':
    unittest.main()

