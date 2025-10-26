# tests/test_log_manager.py
import unittest
import os
from unittest.mock import patch, mock_open

# Asegurarse de que el módulo src.log_manager se pueda encontrar
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src import log_manager

class TestLogManager(unittest.TestCase):

    def setUp(self):
        """Configura un entorno de prueba limpio antes de cada test."""
        self.log_dir = 'C:\\Users\\Mitxe\\OneDrive\\Escritorio\\repos\\Equipo_Desarrollo\\OptiTech-System-Optimizer-V2\\logs'
        self.log_file_path = os.path.join(self.log_dir, 'OptiTech_System_Optimizer.log')
        # Asegurarse de que el directorio de logs exista para las pruebas
        os.makedirs(self.log_dir, exist_ok=True)

    def tearDown(self):
        """Limpia el entorno de prueba después de cada test."""
        if os.path.exists(self.log_file_path):
            os.remove(self.log_file_path)

    @patch('builtins.print')
    def test_view_logs_existing_file(self, mock_print):
        """Prueba que view_logs lee y muestra el contenido de un archivo de log existente."""
        # Preparar
        log_content = "INFO: Iniciando aplicación...\nERROR: Fallo crítico.\n"
        with open(self.log_file_path, 'w', encoding='utf-8') as f:
            f.write(log_content)

        # Actuar
        log_manager.view_logs(self.log_dir)

        # Afirmar
        mock_print.assert_any_call("--- Mostrando contenido del log: OptiTech_System_Optimizer.log ---")
        mock_print.assert_any_call(log_content)
        mock_print.assert_any_call("--- Fin del log ---")

    @patch('builtins.print')
    def test_view_logs_non_existing_file(self, mock_print):
        """Prueba que view_logs muestra un mensaje de error si el archivo no existe."""
        # Actuar
        log_manager.view_logs(self.log_dir)

        # Afirmar
        mock_print.assert_any_call(f"El archivo de log no se encontró en {self.log_file_path}")

if __name__ == '__main__':
    unittest.main()