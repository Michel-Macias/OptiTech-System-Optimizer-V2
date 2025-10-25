# tests/test_system_maintenance.py

import unittest
from unittest.mock import patch, MagicMock
import os
import datetime
from src import system_maintenance

class TestSystemMaintenance(unittest.TestCase):

    @patch('src.system_maintenance.subprocess.run')
    @patch('src.system_maintenance.utils.get_backup_dir')
    def test_backup_registry_success(self, mock_get_backup_dir, mock_subprocess_run):
        """Prueba que el backup del registro se ejecuta y devuelve True si tiene éxito."""
        # Configuración del mock
        mock_backup_dir = "C:\\test\\backup"
        mock_get_backup_dir.return_value = mock_backup_dir
        
        # Simular una ejecución exitosa del comando
        mock_subprocess_run.return_value = MagicMock(returncode=0, stdout="Success", stderr="")

        # Llamar a la función
        result = system_maintenance.backup_registry()

        # Verificaciones
        self.assertTrue(result)
        
        # Verificar que se llamó a get_backup_dir
        mock_get_backup_dir.assert_called_once()
        
        # Verificar que subprocess.run fue llamado con los argumentos correctos
        called_args, _ = mock_subprocess_run.call_args
        self.assertEqual(called_args[0][0], "reg")
        self.assertEqual(called_args[0][1], "export")
        self.assertEqual(called_args[0][2], "HKEY_CURRENT_USER")
        self.assertTrue(called_args[0][3].startswith(os.path.join(mock_backup_dir, "registry_backup_")))
        self.assertEqual(called_args[0][4], "/y")

    @patch('src.system_maintenance.subprocess.run')
    @patch('os.path.exists')
    def test_restore_registry_success(self, mock_os_path_exists, mock_subprocess_run):
        """Prueba que la restauración del registro se ejecuta y devuelve True si tiene éxito."""
        # Configuración del mock
        mock_backup_file = "C:\\test\\backup\\registry_backup_20230101_120000.reg"
        mock_os_path_exists.return_value = True
        mock_subprocess_run.return_value = MagicMock(returncode=0, stdout="Success", stderr="")

        # Llamar a la función
        result = system_maintenance.restore_registry(mock_backup_file)

        # Verificaciones
        self.assertTrue(result)
        mock_os_path_exists.assert_called_once_with(mock_backup_file)
        
        # Verificar que subprocess.run fue llamado con los argumentos correctos
        mock_subprocess_run.assert_called_once_with(["reg", "import", mock_backup_file], capture_output=True, text=True, check=True)

    @patch('src.system_maintenance.subprocess.run')
    def test_create_system_restore_point_success(self, mock_subprocess_run):
        """Prueba que la creación de un punto de restauración del sistema se ejecuta y devuelve True si tiene éxito."""
        # Configuración del mock
        mock_subprocess_run.return_value = MagicMock(returncode=0, stdout="Success", stderr="")

        # Llamar a la función
        description = "Punto de restauración creado por OptiTech System Optimizer"
        result = system_maintenance.create_system_restore_point(description)

        # Verificaciones
        self.assertTrue(result)
        
        # Verificar que subprocess.run fue llamado con el comando correcto de PowerShell
        expected_command = [
            "powershell.exe",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-Command",
            f"Checkpoint-Computer -Description '{description}' -RestorePointType 'MODIFY_SETTINGS'"
        ]
        mock_subprocess_run.assert_called_once_with(expected_command, capture_output=True, text=True, check=True)

    @patch('src.system_maintenance.subprocess.run')
    def test_run_sfc_success(self, mock_subprocess_run):
        """Prueba que el escaneo SFC se ejecuta y devuelve True si tiene éxito."""
        # Configuración del mock
        mock_subprocess_run.return_value = MagicMock(returncode=0, stdout="Success", stderr="")

        # Llamar a la función
        result = system_maintenance.run_sfc()

        # Verificaciones
        self.assertTrue(result)
        
        # Verificar que subprocess.run fue llamado con el comando correcto
        mock_subprocess_run.assert_called_once_with(["sfc", "/scannow"], capture_output=True, text=True, check=True)

    @patch('src.system_maintenance.subprocess.run')
    def test_run_dism_success(self, mock_subprocess_run):
        """Prueba que el escaneo DISM se ejecuta y devuelve True si tiene éxito."""
        # Configuración del mock
        mock_subprocess_run.return_value = MagicMock(returncode=0, stdout="Success", stderr="")

        # Llamar a la función
        result = system_maintenance.run_dism()

        # Verificaciones
        self.assertTrue(result)
        
        # Verificar que subprocess.run fue llamado con el comando correcto
        expected_command = ["DISM", "/Online", "/Cleanup-Image", "/RestoreHealth"]
        mock_subprocess_run.assert_called_once_with(expected_command, capture_output=True, text=True, check=True)

    @patch('src.system_maintenance.subprocess.run')
    def test_run_chkdsk_success(self, mock_subprocess_run):
        """Prueba que el escaneo CHKDSK se ejecuta y devuelve True si tiene éxito."""
        # Configuración del mock
        mock_subprocess_run.return_value = MagicMock(returncode=0, stdout="Success", stderr="")

        # Llamar a la función
        result = system_maintenance.run_chkdsk('C:')

        # Verificaciones
        self.assertTrue(result)
        
        # Verificar que subprocess.run fue llamado con el comando correcto
        expected_command = ["chkdsk", "C:", "/F", "/R"]
        mock_subprocess_run.assert_called_once_with(expected_command, capture_output=True, text=True, check=True)

