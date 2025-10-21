import unittest
import sys
import os
from src import privileges

class TestPrivilegeElevation(unittest.TestCase):

    def setUp(self):
        self.privilege_checker = privileges

    def test_is_not_admin_initially(self):
        # Esta prueba debería pasar si no se ejecuta como administrador en Windows, o en un sistema que no sea Windows
        if sys.platform == 'win32' and self.privilege_checker.is_admin():
            self.skipTest("Saltando test_is_not_admin_initially ya que se está ejecutando como administrador en Windows")
        self.assertFalse(self.privilege_checker.is_admin(), "Se esperaba no ser administrador inicialmente en un sistema que no sea Windows o no elevado")

    def test_is_admin_after_elevation_attempt(self):
        # Esta prueba asume que se ejecuta *después* de que se haya intentado una elevación,
        # o que se ejecuta en un contexto ya elevado en Windows.
        if sys.platform == 'win32':
            # Si estamos en Windows, y esta prueba se está ejecutando, esperamos que is_admin() sea True
            # si la elevación fue exitosa.
            self.assertTrue(self.privilege_checker.is_admin(), "Se esperaba ser administrador después de un intento de elevación exitoso en Windows")
        else:
            self.skipTest("Saltando test_is_admin_after_elevation_attempt en una plataforma que no sea Windows")

if __name__ == '__main__':
    unittest.main()