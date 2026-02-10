"""Rich display functions for Jem HR Demo CLI."""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

_console: Console | None = None

LANGUAGE_NAMES = {
    "en": "English",
    "zu": "isiZulu",
    "xh": "isiXhosa",
    "af": "Afrikaans",
    "nso": "Sepedi",
    "st": "Sesotho",
}

INTENT_LABELS = {
    "hr_query": "HR Agent",
    "ewa_request": "EWA Agent",
    "policy_question": "Policy RAG",
}


def get_console() -> Console:
    """Get or create the Rich Console singleton."""
    global _console
    if _console is None:
        _console = Console()
    return _console


def display_welcome_banner(console: Console) -> None:
    """Display the welcome banner."""
    console.print(
        Panel(
            "[bold cyan]Jem HR[/bold cyan] — Intelligent HR Assistant Demo\n"
            "[dim]MCP Server • LangGraph • RAG • Multi-Language[/dim]",
            title="[bold white]Welcome[/bold white]",
            border_style="cyan",
        )
    )


def display_employee_list(console: Console, employees: list[dict]) -> None:
    """Display employee selection table."""
    table = Table(title="Select an Employee", border_style="cyan")
    table.add_column("#", style="bold", width=4)
    table.add_column("ID", style="dim")
    table.add_column("Name", style="bold")
    table.add_column("Department")
    table.add_column("Role")

    for i, emp in enumerate(employees, 1):
        table.add_row(
            str(i),
            emp["id"],
            emp["name"],
            emp["department"],
            emp["role"],
        )
    console.print(table)


def display_employee_info(console: Console, employee: dict) -> None:
    """Display selected employee profile."""
    table = Table(show_header=False, border_style="green", padding=(0, 2))
    table.add_column("Field", style="bold")
    table.add_column("Value")

    table.add_row("ID", employee["id"])
    table.add_row("Name", employee["name"])
    table.add_row("Department", employee["department"])
    table.add_row("Role", employee["role"])
    table.add_row("Hire Date", employee.get("hire_date", "N/A"))
    table.add_row("Hourly Rate", f"R{employee.get('hourly_rate', 0):.2f}")
    table.add_row("Language", LANGUAGE_NAMES.get(employee.get("preferred_language", "en"), "English"))
    table.add_row("Status", employee.get("employment_status", "N/A"))

    console.print(Panel(table, title=f"[bold]{employee['name']}[/bold]", border_style="green"))


def display_routing_info(console: Console, language: str, intent: str) -> None:
    """Display routing information for demo visibility."""
    lang_name = LANGUAGE_NAMES.get(language, language)
    intent_label = INTENT_LABELS.get(intent, intent)
    console.print(
        f"  [dim]Language: {lang_name} | Routed to: {intent_label}[/dim]"
    )


def display_response(console: Console, response: str, intent: str) -> None:
    """Display agent response in a Rich Panel."""
    if intent == "error":
        style = "red"
        title = "Error"
    else:
        style = "blue"
        title = INTENT_LABELS.get(intent, "Response")

    console.print(Panel(response, title=f"[bold]{title}[/bold]", border_style=style))
