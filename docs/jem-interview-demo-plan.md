# Jem HR Interview Demo - Technical Plan

## Project Codename: "Jem Agent Demo"

**Goal:** Build a production-quality demo that showcases AI-native thinking, MCP architecture, multi-agent patterns, and South African language support - all directly relevant to Jem HR's platform.

**Interview Date:** Tomorrow
**Interviewer:** Simon Ellis (CEO) + Senior Developer

---

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           JEM AGENT DEMO                                     │
└─────────────────────────────────────────────────────────────────────────────┘

                    ┌─────────────────────────────────┐
                    │         DEMO INTERFACE          │
                    │   (CLI or Simple Web Chat)      │
                    └───────────────┬─────────────────┘
                                    │
                    ┌───────────────▼─────────────────┐
                    │       LANGGRAPH ORCHESTRATOR    │
                    │                                 │
                    │  ┌─────────┐  ┌─────────────┐  │
                    │  │Language │  │   Router    │  │
                    │  │Detector │─►│    Node     │  │
                    │  └─────────┘  └──────┬──────┘  │
                    │                      │         │
                    │     ┌────────────────┼────────────────┐
                    │     ▼                ▼                ▼
                    │ ┌────────┐    ┌──────────┐    ┌──────────┐
                    │ │  HR    │    │  Policy  │    │   EWA    │
                    │ │ Agent  │    │   RAG    │    │  Agent   │
                    │ └───┬────┘    └────┬─────┘    └────┬─────┘
                    └─────┼──────────────┼───────────────┼─────┘
                          │              │               │
                          ▼              ▼               ▼
                    ┌─────────────────────────────────────────┐
                    │           MCP SERVER LAYER              │
                    │                                         │
                    │  ┌────────────┐  ┌────────────────┐    │
                    │  │  HR Tools  │  │  Policy Store  │    │
                    │  │            │  │  (Vector DB)   │    │
                    │  └────────────┘  └────────────────┘    │
                    │                                         │
                    │  Tools:                                 │
                    │  - get_employee()                       │
                    │  - get_leave_balance()                  │
                    │  - submit_leave_request()               │
                    │  - get_payslip()                        │
                    │  - check_ewa_eligibility()              │
                    │  - request_ewa_advance()                │
                    │  - search_hr_policies()                 │
                    └─────────────────────────────────────────┘
                                    │
                    ┌───────────────▼─────────────────┐
                    │         DATA LAYER              │
                    │                                 │
                    │  ┌────────────┐ ┌────────────┐ │
                    │  │  SQLite    │ │  ChromaDB  │ │
                    │  │  (HR Data) │ │  (Policies)│ │
                    │  └────────────┘ └────────────┘ │
                    └─────────────────────────────────┘
```

---

## Component Breakdown

### 1. MCP Server: `jem-hr-server`

**Purpose:** Expose HR operations as tools that any MCP-compatible AI can use.

**Tools to Implement:**

| Tool | Description | Input | Output |
|------|-------------|-------|--------|
| `get_employee` | Fetch employee details | employee_id | name, dept, role, hire_date |
| `get_leave_balance` | Check remaining leave | employee_id | annual, sick, family days |
| `submit_leave_request` | Request time off | employee_id, dates, type | request_id, status |
| `get_payslip` | Retrieve payslip | employee_id, month | earnings, deductions, net |
| `check_ewa_eligibility` | EWA availability | employee_id | eligible, max_amount, reason |
| `request_ewa_advance` | Request early wages | employee_id, amount | txn_id, status, disbursement_date |
| `search_policies` | RAG over HR docs | query, language | relevant_policy, source |

**Data Storage:** SQLite for simplicity, easy to demo

---

### 2. LangGraph Orchestrator

**Purpose:** Route user intents to appropriate agents, manage conversation state.

**Nodes:**

```
START
  │
  ▼
┌─────────────────┐
│ Language Detect │ ──► Detect SA language, set response language
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Intent Router  │ ──► Classify: HR_QUERY | POLICY_QUESTION | EWA_REQUEST | CHITCHAT
└────────┬────────┘
         │
    ┌────┴────┬────────────┬────────────┐
    ▼         ▼            ▼            ▼
┌───────┐ ┌───────┐ ┌──────────┐ ┌──────────┐
│  HR   │ │Policy │ │   EWA    │ │ Fallback │
│ Agent │ │  RAG  │ │  Agent   │ │  Agent   │
└───┬───┘ └───┬───┘ └────┬─────┘ └────┬─────┘
    │         │          │            │
    └─────────┴──────────┴────────────┘
                    │
                    ▼
         ┌─────────────────┐
         │ Response Format │ ──► Format in detected language
         └────────┬────────┘
                  │
                  ▼
                 END
```

**State Schema:**

```python
class AgentState(TypedDict):
    messages: list[BaseMessage]
    language: str  # detected language code
    employee_id: str | None  # current employee context
    intent: str  # classified intent
    tool_results: dict  # results from MCP tools
