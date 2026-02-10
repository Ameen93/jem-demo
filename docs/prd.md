---
stepsCompleted:
  - step-01-init
  - step-02-discovery
  - step-03-success
  - step-04-journeys
  - step-05-domain
  - step-06-innovation
  - step-07-project-type
  - step-08-scoping
  - step-09-functional
  - step-10-nonfunctional
  - step-11-polish
  - step-12-complete
inputDocuments:
  - jem-interview-demo-plan.md
workflowType: 'prd'
documentCounts:
  briefs: 0
  research: 0
  projectDocs: 0
  plans: 1
classification:
  projectType: api_backend_developer_tool
  domain: fintech
  complexity: medium
  projectContext: greenfield
---

# Product Requirements Document - Jem HR Interview Demo

**Author:** Ameen
**Date:** 2026-02-10

## Executive Summary

**Project:** Jem HR Interview Demo - A working demonstration of AI-native HR agent architecture

**Purpose:** Prove technical competency for Senior Product Engineer role at Jem HR by demonstrating:
- MCP server implementation (7 tools)
- LangGraph multi-agent orchestration
- RAG-powered policy Q&A
- South African language support (NLLB)

**Audience:** CEO Simon Ellis + Senior Developer (technical interview)

**Deadline:** Tonight (2026-02-10)

**Demo Scenarios:**
1. Sipho requests EWA in isiZulu → Happy path transaction
2. Pieter asks policy question in Afrikaans → RAG retrieval with citations
3. Nomvula checks leave balance in English → HR agent query

## Success Criteria

### User Success (Interview Impact)

The demo must achieve these outcomes with the interviewers (CEO Simon Ellis + Senior Developer):

- **"This person gets MCP"** - Working MCP server with 6+ tools, properly structured following the protocol specification
- **"They understand agents"** - LangGraph routing between HR/EWA/Policy agents with clear state management
- **"Production thinking"** - Comprehensive comments explaining local implementation vs production architecture differences
- **"They care about our users"** - Multi-language support for South African frontline workers (isiZulu, isiXhosa, Afrikaans)
- **"Domain knowledge"** - Realistic HR/EWA scenarios that match Jem's actual product offering

### Business Success

- **Primary Outcome:** Receive job offer from Jem HR
- **Secondary Outcome:** Portfolio piece showcasing AI-native architecture patterns

### Technical Success

| Component | Success Criteria |
|-----------|------------------|
| MCP Server | All 6 tools callable with proper error handling and typed responses |
| LangGraph | Intent routing works, state flows correctly between nodes |
| RAG | Policy retrieval returns relevant chunks with source citations |
| Translation | NLLB model loads successfully, translates between English and SA languages |
| CLI Demo | Smooth demo flow with rich terminal formatting, no crashes |
| Database | Auto-seeds on first run, queries return correct data |

### Measurable Outcomes

- Demo runs end-to-end without errors
- Can show 3 different demo scenarios (English HR query, isiZulu EWA request, Policy question)
- Code is clean, well-commented, and explainable in interview context
- Can articulate local vs production architecture decisions for any component

## Product Scope

### MVP - Minimum Viable Product

Must ship tonight:

1. **Database Layer**
   - SQLite with schema for employees, leave_balances, timesheets, ewa_transactions
   - Auto-seed with 12 realistic SA employee profiles
   - Connection utilities

2. **MCP Server**
   - 6 core tools: get_employee, get_leave_balance, submit_leave_request, get_payslip, check_ewa_eligibility, request_ewa_advance
   - Proper MCP protocol implementation
   - Tool for policy search (RAG integration)

3. **LangGraph Orchestrator**
   - State schema with messages, language, employee_id, intent
   - Language detection node
   - Intent router node
   - HR agent, EWA agent, Policy RAG nodes
   - Response formatting node

4. **Policy RAG**
   - ChromaDB vector store (embedded)
   - Leave policy and EWA policy documents indexed
   - Retrieval with source citations

5. **CLI Demo Interface**
   - Rich terminal formatting
   - Employee context selection
   - Conversation loop

### Growth Features (Should Have)

- NLLB multi-language support (isiZulu, isiXhosa, Afrikaans translation)
- Comprehensive code comments explaining local vs production patterns
- Error handling with graceful degradation

### Vision (Future / If Time Permits)

- Claude Desktop MCP configuration for native integration
- Conversation memory with PostgreSQL checkpointing
- Simple web UI alternative to CLI

## User Personas

### Employee Profiles (12)

