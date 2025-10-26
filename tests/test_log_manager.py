import unittest
import os
import sys
from unittest.mock import patch

# Añadir el directorio src al sys.path para permitir importaciones directas
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# Ahora que el path está configurado, podemos importar los módulos de src
# Este import se moverá dentro de los métodos de test o setUp para asegurar que
# el patching ocurra antes de la importación del módulo que queremos probar.

class TestLogManager(unittest.TestCase):

    def setUp(self):
        """Configura un entorno de prueba limpio antes de cada test."""
        self.test_log_dir = os.path.join(os.path.dirname(__file__), 'temp_test_logs')
        os.makedirs(self.test_log_dir, exist_ok=True)

        # Crear algunos archivos de log de prueba
        self.log_files_to_create = ['app.log', 'app.log.1', 'unrelated.txt']
        self.log_contents = {}
        for log_file in self.log_files_to_create:
            content = f'Contenido de {log_file}'
            self.log_contents[log_file] = content
            with open(os.path.join(self.test_log_dir, log_file), 'w') as f:
                f.write(content)

        # --- Patching ---
        # Es crucial parchear 'config_manager' ANTES de que 'log_manager' lo importe.
        # La mejor manera de asegurar esto es parchear la dependencia directa.
        self.config_patcher = patch('log_manager.config_manager')
        self.mock_config_manager = self.config_patcher.start()
        
        # Configuramos el mock para que devuelva nuestro directorio de prueba
        self.mock_config_manager.get_log_path.return_value = self.test_log_dir
        self.mock_config_manager.get_default_encoding.return_value = 'utf-8'
        
        # Importamos LogManager DESPUÉS de que el parche esté activo
        from log_manager import LogManager
        self.log_manager = LogManager()


    def tearDown(self):
        """Limpia el entorno de prueba después de cada test."""
        # Detener el parche
        self.config_patcher.stop()

        # Limpiar el directorio de logs de prueba
        for file_name in os.listdir(self.test_log_dir):
            os.remove(os.path.join(self.test_log_dir, file_name))
        os.rmdir(self.test_log_dir)

    def test_get_log_files(self):
        """Prueba que se listen correctamente solo los archivos de log."""
        log_files = self.log_manager.get_log_files()
        
        # Debería encontrar 'app.log' y 'app.log.1', pero no 'unrelated.txt'
        self.assertEqual(len(log_files), 2)
        self.assertIn('app.log', log_files)
        self.assertIn('app.log.1', log_files)
        self.assertNotIn('unrelated.txt', log_files)

    def test_view_log_content_existing(self):
        """Prueba la visualización del contenido de un archivo de log existente."""
        log_to_view = 'app.log'
        content = self.log_manager.view_log_content(log_to_view)
        self.assertEqual(content, self.log_contents[log_to_view])

    def test_view_log_content_non_existing(self):
        """Prueba que devuelve None al intentar ver un log inexistente."""
        content = self.log_manager.view_log_content('non_existing_log.log')
        self.assertIsNone(content)

    def test_view_log_content_outside_log_dir(self):
        """Prueba que no se pueda acceder a archivos fuera del directorio de logs."""
        # Intento de path traversal
        malicious_path = os.path.join('..', '..', 'README.md')
        content = self.log_manager.view_log_content(malicious_path)
        self.assertIsNone(content)

    def test_delete_log_file_existing(self):
        """Prueba la eliminación de un archivo de log existente."""
        log_to_delete = 'app.log.1'
        log_path = os.path.join(self.test_log_dir, log_to_delete)
        
        self.assertTrue(os.path.exists(log_path))
        result = self.log_manager.delete_log_file(log_to_delete)
        self.assertTrue(result)
        self.assertFalse(os.path.exists(log_path))

    def test_delete_log_file_non_existing(self):
        """Prueba que devuelve False al intentar eliminar un log inexistente."""
        result = self.log_manager.delete_log_file('non_existing_log.log')
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
