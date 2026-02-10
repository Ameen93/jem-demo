---
stepsCompleted:
  - step-01-init
  - step-02-context
  - step-03-starter
  - step-04-decisions
  - step-05-patterns
  - step-06-structure
  - step-07-validation
  - step-08-complete
status: complete
completedAt: '2026-02-10'
inputDocuments:
  - prd.md
  - jem-interview-demo-plan.md
workflowType: 'architecture'
project_name: 'Jem HR Interview Demo'
user_name: 'Ameen'
date: '2026-02-10'
---

# Architecture Decision Document

_This document builds collaboratively through step-by-step discovery. Sections are appended as we work through each architectural decision together._

## Project Context Analysis

### Requirements Overview

**Functional Requirements (33 total):**
- Employee Information (4 FRs): Profile retrieval, language preference, employment status
- Leave Management (5 FRs): Balance queries, request submission, validation, accrual tracking
- EWA (7 FRs): Eligibility, calculation, outstanding balance, transaction processing
- Payroll (3 FRs): Payslip retrieval, earnings calculation, deductions display
- Policy RAG (4 FRs): Natural language queries, retrieval, citations, HR policy coverage
- Language Support (3 FRs): Detection, response translation, policy translation
- Conversation (4 FRs): Intent classification, routing, context, CLI formatting
- Demo Operations (3 FRs): Employee selection, formatted output, auto-seeding

**Non-Functional Requirements (16 total):**
- Performance: Sub-second tool invocations, 5-second conversation turns
- Reliability: Zero crashes, graceful error handling, English fallback
- Integration: MCP JSON-RPC 2.0, embedded ChromaDB, auto-init SQLite

**Scale & Complexity:**
- Primary domain: API/Backend Developer Tool
- Complexity level: Medium (demo scope, single-user, local execution)
- Estimated architectural components: 5 (MCP Server, LangGraph, RAG, Translation, CLI)

### Technical Constraints & Dependencies

- Must run locally without external services (except Anthropic API)
- NLLB model download required (~600MB one-time)
- ChromaDB embedded mode (no separate server)
- SQLite file-based (no PostgreSQL)
- Python 3.11+ required for modern typing

### Cross-Cutting Concerns Identified

1. **Error Handling** - Every layer must catch and gracefully handle failures
2. **Employee Context** - Must flow through LangGraph state to all agents
3. **Language Consistency** - Detected language must propagate to response formatting
4. **Demo Mode** - All components need to support employee selection at runtime

## Starter Template Evaluation

### Primary Technology Domain

Python API/Backend + CLI Tool - Custom MCP server with LangGraph orchestration

### Starter Options Considered

| Option | Status | Reason |
|--------|--------|--------|
| LangGraph Templates | Rejected | No MCP integration |
| MCP Python SDK Examples | Partial | Too basic, no agent orchestration |
| Custom Structure | Selected | Matches PRD architecture exactly |

### Selected Approach: Custom Python Project

**Rationale:** No existing starter combines MCP + LangGraph + RAG. The PRD already defines optimal structure.

**Initialization Command:**

```bash
# Using uv (recommended - fast Python package manager)
mkdir jem-demo && cd jem-demo
uv init
uv add mcp langgraph langchain-anthropic chromadb sqlalchemy rich python-dotenv

# Or using pip
mkdir jem-demo && cd jem-demo
python -m venv .venv && source .venv/bin/activate
pip install mcp langgraph langchain-anthropic chromadb sqlalchemy rich python-dotenv
```

**Project Structure Established:**

```
src/
├── mcp_server/     # MCP protocol layer
├── agents/         # LangGraph orchestration
├── rag/            # ChromaDB + retrieval
├── i18n/           # NLLB translation
└── db/             # SQLAlchemy models
```

**Note:** Project initialization is the first implementation task.

## Core Architectural Decisions

### Decision Priority Analysis

**Critical Decisions (Block Implementation):**
- Error handling pattern: Try/catch at boundaries
- LangGraph flow: Conditional routing to specialized agents
- MCP response format: Typed dict returns

**Important Decisions (Shape Architecture):**
- RAG strategy: Document-level embedding (no chunking)
- State management: Single AgentState TypedDict flows through graph

**Deferred (Not Needed for Demo):**
- Authentication (mock employee selection)
- CI/CD (local execution only)
- Caching (single-user demo)

