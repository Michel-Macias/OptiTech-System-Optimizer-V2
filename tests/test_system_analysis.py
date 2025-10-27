# tests/test_system_analysis.py

import unittest
from unittest.mock import patch, MagicMock, mock_open
import tempfile
import os
from src import system_analysis

class TestSystemAnalysis(unittest.TestCase):

    @patch('psutil.disk_usage')
    @patch('psutil.disk_partitions')
    @patch('psutil.virtual_memory')
    @patch('psutil.cpu_freq')
    @patch('psutil.cpu_percent')
    @patch('psutil.cpu_count')
    @patch('platform.node', return_value='TestHost')
    @patch('platform.machine', return_value='x86_64')
    @patch('platform.version', return_value='10.0.22000')
    @patch('platform.release', return_value='11')
    @patch('platform.system', return_value='Windows')
    def test_get_system_specs_success(self, mock_system, mock_release, mock_version, mock_machine, mock_node, 
                                      mock_cpu_count, mock_cpu_percent, mock_cpu_freq, mock_virtual_memory, 
                                      mock_disk_partitions, mock_disk_usage):
        """Prueba la recopilación exitosa de especificaciones del sistema."""
        # --- Mock CPU ---
        mock_cpu_count.side_effect = [4, 8] # physical, total
        mock_cpu_freq_obj = MagicMock()
        mock_cpu_freq_obj.max = 3400.0
        mock_cpu_freq_obj.min = 1200.0
        mock_cpu_freq_obj.current = 2800.0
        mock_cpu_freq.return_value = mock_cpu_freq_obj
        mock_cpu_percent.side_effect = [[10.0, 20.0, 30.0, 40.0, 15.0, 25.0, 35.0, 45.0], 25.0] # percpu, total

        # --- Mock Memory ---
        mock_svmem = MagicMock()
        mock_svmem.total = 16 * 1024**3
        mock_svmem.available = 8 * 1024**3
        mock_svmem.used = 8 * 1024**3
        mock_svmem.percent = 50.0
        mock_virtual_memory.return_value = mock_svmem

        # --- Mock Disk ---
        mock_partition = MagicMock()
        mock_partition.device = 'C:\\'
        mock_partition.mountpoint = 'C:\\'
        mock_partition.fstype = 'NTFS'
        mock_disk_partitions.return_value = [mock_partition]
        
        mock_usage = MagicMock()
        mock_usage.total = 500 * 1024**3
        mock_usage.used = 200 * 1024**3
        mock_usage.free = 300 * 1024**3
        mock_usage.percent = 40.0
        mock_disk_usage.return_value = mock_usage

        # Call the function
        specs = system_analysis.get_system_specs()

        # --- Assertions ---
        self.assertIsNotNone(specs)

        # OS Info
        self.assertEqual(specs['os_info']['system'], 'Windows')
        self.assertEqual(specs['os_info']['hostname'], 'TestHost')

        # CPU Info
        self.assertEqual(specs['cpu_info']['physical_cores'], 4)
        self.assertEqual(specs['cpu_info']['total_cores'], 8)
        self.assertEqual(specs['cpu_info']['total_usage'], '25.0%')

        # Memory Info
        self.assertEqual(specs['memory_info']['total'], '16.00 GB')
        self.assertEqual(specs['memory_info']['percentage'], '50.0%')

        # Disk Info
        self.assertEqual(len(specs['disk_info']), 1)
        self.assertEqual(specs['disk_info'][0]['device'], 'C:\\')
        self.assertEqual(specs['disk_info'][0]['total_size'], '500.00 GB')
        self.assertEqual(specs['disk_info'][0]['percentage'], '40.0%')

    @patch('platform.system', MagicMock(side_effect=Exception("Test Error")))
    def test_get_system_specs_failure(self):
        """Prueba el fallo durante la recopilación de especificaciones."""
        specs = system_analysis.get_system_specs()
        self.assertIsNone(specs)

    @patch('psutil.win_service_iter')
    def test_get_service_status_success(self, mock_service_iter):
        """Prueba la recopilación exitosa de estados de servicios."""
        # Create mock service objects
        service1 = MagicMock()
        service1.status.return_value = 'running'
        service2 = MagicMock()
        service2.status.return_value = 'running'
        service3 = MagicMock()
        service3.status.return_value = 'stopped'
        service4 = MagicMock()
        service4.status.return_value = 'paused'

        mock_service_iter.return_value = [service1, service2, service3, service4]

        status_counts = system_analysis.get_service_status()

        self.assertIsNotNone(status_counts)
        self.assertEqual(status_counts['total'], 4)
        self.assertEqual(status_counts['running'], 2)
        self.assertEqual(status_counts['stopped'], 1)
        self.assertEqual(status_counts['paused'], 1)

    @patch('src.system_analysis.get_system_specs')
    @patch('src.system_analysis.get_service_status')
    @patch('src.system_analysis.config_manager.get_report_path')
    @patch("builtins.open", new_callable=mock_open)
    def test_run_system_analysis_success(self, mock_file, mock_get_report_path, mock_get_service_status, mock_get_system_specs):
        """Prueba la función principal que ejecuta el análisis."""
        # --- Mock return values ---
        mock_get_system_specs.return_value = {
            'os_info': {'system': 'TestOS', 'release': '1.0', 'version': '1.0.0', 'hostname': 'TestHost', 'architecture': 'x64'},
            'cpu_info': {'physical_cores': 2, 'total_cores': 4, 'current_frequency': '2000.00 Mhz', 'min_frequency': '1000.00 Mhz', 'max_frequency': '3000.00 Mhz', 'total_usage': '50.0%'},
            'memory_info': {'total': '16.00 GB', 'available': '8.00 GB', 'used': '8.00 GB', 'percentage': '50.0%'},
            'disk_info': [{'device': 'D:\\', 'mountpoint': 'D:\\', 'fstype': 'NTFS', 'total_size': '100.00 GB', 'used': '50.00 GB', 'free': '50.00 GB', 'percentage': '50.0%'}]
        }
        mock_get_service_status.return_value = {'total': 10, 'running': 5, 'stopped': 4, 'paused': 1}
        
        temp_dir = tempfile.gettempdir()
        mock_get_report_path.return_value = temp_dir

        # Run the analysis
        system_analysis.run_system_analysis()

        # --- Assertions ---
        mock_file.assert_called_once()
        # Check that the file was opened in write mode with correct encoding
        self.assertEqual(mock_file.call_args[0][1], 'w')
        self.assertEqual(mock_file.call_args[1]['encoding'], 'utf-8')

        # Get the content that was written to the file
        written_content = mock_file().write.call_args[0][0]
        
        self.assertIn("Informe de Análisis de OptiTech System Optimizer", written_content)
        self.assertIn("Sistema:    TestOS 1.0", written_content)
        self.assertIn("Carga Total: 50.0%", written_content)
        self.assertIn("En uso:     8.00 GB (50.0%)", written_content)
        self.assertIn("Servicios Totales: 10", written_content)
        self.assertIn("Dispositivo: D:\\", written_content)


if __name__ == '__main__':
    unittest.main()
