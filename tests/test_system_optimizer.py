# tests/test_system_optimizer.py

import unittest
import os
import json
from unittest.mock import patch, mock_open, call
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

    @patch('src.utils.set_registry_value')
    @patch('src.config_manager.load_config')
    def test_optimize_visual_effects(self, mock_load_config, mock_set_registry_value):
        """
        Prueba que la función de optimización de efectos visuales carga la configuración
        y llama a las funciones de modificación del registro correctamente.
        """
        # Arrange: Configuración simulada que devolverá el config_manager
        mock_settings = [
            {
                "description": "Disable menu animations",
                "hive": "HKEY_CURRENT_USER",
                "key": "Control Panel\\Desktop",
                "value_name": "MenuShowDelay",
                "optimized_value": "0",
                "value_type": "REG_SZ"
            },
            {
                "description": "Disable window animations",
                "hive": "HKEY_CURRENT_USER",
                "key": "Software\\Microsoft\\Windows\\DWM",
                "value_name": "EnableAnimations",
                "optimized_value": 0,
                "value_type": "REG_DWORD"
            }
        ]
        mock_load_config.return_value = mock_settings
        mock_set_registry_value.return_value = (True, "") # Simula éxito

        # Act: Llama a la función que estamos probando (aún no existe)
        system_optimizer.optimize_visual_effects()

        # Assert: Verifica que todo fue llamado como se esperaba
        mock_load_config.assert_called_once_with("visual_effects_settings.json")

        expected_calls = [
            unittest.mock.call(
                hive="HKEY_CURRENT_USER",
                key="Control Panel\\Desktop",
                value_name="MenuShowDelay",
                value="0",
                value_type="REG_SZ"
            ),
            unittest.mock.call(
                hive="HKEY_CURRENT_USER",
                key="Software\\Microsoft\\Windows\\DWM",
                value_name="EnableAnimations",
                value=0,
                value_type="REG_DWORD"
            )
        ]
        mock_set_registry_value.assert_has_calls(expected_calls, any_order=True)

    @patch('src.system_optimizer.get_service_status')
    @patch('src.system_optimizer.set_service_startup_type')
    @patch('src.system_optimizer.config_manager.load_config')
    def test_optimize_services(self, mock_load_config, mock_set_service, mock_get_status):
        """
        Prueba que la función de optimización de servicios carga la configuración,
        comprueba el estado del servicio y llama a la utilidad para deshabilitarlo.
        """
        # Arrange: Configuración simulada de servicios y estado
        mock_services_config = {
            "services": [
                {"name": "TestService1", "description": "A test service"},
                {"name": "TestService2", "description": "Another test service"}
            ]
        }
        mock_load_config.return_value = mock_services_config
        mock_set_service.return_value = True  # Simula éxito
        mock_get_status.return_value = {'startup': 'AUTO_START'} # Simula que no está deshabilitado

        # Act: Llama a la función que estamos probando
        system_optimizer.optimize_services()

        # Assert: Verifica las llamadas a los mocks
        mock_load_config.assert_called_once_with("services_to_optimize.json")

        # Verifica que se comprueba el estado de cada servicio
        status_calls = [call("TestService1"), call("TestService2")]
        mock_get_status.assert_has_calls(status_calls, any_order=True)

        # Verifica que se intenta deshabilitar cada servicio
        set_service_calls = [
            call("TestService1", "disabled"),
            call("TestService2", "disabled")
        ]
        mock_set_service.assert_has_calls(set_service_calls, any_order=True)

    @patch('subprocess.run')
    @patch('src.system_optimizer.config_manager.load_config')
    def test_optimize_power_plan(self, mock_load_config, mock_run):
        """
        Prueba que la función para optimizar el plan de energía carga la configuración
        y llama al comando powercfg correctamente.
        """
        # Arrange: Configuración simulada y mock de subprocess.run
        mock_config = {"high_performance_guid": "TEST-GUID-HIGH-PERFORMANCE"}
        mock_load_config.return_value = mock_config
        mock_run.return_value = unittest.mock.Mock(returncode=0) # Simula éxito

        # Act: Llama a la función que estamos probando
        system_optimizer.optimize_power_plan()

        # Assert: Verifica las llamadas a los mocks
        mock_load_config.assert_called_once_with("power_plan_settings.json")
        mock_run.assert_called_once_with(
            ["powercfg", "/setactive", "TEST-GUID-HIGH-PERFORMANCE"],
            capture_output=True, text=True, encoding='utf-8', errors='replace'
        )

if __name__ == '__main__':
    unittest.main()