### Data Architecture

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Database | SQLite | Simple, file-based, auto-seeds |
| ORM | SQLAlchemy 2.0 | Type hints, async support |
| Migrations | None | Fresh DB each demo run |
| Vector Store | ChromaDB embedded | No server, persistent |

### API & Communication

| Decision | Choice | Rationale |
|----------|--------|-----------|
| MCP Transport | stdio | Standard for local MCP |
| Protocol | JSON-RPC 2.0 | MCP specification |
| Tool Returns | Typed dicts | Simple, LLM interprets |
| Error Format | `{success, data/error}` | Consistent pattern |

### Agent Architecture

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Orchestration | LangGraph conditional | Simple router, clear flow |
| State | Single TypedDict | Shared context |
| Agents | 3 specialized | HR, EWA, Policy |
| Language | Detect once, use throughout | State.language field |

### Implementation Sequence

1. Database + models + seed data
2. MCP server + tools (no orchestration yet)
3. LangGraph graph + nodes
4. RAG setup + policy indexing
5. CLI demo interface
6. (If time) NLLB translation

## Implementation Patterns & Consistency Rules

### Naming Patterns

**Python Code (PEP 8):**
- Functions/variables: `snake_case` → `get_employee`, `employee_id`
- Classes: `PascalCase` → `AgentState`, `EmployeeNotFound`
- Constants: `UPPER_SNAKE` → `MAX_EWA_AMOUNT`, `DEFAULT_LANGUAGE`
- Files: `snake_case.py` → `hr_tools.py`, `ewa_agent.py`

**Database (SQLAlchemy):**
- Tables: plural, snake_case → `employees`, `leave_balances`, `ewa_transactions`
- Columns: snake_case → `employee_id`, `hourly_rate`, `hire_date`
- Foreign keys: `{table}_id` → `employee_id`

**MCP Tools:**
- Tool names: snake_case verbs → `get_employee`, `check_ewa_eligibility`
- Parameters: snake_case → `employee_id`, `leave_type`

### Structure Patterns

**File Organization:**
```
src/
├── mcp_server/
│   ├── __init__.py
│   ├── server.py          # MCP server entry point
│   └── tools/
│       ├── __init__.py    # Exports all tools
│       ├── hr_tools.py    # get_employee, get_leave_balance, etc.
│       ├── ewa_tools.py   # check_ewa_eligibility, request_ewa_advance
│       └── policy_tools.py # search_policies
├── agents/
│   ├── __init__.py
│   ├── graph.py           # LangGraph definition
│   ├── state.py           # AgentState TypedDict
│   └── nodes/
│       ├── __init__.py
│       ├── language_detect.py
│       ├── intent_router.py
│       ├── hr_agent.py
│       ├── ewa_agent.py
│       └── policy_rag.py
├── db/
│   ├── __init__.py
│   ├── models.py          # SQLAlchemy models
│   ├── connection.py      # get_session()
│   └── seed.py            # seed_database()
└── rag/
    ├── __init__.py
    ├── vectorstore.py     # ChromaDB setup
    └── retriever.py       # Policy retrieval
```

### Format Patterns

**MCP Tool Response Format:**
```python
# Success
{"success": True, "data": {...}}

# Error
{"success": False, "error": "Human readable message", "code": "ERROR_CODE"}
```

**LangGraph State (Single Source of Truth):**
```python
class AgentState(TypedDict):
    messages: list[BaseMessage]
    language: str                   # "en", "zu", "xh", "af"
    employee_id: str | None
    employee: dict | None           # Cached employee data
    intent: str                     # "hr_query", "ewa_request", "policy_question"
    tool_results: dict
    response: str
    error: str | None
```

**State Updates (Immutable):**
```python
# CORRECT - return new state
def language_detect(state: AgentState) -> AgentState:
    detected = detect_language(state["messages"][-1].content)
    return {**state, "language": detected}

# WRONG - never mutate
def language_detect(state: AgentState) -> AgentState:
    state["language"] = detected  # NO!
    return state
```

### Process Patterns

**Error Handling (Boundary Pattern):**
```python
# MCP tool level - catch and return structured error
@tool
async def get_employee(employee_id: str) -> dict:
    try:
        employee = await db.get_employee(employee_id)
        return {"success": True, "data": employee.to_dict()}
    except EmployeeNotFound:
        return {"success": False, "error": f"Employee {employee_id} not found", "code": "NOT_FOUND"}
    except Exception as e:
        logger.exception("Unexpected error in get_employee")
        return {"success": False, "error": "Internal error", "code": "INTERNAL"}

# LangGraph node level - set error state, don't raise
def ewa_agent(state: AgentState) -> AgentState:
    try:
        result = process_ewa_request(state)
        return {**state, "tool_results": result}
    except Exception as e:
        logger.exception("EWA agent error")
        return {**state, "error": "Unable to process EWA request"}
```

