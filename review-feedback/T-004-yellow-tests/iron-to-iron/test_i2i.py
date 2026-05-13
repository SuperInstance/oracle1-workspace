"""
iron-to-iron (I2I) Test Suite
I2I protocol — git-native agent communication. 13+ message types.

[I2I:DELIVERY] T-004 iron-to-iron comprehensive test coverage
Covers: all 13 message type formats, branch naming validation, commit
message parsing, trust verification, beachcomb scanning, dispute resolution
flow, and edge cases.
"""

import pytest
import re
import hashlib
import hmac
import json
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Optional


# ---------------------------------------------------------------------------
# I2I Protocol — Message Types
# ---------------------------------------------------------------------------

class I2IMessageType(Enum):
    """All 13 I2I message types."""
    SIGNAL = "SIGNAL"
    DELIVERY = "DELIVERY"
    REVIEW = "REVIEW"
    PROPOSAL = "PROPOSAL"
    VOCAB = "VOCAB"
    DIRECTIVE = "DIRECTIVE"
    DISCOVERY = "DISCOVERY"
    QUESTION = "QUESTION"
    RESPONSE = "RESPONSE"
    ACCEPT = "ACCEPT"
    REJECT = "REJECT"
    DISPUTE = "DISPUTE"
    MERGE = "MERGE"


ALL_MESSAGE_TYPES = list(I2IMessageType)


# ---------------------------------------------------------------------------
# I2I Commit Message Format
# ---------------------------------------------------------------------------

# Pattern: [I2I:TYPE] subject body
I2I_COMMIT_PATTERN = re.compile(
    r"^\[I2I:(SIGNAL|DELIVERY|REVIEW|PROPOSAL|VOCAB|DIRECTIVE|"
    r"DISCOVERY|QUESTION|RESPONSE|ACCEPT|REJECT|DISPUTE|MERGE)\]\s+(.+)$",
    re.MULTILINE,
)


@dataclass
class I2ICommitMessage:
    """Parsed I2I commit message."""
    message_type: I2IMessageType
    subject: str
    body: str = ""
    agent: str = ""
    task_ref: str = ""

    def to_string(self) -> str:
        """Serialize back to I2I commit format."""
        prefix = f"[I2I:{self.message_type.value}]"
        parts = [f"{prefix} {self.subject}"]
        if self.body:
            parts.append("")
            parts.append(self.body)
        return "\n".join(parts)


def parse_i2i_commit(message: str) -> I2ICommitMessage:
    """Parse an I2I commit message string.

    Raises ValueError if the message doesn't match I2I format.
    """
    lines = message.strip().split("\n")
    if not lines:
        raise ValueError("Empty commit message")

    match = I2I_COMMIT_PATTERN.match(lines[0])
    if not match:
        raise ValueError(f"Invalid I2I commit format: {lines[0]!r}")

    type_str = match.group(1)
    subject = match.group(2)

    try:
        msg_type = I2IMessageType(type_str)
    except ValueError:
        raise ValueError(f"Unknown I2I message type: {type_str}")

    body = "\n".join(lines[1:]).strip() if len(lines) > 1 else ""

    # Try to extract task reference (e.g., T-001, T-042)
    task_match = re.search(r"(T-\d+)", subject)
    task_ref = task_match.group(1) if task_match else ""

    return I2ICommitMessage(
        message_type=msg_type,
        subject=subject,
        body=body,
        task_ref=task_ref,
    )


def format_i2i_commit(
    msg_type: I2IMessageType,
    subject: str,
    body: str = "",
) -> str:
    """Format an I2I commit message string."""
    prefix = f"[I2I:{msg_type.value}]"
    result = f"{prefix} {subject}"
    if body:
        result += f"\n\n{body}"
    return result


# ---------------------------------------------------------------------------
# Branch Naming Convention
# ---------------------------------------------------------------------------

# Valid patterns:
#   {agent}/T-{id}          — task branch
#   {agent}/fix/{issue}     — fix branch
#   {agent}/experiment/{name} — experiment branch

BRANCH_TASK_PATTERN = re.compile(r"^([a-zA-Z0-9_-]+)/T-(\d+)$")
BRANCH_FIX_PATTERN = re.compile(r"^([a-zA-Z0-9_-]+)/fix/(.+)$")
BRANCH_EXPERIMENT_PATTERN = re.compile(r"^([a-zA-Z0-9_-]+)/experiment/(.+)$")


@dataclass
class BranchInfo:
    """Parsed branch name."""
    agent: str
    kind: str  # "task", "fix", "experiment"
    identifier: str  # task ID, issue name, or experiment name

    def to_string(self) -> str:
        """Reconstruct the branch name."""
        if self.kind == "task":
            return f"{self.agent}/T-{self.identifier}"
        elif self.kind == "fix":
            return f"{self.agent}/fix/{self.identifier}"
        elif self.kind == "experiment":
            return f"{self.agent}/experiment/{self.identifier}"
        return f"{self.agent}/{self.identifier}"


