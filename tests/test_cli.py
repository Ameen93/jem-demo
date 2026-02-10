"""Tests for CLI module with Rich formatting (Stories 6.1-6.3)."""

from io import StringIO
from unittest.mock import MagicMock, patch

from rich.console import Console


class TestCLIModule:
    """Tests for CLI display functions (Story 6.1)."""

    def test_console_initializes(self):
        """Rich Console initializes without errors."""
        from src.cli.display import get_console

        console = get_console()
        assert isinstance(console, Console)

    def test_display_welcome_banner(self):
        """Welcome banner renders without crash."""
        from src.cli.display import display_welcome_banner

        buf = StringIO()
        console = Console(file=buf, force_terminal=True, width=80)
        display_welcome_banner(console)
        output = buf.getvalue()
        assert "Jem HR" in output

    def test_display_employee_info(self):
        """Employee info displays in a formatted table."""
        from src.cli.display import display_employee_info

        employee = {
            "id": "EMP001",
            "name": "Sipho Dlamini",
            "department": "Retail - Checkers Sandton",
            "role": "Sales Assistant",
            "hire_date": "2024-03-15",
            "hourly_rate": 48.50,
            "preferred_language": "zu",
            "employment_status": "active",
        }
        buf = StringIO()
        console = Console(file=buf, force_terminal=True, width=80)
        display_employee_info(console, employee)
        output = buf.getvalue()
        assert "Sipho Dlamini" in output
        assert "EMP001" in output

    def test_display_response(self):
        """Response displays in a Rich Panel."""
        from src.cli.display import display_response

        buf = StringIO()
        console = Console(file=buf, force_terminal=True, width=80)
        display_response(console, "You have 12 annual leave days.", "hr_agent")
        output = buf.getvalue()
        assert "12 annual leave days" in output

    def test_display_response_with_error(self):
        """Error response displays gracefully."""
        from src.cli.display import display_response

        buf = StringIO()
        console = Console(file=buf, force_terminal=True, width=80)
        display_response(console, "Sorry, something went wrong.", "error")
        output = buf.getvalue()
        assert "something went wrong" in output


class TestEmployeeSelection:
    """Tests for employee selection flow (Story 6.2)."""

    def test_display_employee_list(self):
        """All employees display in a selection table."""
        from src.cli.display import display_employee_list

        employees = [
            {"id": "EMP001", "name": "Sipho Dlamini", "department": "Retail", "role": "Sales Assistant"},
            {"id": "EMP002", "name": "Thandiwe Nkosi", "department": "Security", "role": "Security Officer"},
        ]
        buf = StringIO()
        console = Console(file=buf, force_terminal=True, width=100)
        display_employee_list(console, employees)
        output = buf.getvalue()
        assert "Sipho Dlamini" in output
        assert "Thandiwe Nkosi" in output

    @patch("src.cli.demo.get_session")
    def test_load_all_employees(self, mock_session_ctx):
        """load_all_employees returns employee dicts from DB."""
        from src.cli.demo import load_all_employees

        mock_session = MagicMock()
        mock_session_ctx.return_value.__enter__ = MagicMock(return_value=mock_session)
        mock_session_ctx.return_value.__exit__ = MagicMock(return_value=False)

        mock_emp = MagicMock()
        mock_emp.to_dict.return_value = {"id": "EMP001", "name": "Sipho"}
        mock_session.query.return_value.all.return_value = [mock_emp]

        result = load_all_employees()
        assert len(result) == 1
        assert result[0]["id"] == "EMP001"


class TestConversationLoop:
    """Tests for conversation loop (Story 6.3)."""

    def test_exit_command_handling(self):
        """'exit' command is recognized as quit signal."""
        from src.cli.demo import is_exit_command

        assert is_exit_command("exit") is True
        assert is_exit_command("quit") is True
        assert is_exit_command("EXIT") is True
        assert is_exit_command("What is my leave?") is False

    def test_display_routing_info(self):
        """Routing info shows which agent handled the request."""
        from src.cli.display import display_routing_info

        buf = StringIO()
        console = Console(file=buf, force_terminal=True, width=80)
        display_routing_info(console, "zu", "hr_query")
        output = buf.getvalue()
        assert "hr_query" in output or "HR" in output
