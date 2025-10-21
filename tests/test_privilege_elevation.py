import unittest
import sys
import os
from src import privileges

class TestPrivilegeElevation(unittest.TestCase):

    def setUp(self):
        self.privilege_checker = privileges

    def test_is_not_admin_initially(self):
        # On non-Windows, or if not admin, this should be False
        self.assertFalse(self.privilege_checker.is_admin(), "Expected to not be admin initially on non-Windows or non-elevated")

if __name__ == '__main__':
    unittest.main()
