"""Main demo runner for Jem HR Demo CLI."""

import logging
import os
import sys

logging.basicConfig(
    level=os.environ.get("LOG_LEVEL", "INFO").upper(),
    format="%(levelname)s: %(message)s",
)

from rich.console import Console
from rich.prompt import IntPrompt, Prompt

from src.agents.graph import build_graph
from src.agents.state import create_initial_state
from src.cli.display import (
    display_employee_info,
    display_employee_list,
    display_response,
    display_routing_info,
    display_welcome_banner,
    get_console,
)
from src.db import Employee, get_session
from src.db.seed import seed_database

logger = logging.getLogger(__name__)

EXIT_COMMANDS = {"exit", "quit", "q", "bye"}


def is_exit_command(text: str) -> bool:
    """Check if the user wants to exit."""
    return text.strip().lower() in EXIT_COMMANDS


def load_all_employees() -> list[dict]:
    """Load all employees from the database."""
    with get_session() as session:
        employees = session.query(Employee).all()
        return [emp.to_dict() for emp in employees]


def ensure_database_ready() -> None:
    """Ensure database is seeded on first run."""
    with get_session() as session:
        count = session.query(Employee).count()
        if count == 0:
            seed_database(session)


def select_employee(console: Console, employees: list[dict]) -> dict | None:
    """Prompt user to select an employee."""
    display_employee_list(console, employees)
    console.print()
    while True:
        try:
            choice = IntPrompt.ask(
                "[bold cyan]Select employee number[/bold cyan]",
                console=console,
            )
            if 1 <= choice <= len(employees):
                return employees[choice - 1]
            console.print(f"[red]Invalid selection. Please enter 1-{len(employees)}.[/red]")
        except (KeyboardInterrupt, EOFError):
            return None


def run_conversation(console: Console, employee: dict, graph) -> None:
    """Run the conversation loop."""
    display_employee_info(console, employee)
    console.print("\n[dim]Type your question, or 'exit' to quit.[/dim]\n")

    while True:
        try:
            user_input = Prompt.ask("[bold green]You[/bold green]", console=console)
        except (KeyboardInterrupt, EOFError):
            break

        if is_exit_command(user_input):
            console.print("[dim]Goodbye![/dim]")
            break

        if not user_input.strip():
            continue

        try:
            state = create_initial_state(employee["id"], user_input)
            result = graph.invoke(state)
            language = result.get("language", "en")
            intent = result.get("intent", "unknown")
            response = result.get("response", "")
            error = result.get("error")

            display_routing_info(console, language, intent)

            if error:
                display_response(console, error, "error")
            elif response:
                display_response(console, response, intent)
            else:
                display_response(console, "No response generated.", "error")
        except Exception:
            logger.exception("Error processing message")
            display_response(console, "Sorry, something went wrong. Please try again.", "error")


def main() -> None:
    """Entry point for the demo CLI."""
    console = get_console()
    display_welcome_banner(console)
    console.print()

    # Ensure database is ready
    ensure_database_ready()

    # Build LangGraph
    graph = build_graph()

    # Load employees
    employees = load_all_employees()
    if not employees:
        console.print("[red]No employees found in database.[/red]")
        sys.exit(1)

    # Select employee
    employee = select_employee(console, employees)
    if employee is None:
        sys.exit(0)

    # Run conversation
    run_conversation(console, employee, graph)


if __name__ == "__main__":
    main()
