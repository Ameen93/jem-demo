---
stepsCompleted:
  - step-01-validate-prerequisites
  - step-02-design-epics
  - step-03-create-stories
  - step-04-final-validation
status: complete
completedAt: '2026-02-10'
inputDocuments:
  - prd.md
  - architecture.md
---

# Jem HR Interview Demo - Epic Breakdown

## Overview

This document provides the complete epic and story breakdown for Jem HR Interview Demo, decomposing the requirements from the PRD and Architecture into implementable stories.

## Requirements Inventory

### Functional Requirements

- **FR1:** System can retrieve employee profile details by employee ID
- **FR2:** System can identify employee's preferred language from profile
- **FR3:** System can access employee's current employment status (active, probation, terminated)
- **FR4:** System can retrieve employee's hire date for tenure calculations
- **FR5:** Employee can view their remaining leave balance by type (annual, sick, family)
- **FR6:** Employee can submit a leave request specifying dates and leave type
- **FR7:** System can validate leave requests against available balance
- **FR8:** System can track leave accrual based on employment type (full-time, part-time)
- **FR9:** System can return leave request status and confirmation
- **FR10:** System can determine if employee is eligible for EWA
- **FR11:** System can calculate hours worked in current pay period
- **FR12:** System can calculate maximum EWA amount (50% of earned, capped at R5,000)
- **FR13:** System can check for outstanding EWA balances
- **FR14:** Employee can request a specific EWA amount
- **FR15:** System can process EWA transactions with fee calculation
- **FR16:** System can enforce probation requirement (3 months) for EWA eligibility
- **FR17:** Employee can view payslip details for a specific month
- **FR18:** System can calculate earnings based on hours worked and hourly rate
- **FR19:** System can display deductions including previous EWA advances
- **FR20:** Employee can ask questions about HR policies in natural language
- **FR21:** System can retrieve relevant policy sections based on query
- **FR22:** System can provide source citations with policy responses
- **FR23:** System can answer policy questions about leave rules, EWA terms, and benefits
- **FR24:** System can detect the language of user input (English, isiZulu, isiXhosa, Afrikaans)
- **FR25:** System can respond to users in their detected language
- **FR26:** System can translate policy content to user's language
- **FR27:** System can classify user intent (HR query, EWA request, Policy question)
- **FR28:** System can route requests to appropriate specialized agent
- **FR29:** System can maintain employee context throughout conversation
- **FR30:** System can format responses appropriately for CLI display
- **FR31:** System can select an employee context for demo purposes
- **FR32:** System can display employee information in formatted terminal output
- **FR33:** System can auto-seed database with sample employee data on first run

### Non-Functional Requirements

- **NFR1:** CLI startup (excluding NLLB) completes within 3 seconds
- **NFR2:** NLLB model loads within 30 seconds on first use
- **NFR3:** MCP tool invocations return within 500ms
- **NFR4:** LangGraph routing decision completes within 200ms
- **NFR5:** Policy RAG retrieval returns within 1 second
- **NFR6:** Full conversation turn completes within 5 seconds
- **NFR7:** System never displays stack traces to user
- **NFR8:** API failures display friendly message and allow retry
- **NFR9:** Database operations use transactions
- **NFR10:** NLLB translation failures fall back to English
- **NFR11:** Demo runs without crashes for 30+ minutes
- **NFR12:** MCP server implements JSON-RPC 2.0 over stdio
- **NFR13:** All 7 MCP tools are discoverable via MCP introspection
- **NFR14:** System validates ANTHROPIC_API_KEY on startup
- **NFR15:** ChromaDB operates in embedded mode
- **NFR16:** SQLite database auto-initializes and seeds if not present

### Additional Requirements (from Architecture)

- **AR1:** Project uses Python 3.11+ with uv package manager
- **AR2:** Dependencies: mcp, langgraph, langchain-anthropic, chromadb, sqlalchemy, rich, python-dotenv
- **AR3:** Custom project structure (no starter template)
- **AR4:** Error handling at boundaries pattern (try/catch in MCP tools and LangGraph nodes)
- **AR5:** Immutable state updates in LangGraph (spread operator pattern)
- **AR6:** PEP 8 naming conventions throughout
- **AR7:** MCP tool response format: `{"success": bool, "data"|"error": ...}`
- **AR8:** Logging with Python logging module (no print statements)

### FR Coverage Map

| FR | Epic | Description |
|----|------|-------------|
| FR1-4 | Epic 1 | Employee profile and status |
| FR5-9 | Epic 2 | Leave management |
| FR10-16 | Epic 3 | EWA operations |
| FR17-19 | Epic 2 | Payroll/payslips |
| FR20-23 | Epic 4 | Policy RAG |
| FR24-26 | Epic 7 | Language support |
| FR27-29 | Epic 5 | Conversation routing |
| FR30-32 | Epic 6 | Demo CLI |
| FR33 | Epic 1 | Auto-seed database |