**Logging Pattern:**
```python
import logging
logger = logging.getLogger(__name__)

# Use appropriate levels
logger.debug("Processing employee %s", employee_id)
logger.info("EWA request processed: %s", transaction_id)
logger.warning("Employee in probation, EWA rejected")
logger.error("Database connection failed")
logger.exception("Unexpected error")  # Includes stack trace
```

### Enforcement Guidelines

**All AI Agents MUST:**
1. Use `snake_case` for all Python identifiers (PEP 8)
2. Return `{"success": bool, "data"|"error": ...}` from MCP tools
3. Update LangGraph state immutably (spread operator pattern)
4. Catch exceptions at boundaries, never let them propagate to user
5. Log with appropriate levels, never print()

**Anti-Patterns to Avoid:**
```python
# WRONG: camelCase
def getEmployee(employeeId): ...

# WRONG: bare return
return employee  # Should be {"success": True, "data": employee}

# WRONG: mutating state
state["language"] = "zu"

# WRONG: exception propagation
raise ValueError("Employee not found")  # Should return error dict

# WRONG: print debugging
print(f"Debug: {employee}")  # Use logger.debug()
```

## Project Structure & Boundaries

### Complete Project Directory Structure

```
jem-demo/
├── README.md                      # Project overview, demo instructions
├── pyproject.toml                 # uv/pip dependencies
├── .env.example                   # Required env vars template
├── .gitignore
│
├── data/
│   ├── policies/
│   │   ├── leave_policy.md        # Leave policy for RAG
│   │   └── ewa_policy.md          # EWA policy for RAG
│   ├── jem_hr.db                  # SQLite database (auto-created)
│   └── chroma/                    # ChromaDB persistence (auto-created)
│
├── src/
│   ├── __init__.py
│   │
│   ├── db/
│   │   ├── __init__.py
│   │   ├── models.py              # Employee, LeaveBalance, Timesheet, EWATransaction
│   │   ├── connection.py          # get_engine(), get_session()
│   │   └── seed.py                # seed_database() - 12 employees
│   │
│   ├── mcp_server/
│   │   ├── __init__.py
│   │   ├── server.py              # MCP server entry, tool registration
│   │   └── tools/
│   │       ├── __init__.py        # Export all tools
│   │       ├── hr_tools.py        # get_employee, get_leave_balance, submit_leave_request, get_payslip
│   │       ├── ewa_tools.py       # check_ewa_eligibility, request_ewa_advance
│   │       └── policy_tools.py    # search_policies
│   │
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── state.py               # AgentState TypedDict
│   │   ├── graph.py               # LangGraph definition, compile()
│   │   └── nodes/
│   │       ├── __init__.py
│   │       ├── language_detect.py # Detect user language
│   │       ├── intent_router.py   # Route to HR/EWA/Policy
│   │       ├── hr_agent.py        # Handle leave, employee queries
│   │       ├── ewa_agent.py       # Handle EWA eligibility, requests
│   │       ├── policy_rag.py      # RAG retrieval + response
│   │       └── response_format.py # Format final response
│   │
│   ├── rag/
│   │   ├── __init__.py
│   │   ├── vectorstore.py         # ChromaDB setup, index_policies()
│   │   └── retriever.py           # retrieve_policy(query) -> chunks
│   │
│   └── i18n/                      # Phase 2 - NLLB translation
│       ├── __init__.py
│       ├── detector.py            # detect_language(text) -> code
│       └── translator.py          # translate(text, from_lang, to_lang)
│
├── scripts/
│   ├── run_demo.py                # CLI demo entry point
│   ├── seed_db.py                 # Standalone DB seeding
│   └── index_policies.py          # Standalone policy indexing
│
└── tests/                         # Optional for demo
    ├── __init__.py
    ├── test_db.py
    ├── test_mcp_tools.py
    └── test_agents.py
```

### FR Category to Location Mapping

