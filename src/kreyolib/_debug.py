import difflib
import os
import shutil
import sys

RESET = "\033[0m"
DIM = "\033[2m"
GREEN = "\033[92m"
RED = "\033[91m"
BG = "\033[48;5;234m"


def _colorize_line(line: str, width: int) -> str:
    if line.startswith(("+++", "+")):
        return f"{GREEN}{BG}{line.ljust(width)}{RESET}"
    if line.startswith(("---", "-")):
        return f"{RED}{BG}{line.ljust(width)}{RESET}"
    if line.startswith("@@"):
        return f"{DIM}{BG}{line.ljust(width)}{RESET}"
    return f"{BG}{line.ljust(width)}{RESET}"


def print_rich_diff(text1: str, text2: str) -> None:
    """Renders a colorized diff of two strings using ANSI escape codes."""
    diff = list(
        difflib.unified_diff(
            [line + "\n" for line in text1.splitlines()],
            [line + "\n" for line in text2.splitlines()],
            fromfile="before",
            tofile="after",
        )
    )

    if not diff:
        print(f"{DIM}No differences found.{RESET}")
        return

    if os.environ.get("NO_COLOR") or not sys.stdout.isatty():
        sys.stdout.write("".join(diff))
        return

    width = shutil.get_terminal_size().columns
    sys.stdout.write("".join(_colorize_line(line.rstrip("\n"), width) + "\n" for line in diff))