## Epic List

### Epic 1: Foundation & Employee Data
**Goal:** Users can view employee profiles with all relevant data for demo scenarios.
**FRs covered:** FR1, FR2, FR3, FR4, FR33

### Epic 2: HR Query Tools
**Goal:** Users can check leave balances, submit leave requests, and view payslips.
**FRs covered:** FR5, FR6, FR7, FR8, FR9, FR17, FR18, FR19

### Epic 3: EWA Tools
**Goal:** Users can check EWA eligibility, see available amounts, and request wage advances.
**FRs covered:** FR10, FR11, FR12, FR13, FR14, FR15, FR16

### Epic 4: Policy Q&A System
**Goal:** Users can ask HR policy questions and receive answers with source citations.
**FRs covered:** FR20, FR21, FR22, FR23

### Epic 5: Intelligent Routing
**Goal:** User messages are automatically classified and routed to the correct agent.
**FRs covered:** FR27, FR28, FR29

### Epic 6: Demo Experience
**Goal:** Complete CLI demo with employee selection and formatted conversation loop.
**FRs covered:** FR30, FR31, FR32

### Epic 7: Multi-Language Support (Phase 2)
**Goal:** Users can interact in isiZulu, isiXhosa, or Afrikaans with translated responses.
**FRs covered:** FR24, FR25, FR26

---

## Epic 1: Foundation & Employee Data

**Goal:** Users can view employee profiles with all relevant data for demo scenarios.

### Story 1.1: Project Scaffolding

As a **developer**,
I want **a properly structured Python project with all dependencies**,
So that **I can begin implementing features immediately**.

**Acceptance Criteria:**

**Given** the project directory exists
**When** I run `uv init && uv add mcp langgraph langchain-anthropic chromadb sqlalchemy rich python-dotenv`
**Then** the project has pyproject.toml with all dependencies
**And** the src/ directory structure matches the architecture document
**And** .env.example contains ANTHROPIC_API_KEY placeholder

### Story 1.2: Database Models

As a **system**,
I want **SQLAlchemy models for employees, leave, timesheets, and EWA transactions**,
So that **I can persist and query HR data**.

**Acceptance Criteria:**

**Given** SQLAlchemy is installed
**When** I import the models module
**Then** Employee model has: id, name, department, role, hire_date, hourly_rate, preferred_language, bank_account_last4, employment_status
**And** LeaveBalance model has: employee_id, leave_type, balance_days, accrued_ytd, used_ytd
**And** Timesheet model has: employee_id, pay_period_start, pay_period_end, hours_worked, status
**And** EWATransaction model has: id, employee_id, amount, fee, status, requested_at, disbursed_at

### Story 1.3: Database Seeding

As a **demo user**,
I want **12 realistic SA employee profiles auto-seeded on first run**,
So that **I have data for demo scenarios**.

**Acceptance Criteria:**

**Given** the database does not exist
**When** I call seed_database()
**Then** 12 employees are created matching PRD personas (Sipho, Thandiwe, Johan, etc.)
**And** each employee has appropriate leave balances
**And** each employee has timesheet entries for current pay period
**And** some employees have outstanding EWA transactions per their scenario

### Story 1.4: Get Employee MCP Tool

As a **calling agent**,
I want **to retrieve employee profile details via MCP tool**,
So that **I can display employee information**.

**Acceptance Criteria:**

**Given** an employee exists with id "EMP001"
**When** I call get_employee(employee_id="EMP001")
**Then** I receive `{"success": true, "data": {employee details}}`
**And** data includes name, department, role, hire_date, preferred_language, employment_status

**Given** an employee does not exist
**When** I call get_employee(employee_id="INVALID")
**Then** I receive `{"success": false, "error": "Employee not found", "code": "NOT_FOUND"}`

---

## Epic 2: HR Query Tools

**Goal:** Users can check leave balances, submit leave requests, and view payslips.

### Story 2.1: Get Leave Balance Tool

As an **employee**,
I want **to check my remaining leave days by type**,
So that **I can plan my time off**.

**Acceptance Criteria:**

**Given** employee "EMP005" (Nomvula) exists with leave balances
**When** I call get_leave_balance(employee_id="EMP005")
**Then** I receive `{"success": true, "data": {"annual": 9, "sick": 7, "family": 2}}`

### Story 2.2: Submit Leave Request Tool

As an **employee**,
I want **to submit a leave request for specific dates**,
So that **I can take time off**.

**Acceptance Criteria:**

**Given** employee has sufficient annual leave balance
**When** I call submit_leave_request(employee_id, start_date, end_date, leave_type="annual")
**Then** leave balance is reduced by the number of days
**And** I receive `{"success": true, "data": {"request_id": "...", "status": "approved", "days": N}}`