def validate_branch_name(name: str) -> bool:
    """Check if a branch name follows I2I naming convention."""
    return bool(
        BRANCH_TASK_PATTERN.match(name)
        or BRANCH_FIX_PATTERN.match(name)
        or BRANCH_EXPERIMENT_PATTERN.match(name)
    )


def parse_branch_name(name: str) -> BranchInfo:
    """Parse an I2I branch name into its components.

    Raises ValueError if the branch name doesn't match any convention.
    """
    match = BRANCH_TASK_PATTERN.match(name)
    if match:
        return BranchInfo(agent=match.group(1), kind="task", identifier=match.group(2))

    match = BRANCH_FIX_PATTERN.match(name)
    if match:
        return BranchInfo(agent=match.group(1), kind="fix", identifier=match.group(2))

    match = BRANCH_EXPERIMENT_PATTERN.match(name)
    if match:
        return BranchInfo(agent=match.group(1), kind="experiment", identifier=match.group(2))

    raise ValueError(f"Invalid I2I branch name: {name}")


# ---------------------------------------------------------------------------
# Web-of-Trust with Signed Commits
# ---------------------------------------------------------------------------

@dataclass
class TrustEntry:
    """A trust endorsement from one agent to another."""
    signer: str
    target: str
    level: int  # 0-5 trust level
    signature: str = ""  # HMAC signature


class WebOfTrust:
    """Manages trust relationships between agents using signed commits."""

    def __init__(self, secret: str = "fleet-secret") -> None:
        self._secret = secret.encode()
        self._endorsements: list[TrustEntry] = []

    def _sign(self, data: str) -> str:
        """Create an HMAC signature for data."""
        return hmac.new(self._secret, data.encode(), hashlib.sha256).hexdigest()

    def endorse(self, signer: str, target: str, level: int) -> TrustEntry:
        """Create a signed trust endorsement."""
        if level < 0 or level > 5:
            raise ValueError(f"Trust level must be 0-5, got {level}")
        payload = f"{signer}->{target}:{level}"
        entry = TrustEntry(
            signer=signer,
            target=target,
            level=level,
            signature=self._sign(payload),
        )
        self._endorsements.append(entry)
        return entry

    def verify(self, entry: TrustEntry) -> bool:
        """Verify a trust endorsement's signature."""
        payload = f"{entry.signer}->{entry.target}:{entry.level}"
        expected = self._sign(payload)
        return hmac.compare_digest(entry.signature, expected)

    def trust_level(self, agent: str) -> float:
        """Compute aggregate trust level for an agent (average of endorsements)."""
        endorsements = [e for e in self._endorsements if e.target == agent and self.verify(e)]
        if not endorsements:
            return 0.0
        return sum(e.level for e in endorsements) / len(endorsements)

    def endorsement_count(self, agent: str) -> int:
        """Count verified endorsements for an agent."""
        return len([e for e in self._endorsements if e.target == agent and self.verify(e)])

    def is_trusted(self, agent: str, min_level: float = 2.0) -> bool:
        """Check if an agent meets a minimum trust threshold."""
        return self.trust_level(agent) >= min_level


# ---------------------------------------------------------------------------
# Beachcombing — Signal Scanning
# ---------------------------------------------------------------------------

@dataclass
class BeachcombResult:
    """A signal discovered during beachcombing."""
    commit_hash: str
    message_type: I2IMessageType
    agent: str
    subject: str
    branch: str
    timestamp: str = ""


def beachcomb_scan(commits: list[dict]) -> list[BeachcombResult]:
    """Scan a list of git commit dicts for I2I signals.

    Each commit dict should have: hash, message, author, branch, timestamp.
    Returns a list of BeachcombResult for valid I2I commits.
    """
    results: list[BeachcombResult] = []
    for commit in commits:
        message = commit.get("message", "")
        try:
            parsed = parse_i2i_commit(message)
            results.append(BeachcombResult(
                commit_hash=commit.get("hash", ""),
                message_type=parsed.message_type,
                agent=commit.get("author", ""),
                subject=parsed.subject,
                branch=commit.get("branch", ""),
                timestamp=commit.get("timestamp", ""),
            ))
        except ValueError:
            continue  # Skip non-I2I commits
    return results


def beachcomb_filter_by_type(
    results: list[BeachcombResult],
    msg_type: I2IMessageType,
) -> list[BeachcombResult]:
    """Filter beachcomb results by message type."""
    return [r for r in results if r.message_type == msg_type]


