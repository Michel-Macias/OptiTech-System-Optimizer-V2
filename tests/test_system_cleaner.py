# tests/test_system_cleaner.py

import unittest
from unittest.mock import patch, MagicMock, call
from src import system_cleaner
import os
import winshell
import subprocess

class TestSystemCleaner(unittest.TestCase):

    @patch('os.path.getsize')
    @patch('os.remove')
    @patch('os.walk')
    @patch('os.path.exists', return_value=True)
    @patch('src.system_cleaner.CLEANUP_PATHS', {
        'basico': ['/mock/temp'],
        'extendido': ['/mock/prefetch'],
        'avanzado': []
    })
    def test_limpiar_archivos_temporales_informe(self, mock_exists, mock_walk, mock_remove, mock_getsize):
        """Prueba que el modo informe calcula el tamaño pero no elimina archivos."""
        # Mock del sistema de archivos
        mock_walk.return_value = [('/mock/temp', ('subdir',), ('file1.tmp', 'file2.log'))]
        mock_getsize.return_value = 1024 # 1 KB por archivo

        total_eliminado, archivos_eliminados = system_cleaner.limpiar_archivos_temporales(nivel='basico', modo_informe=True)

        self.assertEqual(archivos_eliminados, 2)
        self.assertEqual(total_eliminado, 2048)
        mock_remove.assert_not_called() # Verificar que no se llamó a os.remove

    @patch('os.path.getsize')
    @patch('os.remove')
    @patch('os.walk')
    @patch('os.path.exists', return_value=True)
    @patch('src.system_cleaner.CLEANUP_PATHS', {
        'basico': ['/mock/temp'],
        'extendido': ['/mock/prefetch'],
        'avanzado': []
    })
    def test_limpiar_archivos_temporales_eliminacion(self, mock_exists, mock_walk, mock_remove, mock_getsize):
        """Prueba que el modo de eliminación llama a os.remove."""
        mock_walk.return_value = [('/mock/temp', (), ('file1.tmp',))]
        mock_getsize.return_value = 512

        total_eliminado, archivos_eliminados = system_cleaner.limpiar_archivos_temporales(nivel='basico', modo_informe=False)

        self.assertEqual(archivos_eliminados, 1)
        self.assertEqual(total_eliminado, 512)
        mock_remove.assert_called_once_with(os.path.join('/mock/temp', 'file1.tmp'))

    @patch('os.path.getsize')
    @patch('os.remove')
    @patch('os.walk')
    @patch('os.path.exists', return_value=True)
    @patch('src.system_cleaner.CLEANUP_PATHS', {
        'basico': ['/mock/temp'],
        'extendido': ['/mock/prefetch'],
        'avanzado': []
    })
    def test_niveles_de_limpieza(self, mock_exists, mock_walk, mock_remove, mock_getsize):
        """Prueba que el nivel 'extendido' incluye las rutas del nivel 'basico'."""
        # Simular dos rutas con un archivo cada una
        mock_walk.side_effect = [
            [('/mock/temp', (), ('file1.tmp',))],
            [('/mock/prefetch', (), ('file2.pf',))]
        ]
        mock_getsize.return_value = 1000

        total_eliminado, archivos_eliminados = system_cleaner.limpiar_archivos_temporales(nivel='extendido', modo_informe=True)

        self.assertEqual(archivos_eliminados, 2)
        self.assertEqual(total_eliminado, 2000)
        # Verificar que se procesaron ambas rutas
        self.assertEqual(mock_walk.call_count, 2)
        mock_walk.assert_has_calls([call('/mock/temp'), call('/mock/prefetch')])

    @patch('os.path.getsize', return_value=1)
    @patch('os.remove', side_effect=PermissionError)
    @patch('os.walk')
    @patch('os.path.exists', return_value=True)
    @patch('src.system_cleaner.CLEANUP_PATHS', {
        'basico': ['/mock/locked_dir'],
        'extendido': [],
        'avanzado': []
    })
    def test_manejo_permission_error(self, mock_exists, mock_walk, mock_remove, mock_getsize):
        """Prueba que la limpieza continúa a pesar de un PermissionError."""
        mock_walk.return_value = [('/mock/locked_dir', (), ('locked_file.lck',))]

        # La función debería capturar la excepción y no relanzarla
        total_eliminado, archivos_eliminados = system_cleaner.limpiar_archivos_temporales(nivel='basico', modo_informe=False)

        # No se eliminó nada, pero el programa no se detuvo
        self.assertEqual(archivos_eliminados, 0)
        self.assertEqual(total_eliminado, 0)
        mock_remove.assert_called_once()

    @patch('winshell.recycle_bin')
    @patch('builtins.print')
    def test_limpiar_papelera_reciclaje_seguro_exito(self, mock_print, mock_recycle_bin):
        """Prueba la limpieza exitosa de la papelera de reciclaje."""
        mock_recycle_bin_instance = MagicMock()
        mock_recycle_bin.return_value = mock_recycle_bin_instance
        mock_recycle_bin_instance.__iter__.return_value = iter([MagicMock()]) # Simular que no está vacía

        resultado = system_cleaner.limpiar_papelera_reciclaje_seguro()

        self.assertTrue(resultado)
        mock_recycle_bin_instance.empty.assert_called_once_with(confirm=False, show_progress=True, sound=False)
        mock_print.assert_any_call("La papelera de reciclaje ha sido vaciada con éxito.")

    @patch('winshell.recycle_bin')
    @patch('builtins.print')
    def test_limpiar_papelera_reciclaje_seguro_ya_vacia(self, mock_print, mock_recycle_bin):
        """Prueba cuando la papelera de reciclaje ya está vacía."""
        mock_recycle_bin_instance = MagicMock()
        mock_recycle_bin.return_value = mock_recycle_bin_instance
        mock_recycle_bin_instance.__iter__.return_value = iter([]) # Simular que está vacía

        resultado = system_cleaner.limpiar_papelera_reciclaje_seguro()

        self.assertTrue(resultado)
        mock_recycle_bin_instance.empty.assert_not_called()
        mock_print.assert_any_call("La papelera de reciclaje ya está vacía.")

    @patch('winshell.recycle_bin')
    @patch('builtins.print')
    def test_limpiar_papelera_reciclaje_seguro_error(self, mock_print, mock_recycle_bin):
        """Prueba el manejo de errores al vaciar la papelera de reciclaje."""
        mock_recycle_bin_instance = MagicMock()
        mock_recycle_bin.return_value = mock_recycle_bin_instance
        mock_recycle_bin_instance.__iter__.return_value = iter([MagicMock()]) # Simular que no está vacía
        mock_recycle_bin_instance.empty.side_effect = Exception("Error de prueba")

        resultado = system_cleaner.limpiar_papelera_reciclaje_seguro()

        self.assertFalse(resultado)
        mock_print.assert_any_call("Error al vaciar la papelera de reciclaje: Error de prueba")

    @patch('subprocess.run')
    @patch('builtins.print')
    def test_limpiar_winsxs_exito(self, mock_print, mock_subprocess_run):
        """Prueba la limpieza exitosa de WinSxS."""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "Limpieza de componentes completada."
        mock_subprocess_run.return_value = mock_result

        resultado = system_cleaner.limpiar_winsxs()

        self.assertTrue(resultado)
        mock_subprocess_run.assert_called_once_with(
            ["Dism.exe", "/online", "/Cleanup-Image", "/StartComponentCleanup"],
            capture_output=True, text=True, check=True, shell=True
        )
        mock_print.assert_any_call("Limpieza de WinSxS completada con éxito.")

    @patch('subprocess.run', side_effect=subprocess.CalledProcessError(1, 'Dism.exe', stderr="Error de DISM"))
    @patch('builtins.print')
    def test_limpiar_winsxs_error_proceso(self, mock_print, mock_subprocess_run):
        """Prueba el manejo de errores de proceso al limpiar WinSxS."""
        resultado = system_cleaner.limpiar_winsxs()

        self.assertFalse(resultado)
        mock_print.assert_any_call("Error al limpiar WinSxS: Error de DISM")

    @patch('subprocess.run', side_effect=Exception("Error inesperado"))
    @patch('builtins.print')
    def test_limpiar_winsxs_error_inesperado(self, mock_print, mock_subprocess_run):
        """Prueba el manejo de errores inesperados al limpiar WinSxS."""
        resultado = system_cleaner.limpiar_winsxs()

        self.assertFalse(resultado)
        mock_print.assert_any_call("Error inesperado al limpiar WinSxS: Error inesperado")

    @patch('src.system_cleaner.is_admin', return_value=True)
    @patch('subprocess.run')
    @patch('builtins.print')
    def test_limpiar_copias_sombra_exito(self, mock_print, mock_subprocess_run, mock_is_admin):
        """Prueba la eliminación exitosa de copias de sombra."""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "Copias de sombra eliminadas."
        mock_subprocess_run.return_value = mock_result

        resultado = system_cleaner.limpiar_copias_sombra()

        self.assertTrue(resultado)
        mock_subprocess_run.assert_called_once_with(
            ["vssadmin", "delete", "shadows", "/all", "/quiet"],
            capture_output=True, text=True, check=False, shell=True
        )
        mock_print.assert_any_call("Eliminación de copias de sombra completada con éxito.")

    @patch('src.system_cleaner.is_admin', return_value=True)
    @patch('subprocess.run')
    @patch('builtins.print')
    def test_limpiar_copias_sombra_error_proceso(self, mock_print, mock_subprocess_run, mock_is_admin):
        """Prueba el manejo de errores de proceso al eliminar copias de sombra."""
        mock_result = MagicMock()
        mock_result.returncode = 1 # Simula un error
        mock_result.stdout = "" # Simula stdout vacío
        mock_result.stderr = "Error de vssadmin" # Simula stderr
        mock_subprocess_run.return_value = mock_result

        resultado = system_cleaner.limpiar_copias_sombra()

        self.assertFalse(resultado)
        mock_subprocess_run.assert_called_once_with(
            ["vssadmin", "delete", "shadows", "/all", "/quiet"],
            capture_output=True, text=True, check=False, shell=True
        )
        mock_print.assert_any_call("Error al eliminar copias de sombra. Mensaje de vssadmin: Error de vssadmin")

    @patch('src.system_cleaner.is_admin', return_value=True)
    @patch('subprocess.run', side_effect=Exception("Error inesperado"))
    @patch('builtins.print')
    def test_limpiar_copias_sombra_error_inesperado(self, mock_print, mock_subprocess_run, mock_is_admin):
        """Prueba el manejo de errores inesperados al eliminar copias de sombra."""
        resultado = system_cleaner.limpiar_copias_sombra()

        self.assertFalse(resultado)
        mock_print.assert_any_call("Error inesperado al eliminar copias de sombra: Error inesperado")

    @patch('builtins.input', side_effect=['1', 'n', 'y', '0']) # Selecciona limpieza básica, no modo informe, confirma, luego sale
    @patch('builtins.print')
    @patch('src.system_cleaner.limpiar_archivos_temporales', return_value=(1024, 1))
    @patch('src.system_cleaner.limpiar_papelera_reciclaje_seguro')
    @patch('src.system_cleaner.limpiar_winsxs')
    @patch('src.system_cleaner.limpiar_copias_sombra')
    @patch('src.utils.show_header')
    @patch('src.utils.confirm_operation', side_effect=[False, True]) # No modo informe, luego confirma la eliminación
    def test_ejecutar_limpiador_flujo_basico(self, mock_confirm_operation, mock_show_header, mock_limpiar_copias_sombra, mock_limpiar_winsxs, mock_limpiar_papelera_reciclaje_seguro, mock_limpiar_archivos_temporales, mock_print, mock_input):
        """Prueba un flujo básico de interacción con el menú del limpiador."""
        system_cleaner.ejecutar_limpiador()

        mock_show_header.assert_called_once_with("Módulo de Limpieza del Sistema")
        mock_limpiar_archivos_temporales.assert_called_once_with(nivel='basico', modo_informe=False)
        mock_limpiar_papelera_reciclaje_seguro.assert_not_called()
        mock_limpiar_winsxs.assert_not_called()
        mock_limpiar_copias_sombra.assert_not_called()
        mock_print.assert_any_call("\nSeleccione una opción de limpieza:")
        mock_print.assert_any_call("Limpieza completada. Total de archivos procesados para eliminación: 1. Espacio total recuperado: 0.00 MB.")

    @patch('builtins.input', side_effect=['3', 'y', '0']) # Selecciona papelera, confirma, luego sale
    @patch('builtins.print')
    @patch('src.system_cleaner.limpiar_archivos_temporales')
    @patch('src.system_cleaner.limpiar_papelera_reciclaje_seguro', return_value=True)
    @patch('src.system_cleaner.limpiar_winsxs')
    @patch('src.system_cleaner.limpiar_copias_sombra')
    @patch('src.utils.show_header')
    @patch('src.utils.confirm_operation', return_value=True) # Confirma la operación
    def test_ejecutar_limpiador_papelera(self, mock_confirm_operation, mock_show_header, mock_limpiar_copias_sombra, mock_limpiar_winsxs, mock_limpiar_papelera_reciclaje_seguro, mock_limpiar_archivos_temporales, mock_print, mock_input):
        """Prueba la opción de vaciar la papelera de reciclaje."""
        system_cleaner.ejecutar_limpiador()

        mock_limpiar_papelera_reciclaje_seguro.assert_called_once_with(confirmar=False, mostrar_progreso=True, sonido=False)
        mock_limpiar_archivos_temporales.assert_not_called()

    @patch('builtins.input', side_effect=['6', '0']) # Opción no válida, luego sale
    @patch('builtins.print')
    @patch('src.utils.show_header')
    def test_ejecutar_limpiador_opcion_invalida(self, mock_show_header, mock_print, mock_input):
        """Prueba la selección de una opción no válida."""
        system_cleaner.ejecutar_limpiador()

        mock_print.assert_any_call("Opción no válida. Por favor, intente de nuevo.")

if __name__ == '__main__':
    unittest.main()
