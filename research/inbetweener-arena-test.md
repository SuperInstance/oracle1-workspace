# Inbetweener Pattern Test

## Storyboard

Here are three arena improvement designs for AI agent training:

**1. King-of-Hill Match Mode**

* **Data Structures:**
	+ `Agent` table with columns for `id`, `name`, `score`, and `current_match_id`
	+ `Match` table with columns for `id`, `winner_id`, and `loser_id`
* **API Endpoints:**
	+ `POST /match`: Create a new match between the current king (top-ranked agent) and a challenger (randomly selected agent)
	+ `PATCH /match/{id}`: Update the match winner and loser
	+ `GET /leaderboard`: Retrieve the current leaderboard with agent scores
* **Skill Improvement Mechanism:** Agents that win matches against the current king earn a score bonus, while losers receive a score penalty. This encourages agents to improve their strategies to defeat the current king and take their place.

**2. Swiss Tournament Bracket**

* **Data Structures:**
	+ `Agent` table with columns for `id`, `name`, and `wins`
	+ `Match` table with columns for `id`, `agent1_id`, `agent2_id`, and `winner_id`
	+ `Tournament` table with columns for `id`, `name`, and `matches` (array of match IDs)
* **API Endpoints:**
	+ `POST /tournament`: Create a new Swiss tournament bracket with a specified number of agents
	+ `GET /tournament/{id}/matches`: Retrieve the matches for a specific tournament
	+ `PATCH /match/{id}`: Update the match winner
* **Skill Improvement Mechanism:** Agents earn points for winning matches, and the agent with the most points at the end of the tournament is declared the winner. This encourages agents to improve their strategies to win as many matches as possible.

**3. Winner-Teaches-Loser Feedback Loop**