def beachcomb_filter_by_agent(
    results: list[BeachcombResult],
    agent: str,
) -> list[BeachcombResult]:
    """Filter beachcomb results by agent."""
    return [r for r in results if r.agent == agent]


# ---------------------------------------------------------------------------
# Dispute Resolution Flow
# ---------------------------------------------------------------------------

class DisputeState(Enum):
    """States in the dispute resolution flow."""
    OPENED = "opened"
    RESPONDED = "responded"
    ESCALATED = "escalated"
    RESOLVED = "resolved"
    WITHDRAWN = "withdrawn"


@dataclass
class Dispute:
    """A dispute between agents."""
    id: str
    challenger: str
    respondent: str
    subject: str
    state: DisputeState = DisputeState.OPENED
    resolution: str = ""

    def respond(self, response: str) -> None:
        """Respondent responds to the dispute."""
        if self.state != DisputeState.OPENED:
            raise ValueError(f"Cannot respond to dispute in {self.state.value} state")
        self.state = DisputeState.RESPONDED
        self.resolution = response

    def escalate(self) -> None:
        """Escalate the dispute to fleet review."""
        if self.state not in (DisputeState.OPENED, DisputeState.RESPONDED):
            raise ValueError(f"Cannot escalate dispute in {self.state.value} state")
        self.state = DisputeState.ESCALATED

    def resolve(self, resolution: str) -> None:
        """Resolve the dispute."""
        if self.state not in (DisputeState.RESPONDED, DisputeState.ESCALATED):
            raise ValueError(f"Cannot resolve dispute in {self.state.value} state")
        self.state = DisputeState.RESOLVED
        self.resolution = resolution

    def withdraw(self) -> None:
        """Withdraw the dispute."""
        if self.state == DisputeState.RESOLVED:
            raise ValueError("Cannot withdraw a resolved dispute")
        self.state = DisputeState.WITHDRAWN


# ===========================================================================
# TESTS
# ===========================================================================


class TestI2IMessageTypes:
    """Test all 13 I2I message type formats."""

    @pytest.mark.parametrize("msg_type", ALL_MESSAGE_TYPES)
    def test_message_type_value(self, msg_type: I2IMessageType) -> None:
        """Each message type should have a string value matching its name."""
        assert msg_type.value == msg_type.name

    @pytest.mark.parametrize("msg_type", ALL_MESSAGE_TYPES)
    def test_format_and_parse_roundtrip(self, msg_type: I2IMessageType) -> None:
        """Every message type should survive format→parse roundtrip."""
        subject = f"Test subject for {msg_type.value}"
        body = "This is the body of the message."
        formatted = format_i2i_commit(msg_type, subject, body)
        parsed = parse_i2i_commit(formatted)
        assert parsed.message_type == msg_type
        assert parsed.subject == subject
        assert parsed.body == body

    def test_thirteen_message_types(self) -> None:
        """I2I protocol must have exactly 13 message types."""
        assert len(I2IMessageType) == 13

    def test_message_type_names(self) -> None:
        """All 13 type names must be present."""
        expected = {
            "SIGNAL", "DELIVERY", "REVIEW", "PROPOSAL", "VOCAB",
            "DIRECTIVE", "DISCOVERY", "QUESTION", "RESPONSE", "ACCEPT",
            "REJECT", "DISPUTE", "MERGE",
        }
        actual = {t.value for t in I2IMessageType}
        assert actual == expected


