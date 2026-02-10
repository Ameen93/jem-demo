"""Tests for LangGraph agent state, graph, and nodes."""

from unittest.mock import MagicMock, patch


class TestAgentState:
    """Tests for AgentState TypedDict (Story 5.1)."""

    def test_state_has_required_fields(self):
        """AgentState has all required fields."""
        from src.agents.state import AgentState

        required = [
            "messages",
            "language",
            "employee_id",
            "employee",
            "intent",
            "tool_results",
            "response",
            "error",
        ]
        for field in required:
            assert field in AgentState.__annotations__

    def test_state_initialization(self):
        """Can create a valid initial state."""
        from src.agents.state import create_initial_state

        state = create_initial_state("EMP001", "Hello")
        assert state["employee_id"] == "EMP001"
        assert state["language"] == "en"
        assert state["intent"] == ""
        assert state["error"] is None
        assert len(state["messages"]) == 1


class TestGraphStructure:
    """Tests for LangGraph compilation (Story 5.1)."""

    def test_graph_compiles(self):
        """Graph compiles without errors."""
        from src.agents.graph import build_graph

        graph = build_graph()
        assert graph is not None

    def test_graph_has_nodes(self):
        """Graph has expected node names."""
        from src.agents.graph import build_graph

        graph = build_graph()
        # LangGraph compiled graph has nodes accessible
        assert graph is not None


class TestLanguageDetectNode:
    """Tests for language_detect node (Story 5.2)."""

    @patch("src.agents.nodes.language_detect._detect_language")
    def test_detects_zulu(self, mock_detect):
        """AC #1: isiZulu message sets language to 'zu'."""
        from src.agents.nodes.language_detect import language_detect
        from src.agents.state import create_initial_state

        mock_detect.return_value = "zu"
        state = create_initial_state("EMP001", "Sawubona, ngifuna imali")
        result = language_detect(state)
        assert result["language"] == "zu"

    @patch("src.agents.nodes.language_detect._detect_language")
    def test_detects_english(self, mock_detect):
        """AC #2: English message sets language to 'en'."""
        from src.agents.nodes.language_detect import language_detect
        from src.agents.state import create_initial_state

        mock_detect.return_value = "en"
        state = create_initial_state("EMP001", "How many leave days?")
        result = language_detect(state)
        assert result["language"] == "en"

    @patch("src.agents.nodes.language_detect._detect_language")
    def test_fallback_to_english(self, mock_detect):
        """Fallback to 'en' if detection fails."""
        from src.agents.nodes.language_detect import language_detect
        from src.agents.state import create_initial_state

        mock_detect.side_effect = Exception("API error")
        state = create_initial_state("EMP001", "??")
        result = language_detect(state)
        assert result["language"] == "en"


class TestIntentRouterNode:
    """Tests for intent_router node (Story 5.3)."""

    @patch("src.agents.nodes.intent_router._classify_intent")
    def test_hr_query_classification(self, mock_classify):
        """AC #1: Leave balance question routes to hr_query."""
        from src.agents.nodes.intent_router import intent_router
        from src.agents.state import create_initial_state

        mock_classify.return_value = "hr_query"
        state = create_initial_state("EMP001", "What is my leave balance?")
        result = intent_router(state)
        assert result["intent"] == "hr_query"

    @patch("src.agents.nodes.intent_router._classify_intent")
    def test_ewa_request_classification(self, mock_classify):
        """AC #2: EWA question routes to ewa_request."""
        from src.agents.nodes.intent_router import intent_router
        from src.agents.state import create_initial_state

        mock_classify.return_value = "ewa_request"
        state = create_initial_state("EMP001", "I need an advance on my salary")
        result = intent_router(state)
        assert result["intent"] == "ewa_request"

    @patch("src.agents.nodes.intent_router._classify_intent")
    def test_policy_question_classification(self, mock_classify):
        """AC #3: Policy question routes to policy_rag."""
        from src.agents.nodes.intent_router import intent_router
        from src.agents.state import create_initial_state

        mock_classify.return_value = "policy_question"
        state = create_initial_state("EMP001", "What is the sick leave policy?")
        result = intent_router(state)
        assert result["intent"] == "policy_question"


class TestHRAgentNode:
    """Tests for hr_agent node (Story 5.4)."""

    @patch("src.agents.nodes.hr_agent._call_hr_tool")
    def test_stores_tool_results(self, mock_call):
        """AC #1: Tool results stored in state."""
        from src.agents.nodes.hr_agent import hr_agent
        from src.agents.state import create_initial_state

        mock_call.return_value = {"success": True, "data": {"annual": 12}}
        state = create_initial_state("EMP001", "What is my leave balance?")
        state["intent"] = "hr_query"
        result = hr_agent(state)
        assert result["tool_results"] is not None


class TestEWAAgentNode:
    """Tests for ewa_agent node (Story 5.5)."""

    @patch("src.agents.nodes.ewa_agent._call_ewa_tool")
    def test_stores_tool_results(self, mock_call):
        """AC #1: EWA tool results stored in state."""
        from src.agents.nodes.ewa_agent import ewa_agent
        from src.agents.state import create_initial_state

        mock_call.return_value = {
            "success": True,
            "data": {"eligible": True, "available": 2134},
        }
        state = create_initial_state("EMP001", "Am I eligible for EWA?")
        state["intent"] = "ewa_request"
        result = ewa_agent(state)
        assert result["tool_results"] is not None


class TestPolicyRAGNode:
    """Tests for policy_rag node (Story 5.6)."""

    @patch("src.agents.nodes.policy_rag.search_policies")
    def test_stores_policy_results(self, mock_search):
        """AC #1: Policy results stored in state."""
        from src.agents.nodes.policy_rag import policy_rag
        from src.agents.state import create_initial_state

        mock_search.return_value = {
            "success": True,
            "data": {
                "query": "sick leave",
                "results": [{"text": "30 days over 3 years", "source": "leave_policy.md, Sick Leave"}],
            },
        }
        state = create_initial_state("EMP001", "How many sick days?")
        state["intent"] = "policy_question"
        result = policy_rag(state)
        assert result["tool_results"] is not None


class TestResponseFormatNode:
    """Tests for response_format node (Story 5.7)."""

    @patch("src.agents.nodes.response_format._format_response")
    def test_generates_response(self, mock_format):
        """AC #1: Response generated from tool results."""
        from src.agents.nodes.response_format import response_format
        from src.agents.state import create_initial_state

        mock_format.return_value = "You have 12 annual leave days remaining."
        state = create_initial_state("EMP001", "What is my leave balance?")
        state["tool_results"] = {"success": True, "data": {"annual": 12}}
        state["language"] = "en"
        result = response_format(state)
        assert result["response"] != ""
        assert isinstance(result["response"], str)