| # | Name | Department | Language | Hourly Rate | Scenario Focus |
|---|------|------------|----------|-------------|----------------|
| 1 | Sipho Dlamini | Retail - Checkers Sandton | isiZulu | R48.50 | EWA request (happy path) |
| 2 | Thandiwe Nkosi | Security - Fidelity Rosebank | isiXhosa | R42.00 | Has outstanding EWA balance |
| 3 | Johan van der Berg | Warehouse - DHL Johannesburg | Afrikaans | R55.00 | Used most of his leave |
| 4 | Lerato Molefe | Call Centre - Vodacom | Sepedi | R38.00 | Still in probation (EWA ineligible) |
| 5 | Nomvula Sithole | Hospitality - Hilton Sandton | English | R45.00 | Leave balance check |
| 6 | Thabo Mokoena | Mining - Anglo American | Sesotho | R85.00 | High earner, max EWA request |
| 7 | Precious Ndlovu | Fast Food - McDonald's | isiZulu | R35.00 | New employee, first EWA |
| 8 | Pieter Botha | Logistics - Shoprite DC | Afrikaans | R52.00 | Policy question about sick leave |
| 9 | Lindiwe Khumalo | Healthcare - Netcare | isiXhosa | R65.00 | Family responsibility leave |
| 10 | David Okonkwo | Manufacturing - Toyota | English | R58.00 | Night shift worker, overtime |
| 11 | Ayanda Zulu | Cleaning - Bidvest | isiZulu | R32.00 | Minimum wage, small EWA |
| 12 | Maria van Wyk | Restaurant - Spur | Afrikaans | R40.00 | Part-time, leave accrual question |

## User Journeys

### Journey 1: Sipho's Urgent EWA Request (isiZulu - Happy Path)

**Opening Scene:**
Sipho Dlamini is a sales assistant at Checkers Sandton. It's the 10th of the month, and his daughter's school fees are due tomorrow. He's already worked 11 days this pay period but won't get paid until the 25th.

**Rising Action:**
Sipho opens WhatsApp and messages the Jem bot: *"Sawubona, ngifuna ukuthola imali yami ngaphambi kosuku lokuhola"* (Hello, I want to get my money before payday)

The agent detects isiZulu, routes to the EWA agent, checks his eligibility:
- 88 hours worked ✓
- Probation complete ✓
- No outstanding balance ✓
- Earned R4,268, can access R2,134 (50%)

**Climax:**
The agent responds in isiZulu with his options. Sipho requests R1,500. The agent confirms, shows the R10 fee, and processes immediately.

**Resolution:**
Within minutes, R1,490 hits Sipho's account ending in 4521. He pays the school fees on time. His next payslip will show the automatic deduction.

**Capabilities Revealed:** Language detection, EWA eligibility calculation, transaction processing, multilingual response

---

### Journey 2: Lerato's EWA Rejection (Sepedi - Edge Case)

**Opening Scene:**
Lerato Molefe just started at Vodacom's call centre 6 weeks ago. She's heard colleagues talk about getting early access to wages and wants to try it.

**Rising Action:**
She messages: *"Ke nyaka go hwetša mašeleng a ka pele ga letšatši la go lefša"* (I want to get my money before payday)

The agent detects Sepedi, routes to EWA agent, checks eligibility:
- Probation complete: ❌ (only 6 weeks, needs 3 months)

**Climax:**
The agent responds in Sepedi, explaining she's not yet eligible: *"O swanetše go fetša dikgwedi tše 3 tša go lekwa pele o ka šomiša EWA. O na le dibeke tše 6 tše di šetšego."*

**Resolution:**
Lerato understands the policy. She's not frustrated because the response was clear and in her language. She knows to try again in 6 weeks.

**Capabilities Revealed:** Graceful rejection handling, probation check, multilingual error messaging

---

### Journey 3: Pieter's Policy Question (Afrikaans - RAG)

**Opening Scene:**
Pieter Botha is a forklift operator at Shoprite's distribution centre. He's been sick for 3 days and is worried about needing a doctor's note.

