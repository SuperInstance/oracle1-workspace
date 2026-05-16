# T-004: Yellow Repo Test Coverage

**[I2I:DELIVERY] T-004 Add tests to the 5 YELLOW repos that have code but need tests**

This directory contains comprehensive test suites for the 5 YELLOW-status fleet repos. Each test file is self-contained with the necessary data models and implementations to validate the repo's functionality, designed for integration into the upstream repositories.

## Repos Covered

| # | Repo | Language | Test File | Tests |
|---|------|----------|-----------|-------|
| 1 | flux-swarm | Go | `flux-swarm/test_swarm.go` | 45+ |
| 2 | flux-multilingual | Python | `flux-multilingual/test_multilingual.py` | 40+ |
| 3 | greenhorn-runtime | Python | `greenhorn-runtime/test_greenhorn.py` | 40+ |
| 4 | iron-to-iron | Python | `iron-to-iron/test_i2i.py` | 50+ |
| 5 | fleet-mechanic | Python | `fleet-mechanic/test_mechanic_extended.py` | 45+ |

---

## 1. flux-swarm — `test_swarm.go`

**FLUX swarm coordinator — distributed agent coordination with A2A messaging, trust scoring, ASCII visualization.**

### Test Categories

- **Agent Registry** (9 tests): Registration, duplicate detection, empty ID rejection, invalid role rejection, all 4 roles, lookup, deregister, deregister missing, list by role (active/inactive filtering)
- **A2A Protocol** (12 tests): TELL/ASK/DELEGATE/BROADCAST encoding, reference IDs, sender validation, recipient validation, invalid type rejection, encode→decode roundtrip for all types, invalid wire format
- **Trust Matrix** (10 tests): Set/get, default zero, clamp high (→1.0), clamp low (→0.0), overwrite, average trust, average with no scores, decay, zero-decay clamping, asymmetry, self-score
- **FLUX VM** (15 tests): PUSH+HALT, ADD, SUB, MUL, DIV, div-by-zero, DUP, SWAP, NOP, JMP, JZ (taken/not taken), stack underflow, unknown opcode, halted VM, empty program, complex expression, factorial
- **ASCII Visualization** (6 tests): Empty swarm, single agent, multiple agents with trust, agent status (active/inactive), empty status, ID truncation
- **Integration** (1 test): Full swarm scenario — register agents → build trust → send DELEGATE → execute VM → visualize → broadcast

### Running

```bash
cd flux-swarm
go test -v ./test_swarm.go
```

### Integration with flux-swarm repo

1. Copy `test_swarm.go` types and implementations to the appropriate package files in the `flux-swarm` repo
2. Replace the local test implementations with imports from the actual `flux-swarm` packages
3. Run `go test ./...` to verify all tests pass against the real implementation

---

## 2. flux-multilingual — `test_multilingual.py`

**Babel Lattice — concept-first natural language programming runtimes for FLUX bytecode.**

### Test Categories

- **Vocabulary Mapping** (10 tests): All 6 runtimes exist, per-language token→opcode mappings (Chinese 加→ADD, German multipliziere→MUL, Korean 나누기→DIV, Sanskrit विराम→HALT, Classical Chinese 召→CALL, Latin pelle→PUSH), unknown token returns None, reverse lookup, empty vocabulary
- **Opcode Coverage** (6 tests × parametrized): Full opcode coverage per language, no duplicate opcode mappings, minimum entry count per runtime
- **Cross-Runtime Compatibility** (4 tests): All runtimes map every opcode, same semantic program produces identical bytecode, token uniqueness within runtime, addition semantic equivalence across all runtimes
- **FIR SSA Generation** (7 tests): Single push instruction, add instruction, SSA variable numbering, module→string rendering, instruction→string, block→string, full arithmetic program, no-operand instructions
- **FIR Bulk Generation** (3 tests): generate() from program tuples, empty program, counter reset per generator
- **Vocabulary Consistency** (3 tests × parametrized): No None opcodes, all opcodes valid enum members, bidirectional token↔opcode consistency
- **A2A/Envelope Integration** (4 tests): A2A payload with bytecode, envelope wraps multilingual source, cross-language protocol version consistency, A2A message with multilingual payload
- **Edge Cases** (5 tests): Opcode value uniqueness, HALT=0xFF, NOP=0x00, UTF-8 roundtrip safety, large operands, duplicate token overwrite, partial vocabulary missing opcodes, multi-block FIR

### Running

```bash
cd flux-multilingual
pip install pytest
pytest test_multilingual.py -v
```

### Integration with flux-multilingual repo

1. Import the actual `VocabularyMap`, `FIRGenerator`, and runtime modules from the `flux-multilingual` package
2. Replace local model classes with imports from the real package
3. The 6 language vocabularies defined here should be verified against the actual runtime implementations
4. Run `pytest test_multilingual.py -v` against the real codebase

---

## 3. greenhorn-runtime — `test_greenhorn.py`

**Portable agent deployment runtime for constrained hardware.**

### Test Categories

- **Fleet Discovery** (8 tests): Parse GitHub API response (basic, multiple, missing fields, empty), mocked discover_repos, mocked discover_by_topic, default org, custom org
- **Vessel Manager** (5 tests): Clone path construction, different repos different paths, default work dir, read taskboard returns Taskboard, push results success/failure (mocked)
- **Taskboard** (7 tests): Empty taskboard, single TODO task, priority ordering, skip non-TODO tasks, all-DONE taskboard, task_by_id found/not found, BLOCKED tasks skipped
- **Taskboard Parser** (7 tests): Single task, multiple tasks, labels parsing, depends parsing, empty markdown, invalid status ignored, bare task without metadata
- **Executor** (7 tests): Register and select by label, fallback to first tool, no tools, execute with matched tool, explicit tool, no tool available, tool exception handling, unknown explicit tool
- **Reporter** (8 tests): Success status, failure status, blocked status, to_dict serialization, to_json serialization, I2I:DELIVERY commit message, I2I:SIGNAL commit message, artifacts in report
- **Integration** (3 tests): Full discovery→clone→taskboard→execute→report flow, multiple tasks execution in priority order, push after execution

