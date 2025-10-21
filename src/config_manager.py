# src/config_manager.py

import os

APP_NAME = "OptiTechOptimizer"
DEFAULT_ENCODING = "utf-8"

def _get_base_app_data_path():
    r"""Returns the base application data path (e.g., %LOCALAPPDATA%\OptiTechOptimizer)."""
    local_app_data = os.path.expandvars('%LOCALAPPDATA%')
    return os.path.join(local_app_data, APP_NAME)

def _create_directory_if_not_exists(path):
    """Creates a directory if it does not exist."""
    os.makedirs(path, exist_ok=True)

class ConfigManager:
    def __init__(self):
        self._app_data_path = _get_base_app_data_path()
        self._log_path = os.path.join(self._app_data_path, "logs")
        self._backup_path = os.path.join(self._app_data_path, "backups")
        self._report_path = os.path.join(self._app_data_path, "reports")

        # Ensure directories exist upon initialization
        _create_directory_if_not_exists(self._app_data_path)
        _create_directory_if_not_exists(self._log_path)
        _create_directory_if_not_exists(self._backup_path)
        _create_directory_if_not_exists(self._report_path)

    def get_app_data_path(self):
        return self._app_data_path

    def get_log_path(self):
        return self._log_path

    def get_backup_path(self):
        return self._backup_path

    def get_report_path(self):
        return self._report_path

    def get_default_encoding(self):
        return DEFAULT_ENCODING

# Instantiate ConfigManager once to ensure directories are created when module is imported
config_manager_instance = ConfigManager()

# Expose functions for direct access if preferred, or just use the instance
def get_app_data_path():
    return config_manager_instance.get_app_data_path()

def get_log_path():
    return config_manager_instance.get_log_path()

def get_backup_path():
    return config_manager_instance.get_backup_path()

def get_report_path():
    return config_manager_instance.get_report_path()

def get_default_encoding():
    return config_manager_instance.get_default_encoding()
