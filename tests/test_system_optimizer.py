# tests/test_system_optimizer.py

import unittest
import os
import json
from unittest.mock import patch, mock_open
from src import system_optimizer

class TestSystemOptimizer(unittest.TestCase):

    def test_load_optimization_profiles_success(self):
        """Prueba que los perfiles de optimización se cargan correctamente desde un JSON válido."""
        mock_data = {
            "services": [
                {"name": "Service1", "description": "Desc1", "level": "safe"},
                {"name": "Service2", "description": "Desc2", "level": "aggressive"}
            ]
        }
        mock_json_data = json.dumps(mock_data)

        # Usamos mock_open para simular la apertura del archivo de configuración
        with patch("builtins.open", mock_open(read_data=mock_json_data)) as mock_file:
            profiles = system_optimizer.load_optimization_profiles('dummy/path/services.json')
            
            # Verificamos que se llamó a open con la ruta correcta
            mock_file.assert_called_once_with('dummy/path/services.json', 'r', encoding='utf-8')
            
            # Verificamos que los perfiles cargados son los correctos
            self.assertEqual(len(profiles), 2)
            self.assertEqual(profiles[0]['name'], 'Service1')
            self.assertEqual(profiles[1]['level'], 'aggressive')

    def test_load_optimization_profiles_file_not_found(self):
        """Prueba que devuelve una lista vacía si el archivo no se encuentra."""
        # Hacemos que open lance un FileNotFoundError
        with patch("builtins.open", side_effect=FileNotFoundError):
            profiles = system_optimizer.load_optimization_profiles('non/existent/path.json')
            self.assertEqual(profiles, [])

    def test_load_optimization_profiles_json_error(self):
        """Prueba que devuelve una lista vacía si el JSON está mal formado."""
        with patch("builtins.open", mock_open(read_data="{malformed-json")):
            profiles = system_optimizer.load_optimization_profiles('dummy/path/bad.json')
            self.assertEqual(profiles, [])

    @patch('subprocess.run')
    def test_get_service_status_running_auto(self, mock_run):
        """Prueba obtener el estado de un servicio que está en ejecución y es automático."""
        # Salida simulada de 'sc.exe query <service>' y 'sc.exe qc <service>'
        mock_query_output = """
        SERVICE_NAME: TestService
        STATE              : 4  RUNNING
        """
        mock_qc_output = """
        [SC] QueryServiceConfig SUCCESS

        SERVICE_NAME: TestService
        START_TYPE         : 2   AUTO_START
        """
        
        # Configuramos el mock para que devuelva las salidas simuladas
        mock_run.side_effect = [
            unittest.mock.Mock(stdout=mock_query_output, returncode=0),
            unittest.mock.Mock(stdout=mock_qc_output, returncode=0)
        ]

        status = system_optimizer.get_service_status('TestService')

        self.assertIsNotNone(status)
        self.assertEqual(status['state'], 'RUNNING')
        self.assertEqual(status['startup'], 'AUTO_START')

    @patch('subprocess.run')
    def test_set_service_startup_type_success(self, mock_run):
        """Prueba que se llama al comando correcto para cambiar el tipo de inicio de un servicio."""
        # Configuramos el mock para que simule una ejecución exitosa
        mock_run.return_value = unittest.mock.Mock(returncode=0)

        result = system_optimizer.set_service_startup_type('TestService', 'disabled')

        # Verificamos que subprocess.run fue llamado con los argumentos correctos
        expected_command = ['sc.exe', 'config', 'TestService', 'start=', 'disabled']
        mock_run.assert_called_once_with(expected_command, capture_output=True, text=True, encoding='utf-8', errors='replace')
        
        # Verificamos que la función devuelve True en caso de éxito
        self.assertTrue(result)

    @patch('src.system_optimizer.set_service_startup_type')
    @patch('src.utils.confirm_operation')
    @patch('src.system_optimizer.get_service_status')
    @patch('src.system_optimizer.load_optimization_profiles')
    def test_run_optimizer_disables_one_service(self, mock_load_profiles, mock_get_status, mock_confirm, mock_set_service):
        """
        Prueba el flujo completo de run_optimizer:
        - Carga un servicio.
        - El usuario confirma la optimización.
        - Se llama a la función para deshabilitar el servicio.
        """
        # Configuración de los mocks
        mock_load_profiles.return_value = [{'name': 'TestService', 'description': 'A test service.'}]
        mock_get_status.return_value = {'state': 'RUNNING', 'startup': 'AUTO_START'}
        mock_confirm.return_value = True  # Simula que el usuario presiona 'y'
        mock_set_service.return_value = True

        # Ejecutamos la función a probar
        system_optimizer.run_optimizer()

        # Verificaciones
        mock_load_profiles.assert_called_once()
        mock_get_status.assert_called_once_with('TestService')
        mock_confirm.assert_called_once()
        mock_set_service.assert_called_once_with('TestService', 'disabled')

if __name__ == '__main__':
    unittest.main()
