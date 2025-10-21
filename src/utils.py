# src/utils.py

import sys
import time

def show_header(text, screen_width=80):
    """
    Displays a centered header with a decorative border.

    Args:
        text (str): The text to display in the header.
        screen_width (int): The width of the header in characters.
    """
    print("=" * screen_width)
    print(text.center(screen_width))
    print("=" * screen_width)
    print() # Add a blank line for spacing

def confirm_operation(prompt):
    """
    Asks the user for confirmation (Y/N) and returns a boolean.

    Args:
        prompt (str): The question to ask the user.

    Returns:
        bool: True if the user confirms, False otherwise.
    """
    while True:
        response = input(f"{prompt} [y/n]: ").lower().strip()
        if response in ['y', 'yes']:
            return True
        elif response in ['n', 'no']:
            return False
        else:
            print("Invalid input. Please enter 'y' or 'n'.")

def show_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=50, fill='█'):
    """
    Displays a progress bar in the console.

    Args:
        iteration (int): current iteration.
        total (int): total iterations.
        prefix (str): prefix string.
        suffix (str): suffix string.
        decimals (int): positive number of decimals in percent complete.
        length (int): character length of bar.
        fill (str): bar fill character.
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // float(total))
    bar = fill * filled_length + '-' * (length - filled_length)
    sys.stdout.write(f'\r{prefix} |{bar}| {percent}% {suffix}')
    sys.stdout.flush()
    if iteration == total:
        sys.stdout.write('\n')
        sys.stdout.flush()

