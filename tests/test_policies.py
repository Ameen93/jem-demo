"""Tests for policy documents and RAG indexing."""

from pathlib import Path

POLICY_DIR = Path(__file__).parent.parent / "data" / "policies"


class TestPolicyDocuments:
    """Tests for policy document content (Story 4.1)."""

    def test_leave_policy_exists(self):
        """Leave policy file exists and is non-empty."""
        path = POLICY_DIR / "leave_policy.md"
        assert path.exists()
        assert path.stat().st_size > 0

    def test_ewa_policy_exists(self):
        """EWA policy file exists and is non-empty."""
        path = POLICY_DIR / "ewa_policy.md"
        assert path.exists()
        assert path.stat().st_size > 0

    def test_leave_policy_sections(self):
        """Leave policy contains required sections."""
        content = (POLICY_DIR / "leave_policy.md").read_text()
        assert "Annual Leave" in content
        assert "Sick Leave" in content
        assert "Family Responsibility Leave" in content

    def test_ewa_policy_sections(self):
        """EWA policy contains required sections."""
        content = (POLICY_DIR / "ewa_policy.md").read_text()
        assert "Eligibility" in content
        assert "Limits" in content
        assert "Fees" in content
        assert "Repayment" in content

    def test_leave_policy_contains_rules(self):
        """Leave policy mentions key rules."""
        content = (POLICY_DIR / "leave_policy.md").read_text()
        assert "15 working days" in content
        assert "medical certificate" in content.lower()

    def test_ewa_policy_contains_rules(self):
        """EWA policy mentions key business rules."""
        content = (POLICY_DIR / "ewa_policy.md").read_text()
        assert "50%" in content
        assert "R5,000" in content
        assert "R10" in content
        assert "3-month probation" in content or "3 months" in content