**Given** employee has insufficient balance
**When** I call submit_leave_request with more days than available
**Then** I receive `{"success": false, "error": "Insufficient leave balance", "code": "INSUFFICIENT_BALANCE"}`

### Story 2.3: Get Payslip Tool

As an **employee**,
I want **to view my payslip for a specific month**,
So that **I can see my earnings and deductions**.

**Acceptance Criteria:**

**Given** employee has timesheet entries for the month
**When** I call get_payslip(employee_id, month="2026-02")
**Then** I receive earnings calculated from hours × hourly_rate
**And** I receive any EWA deductions from that period
**And** I receive net pay after deductions

---

## Epic 3: EWA Tools

**Goal:** Users can check EWA eligibility, see available amounts, and request wage advances.

### Story 3.1: Check EWA Eligibility Tool

As an **employee**,
I want **to check if I'm eligible for an earned wage advance**,
So that **I know how much I can access**.

**Acceptance Criteria:**

**Given** Sipho (EMP001) has worked 88 hours, completed probation, no outstanding balance
**When** I call check_ewa_eligibility(employee_id="EMP001")
**Then** I receive `{"success": true, "data": {"eligible": true, "earned": 4268, "available": 2134, "outstanding": 0}}`

**Given** Lerato (EMP004) is still in probation (6 weeks)
**When** I call check_ewa_eligibility(employee_id="EMP004")
**Then** I receive `{"success": true, "data": {"eligible": false, "reason": "Probation not complete", "weeks_remaining": 6}}`

**Given** Thandiwe (EMP002) has R800 outstanding
**When** I call check_ewa_eligibility(employee_id="EMP002")
**Then** available amount is reduced by outstanding balance

### Story 3.2: Request EWA Advance Tool

As an **employee**,
I want **to request a specific amount as an advance**,
So that **I can access my earned wages early**.

**Acceptance Criteria:**

**Given** employee is eligible with R2,134 available
**When** I call request_ewa_advance(employee_id, amount=1500)
**Then** EWA transaction is created with amount=1500, fee=10, status="disbursed"
**And** I receive `{"success": true, "data": {"transaction_id": "...", "amount": 1500, "fee": 10, "net": 1490}}`

**Given** employee requests more than available
**When** I call request_ewa_advance(employee_id, amount=5000)
**Then** I receive `{"success": false, "error": "Amount exceeds available balance", "code": "EXCEEDS_AVAILABLE"}`

---

## Epic 4: Policy Q&A System

**Goal:** Users can ask HR policy questions and receive answers with source citations.

### Story 4.1: Policy Documents