class TestCommitMessageParsing:
    """Test I2I commit message parsing."""

    def test_parse_signal(self) -> None:
        """Parse a SIGNAL commit message."""
        msg = "[I2I:SIGNAL] Fleet alert: new repo discovered"
        parsed = parse_i2i_commit(msg)
        assert parsed.message_type == I2IMessageType.SIGNAL
        assert "new repo discovered" in parsed.subject

    def test_parse_delivery(self) -> None:
        """Parse a DELIVERY commit message with task reference."""
        msg = "[I2I:DELIVERY] T-004 Add comprehensive tests"
        parsed = parse_i2i_commit(msg)
        assert parsed.message_type == I2IMessageType.DELIVERY
        assert parsed.task_ref == "T-004"

    def test_parse_review(self) -> None:
        """Parse a REVIEW commit message."""
        msg = "[I2I:REVIEW] T-002 Code review feedback"
        parsed = parse_i2i_commit(msg)
        assert parsed.message_type == I2IMessageType.REVIEW
        assert parsed.task_ref == "T-002"

    def test_parse_proposal(self) -> None:
        """Parse a PROPOSAL commit message."""
        msg = "[I2I:PROPOSAL] Add new fleet communication channel"
        parsed = parse_i2i_commit(msg)
        assert parsed.message_type == I2IMessageType.PROPOSAL

    def test_parse_vocab(self) -> None:
        """Parse a VOCAB commit message."""
        msg = "[I2I:VOCAB] Define new I2I message types for review flow"
        parsed = parse_i2i_commit(msg)
        assert parsed.message_type == I2IMessageType.VOCAB

    def test_parse_directive(self) -> None:
        """Parse a DIRECTIVE commit message."""
        msg = "[I2I:DIRECTIVE] All agents must sign commits"
        parsed = parse_i2i_commit(msg)
        assert parsed.message_type == I2IMessageType.DIRECTIVE

    def test_parse_discovery(self) -> None:
        """Parse a DISCOVERY commit message."""
        msg = "[I2I:DISCOVERY] Found new fleet member: greenhorn-runtime"
        parsed = parse_i2i_commit(msg)
        assert parsed.message_type == I2IMessageType.DISCOVERY

    def test_parse_question(self) -> None:
        """Parse a QUESTION commit message."""
        msg = "[I2I:QUESTION] What is the trust threshold for merge?"
        parsed = parse_i2i_commit(msg)
        assert parsed.message_type == I2IMessageType.QUESTION

    def test_parse_response(self) -> None:
        """Parse a RESPONSE commit message."""
        msg = "[I2I:RESPONSE] Trust threshold is 2.0"
        parsed = parse_i2i_commit(msg)
        assert parsed.message_type == I2IMessageType.RESPONSE

    def test_parse_accept(self) -> None:
        """Parse an ACCEPT commit message."""
        msg = "[I2I:ACCEPT] T-003 Code approved"
        parsed = parse_i2i_commit(msg)
        assert parsed.message_type == I2IMessageType.ACCEPT

    def test_parse_reject(self) -> None:
        """Parse a REJECT commit message."""
        msg = "[I2I:REJECT] T-005 Does not meet fleet standards"
        parsed = parse_i2i_commit(msg)
        assert parsed.message_type == I2IMessageType.REJECT

    def test_parse_dispute(self) -> None:
        """Parse a DISPUTE commit message."""
        msg = "[I2I:DISPUTE] T-006 Implementation disagreement"
        parsed = parse_i2i_commit(msg)
        assert parsed.message_type == I2IMessageType.DISPUTE

    def test_parse_merge(self) -> None:
        """Parse a MERGE commit message."""
        msg = "[I2I:MERGE] greenhorn/T-001 into main"
        parsed = parse_i2i_commit(msg)
        assert parsed.message_type == I2IMessageType.MERGE

    def test_parse_with_body(self) -> None:
        """Parse a commit message with multi-line body."""
        msg = "[I2I:DELIVERY] T-010 Implement feature\n\nDetailed description\nacross multiple lines."
        parsed = parse_i2i_commit(msg)
        assert parsed.message_type == I2IMessageType.DELIVERY
        assert "Detailed description" in parsed.body

    def test_parse_invalid_format(self) -> None:
        """Non-I2I commits should raise ValueError."""
        with pytest.raises(ValueError, match="Invalid I2I commit format"):
            parse_i2i_commit("Regular commit message without I2I prefix")

    def test_parse_empty_message(self) -> None:
        """Empty message should raise ValueError."""
        with pytest.raises(ValueError):
            parse_i2i_commit("")

    def test_parse_unknown_type(self) -> None:
        """Unknown message type in valid format should raise ValueError."""
        with pytest.raises(ValueError):
            parse_i2i_commit("[I2I:INVALID] Something")

    def test_parse_task_ref_extraction(self) -> None:
        """Task references (T-NNN) should be extracted from subject."""
        msg = "[I2I:DELIVERY] T-042 Fix critical bug"
        parsed = parse_i2i_commit(msg)
        assert parsed.task_ref == "T-042"

    def test_parse_no_task_ref(self) -> None:
        """Messages without task references should have empty task_ref."""
        msg = "[I2I:SIGNAL] General fleet announcement"
        parsed = parse_i2i_commit(msg)
        assert parsed.task_ref == ""

    def test_serialize_back_to_string(self) -> None:
        """I2ICommitMessage.to_string() should produce valid I2I format."""
        commit = I2ICommitMessage(
            message_type=I2IMessageType.DELIVERY,
            subject="T-001 Add tests",
        )
        result = commit.to_string()
        assert result.startswith("[I2I:DELIVERY]")
        assert "T-001 Add tests" in result