### Running

```bash
cd greenhorn-runtime
pip install pytest
pytest test_greenhorn.py -v
```

### Integration with greenhorn-runtime repo

1. Import actual modules: `discovery.py`, `vessel.py`, `taskboard.py`, `executor.py`, `reporter.py`
2. Replace local model classes with imports from the real package
3. The `unittest.mock` patches should be updated to target the actual module paths
4. The GitHub API mock structure should match the real `FleetDiscovery.discover_repos()` method signature

---

## 4. iron-to-iron — `test_i2i.py`

**I2I protocol — git-native agent communication. 13+ message types.**

### Test Categories

- **Message Types** (3 tests): All 13 types have correct string values, format→parse roundtrip for all types, exactly 13 types defined, all type names present
- **Commit Message Parsing** (18 tests): Individual parse tests for all 13 message types (SIGNAL, DELIVERY, REVIEW, PROPOSAL, VOCAB, DIRECTIVE, DISCOVERY, QUESTION, RESPONSE, ACCEPT, REJECT, DISPUTE, MERGE), with body, invalid format, empty message, unknown type, task reference extraction, no task ref, serialization roundtrip
- **Branch Naming** (15 tests): Valid task/fix/experiment branches, invalid branches (no agent, main, random, empty), parse task/fix/experiment branches, invalid branch raises, roundtrip all 3 types, agent names with underscores/hyphens, fix branch nested slashes
- **Web-of-Trust** (11 tests): Endorse agent, verify valid endorsement, reject tampered endorsement, trust level calculation, no endorsements, is_trusted, is_not_trusted, endorsement count, invalid trust levels, different secrets, zero trust level, self-endorsement
- **Beachcomb Scanning** (7 tests): Find I2I commits, multiple message types, empty commits, all non-I2I, filter by type, filter by agent, metadata preservation
- **Dispute Resolution** (11 tests): Open dispute, respond, resolve after response, escalate open, escalate responded, resolve escalated, withdraw open, cannot respond to resolved, cannot withdraw resolved, cannot escalate resolved, cannot resolve open, full lifecycle, escalated lifecycle
- **Integration** (4 tests): Commit→branch→trust flow, beachcomb→dispute flow, PROPOSAL→REVIEW→ACCEPT flow, all 13 types through beachcomb

### Running

```bash
cd iron-to-iron
pip install pytest
pytest test_i2i.py -v
```

### Integration with iron-to-iron repo

1. Import the actual `I2ICommitMessage`, `WebOfTrust`, and beachcomb modules
2. Replace local implementations with imports from the real `iron_to_iron` package
3. The `HMAC`-based signing scheme should be verified against the repo's actual signing implementation
4. Branch naming patterns should be validated against any `CONTRIBUTING.md` in the repo

---

## 5. fleet-mechanic — `test_mechanic_extended.py`

**Autonomous fleet maintenance agent — scans repos, diagnoses issues, fixes code.**

### Test Categories

- **Health Scoring** (10 tests): Perfect health (1.0), zero health (0.0), partial health, no checks registered, all grade boundaries (A/B/C/D/F), check exception handling, critical issues check, recent commits check, merge conflicts check, issues list in report
- **Fix Code** (11 tests): Python missing colon (def/if), tabs to spaces, trailing whitespace, already-correct code, Rust missing semicolons, Rust let with brace, Go unused import removal, Go keep used import, empty code, original code preservation
- **Gen Code** (8 tests): Parse basic spec, parse with imports, parse empty spec, generate Python, generate Python with imports, generate Rust, generate Go, unsupported language, spec comments ignored
- **Fleet Review** (7 tests): Compliant repo, missing README, missing TASKBOARD, missing CI, low I2I compliance, missing README sections, review recommendations, empty repo
- **Gen Docs** (8 tests): Basic README, features list, custom installation, contributing section, default installation, sections list, custom license, file path
- **Codespace** (4 tests): Python/Go/Rust codespace configs, unknown language
- **Integration** (3 tests): Health→fix flow, review→gen_docs flow, full maintenance cycle (health→fix→gen_code→gen_docs→review)

### Running

```bash
cd fleet-mechanic
pip install pytest
pytest test_mechanic_extended.py -v
```

### Integration with fleet-mechanic repo

1. Import actual modules: `mechanic.py`, `fix_code.py`, `gen_code.py`, `review.py`
2. The existing 35 tests (mechanic.py:10, fix_code.py:8, gen_code.py:8, review.py:9) should continue passing
3. This extended test suite adds edge cases and integration scenarios on top of the existing tests
4. The `HealthChecker` and `FleetReviewer` should be reconciled with the repo's existing health and review modules

---

## Design Principles

1. **Self-contained**: Each test file includes the necessary data models and minimal implementations so tests can be validated independently before integration
2. **Mocked externals**: All GitHub API calls, git operations, and external services are mocked using `unittest.mock`
3. **Comprehensive edge cases**: Boundary conditions, empty inputs, error states, and malformed data are tested
4. **Protocol compliance**: I2I commit format (`[I2I:TYPE]`) is used throughout for fleet consistency
5. **Type-annotated**: All Python code uses proper type hints; Go code follows standard conventions

## I2I Commit Format

All test files follow the I2I commit message format:

```
[I2I:DELIVERY] T-004 {repo} comprehensive test coverage
```