* **Data Structures:**
	+ `Agent` table with columns for `id`, `name`, and `knowledge_graph` (graph data structure representing agent's knowledge)
	+ `Match` table with columns for `id`, `winner_id`, `loser_id`, and `feedback_data` (data representing the winner's strategy)
* **API Endpoints:**
	+ `POST /match`: Create a new match between two agents
	+ `PATCH /match/{id}`: Update the match winner and feedback data
	+ `GET /agent/{id}/knowledge_graph`: Retrieve an agent's knowledge graph
* **Skill Improvement Mechanism:** After a match, the winner shares its strategy (represented as feedback data) with the loser, who incorporates this knowledge into its own knowledge graph. This encourages agents to learn from each other's strengths and weaknesses.

## Decomposition Option 1: Top-down (schemas first)

# Top-Down Implementation Task Breakdown (Schemas First)
## Complexity Key
- **S**: Small (straightforward, single focused task: boilerplate, simple CRUD, basic validations)
- **M**: Medium (includes business logic, multiple database queries, standard integration work)
- **L**: Large (complex algorithms, cross-component coordination, large-scale setup)

---

## Layer 1: Foundational Schema & Infrastructure (Starting Point per Requirements)
### Task 1.1: Base Schema & Dev Tooling Setup
**Associated Files**:
`pyproject.toml`/`package.json`, `docker-compose.yml` (local DB), `.env.example`, `alembbic/` (migrations tooling)
**Work**:
1.  Define project dependencies (ORM, API framework, DB tooling)
2.  Set up local development database stack
3.  Configure shared DB migration tooling (Alembic/Drizzle) and base schema primitives (UUID primary keys, `created_at`/`updated_at` timestamps)
**Complexity**: S
**Dependencies**: None (project bootstrapping only)

---
### Task 1.2: Universal Agent Database & API Schema
**Associated Files**:
`src/db/models/agent.py`, `src/db/schemas/agent.py`, DB migration file
**Work**:
1.  Create core `Agent` table with mandatory `id` and `name` fields
2.  Add extensible optional fields: `score` (King of Hill), `wins` (Swiss Tournament), `current_match_id` (King of Hill)
3.  Build Pydantic/REST API schemas for agent data responses and requests
**Complexity**: S
**Dependencies**: Task 1.1

---

## Layer 2: Mode-Specific Data Models
### Task 2.1: King of the Hill (KoH) Match Schema
**Associated Files**:
`src/db/models/koh_match.py`
**Work**:
1.  Define `KoHMatch` table with columns: `id`, `winner_id` (foreign key to `Agent.id`), `loser_id` (foreign key to `Agent.id`)
2.  Add foreign key constraints to prevent invalid agent references
**Complexity**: S
**Dependencies**: Task 1.2

---
### Task 2.2: Swiss Tournament Schema
**Associated Files**:
`src/db/models/swiss_match.py`, `src/db/models/tournament.py`
**Work**:
1.  Define `SwissMatch` table with `id`, `agent1_id`, `agent2_id`, `winner_id` (all foreign keys to `Agent.id`)
2.  Define `Tournament` table with `

## Decomposition Option 2: API-first (endpoints first)

# API-First Arena Training Plan Decomposition Tasks
All tasks are ordered by API-first workflow, with clear scope, files, functions, complexity, and dependencies. Complexity ratings:
- **S**: Small (1-2 dev days, boilerplate/standard logic)
- **M**: Medium (3-5 dev days, feature-specific business logic)
- **L**: Large (6+ dev days, complex stateful logic, cross-service coordination)

---

## Phase 1: API Contract Design (API-First Core)
### Task 1: OpenAPI Specification Definition
| File | Functions | Complexity | Dependencies |
|---|---|---|---|
| `docs/openapi-spec.yml` | 1.  Define all standardized endpoints:<br>    - KoH: `POST /match`, `PATCH /match/{id}`, `GET /leaderboard`<br>    - Swiss Tournament: `POST /tournament`, `GET /tournament/{id}/matches`, `PATCH /match/{id}`<br>2.  Standardize request/response schemas (CreateMatchRequest, UpdateMatchRequest, LeaderboardResponse, etc.)<br>3.  Document error codes (400, 404, 409 for conflicts) | M | OpenAPI tooling, Swagger/Redoc for preview |

---

## Phase 2: Shared Infrastructure & Database Setup
### Task 2: Core API & Dependency Boilerplate
| File | Functions | Complexity | Dependencies |
|---|---|---|---|
| `src/api/main.py`, `src/api/dependencies.py`, `src/api/routers/__init__.py` | 1.  Initialize FastAPI app tied to the OpenAPI spec<br>2.  Shared dependencies: `get_db_session`, `get_current_agent` for authenticated agent context<br>3.  Centralized error handling + router stubs for both feature modes | S | FastAPI, Uvicorn, Pydantic, SQLAlchemy/Prisma, python-dotenv |

### Task3: Shared Database ORM & Schema Models
| File | Functions | Complexity | Dependencies |
|---|---|---|---|
| `src/db/models.py`, `src/db/schemas.py` | 1.  Core `Agent` model: `id`, `name`, `score`, `wins`, `current_match_id`<br>2.  Shared `Match` model: `id`, `agent1_id`, `agent2_id`, `winner_id`, `loser_id`, timestamps<br>3.  `Tournament` model: `id`, `name`, `type`, `match_ids`, `status`<br>4.  Pydantic validation schemas aligned to OpenAPI spec | M | SQLAlchemy/Prisma, P

## Decomposition Option 3: Feature-complete (one at a time)

# Organized Implementation Tasks (Feature-Complete One at a Time)
Tasks are grouped first by shared foundational infrastructure, then fully completed King of the Hill (KoH) mode, then fully completed Swiss Tournament mode. Each task includes required files, core functions, complexity sizing, and dependencies:
> Complexity definitions:
> - **S (Small)**: <1 day of work, single developer, minimal cross-component changes
> - **M (Medium)**: 1-3 days of work, small cross-component changes
> - **L (Large)**: 3-7 days of work, complex logic or cross-system changes

---

## Shared Foundational Tasks (Required for Both Modes)
These set up reusable core infrastructure used by both training modes:
1.  ### Task S1: Unified Database Schema & ORM Models
    - **Files**: `src/db/schema.sql`, `src/db/models/agent.py`, `src/db/models/match.py`
    - **Core Functions**:
      - `Agent` model: `get_agent_by_id()`, `list_agents()`, `update_agent_score()`, `update_agent_wins()`, `assign_agent_to_match()`, `remove_agent_from_match()`
      - `Match` model: `create_match()`, `get_match_by_id()`, `update_match_base()`
    - **Complexity**: Medium (M)
    - **Dependencies**: None (initial project setup)
    - Notes: Defines unified tables with all fields needed for both modes:
      - `agents`: `id`, `name`, `score`, `wins`, `current_match_id`
      - `matches`: `id`, `agent1_id`, `agent2_id`, `winner_id`, `loser_id`, `match_type`, `tournament_id`, `created_at`, `updated_at`

2.  ### Task S2: Shared API Utilities & Base Router
    - **Files**: `src/api/main.py`, `src/api/deps.py`, `src/utils/responses.py`
    - **Core Functions**:
      - FastAPI app initialization, database session dependency injection
      - Standardized success/error JSON response handlers
      - Pagination helpers for list endpoints
    - **Complexity**: Small (S)
    - **Dependencies**: Task S1

---

## Phase 1: King of the Hill (Full Feature-Complete First)
All tasks required for a production-ready KoH mode:
3.  ### Task K1: KoH Match Creation Endpoint & Logic
    - **Files**: `src/api/routers/koh.py`, `src/services/koh_match_service.py`
    - **Core Functions**:
      - `get_current_king()`: Fetches top-ranked agent ordered by `score` descending

## Decomposition (Seed-2.0-mini, temp 0.85)

### 5 Implementation Tasks (aligned to KOTH + Swiss + Feedback Loop)
1.  **File**: `arena/match_runtime.py`
    **Function**: `run_head_to_head(model_a, model_b, eval_prompt) -> MatchResult`
    **Complexity**: S
2.  **File**: `arena/koth_manager.py`
    **Function**: `update_koth_champion(challenger_outcome, current_champ) -> AIModel`
    **Complexity**: M
3.  **File**: `arena/swiss_pairing.py`
    **Function**: `generate_swiss_pairs(registered_models, past_matchups) -> list[tuple]`
    **Complexity**: L
4.  **File**: `arena/leaderboard_db.py`
    **Function**: `sync_elo_ratings(match_results) -> dict`
    **Complexity**: M
5.  **File**: `pipelines/feedback_loop.py`
    **Function**: `trigger_model_iteration(qualifying_models, match_history) -> str`
    **Complexity**: L

## Verdict
Pattern works well. Storyboard provides architecture, Seed decomposition gives concrete tasks with complexity estimates.
Best for: medium-complexity features where you need both design vision and implementation granularity.