| FR Category | Location | Key Files |
|-------------|----------|-----------|
| Employee Info (FR1-4) | `src/db/`, `src/mcp_server/tools/hr_tools.py` | `models.py`, `hr_tools.py` |
| Leave Management (FR5-9) | `src/mcp_server/tools/hr_tools.py` | `hr_tools.py` |
| EWA (FR10-16) | `src/mcp_server/tools/ewa_tools.py` | `ewa_tools.py` |
| Payroll (FR17-19) | `src/mcp_server/tools/hr_tools.py` | `hr_tools.py` |
| Policy RAG (FR20-23) | `src/rag/`, `src/mcp_server/tools/policy_tools.py` | `retriever.py`, `policy_tools.py` |
| Language (FR24-26) | `src/i18n/`, `src/agents/nodes/language_detect.py` | `detector.py`, `translator.py` |
| Conversation (FR27-30) | `src/agents/` | `graph.py`, `nodes/` |
| Demo Ops (FR31-33) | `scripts/`, `src/db/seed.py` | `run_demo.py`, `seed.py` |

### Architectural Boundaries

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLI LAYER                                │
│                      scripts/run_demo.py                         │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    ORCHESTRATION LAYER                           │
│                      src/agents/graph.py                         │
└────────────────────────────┬────────────────────────────────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
┌─────────────────┐ ┌─────────────┐ ┌─────────────────┐
│   HR AGENT      │ │  EWA AGENT  │ │   POLICY RAG    │
└────────┬────────┘ └──────┬──────┘ └────────┬────────┘
         │                 │                  │
         ▼                 ▼                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                       MCP TOOL LAYER                             │
│                    src/mcp_server/tools/                         │
└────────────────────────────┬────────────────────────────────────┘
                             │
              ┌──────────────┴──────────────┐
              ▼                             ▼
┌─────────────────────────┐   ┌─────────────────────────┐
│      DATA LAYER         │   │       RAG LAYER         │
│        src/db/          │   │        src/rag/         │
└─────────────────────────┘   └─────────────────────────┘
```

### Data Flow

```
User Input (CLI)
      │
      ▼
┌─────────────────┐
│ language_detect │ ──► state.language = "zu"
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  intent_router  │ ──► state.intent = "ewa_request"
└────────┬────────┘
         │
         ▼ (conditional edge based on intent)
┌─────────────────┐
│    ewa_agent    │ ──► calls check_ewa_eligibility tool
└────────┬────────┘     state.tool_results = {...}
         │
         ▼
┌─────────────────┐
│ response_format │ ──► state.response = "Sawubona Sipho..."
└────────┬────────┘
         │
         ▼
     CLI Output
```

## Architecture Validation Results

### Coherence Validation ✅

**Decision Compatibility:** All technology choices (Python 3.11, SQLite, ChromaDB, LangGraph, MCP, Rich) work together without conflicts. Standard Python ecosystem with well-maintained libraries.

**Pattern Consistency:** PEP 8 naming, SQLAlchemy ORM patterns, and LangGraph state management are all consistent with Python best practices.

**Structure Alignment:** Project structure directly supports the 5-layer architecture (CLI → Orchestration → Agents → MCP Tools → Data/RAG).

### Requirements Coverage ✅

| Category | FRs | Coverage |
|----------|-----|----------|
| Employee Info | FR1-4 | `db/models.py`, `hr_tools.py` |
| Leave Mgmt | FR5-9 | `hr_tools.py` |
| EWA | FR10-16 | `ewa_tools.py` |
| Payroll | FR17-19 | `hr_tools.py` |
| Policy RAG | FR20-23 | `rag/`, `policy_tools.py` |
| Language | FR24-26 | `i18n/`, `language_detect.py` |
| Conversation | FR27-30 | `agents/graph.py`, nodes |
| Demo Ops | FR31-33 | `scripts/`, `seed.py` |

**NFR Coverage:** All 16 NFRs addressed through architecture decisions.

### Architecture Completeness Checklist

- [x] Project context analyzed
- [x] Technology stack specified with versions
- [x] Implementation patterns with examples
- [x] Anti-patterns documented
- [x] Complete project structure
- [x] FR-to-location mapping
- [x] Layer boundaries defined
- [x] Data flow documented

### Architecture Readiness Assessment

**Overall Status:** READY FOR IMPLEMENTATION

**Confidence Level:** High

**Key Strengths:**
- Clear separation of concerns across 5 layers
- Every FR mapped to specific files
- Concrete code examples for all patterns
- Simple architecture appropriate for demo scope

**First Implementation Priority:**
1. Create project structure with `uv init`
2. Implement `db/models.py` + `seed.py`
3. Implement MCP tools
4. Build LangGraph orchestration
5. Add RAG layer
6. Create CLI demo