**Rising Action:**
He messages: *"Hoeveel dae kan ek siek wees sonder 'n doktersbrief?"* (How many days can I be sick without a doctor's note?)

The agent detects Afrikaans, routes to Policy RAG, searches the sick leave policy.

**Climax:**
The RAG retrieves the relevant section: "Medical certificate required for absences exceeding 2 consecutive days."

The agent responds in Afrikaans: *"Volgens die Siekteverlofbeleid (Afdeling 2): 'n Mediese sertifikaat word benodig vir afwesighede van meer as 2 opeenvolgende dae. Aangesien jy 3 dae siek was, sal jy 'n doktersbrief nodig hê."*

**Resolution:**
Pieter knows he needs the certificate. He goes to the clinic that afternoon.

**Capabilities Revealed:** RAG policy retrieval, citation of source, multilingual policy explanation

---

### Journey 4: Nomvula's Leave Balance (English - HR Query)

**Opening Scene:**
Nomvula Sithole is planning her December holiday. She's a receptionist at Hilton Sandton and wants to know how many days she can take.

**Rising Action:**
She messages: "Hi, how many leave days do I have left?"

The agent detects English, routes to HR agent, queries leave balance.

**Climax:**
The agent retrieves her balance:
- Annual: 9 days remaining
- Sick: 7 days remaining
- Family: 2 days remaining

**Resolution:**
Nomvula can plan her 9-day December trip confidently. She asks to submit a leave request, which the agent processes.

**Capabilities Revealed:** Leave balance query, multiple leave types, leave request submission

---

### Journey 5: Thandiwe's Outstanding Balance (isiXhosa - Edge Case)

**Opening Scene:**
Thandiwe Nkosi is a security officer at Fidelity. She took an R800 EWA advance last week and wants more.

**Rising Action:**
She messages: *"Ndifuna ukuboleka imali engakumbi"* (I want to borrow more money)

The agent checks her account:
- Outstanding EWA: R800 (disbursed, not yet repaid)
- Earned this period: R4,032
- Available after outstanding: R1,216

**Climax:**
The agent explains in isiXhosa that she still has R800 outstanding, but can access an additional R1,216 if needed.

**Resolution:**
Thandiwe decides to wait until her current advance is repaid next week. She appreciates the transparency.

**Capabilities Revealed:** Outstanding balance tracking, available amount calculation, clear communication

---

### Journey 6: Thabo's Maximum EWA (Sesotho - High Earner)

**Opening Scene:**
Thabo Mokoena works at Anglo American mine. He earns R85/hour and has worked 96 hours (overtime) this period. He needs the maximum possible for a family emergency.

**Rising Action:**
He messages: *"Ke batla chelete e kaalo ka kamoo ke e fumanang"* (I want as much money as I can get)

The agent calculates:
- Earned: R8,160
- 50% available: R4,080
- Capped at: R5,000 max → R4,080 available

**Climax:**
The agent responds in Sesotho with the maximum amount and processes the full R4,080 request.

**Resolution:**
Thabo handles his family emergency. The clear calculation helped him understand exactly what was available.

**Capabilities Revealed:** Overtime calculation, 50% rule, R5,000 cap handling

---

### Journey 7: Lindiwe's Family Leave (isiXhosa - Special Leave Type)

**Opening Scene:**
Lindiwe Khumalo is a nurse at Netcare. Her child is sick and she needs to take family responsibility leave.

**Rising Action:**
She messages: *"Umntwana wam uyagula, ndifuna ikhefu losapho"* (My child is sick, I want family leave)

The agent routes to HR, checks her family responsibility leave balance: 2 days remaining.

**Climax:**
The agent confirms she can take family responsibility leave and asks for the dates. She requests 1 day for tomorrow.

**Resolution:**
Leave request submitted. Lindiwe can care for her child without worrying about annual leave.

**Capabilities Revealed:** Multiple leave types, family responsibility leave policy, request submission

---

### Journey 8: Maria's Part-Time Question (Afrikaans - Policy Edge Case)

**Opening Scene:**
Maria van Wyk works part-time at Spur, 20 hours per week. She's confused about how her leave accrues compared to full-time staff.

**Rising Action:**
She messages: *"Hoe werk verlof vir deeltydse werkers?"* (How does leave work for part-time workers?)

The agent routes to Policy RAG, searches for part-time leave accrual.

**Climax:**
The RAG retrieves: "Part-time employees accrue leave proportionally based on hours worked. 20 hours/week = 50% of full-time accrual."

**Resolution:**
Maria understands she gets 7.5 days per year instead of 15. The policy is now clear.

**Capabilities Revealed:** Policy RAG for edge cases, proportional calculations

---

### Journey Requirements Summary

| Journey | Key Capabilities |
|---------|------------------|
| Sipho (EWA happy path) | Language detection, EWA calculation, transaction processing |
| Lerato (EWA rejection) | Probation check, graceful error handling, multilingual |
| Pieter (Policy question) | RAG retrieval, source citations, Afrikaans response |
| Nomvula (Leave balance) | HR query, multiple leave types, English |
| Thandiwe (Outstanding balance) | Balance tracking, available amount calculation |
| Thabo (Max EWA) | Overtime handling, 50% rule, R5,000 cap |
| Lindiwe (Family leave) | Special leave types, request submission |
| Maria (Part-time policy) | RAG edge cases, proportional rules |

## Innovation & Novel Patterns

### Detected Innovation Areas

| Innovation | Description | Why It Matters |
|------------|-------------|----------------|
| **MCP Server** | Anthropic's Model Context Protocol - standardized way for AI to use tools | Bleeding edge (< 6 months old), exact pattern Jem is adopting |
| **LangGraph Multi-Agent** | State machine orchestration for AI agents with routing | Production-grade agent architecture, not simple chains |
| **Local NLLB Translation** | Meta's No Language Left Behind running locally | Shows understanding of edge inference, SA language support |
| **AI-Native Architecture** | Designed LLM-first, not retrofitted | Demonstrates modern AI engineering thinking |

### Interview Relevance

These innovations directly align with Jem's job requirements:
- MCP is explicitly listed as a required skill
- LangGraph orchestration is their agent architecture
- Multi-language for frontline workers is their core mission
- AI-native thinking is their company identity

### Validation Approach

Each innovation will be validated through the working demo:
- MCP: Tools are discoverable and callable by Claude
- LangGraph: Intents route correctly to specialized agents
- NLLB: Translations are accurate for SA languages
- Architecture: Code comments explain production patterns

## Technical Architecture

### MCP Server Specification

**Transport:** stdio (JSON-RPC via stdin/stdout)

**Tools Exposed:**

| Tool | Input | Output | Description |
|------|-------|--------|-------------|
| `get_employee` | employee_id: str | Employee details | Fetch employee profile |
| `get_leave_balance` | employee_id: str | Leave balances by type | Check remaining leave days |
| `submit_leave_request` | employee_id, start_date, end_date, leave_type | Request ID, status | Submit leave request |
| `get_payslip` | employee_id, month: str | Payslip details | Retrieve payslip data |
| `check_ewa_eligibility` | employee_id: str | Eligibility, max_amount, reason | Check EWA availability |
| `request_ewa_advance` | employee_id, amount: float | Transaction ID, status | Request wage advance |
| `search_policies` | query: str, language: str | Policy text, source | RAG search over HR policies |

### LangGraph State Schema

```python
class AgentState(TypedDict):
    messages: list[BaseMessage]    # Conversation history
    language: str                   # Detected language (en, zu, xh, af)
    employee_id: str | None         # Current employee context
    intent: str                     # Classified intent
    tool_results: dict              # Results from MCP tool calls
    response: str                   # Final formatted response
```

### Technology Stack

| Layer | Technology | Version |
|-------|------------|---------|
| Runtime | Python | 3.11+ |
| MCP | mcp | >= 1.0.0 |
| Agents | langgraph, langchain | >= 0.2.0 |
| LLM | langchain-anthropic | >= 0.3.0 |
| Vector Store | chromadb | >= 0.5.0 |
| Translation | transformers, torch | >= 4.40.0 |
| Database | SQLite + sqlalchemy | >= 2.0.0 |
| CLI | rich | >= 13.0.0 |

### Authentication

- **LLM Access:** `ANTHROPIC_API_KEY` environment variable
- **User Auth:** None (demo context - employee selected at runtime)
- **Production Note:** Would integrate with WhatsApp phone number → employee lookup

### Data Formats

- **MCP Protocol:** JSON-RPC 2.0 over stdio
- **Database:** SQLite with SQLAlchemy ORM
- **Embeddings:** ChromaDB with default sentence-transformers
- **Translation:** NLLB-200 tokenizer format

## Project Scoping & Phased Development

### MVP Strategy & Philosophy

**MVP Approach:** Problem-Solving MVP - Prove technical competency through working demonstration
**Resource Requirements:** Solo developer, one evening, Anthropic API key

### MVP Feature Set (Phase 1) - MUST SHIP

**Core Journeys Supported:**
- Sipho's EWA Request (isiZulu happy path)
- Pieter's Policy Question (Afrikaans RAG)
- Nomvula's Leave Balance (English HR query)

**Must-Have Capabilities:**
1. Database Layer - SQLite with all 12 employee profiles seeded
2. MCP Server - All 7 tools callable with typed responses
3. LangGraph Orchestrator - Intent routing to HR/EWA/Policy agents
4. Policy RAG - ChromaDB with leave and EWA policies
5. CLI Demo - Rich terminal formatting with employee selection

### Post-MVP Features

**Phase 2 (Growth - Tonight if time permits):**
- NLLB multi-language translation (isiZulu, isiXhosa, Afrikaans)
- Comprehensive production-pattern code comments
- Error handling with graceful degradation

**Phase 3 (Vision - Future/Portfolio enhancement):**
- Claude Desktop MCP configuration file
- PostgreSQL conversation checkpointing
- Simple web UI alternative

### Risk Mitigation Strategy

**Technical Risks:**
- NLLB load time → Use distilled-600M, pre-download, fallback to English
- Graph complexity → Keep flat, 5 nodes max, no nested agents

**Demo Risks:**
- Runtime crashes → Extensive try/catch, never show stack traces
- API failures → Cache responses for known demo paths

**Resource Risks:**
- Time pressure → Phase 1 is the hard stop, Phase 2 only if 70% time remaining

## Functional Requirements

### Employee Information

- **FR1:** System can retrieve employee profile details by employee ID
- **FR2:** System can identify employee's preferred language from profile
- **FR3:** System can access employee's current employment status (active, probation, terminated)
- **FR4:** System can retrieve employee's hire date for tenure calculations

### Leave Management

- **FR5:** Employee can view their remaining leave balance by type (annual, sick, family)
- **FR6:** Employee can submit a leave request specifying dates and leave type
- **FR7:** System can validate leave requests against available balance
- **FR8:** System can track leave accrual based on employment type (full-time, part-time)
- **FR9:** System can return leave request status and confirmation

### Earned Wage Access (EWA)

- **FR10:** System can determine if employee is eligible for EWA
- **FR11:** System can calculate hours worked in current pay period
- **FR12:** System can calculate maximum EWA amount (50% of earned, capped at R5,000)
- **FR13:** System can check for outstanding EWA balances
- **FR14:** Employee can request a specific EWA amount
- **FR15:** System can process EWA transactions with fee calculation
- **FR16:** System can enforce probation requirement (3 months) for EWA eligibility

### Payroll Information

- **FR17:** Employee can view payslip details for a specific month
- **FR18:** System can calculate earnings based on hours worked and hourly rate
- **FR19:** System can display deductions including previous EWA advances

### HR Policy Information

- **FR20:** Employee can ask questions about HR policies in natural language
- **FR21:** System can retrieve relevant policy sections based on query
- **FR22:** System can provide source citations with policy responses
- **FR23:** System can answer policy questions about leave rules, EWA terms, and benefits

### Language Support

- **FR24:** System can detect the language of user input (English, isiZulu, isiXhosa, Afrikaans)
- **FR25:** System can respond to users in their detected language
- **FR26:** System can translate policy content to user's language

### Conversation Management

- **FR27:** System can classify user intent (HR query, EWA request, Policy question)
- **FR28:** System can route requests to appropriate specialized agent
- **FR29:** System can maintain employee context throughout conversation
- **FR30:** System can format responses appropriately for CLI display

### Demo Operations

- **FR31:** System can select an employee context for demo purposes
- **FR32:** System can display employee information in formatted terminal output
- **FR33:** System can auto-seed database with sample employee data on first run

## Non-Functional Requirements

### Performance

- **NFR1:** CLI startup (excluding NLLB) completes within 3 seconds
- **NFR2:** NLLB model loads within 30 seconds on first use (acceptable one-time cost)
- **NFR3:** MCP tool invocations return within 500ms (database queries)
- **NFR4:** LangGraph routing decision completes within 200ms
- **NFR5:** Policy RAG retrieval returns within 1 second
- **NFR6:** Full conversation turn (user input → response displayed) completes within 5 seconds (excluding initial NLLB load)

### Reliability

- **NFR7:** System never displays stack traces to user - all errors gracefully handled
- **NFR8:** API failures (Anthropic unavailable) display friendly message and allow retry
- **NFR9:** Database operations use transactions to prevent data corruption
- **NFR10:** NLLB translation failures fall back to English response
- **NFR11:** Demo runs end-to-end without crashes for 30+ minute interview session

### Integration

- **NFR12:** MCP server implements JSON-RPC 2.0 over stdio per MCP specification
- **NFR13:** All 7 MCP tools are discoverable via standard MCP introspection
- **NFR14:** System validates `ANTHROPIC_API_KEY` environment variable on startup
- **NFR15:** ChromaDB operates in embedded mode (no external server required)
- **NFR16:** SQLite database auto-initializes and seeds if not present
