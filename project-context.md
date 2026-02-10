# Jem HR Interview Demo - Project Context

This file contains rules and context for AI agents working on this project.

## Project Overview

- **Project:** Jem HR Interview Demo
- **Purpose:** Technical interview demo for Jem HR (Senior Product Engineer role)
- **Stack:** Python 3.11+, MCP, LangGraph, ChromaDB, SQLite, Rich

## Documentation

- PRD: `docs/prd.md`
- Architecture: `docs/architecture.md`
- Epics & Stories: `docs/epics.md`

## Development Workflow

### Story Development Process

For each story, follow this workflow exactly:

#### 1. Start Story - Create Branch

```bash
# Branch naming: story/{epic}-{story}-{short-description}
git checkout main
git pull origin main
git checkout -b story/1-1-project-scaffolding
```

#### 2. Implement Story

- Follow the acceptance criteria in `docs/epics.md`
- Follow patterns defined in `docs/architecture.md`
- Commit frequently with clear messages

#### 3. Local Code Review with Codex

Before pushing, run a local code review:

```bash
# Use Codex to review the changes
codex review
```

Address any issues identified by Codex before proceeding.

#### 4. Push to GitHub

```bash
git push -u origin story/1-1-project-scaffolding
```

#### 5. Wait for CI Tests

- Wait for GitHub Actions / CI tests to pass
- If tests fail, fix locally and push again
- Do NOT proceed until all checks pass

#### 6. Merge and Cleanup

```bash
# After CI passes, merge to main
git checkout main
git pull origin main
git merge story/1-1-project-scaffolding
git push origin main
git branch -d story/1-1-project-scaffolding
git push origin --delete story/1-1-project-scaffolding
```

#### 7. Next Story

- Mark current story as complete
- Proceed to next story in sequence
- Repeat from step 1

### Branch Naming Convention

```
story/{epic_number}-{story_number}-{short-description}
```

Examples:
- `story/1-1-project-scaffolding`
- `story/1-2-database-models`
- `story/2-1-leave-balance-tool`
- `story/5-3-intent-router`

### Commit Message Format

```
{type}: {short description}

{optional body with details}

Story: {epic}.{story}
```

Types: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`

Example:
```
feat: add Employee SQLAlchemy model

- Added Employee model with all fields per architecture doc
- Added LeaveBalance, Timesheet, EWATransaction models
- Created connection.py with get_engine() and get_session()

Story: 1.2
```

## Code Standards

- Follow PEP 8 naming conventions
- Use type hints throughout
- MCP tool response format: `{"success": bool, "data"|"error": ...}`
- Error handling at boundaries (try/catch in tools and nodes)
- Use logging module, never print()
- Immutable state updates in LangGraph

## Testing

- Run tests before pushing: `pytest`
- Ensure all MCP tools are testable
- Test edge cases defined in acceptance criteria

## Environment

Required environment variables:
- `ANTHROPIC_API_KEY` - For Claude API access

Optional:
- `LOG_LEVEL` - Logging verbosity (default: INFO)
