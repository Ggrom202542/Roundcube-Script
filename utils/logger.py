
"""
Console Logger
"""

from datetime import datetime


class ConsoleColor:
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    RESET = "\033[0m"


def log_info(message: str):
    print(
        f"{ConsoleColor.BLUE}"
        f"[INFO]"
        f"{ConsoleColor.RESET} "
        f"{datetime.now()} - {message}"
    )


def log_success(message: str):
    print(
        f"{ConsoleColor.GREEN}"
        f"[SUCCESS]"
        f"{ConsoleColor.RESET} "
        f"{datetime.now()} - {message}"
    )


def log_warning(message: str):
    print(
        f"{ConsoleColor.YELLOW}"
        f"[WARNING]"
        f"{ConsoleColor.RESET} "
        f"{datetime.now()} - {message}"
    )


def log_error(message: str):
    print(
        f"{ConsoleColor.RED}"
        f"[ERROR]"
        f"{ConsoleColor.RESET} "
        f"{datetime.now()} - {message}"
    )