```

---

### 3. Policy RAG System

**Purpose:** Answer questions about HR policies using retrieved context.

**Components:**
- **Vector Store:** ChromaDB (embedded, no server needed)
- **Embeddings:** OpenAI or local model
- **Documents:** Sample HR policy docs (leave policy, EWA terms, benefits guide)

**Flow:**
1. User asks: "How many sick days do I get?"
2. Embed query → Search vector store
3. Retrieve top-k policy chunks
4. LLM generates answer with citations

---

### 4. Multi-Language Support

**South African Official Languages (12):**
1. English
2. Afrikaans
3. isiZulu
4. isiXhosa
5. isiNdebele
6. Sepedi (Northern Sotho)
7. Sesotho (Southern Sotho)
8. Setswana
9. siSwati
10. Tshivenda
11. Xitsonga
12. South African Sign Language

**Priority for Demo (most spoken by frontline workers):**
1. English (business standard)
2. isiZulu (23% of population)
3. isiXhosa (16% of population)
4. Afrikaans (13% of population)
5. Sepedi (9% of population)

**Implementation Approach:** TBD - needs research on:
- LLM capabilities for SA languages
- Translation APIs (Google, Azure, local models)
- Prompt engineering for multilingual responses

---

## Mock Data Design

### Employees Table

```sql
CREATE TABLE employees (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    department TEXT,
    role TEXT,
    hire_date DATE,
    hourly_rate DECIMAL(10,2),
    preferred_language TEXT DEFAULT 'en',
    bank_account_last4 TEXT
);
```

### Sample Employees

| ID | Name | Department | Language | Hourly Rate |
|----|------|------------|----------|-------------|
| EMP001 | Sipho Dlamini | Retail - Checkers | zu | R48.50 |
| EMP002 | Thandiwe Nkosi | Security - Fidelity | xh | R42.00 |
| EMP003 | Johan van der Berg | Warehouse - DHL | af | R55.00 |
| EMP004 | Lerato Molefe | Call Centre - Vodacom | nso | R38.00 |
| EMP005 | Nomvula Sithole | Hospitality - Hilton | en | R45.00 |

### Leave Balances

```sql
CREATE TABLE leave_balances (
    employee_id TEXT REFERENCES employees(id),
    leave_type TEXT,  -- annual, sick, family, maternity
    balance_days DECIMAL(4,1),
    accrued_ytd DECIMAL(4,1),
    used_ytd DECIMAL(4,1)
);
```

### Timesheets (for EWA calculation)

```sql
CREATE TABLE timesheets (
    employee_id TEXT REFERENCES employees(id),
    pay_period_start DATE,
    pay_period_end DATE,
    hours_worked DECIMAL(5,2),
    status TEXT  -- approved, pending, disputed
);
```

### EWA Transactions

```sql
CREATE TABLE ewa_transactions (
    id TEXT PRIMARY KEY,
    employee_id TEXT REFERENCES employees(id),
    amount DECIMAL(10,2),
    requested_at TIMESTAMP,
    status TEXT,  -- pending, approved, disbursed, repaid
    disbursed_at TIMESTAMP,
    repayment_date DATE
);
```

---

## Sample HR Policy Documents (for RAG)

### Document 1: Leave Policy
```
LEAVE POLICY - Effective January 2024

1. ANNUAL LEAVE
   - All employees are entitled to 15 working days annual leave per year
   - Leave accrues at 1.25 days per month
   - Unused leave may be carried over (maximum 5 days)
   - Leave requests require 7 days notice for periods over 3 days

2. SICK LEAVE
   - Employees receive 30 days sick leave over a 3-year cycle
   - Medical certificate required for absences exceeding 2 consecutive days
   - Mental health days are treated as sick leave

3. FAMILY RESPONSIBILITY LEAVE
   - 3 days per year for family emergencies
   - Birth of child, death of immediate family member, illness of child
```

### Document 2: Earned Wage Access Policy
```
EARNED WAGE ACCESS (EWA) POLICY

1. ELIGIBILITY
   - Permanent employees who have completed probation (3 months)
   - Must have worked minimum 5 days in current pay period
   - No outstanding EWA balance from previous period

2. LIMITS
   - Maximum 50% of earned wages available for advance
   - Minimum request: R100
   - Maximum request: R5,000 per pay period

3. FEES
   - No interest charged on advances
   - Transaction fee: R10 per advance

4. REPAYMENT
   - Automatically deducted from next payroll
   - Cannot be extended or rolled over
```

---

## Demo Script

**Scenario:** Show the agent handling queries from different employees in different languages.

### Demo 1: English - Leave Balance Query
```
User: "Hi, I'm Nomvula from Hilton. How many leave days do I have?"

Agent: [Detects English, routes to HR Agent, calls get_leave_balance]
       "Hello Nomvula! Here's your leave balance:
        - Annual leave: 12 days remaining
        - Sick leave: 8 days remaining
        - Family responsibility: 2 days remaining

        Would you like to submit a leave request?"