class TestBranchNaming:
    """Test I2I branch naming conventions."""

    def test_valid_task_branch(self) -> None:
        """Task branch: {agent}/T-{id} should be valid."""
        assert validate_branch_name("greenhorn/T-001") is True

    def test_valid_fix_branch(self) -> None:
        """Fix branch: {agent}/fix/{issue} should be valid."""
        assert validate_branch_name("mechanic/fix/broken-test") is True

    def test_valid_experiment_branch(self) -> None:
        """Experiment branch: {agent}/experiment/{name} should be valid."""
        assert validate_branch_name("scout/experiment/new-approach") is True

    def test_invalid_branch_no_agent(self) -> None:
        """Branch without agent prefix should be invalid."""
        assert validate_branch_name("T-001") is False

    def test_invalid_branch_main(self) -> None:
        """'main' branch should not match I2I pattern."""
        assert validate_branch_name("main") is False

    def test_invalid_branch_random(self) -> None:
        """Random branch names should be invalid."""
        assert validate_branch_name("feature/something") is False

    def test_invalid_branch_empty(self) -> None:
        """Empty branch name should be invalid."""
        assert validate_branch_name("") is False

    def test_parse_task_branch(self) -> None:
        """Parse a task branch name."""
        info = parse_branch_name("greenhorn/T-042")
        assert info.agent == "greenhorn"
        assert info.kind == "task"
        assert info.identifier == "042"

    def test_parse_fix_branch(self) -> None:
        """Parse a fix branch name."""
        info = parse_branch_name("mechanic/fix/broken-auth")
        assert info.agent == "mechanic"
        assert info.kind == "fix"
        assert info.identifier == "broken-auth"

    def test_parse_experiment_branch(self) -> None:
        """Parse an experiment branch name."""
        info = parse_branch_name("scout/experiment/neural-net")
        assert info.agent == "scout"
        assert info.kind == "experiment"
        assert info.identifier == "neural-net"

    def test_parse_invalid_branch_raises(self) -> None:
        """Parsing an invalid branch name should raise ValueError."""
        with pytest.raises(ValueError, match="Invalid I2I branch name"):
            parse_branch_name("invalid/branch/format")

    def test_branch_roundtrip_task(self) -> None:
        """Task branch should survive parse→to_string roundtrip."""
        original = "greenhorn/T-001"
        info = parse_branch_name(original)
        assert info.to_string() == original

    def test_branch_roundtrip_fix(self) -> None:
        """Fix branch should survive parse→to_string roundtrip."""
        original = "mechanic/fix/typo-in-docs"
        info = parse_branch_name(original)
        assert info.to_string() == original

    def test_branch_roundtrip_experiment(self) -> None:
        """Experiment branch should survive parse→to_string roundtrip."""
        original = "scout/experiment/new-algo"
        info = parse_branch_name(original)
        assert info.to_string() == original

    def test_agent_name_with_underscores(self) -> None:
        """Agent names may contain underscores."""
        assert validate_branch_name("green_horn/T-001") is True

    def test_agent_name_with_hyphens(self) -> None:
        """Agent names may contain hyphens."""
        assert validate_branch_name("fleet-mechanic/T-005") is True

    def test_fix_branch_nested_slashes(self) -> None:
        """Fix branch identifiers can contain slashes."""
        assert validate_branch_name("agent/fix/auth/login-bug") is True


