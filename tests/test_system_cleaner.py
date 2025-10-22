# tests/test_system_cleaner.py

import unittest
from unittest.mock import patch, MagicMock, call
from src import system_cleaner
import os

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

if __name__ == '__main__':
    unittest.main()
