# src/privileges.py

import sys
import os
import subprocess

# Import ctypes only if on Windows
if sys.platform == 'win32':
    import ctypes

def is_admin():
    """Checks if the current process is running with administrative privileges."""
    if sys.platform == 'win32':
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    else:
        # On non-Windows, assume not admin for testing/development purposes
        return False

def elevate(cmd_args=None):
    """Attempts to re-run the current script with administrative privileges (Windows only).

    Args:
        cmd_args (list[str] | None): Optional list of command-line arguments to pass to the
            Python executable (e.g. ['-m', 'src.main', ...]). If None, the function will
            attempt to re-run the current script file using sys.argv[0] and remaining args.
    """
    if sys.platform == 'win32':
        if not is_admin():
            try:
                if cmd_args:
                    params = subprocess.list2cmdline(cmd_args + sys.argv[1:])
                else:
                    script = os.path.abspath(sys.argv[0])
                    params = subprocess.list2cmdline([script] + sys.argv[1:])

                ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)
                sys.exit(0) # Exit the current non-elevated process
            except Exception as e:
                print(f"Error durante privilege elevation: {e}")
                sys.exit(1)
    else:
        print("Privilege elevation is a Windows-specific function. Skipping on non-Windows platform.")
        # For testing on non-Windows, we can just return or raise a specific exception
        # For now, we'll just print and return, allowing tests to proceed without SystemExit
        return