class TestWebOfTrust:
    """Test trust verification with signed commits."""

    def test_endorse_agent(self) -> None:
        """Should create a signed trust endorsement."""
        wot = WebOfTrust(secret="test-secret")
        entry = wot.endorse("agent-a", "agent-b", 4)
        assert entry.signer == "agent-a"
        assert entry.target == "agent-b"
        assert entry.level == 4
        assert entry.signature != ""

    def test_verify_valid_endorsement(self) -> None:
        """Valid endorsement should verify successfully."""
        wot = WebOfTrust(secret="test-secret")
        entry = wot.endorse("agent-a", "agent-b", 3)
        assert wot.verify(entry) is True

    def test_reject_tampered_endorsement(self) -> None:
        """Tampered endorsement should fail verification."""
        wot = WebOfTrust(secret="test-secret")
        entry = wot.endorse("agent-a", "agent-b", 3)
        # Tamper with the level
        tampered = TrustEntry(
            signer=entry.signer,
            target=entry.target,
            level=5,  # Changed from 3 to 5
            signature=entry.signature,
        )
        assert wot.verify(tampered) is False

    def test_trust_level_calculation(self) -> None:
        """Trust level should be average of verified endorsements."""
        wot = WebOfTrust(secret="test-secret")
        wot.endorse("agent-a", "agent-c", 4)
        wot.endorse("agent-b", "agent-c", 2)
        assert wot.trust_level("agent-c") == 3.0  # (4+2)/2

    def test_trust_level_no_endorsements(self) -> None:
        """Unknown agent should have trust level 0."""
        wot = WebOfTrust()
        assert wot.trust_level("unknown") == 0.0

    def test_is_trusted(self) -> None:
        """Agent with sufficient trust should be trusted."""
        wot = WebOfTrust(secret="test-secret")
        wot.endorse("agent-a", "agent-b", 4)
        wot.endorse("agent-c", "agent-b", 3)
        assert wot.is_trusted("agent-b", min_level=2.0) is True

    def test_is_not_trusted(self) -> None:
        """Agent with insufficient trust should not be trusted."""
        wot = WebOfTrust(secret="test-secret")
        wot.endorse("agent-a", "agent-b", 1)
        assert wot.is_trusted("agent-b", min_level=2.0) is False

    def test_endorsement_count(self) -> None:
        """Should count verified endorsements correctly."""
        wot = WebOfTrust(secret="test-secret")
        wot.endorse("a", "target", 3)
        wot.endorse("b", "target", 4)
        wot.endorse("c", "other", 5)
        assert wot.endorsement_count("target") == 2

    def test_invalid_trust_level(self) -> None:
        """Trust level outside 0-5 should raise ValueError."""
        wot = WebOfTrust()
        with pytest.raises(ValueError, match="Trust level must be 0-5"):
            wot.endorse("a", "b", 6)
        with pytest.raises(ValueError, match="Trust level must be 0-5"):
            wot.endorse("a", "b", -1)

    def test_different_secrets_different_signatures(self) -> None:
        """Endorsements signed with different secrets should not verify."""
        wot1 = WebOfTrust(secret="secret-1")
        wot2 = WebOfTrust(secret="secret-2")
        entry = wot1.endorse("a", "b", 3)
        assert wot2.verify(entry) is False

    def test_zero_trust_level(self) -> None:
        """Trust level 0 is valid (no trust)."""
        wot = WebOfTrust()
        entry = wot.endorse("a", "b", 0)
        assert entry.level == 0
        assert wot.verify(entry) is True

    def test_self_endorsement(self) -> None:
        """An agent can endorse itself (though it may be discounted)."""
        wot = WebOfTrust()
        entry = wot.endorse("a", "a", 5)
        assert wot.verify(entry) is True
        assert wot.trust_level("a") == 5.0


class TestBeachcombScanning:
    """Test beachcombing protocol for signal scanning."""

    def test_scan_finds_i2i_commits(self) -> None:
        """Beachcomb should find I2I-formatted commits."""
        commits = [
            {
                "hash": "abc123",
                "message": "[I2I:SIGNAL] Fleet alert",
                "author": "scout-1",
                "branch": "scout/T-001",
                "timestamp": "2025-01-01T00:00:00Z",
            },
            {
                "hash": "def456",
                "message": "Regular commit without I2I format",
                "author": "developer",
                "branch": "main",
                "timestamp": "2025-01-01T01:00:00Z",
            },
        ]
        results = beachcomb_scan(commits)
        assert len(results) == 1
        assert results[0].message_type == I2IMessageType.SIGNAL
        assert results[0].commit_hash == "abc123"

    def test_scan_multiple_i2i_types(self) -> None:
        """Beachcomb should identify different I2I message types."""
        commits = [
            {"hash": "h1", "message": "[I2I:SIGNAL] Alert", "author": "a1", "branch": "main"},
            {"hash": "h2", "message": "[I2I:DELIVERY] T-001 Done", "author": "a2", "branch": "a2/T-001"},
            {"hash": "h3", "message": "[I2I:REVIEW] T-002 LGTM", "author": "a3", "branch": "main"},
        ]
        results = beachcomb_scan(commits)
        assert len(results) == 3
        types = {r.message_type for r in results}
        assert types == {I2IMessageType.SIGNAL, I2IMessageType.DELIVERY, I2IMessageType.REVIEW}

    def test_scan_empty_commits(self) -> None:
        """Beachcomb should return empty list for no commits."""
        results = beachcomb_scan([])
        assert results == []

    def test_scan_all_non_i2i(self) -> None:
        """Beachcomb should skip all non-I2I commits."""
        commits = [
            {"hash": "h1", "message": "Regular commit", "author": "a1", "branch": "main"},
            {"hash": "h2", "message": "Another commit", "author": "a2", "branch": "main"},
        ]
        results = beachcomb_scan(commits)
        assert len(results) == 0

    def test_filter_by_type(self) -> None:
        """Should filter beachcomb results by message type."""
        results = [
            BeachcombResult("h1", I2IMessageType.SIGNAL, "a1", "Alert", "main"),
            BeachcombResult("h2", I2IMessageType.DELIVERY, "a2", "T-001", "a2/T-001"),
            BeachcombResult("h3", I2IMessageType.SIGNAL, "a3", "Notice", "main"),
        ]
        signals = beachcomb_filter_by_type(results, I2IMessageType.SIGNAL)
        assert len(signals) == 2

    def test_filter_by_agent(self) -> None:
        """Should filter beachcomb results by agent."""
        results = [
            BeachcombResult("h1", I2IMessageType.SIGNAL, "scout-1", "Alert", "main"),
            BeachcombResult("h2", I2IMessageType.DELIVERY, "greenhorn-1", "T-001", "gh/T-001"),
            BeachcombResult("h3", I2IMessageType.SIGNAL, "scout-1", "Notice", "main"),
        ]
        scout_results = beachcomb_filter_by_agent(results, "scout-1")
        assert len(scout_results) == 2

    def test_scan_preserves_metadata(self) -> None:
        """Beachcomb should preserve commit metadata."""
        commits = [
            {
                "hash": "abc123",
                "message": "[I2I:DELIVERY] T-042 Implementation",
                "author": "greenhorn-1",
                "branch": "greenhorn-1/T-042",
                "timestamp": "2025-06-15T12:00:00Z",
            },
        ]
        results = beachcomb_scan(commits)
        assert len(results) == 1
        r = results[0]
        assert r.commit_hash == "abc123"
        assert r.agent == "greenhorn-1"
        assert r.branch == "greenhorn-1/T-042"
        assert r.timestamp == "2025-06-15T12:00:00Z"