```

### Demo 2: isiZulu - EWA Request
```
User: "Sawubona, ngifuna ukuthola imali yami ngaphambi kosuku lokuhola"
      (Hello, I want to get my money before payday)

Agent: [Detects isiZulu, routes to EWA Agent]
       "Sawubona Sipho! Ngikuhlolile i-akhawunti yakho:
        - Usebenze izinsuku ezingu-12 kule nkathi yokukhokha
        - Uhola: R4,656
        - Ungathola kuze kube ngu-R2,328 (50%)

        Ufuna ukucela malini?"
```

### Demo 3: Policy Question
```
User: "What happens if I don't use all my leave days?"

Agent: [Routes to Policy RAG]
       "According to the Leave Policy (Section 1):
        Unused annual leave may be carried over to the next year,
        with a maximum of 5 days. Any leave beyond 5 days will
        be forfeited unless special arrangements are made with HR.

        Source: Leave Policy, January 2024"
```

---

## File Structure

```
jem-demo/
├── README.md
├── pyproject.toml
├── .env.example
│
├── src/
│   ├── __init__.py
│   │
│   ├── mcp_server/
│   │   ├── __init__.py
│   │   ├── server.py          # Main MCP server
│   │   ├── tools/
│   │   │   ├── __init__.py
│   │   │   ├── hr_tools.py     # Leave, employee tools
│   │   │   ├── ewa_tools.py    # EWA eligibility, requests
│   │   │   └── policy_tools.py # RAG search tool
│   │   └── db/
│   │       ├── __init__.py
│   │       ├── models.py       # SQLAlchemy models
│   │       └── seed.py         # Seed data
│   │
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── graph.py            # LangGraph definition
│   │   ├── nodes/
│   │   │   ├── __init__.py
│   │   │   ├── language_detect.py
│   │   │   ├── router.py
│   │   │   ├── hr_agent.py
│   │   │   ├── ewa_agent.py
│   │   │   └── policy_rag.py
│   │   └── state.py            # State schema
│   │
│   ├── rag/
│   │   ├── __init__.py
│   │   ├── embeddings.py
│   │   ├── vectorstore.py
│   │   └── retriever.py
│   │
│   └── i18n/
│       ├── __init__.py
│       ├── detector.py         # Language detection
│       ├── translator.py       # Translation layer
│       └── prompts/            # Language-specific prompts
│           ├── en.yaml
│           ├── zu.yaml
│           ├── xh.yaml
│           └── af.yaml
│
├── data/
│   ├── employees.json          # Seed data
│   ├── policies/               # HR policy documents
│   │   ├── leave_policy.md
│   │   ├── ewa_policy.md
│   │   └── benefits_guide.md
│   └── jem_hr.db              # SQLite database
│
├── tests/
│   ├── test_mcp_server.py
│   ├── test_agents.py
│   └── test_rag.py
│
└── scripts/
    ├── seed_db.py
    ├── index_policies.py
    └── run_demo.py
```

---

## Implementation Phases

### Phase 1: Foundation (MUST HAVE)
- [ ] SQLite database with seed data
- [ ] Basic MCP server with 3 core tools (get_employee, get_leave_balance, check_ewa)
- [ ] CLI demo interface

### Phase 2: Intelligence (SHOULD HAVE)
- [ ] LangGraph orchestrator with routing
- [ ] Policy RAG with ChromaDB
- [ ] Full tool suite (6 tools)

### Phase 3: Polish (NICE TO HAVE)
- [ ] Multi-language support (isiZulu, isiXhosa, Afrikaans)
- [ ] Simple web UI
- [ ] Conversation memory/checkpointing

---

## Dependencies

```toml
[project]
dependencies = [
    "mcp>=1.0.0",
    "langgraph>=0.2.0",
    "langchain>=0.3.0",
    "langchain-anthropic>=0.3.0",
    "chromadb>=0.5.0",
    "sqlalchemy>=2.0.0",
    "pydantic>=2.0.0",
    "python-dotenv>=1.0.0",
]
```

---

## Open Questions

1. **Language Detection:** Use LLM-based detection or dedicated library (langdetect, lingua)?
2. **Translation Strategy:**
   - Claude handles translation in prompts?
   - External translation API?
   - Pre-translated response templates?
3. **Demo Interface:** CLI sufficient or need simple web UI?
4. **Embedding Model:** OpenAI embeddings or local model for offline demo?

---

## Success Criteria

The demo should prove:

1. **I understand MCP** - Built a working MCP server with multiple tools
2. **I can build agents** - LangGraph orchestration with routing
3. **I know RAG** - Policy Q&A with citations
4. **I care about users** - Multi-language support for frontline workers
5. **I ship quality** - Clean code, proper structure, error handling
6. **I understand Jem's domain** - Realistic HR/EWA scenarios

---

## Next Steps

1. Finalize architecture decisions (open questions above)
2. Research SA language support options
3. Scaffold project structure
4. Implement Phase 1
5. Test with Claude Desktop / Claude Code
6. Add Phase 2 if time permits
7. Prepare demo script and talking points
