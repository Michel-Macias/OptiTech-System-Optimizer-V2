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

    @patch('src.system_optimizer.optimize_visual_effects')
    @patch('builtins.input', side_effect=['1', '6'])
    def test_run_optimizer_menu_selection(self, mock_input, mock_visual_effects):
        """
        Prueba que el menú de Run-Optimizer llama a la función correcta según la selección del usuario.
        """
        # Act
        system_optimizer.run_optimizer()

        # Assert
        mock_visual_effects.assert_called_once()

    @patch('src.utils.set_registry_value')
    @patch('src.config_manager.load_config')
    @patch('builtins.input', side_effect=['y'])
    def test_optimize_visual_effects(self, mock_input, mock_load_config, mock_set_registry_value):
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
    @patch('src.config_manager.ConfigManager.load_services_to_optimize_config')
    @patch('builtins.input', side_effect=['1', 'y'])
    def test_optimize_services(self, mock_input, mock_load_services_config, mock_set_service, mock_get_status):
        """
        Prueba que la función de optimización de servicios carga la configuración,
        comprueba el estado del servicio y llama a la utilidad para deshabilitarlo.
        """
        # Arrange: Configuración simulada de servicios y estado
        mock_services_config = [
            {"name": "TestService1", "description": "A test service", "recommended_startup_type": "disabled", "risk_level": "bajo"},
            {"name": "TestService2", "description": "Another test service", "recommended_startup_type": "manual", "risk_level": "medio"}
        ]
        mock_load_services_config.return_value = mock_services_config
        mock_set_service.return_value = True  # Simula éxito
        mock_get_status.side_effect = [
            {'startup': 'auto', 'state': 'running'}, # TestService1 no está deshabilitado
            {'startup': 'auto', 'state': 'running'}  # TestService2 no está manual
        ]

        # Act: Llama a la función que estamos probando
        system_optimizer.optimize_services()

        # Assert: Verifica las llamadas a los mocks
        mock_load_services_config.assert_called_once() # No necesita argumentos ya que es un método de instancia

        # Verifica que se comprueba el estado de cada servicio
        status_calls = [call("TestService1"), call("TestService2")]
        mock_get_status.assert_has_calls(status_calls, any_order=False)

        # Verifica que se intenta deshabilitar cada servicio con su tipo recomendado
        set_service_calls = [
            call("TestService1", "disabled"),
            call("TestService2", "manual")
        ]
        mock_set_service.assert_has_calls(set_service_calls, any_order=False)

    @patch('src.system_optimizer.get_service_status')
    @patch('src.system_optimizer.set_service_startup_type')
    @patch('src.config_manager.ConfigManager.load_services_to_optimize_config')
    @patch('builtins.input', side_effect=['1', 'y'])
    def test_optimize_services_already_in_desired_state(self, mock_input, mock_load_services_config, mock_set_service, mock_get_status):
        """
        Prueba que optimize_services no intenta cambiar el tipo de inicio de un servicio
        si ya está en el estado recomendado.
        """
        mock_services_config = [
            {"name": "TestService1", "description": "A test service", "recommended_startup_type": "disabled", "risk_level": "bajo"}
        ]
        mock_load_services_config.return_value = mock_services_config
        mock_get_status.return_value = {'startup': 'disabled', 'state': 'stopped'} # Ya deshabilitado

        system_optimizer.optimize_services()

        mock_load_services_config.assert_called_once()
        mock_get_status.assert_called_once_with("TestService1")
        mock_set_service.assert_not_called() # No debería llamarse si ya está en el estado deseado

    @patch('src.system_optimizer.get_service_status')
    @patch('src.system_optimizer.set_service_startup_type')
    @patch('src.config_manager.ConfigManager.load_services_to_optimize_config')
    @patch('builtins.input', side_effect=['1', 'y'])
    def test_optimize_services_critical_error_get_status(self, mock_input, mock_load_services_config, mock_set_service, mock_get_status):
        """
        Prueba que optimize_services maneja un error crítico (None) al obtener el estado del servicio.
        """
        mock_services_config = [
            {"name": "TestService1", "description": "A test service", "recommended_startup_type": "disabled", "risk_level": "bajo"}
        ]
        mock_load_services_config.return_value = mock_services_config
        mock_get_status.return_value = None # Simula un error crítico

        system_optimizer.optimize_services()

        mock_load_services_config.assert_called_once()
        mock_get_status.assert_called_once_with("TestService1")
        mock_set_service.assert_not_called() # No debería intentar cambiar el servicio si hay un error crítico

    @patch('src.system_optimizer.get_service_status')
    @patch('src.system_optimizer.set_service_startup_type')
    @patch('src.config_manager.ConfigManager.load_services_to_optimize_config')
    @patch('builtins.input', side_effect=['1', 'y'])
    def test_optimize_services_not_found(self, mock_input, mock_load_services_config, mock_set_service, mock_get_status):
        """
        Prueba que optimize_services maneja un servicio que no se encuentra en el sistema.
        """
        mock_services_config = [
            {"name": "TestService1", "description": "A test service", "recommended_startup_type": "disabled", "risk_level": "bajo"}
        ]
        mock_load_services_config.return_value = mock_services_config
        mock_get_status.return_value = {'startup': 'not_found', 'state': 'not_found'} # Simula servicio no encontrado

        system_optimizer.optimize_services()

        mock_load_services_config.assert_called_once()
        mock_get_status.assert_called_once_with("TestService1")
        mock_set_service.assert_not_called() # No debería intentar cambiar el servicio si no se encuentra

    @patch('src.system_optimizer.get_service_status')
    @patch('src.system_optimizer.set_service_startup_type')
    @patch('builtins.input', side_effect=['y'])
    def test_restore_services_to_original_state(self, mock_input, mock_set_service, mock_get_status):
        """
        Prueba la función restore_services_to_original_state.
        """
        # Arrange: Simular que se optimizaron algunos servicios y se guardaron sus estados originales
        system_optimizer._original_service_states = [
            {'name': 'ServiceA', 'original_startup_type': 'auto'},
            {'name': 'ServiceB', 'original_startup_type': 'manual'}
        ]

        # Simular que los servicios están en un estado diferente al original para que se intente el cambio
        mock_get_status.side_effect = [
            {'startup': 'disabled', 'state': 'stopped'}, # ServiceA
            {'startup': 'disabled', 'state': 'stopped'}  # ServiceB
        ]
        mock_set_service.return_value = True # Simular éxito en el cambio

        # Act
        system_optimizer.restore_services_to_original_state()

        # Assert
        mock_get_status.assert_has_calls([call('ServiceA'), call('ServiceB')], any_order=False)
        mock_set_service.assert_has_calls([
            call('ServiceA', 'auto'),
            call('ServiceB', 'manual')
        ], any_order=False)
        self.assertEqual(system_optimizer._original_service_states, []) # La lista debe limpiarse al final

    @patch('subprocess.run')
    @patch('src.system_optimizer.config_manager.load_config')
    @patch('builtins.input', side_effect=['y'])
    def test_optimize_power_plan(self, mock_input, mock_load_config, mock_run):
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

    @patch('subprocess.run')
    @patch('builtins.input', side_effect=['y'])
    def test_optimize_network(self, mock_input, mock_run):
        """
        Prueba que la función de optimización de red llama a los comandos correctos.
        """
        # Arrange: Configura el mock para simular éxito en todos los comandos
        mock_run.return_value = unittest.mock.Mock(returncode=0)

        # Act: Llama a la función que estamos probando
        system_optimizer.optimize_network()

        # Assert: Verifica que se llamaron los comandos de red esperados
        expected_commands = [
            call(["ipconfig", "/release"], capture_output=True, text=True, check=True),
            call(["ipconfig", "/renew"], capture_output=True, text=True, check=True),
            call(["ipconfig", "/flushdns"], capture_output=True, text=True, check=True),
            call(["netsh", "winsock", "reset"], capture_output=True, text=True, check=True),
            call(["netsh", "int", "ip", "reset"], capture_output=True, text=True, check=True)
        ]
        mock_run.assert_has_calls(expected_commands, any_order=False)


if __name__ == '__main__':
    unittest.main()