class TestDisputeResolution:
    """Test the dispute resolution flow."""

    def test_open_dispute(self) -> None:
        """Should create a dispute in OPENED state."""
        dispute = Dispute(id="D-001", challenger="agent-a", respondent="agent-b", subject="Code quality")
        assert dispute.state == DisputeState.OPENED

    def test_respond_to_dispute(self) -> None:
        """Respondent should be able to respond to an open dispute."""
        dispute = Dispute(id="D-001", challenger="a", respondent="b", subject="Test")
        dispute.respond("The code is correct per spec")
        assert dispute.state == DisputeState.RESPONDED

    def test_resolve_after_response(self) -> None:
        """Dispute should be resolvable after response."""
        dispute = Dispute(id="D-001", challenger="a", respondent="b", subject="Test")
        dispute.respond("My response")
        dispute.resolve("Accepted response, dispute resolved")
        assert dispute.state == DisputeState.RESOLVED
        assert "Accepted" in dispute.resolution

    def test_escalate_open_dispute(self) -> None:
        """Should be able to escalate an open dispute."""
        dispute = Dispute(id="D-001", challenger="a", respondent="b", subject="Test")
        dispute.escalate()
        assert dispute.state == DisputeState.ESCALATED

    def test_escalate_responded_dispute(self) -> None:
        """Should be able to escalate a responded dispute."""
        dispute = Dispute(id="D-001", challenger="a", respondent="b", subject="Test")
        dispute.respond("Response")
        dispute.escalate()
        assert dispute.state == DisputeState.ESCALATED

    def test_resolve_escalated_dispute(self) -> None:
        """Should be able to resolve an escalated dispute."""
        dispute = Dispute(id="D-001", challenger="a", respondent="b", subject="Test")
        dispute.escalate()
        dispute.resolve("Fleet decided in favor of respondent")
        assert dispute.state == DisputeState.RESOLVED

    def test_withdraw_open_dispute(self) -> None:
        """Should be able to withdraw an open dispute."""
        dispute = Dispute(id="D-001", challenger="a", respondent="b", subject="Test")
        dispute.withdraw()
        assert dispute.state == DisputeState.WITHDRAWN

    def test_cannot_respond_to_resolved_dispute(self) -> None:
        """Cannot respond to an already resolved dispute."""
        dispute = Dispute(id="D-001", challenger="a", respondent="b", subject="Test")
        dispute.respond("R")
        dispute.resolve("Done")
        with pytest.raises(ValueError, match="Cannot respond"):
            dispute.respond("Another response")

    def test_cannot_withdraw_resolved_dispute(self) -> None:
        """Cannot withdraw an already resolved dispute."""
        dispute = Dispute(id="D-001", challenger="a", respondent="b", subject="Test")
        dispute.respond("R")
        dispute.resolve("Done")
        with pytest.raises(ValueError, match="Cannot withdraw"):
            dispute.withdraw()

    def test_cannot_escalate_resolved_dispute(self) -> None:
        """Cannot escalate an already resolved dispute."""
        dispute = Dispute(id="D-001", challenger="a", respondent="b", subject="Test")
        dispute.respond("R")
        dispute.resolve("Done")
        with pytest.raises(ValueError, match="Cannot escalate"):
            dispute.escalate()

    def test_cannot_resolve_open_dispute(self) -> None:
        """Cannot resolve a dispute that hasn't been responded to."""
        dispute = Dispute(id="D-001", challenger="a", respondent="b", subject="Test")
        with pytest.raises(ValueError, match="Cannot resolve"):
            dispute.resolve("Early resolution")

    def test_full_dispute_lifecycle(self) -> None:
        """Test the full dispute lifecycle: open → respond → resolve."""
        dispute = Dispute(id="D-010", challenger="agent-a", respondent="agent-b", subject="Implementation")
        assert dispute.state == DisputeState.OPENED

        dispute.respond("My implementation follows the spec")
        assert dispute.state == DisputeState.RESPONDED

        dispute.resolve("Agreed: implementation is correct")
        assert dispute.state == DisputeState.RESOLVED
        assert "correct" in dispute.resolution

    def test_dispute_with_escalation_lifecycle(self) -> None:
        """Test dispute lifecycle with escalation: open → respond → escalate → resolve."""
        dispute = Dispute(id="D-011", challenger="a", respondent="b", subject="Disagreement")
        dispute.respond("My side")
        dispute.escalate()
        dispute.resolve("Fleet council decision")
        assert dispute.state == DisputeState.RESOLVED