As a **system**,
I want **leave and EWA policy documents in data/policies/**,
So that **they can be indexed for RAG retrieval**.

**Acceptance Criteria:**

**Given** the data/policies/ directory exists
**When** I check the contents
**Then** leave_policy.md contains annual leave rules, sick leave rules, family leave rules
**And** ewa_policy.md contains eligibility, limits, fees, repayment terms

### Story 4.2: Policy Indexing

As a **system**,
I want **policies indexed in ChromaDB on startup**,
So that **I can retrieve relevant sections for queries**.

**Acceptance Criteria:**

**Given** ChromaDB is configured for embedded mode
**When** I call index_policies()
**Then** both policy documents are embedded and stored
**And** the chroma/ directory persists the index

### Story 4.3: Search Policies Tool

As an **employee**,
I want **to ask HR policy questions in natural language**,
So that **I understand company policies**.

**Acceptance Criteria:**

**Given** policies are indexed
**When** I call search_policies(query="How many sick days without a doctor's note?")
**Then** I receive relevant policy text about sick leave
**And** I receive source citation (e.g., "Sick Leave Policy, Section 2")

---

## Epic 5: Intelligent Routing

**Goal:** User messages are automatically classified and routed to the correct agent.

### Story 5.1: LangGraph State and Structure

As a **system**,
I want **an AgentState TypedDict and compiled graph**,
So that **state flows correctly between nodes**.

**Acceptance Criteria:**

**Given** LangGraph is installed
**When** I import the graph module
**Then** AgentState has: messages, language, employee_id, employee, intent, tool_results, response, error
**And** the graph compiles without errors

### Story 5.2: Language Detection Node

As a **system**,
I want **to detect the user's language from their message**,
So that **I can respond in the same language**.

**Acceptance Criteria:**

**Given** user sends "Sawubona, ngifuna imali"
**When** the language_detect node runs
**Then** state.language = "zu"

**Given** user sends "How many leave days?"
**When** the language_detect node runs
**Then** state.language = "en"

### Story 5.3: Intent Router Node

As a **system**,
I want **to classify user intent and route to the right agent**,
So that **requests are handled by specialists**.

**Acceptance Criteria:**

**Given** user asks about leave balance
**When** intent_router runs
**Then** state.intent = "hr_query" and routes to hr_agent

**Given** user asks about early wage access
**When** intent_router runs
**Then** state.intent = "ewa_request" and routes to ewa_agent

**Given** user asks about policy rules
**When** intent_router runs
**Then** state.intent = "policy_question" and routes to policy_rag

### Story 5.4: HR Agent Node

As a **system**,
I want **an HR agent that calls leave and payslip tools**,
So that **HR queries are answered**.

**Acceptance Criteria:**

**Given** intent is "hr_query" and user asks about leave
**When** hr_agent runs
**Then** it calls get_leave_balance and stores result in state.tool_results

### Story 5.5: EWA Agent Node

As a **system**,
I want **an EWA agent that handles eligibility and advances**,
So that **EWA requests are processed**.

**Acceptance Criteria:**

**Given** intent is "ewa_request"
**When** ewa_agent runs
**Then** it calls check_ewa_eligibility or request_ewa_advance based on context

### Story 5.6: Policy RAG Node

As a **system**,
I want **a policy node that retrieves and answers policy questions**,
So that **policy queries get cited answers**.

**Acceptance Criteria:**

**Given** intent is "policy_question"
**When** policy_rag node runs
**Then** it calls search_policies and formats response with citation

### Story 5.7: Response Format Node

As a **system**,
I want **responses formatted appropriately for the detected language**,
So that **users receive natural responses**.

**Acceptance Criteria:**

**Given** tool_results exist and language is detected
**When** response_format runs
**Then** state.response contains a natural language answer
**And** response is in the user's detected language (Phase 1: English only)

---

## Epic 6: Demo Experience

**Goal:** Complete CLI demo with employee selection and formatted conversation loop.

### Story 6.1: CLI with Rich Formatting

As a **demo presenter**,
I want **a beautiful terminal interface with Rich formatting**,
So that **the demo looks professional**.

**Acceptance Criteria:**

**Given** Rich is installed
**When** I run the demo script
**Then** output uses Rich panels, tables, and colors
**And** employee info displays in formatted tables
**And** conversation has clear visual separation

### Story 6.2: Employee Selection Flow

As a **demo presenter**,
I want **to select an employee context at the start**,
So that **I can demonstrate different scenarios**.

**Acceptance Criteria:**

**Given** the demo starts
**When** I see the employee list
**Then** all 12 employees are shown with name, department, scenario focus
**And** I can select an employee by number
**And** the selected employee's context is set for the conversation

### Story 6.3: Conversation Loop

As a **demo presenter**,
I want **a conversation loop that processes messages through the graph**,
So that **I can demonstrate the full agent flow**.

**Acceptance Criteria:**

**Given** an employee is selected
**When** I type a message and press enter
**Then** the message is processed through the LangGraph
**And** the response is displayed with Rich formatting
**And** I can continue the conversation or type 'exit' to quit

---

## Epic 7: Multi-Language Support (Phase 2)

**Goal:** Users can interact in isiZulu, isiXhosa, or Afrikaans with translated responses.

### Story 7.1: NLLB Model Loading

As a **system**,
I want **NLLB-200-distilled-600M loaded for translation**,
So that **I can translate between languages**.

**Acceptance Criteria:**

**Given** transformers and torch are installed
**When** I initialize the translator
**Then** the NLLB model loads (within 30 seconds)
**And** if loading fails, the system falls back to English-only mode

### Story 7.2: Language Detection Enhancement

As a **system**,
I want **robust language detection for SA languages**,
So that **I correctly identify isiZulu, isiXhosa, Afrikaans, Sepedi, Sesotho**.

**Acceptance Criteria:**

**Given** NLLB is loaded
**When** user sends isiZulu text
**Then** language is detected as "zul_Latn"

### Story 7.3: Response Translation

As a **system**,
I want **responses translated to the user's language**,
So that **users receive answers in their preferred language**.

**Acceptance Criteria:**

**Given** response is in English and user language is isiZulu
**When** response_format runs
**Then** response is translated to isiZulu via NLLB
**And** translation failures fall back to English

---

## Story Summary

| Epic | Stories | FRs Covered |
|------|---------|-------------|
| Epic 1: Foundation | 4 | FR1-4, FR33 |
| Epic 2: HR Tools | 3 | FR5-9, FR17-19 |
| Epic 3: EWA Tools | 2 | FR10-16 |
| Epic 4: Policy RAG | 3 | FR20-23 |
| Epic 5: Routing | 7 | FR27-29 |
| Epic 6: Demo CLI | 3 | FR30-32 |
| Epic 7: Language | 3 | FR24-26 |
| **Total** | **25 stories** | **All 33 FRs** |
