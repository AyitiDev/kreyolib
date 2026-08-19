import difflib
from rich.console import Console
from rich.syntax import Syntax


def print_rich_diff(text1: str, text2: str, theme: str = "monokai") -> None:
    """Renders a colorized diff of two strings using Rich's diff lexer."""
    console = Console()
    
    # Ensure lines end with newlines for unified_diff
    lines1 = [line + "\n" for line in text1.splitlines()]
    lines2 = [line + "\n" for line in text2.splitlines()]
    
    diff_generator = difflib.unified_diff(
        lines1,
        lines2,
        fromfile="before",
        tofile="after",
    )
    diff_text = "".join(diff_generator)
    
    if not diff_text:
        console.print("[dim]No differences found.[/dim]")
        return

    syntax_diff = Syntax(diff_text, "diff", theme=theme, line_numbers=False)
    console.print(syntax_diff)
