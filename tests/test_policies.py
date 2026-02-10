"""Tests for policy documents, RAG indexing, and search_policies tool."""

import tempfile
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


class TestPolicyIndexing:
    """Tests for ChromaDB policy indexing (Story 4.2)."""

    def test_index_policies_creates_collection(self):
        """Indexing creates a ChromaDB collection with documents."""
        from src.rag.vectorstore import get_collection, index_policies

        with tempfile.TemporaryDirectory() as tmpdir:
            collection = get_collection(persist_dir=tmpdir)
            index_policies(collection)
            assert collection.count() > 0

    def test_index_policies_stores_both_documents(self):
        """Both leave and EWA policies are indexed."""
        from src.rag.vectorstore import get_collection, index_policies

        with tempfile.TemporaryDirectory() as tmpdir:
            collection = get_collection(persist_dir=tmpdir)
            index_policies(collection)
            results = collection.get()
            sources = set(m["source"] for m in results["metadatas"])
            assert "leave_policy.md" in sources
            assert "ewa_policy.md" in sources

    def test_index_policies_has_sections(self):
        """Indexed documents have section metadata."""
        from src.rag.vectorstore import get_collection, index_policies

        with tempfile.TemporaryDirectory() as tmpdir:
            collection = get_collection(persist_dir=tmpdir)
            index_policies(collection)
            results = collection.get()
            sections = [m.get("section") for m in results["metadatas"]]
            assert any(s for s in sections if s)

    def test_index_policies_idempotent(self):
        """Running index_policies twice doesn't duplicate."""
        from src.rag.vectorstore import get_collection, index_policies

        with tempfile.TemporaryDirectory() as tmpdir:
            collection = get_collection(persist_dir=tmpdir)
            index_policies(collection)
            count1 = collection.count()
            index_policies(collection)
            count2 = collection.count()
            assert count1 == count2


class TestSearchPolicies:
    """Tests for search_policies MCP tool (Story 4.3)."""

    def test_search_returns_relevant_results(self):
        """Searching for sick leave returns relevant content."""
        from src.mcp_server.tools.policy_tools import search_policies
        from src.rag.vectorstore import get_collection, index_policies

        with tempfile.TemporaryDirectory() as tmpdir:
            collection = get_collection(persist_dir=tmpdir)
            index_policies(collection)
            result = search_policies(
                "How many sick days without a doctor's note?",
                collection=collection,
            )
            assert result["success"] is True
            results = result["data"]["results"]
            assert len(results) > 0
            # Should find sick leave content
            combined = " ".join(r["text"] for r in results).lower()
            assert "sick" in combined

    def test_search_includes_citations(self):
        """Search results include source citations."""
        from src.mcp_server.tools.policy_tools import search_policies
        from src.rag.vectorstore import get_collection, index_policies

        with tempfile.TemporaryDirectory() as tmpdir:
            collection = get_collection(persist_dir=tmpdir)
            index_policies(collection)
            result = search_policies("annual leave", collection=collection)
            results = result["data"]["results"]
            for r in results:
                assert "source" in r

    def test_search_ewa_policy(self):
        """Searching for EWA returns EWA policy content."""
        from src.mcp_server.tools.policy_tools import search_policies
        from src.rag.vectorstore import get_collection, index_policies

        with tempfile.TemporaryDirectory() as tmpdir:
            collection = get_collection(persist_dir=tmpdir)
            index_policies(collection)
            result = search_policies("EWA eligibility", collection=collection)
            assert result["success"] is True
            combined = " ".join(r["text"] for r in result["data"]["results"]).lower()
            assert "eligib" in combined
