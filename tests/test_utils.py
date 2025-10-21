# tests/test_utils.py

import unittest
from unittest.mock import patch, call
import io
import sys
from src import utils

class TestUtils(unittest.TestCase):

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_show_header(self, mock_stdout):
        utils.show_header("Test Header", screen_width=20)
        expected_output = (
            "====================\n"
            "    Test Header     \n"
            "====================\n\n"
        )
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    @patch('builtins.input', side_effect=['y'])
    def test_confirm_operation_yes(self, mock_input):
        self.assertTrue(utils.confirm_operation("Proceed?"))

    @patch('builtins.input', side_effect=['n'])
    def test_confirm_operation_no(self, mock_input):
        self.assertFalse(utils.confirm_operation("Proceed?"))

    @patch('builtins.input', side_effect=['yes'])
    def test_confirm_operation_yes_long(self, mock_input):
        self.assertTrue(utils.confirm_operation("Proceed?"))

    @patch('builtins.input', side_effect=['no'])
    def test_confirm_operation_no_long(self, mock_input):
        self.assertFalse(utils.confirm_operation("Proceed?"))

    @patch('builtins.input', side_effect=['invalid', 'y'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_confirm_operation_invalid_then_yes(self, mock_stdout, mock_input):
        result = utils.confirm_operation("Proceed?")
        self.assertTrue(result)
        self.assertIn("Invalid input", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_show_progress_bar(self, mock_stdout):
        total = 100
        utils.show_progress_bar(0, total, prefix='Progress:', suffix='Complete', length=10)
        self.assertIn('\rProgress: |----------| 0.0% Complete', mock_stdout.getvalue())

        mock_stdout.seek(0)
        mock_stdout.truncate(0)

        utils.show_progress_bar(50, total, prefix='Progress:', suffix='Complete', length=10)
        self.assertIn('\rProgress: |█████-----| 50.0% Complete', mock_stdout.getvalue())

        mock_stdout.seek(0)
        mock_stdout.truncate(0)

        utils.show_progress_bar(100, total, prefix='Progress:', suffix='Complete', length=10)
        # The final output includes a newline
        self.assertIn('\rProgress: |██████████| 100.0% Complete', mock_stdout.getvalue())
        self.assertTrue(mock_stdout.getvalue().endswith('\n'))


if __name__ == '__main__':
    unittest.main()