class TestIntegration:
    """Integration tests combining multiple I2I components."""

    def test_commit_to_branch_to_trust(self) -> None:
        """Test the flow: commit message → branch validation → trust verification."""
        # 1. Agent makes a DELIVERY commit
        commit_msg = format_i2i_commit(I2IMessageType.DELIVERY, "T-001 Add tests")
        parsed = parse_i2i_commit(commit_msg)
        assert parsed.message_type == I2IMessageType.DELIVERY

        # 2. Validate the branch name
        branch = "greenhorn/T-001"
        assert validate_branch_name(branch) is True
        info = parse_branch_name(branch)
        assert info.kind == "task"

        # 3. Verify trust
        wot = WebOfTrust(secret="fleet-key")
        endorsement = wot.endorse("coordinator", "greenhorn", 4)
        assert wot.verify(endorsement) is True
        assert wot.is_trusted("greenhorn", min_level=2.0)

    def test_beachcomb_to_dispute_flow(self) -> None:
        """Test: beachcomb scan → detect dispute → resolution flow."""
        # 1. Beachcomb finds a DISPUTE signal
        commits = [
            {
                "hash": "h1",
                "message": "[I2I:DISPUTE] T-005 Implementation disagreement",
                "author": "agent-a",
                "branch": "agent-a/T-005",
            },
        ]
        results = beachcomb_scan(commits)
        assert len(results) == 1
        assert results[0].message_type == I2IMessageType.DISPUTE

        # 2. Open a dispute
        dispute = Dispute(
            id="D-001",
            challenger="agent-a",
            respondent="agent-b",
            subject="T-005 Implementation disagreement",
        )
        assert dispute.state == DisputeState.OPENED

        # 3. Respond and resolve
        dispute.respond("Implementation follows spec v2")
        dispute.resolve("Spec v2 confirmed, dispute resolved")
        assert dispute.state == DisputeState.RESOLVED

        # 4. Merge after resolution
        merge_msg = format_i2i_commit(I2IMessageType.MERGE, "agent-b/T-005 into main")
        parsed = parse_i2i_commit(merge_msg)
        assert parsed.message_type == I2IMessageType.MERGE

    def test_proposal_to_accept_flow(self) -> None:
        """Test: PROPOSAL → REVIEW → ACCEPT flow."""
        # 1. Agent submits proposal
        proposal = format_i2i_commit(
            I2IMessageType.PROPOSAL,
            "Add new message type: DELEGATE",
            body="Proposed new I2I message type for task delegation.",
        )
        parsed = parse_i2i_commit(proposal)
        assert parsed.message_type == I2IMessageType.PROPOSAL

        # 2. Review
        review = format_i2i_commit(I2IMessageType.REVIEW, "Proposal looks good")
        parsed_review = parse_i2i_commit(review)
        assert parsed_review.message_type == I2IMessageType.REVIEW

        # 3. Accept
        accept = format_i2i_commit(I2IMessageType.ACCEPT, "Add new message type: DELEGATE")
        parsed_accept = parse_i2i_commit(accept)
        assert parsed_accept.message_type == I2IMessageType.ACCEPT

    def test_all_13_types_through_beachcomb(self) -> None:
        """All 13 message types should be detectable via beachcomb scanning."""
        commits = []
        for i, msg_type in enumerate(ALL_MESSAGE_TYPES):
            commits.append({
                "hash": f"h{i:03d}",
                "message": f"[I2I:{msg_type.value}] Test message {i}",
                "author": f"agent-{i}",
                "branch": f"agent-{i}/T-{i:03d}",
            })

        results = beachcomb_scan(commits)
        assert len(results) == 13
        found_types = {r.message_type for r in results}
        assert found_types == set(I2IMessageType)
