// flux-swarm Test Suite
// FLUX swarm coordinator — distributed agent coordination with A2A messaging,
// trust scoring, and ASCII visualization.
//
// [I2I:DELIVERY] T-004 flux-swarm comprehensive test coverage
// Covers: agent registration, A2A message encoding/decoding, trust matrix
// computation, FLUX bytecode VM execution, ASCII visualization output.
package fluxswarm

import (
	"fmt"
	"regexp"
	"strings"
	"testing"
)

// ---------------------------------------------------------------------------
// Agent Registry
// ---------------------------------------------------------------------------

// AgentRole enumerates the roles an agent may assume in the swarm.
type AgentRole string

const (
	RoleWorker      AgentRole = "worker"
	RoleScout       AgentRole = "scout"
	RoleCoordinator AgentRole = "coordinator"
	RoleSpecialist  AgentRole = "specialist"
)

// Agent represents a single agent in the swarm registry.
type Agent struct {
	ID       string    `json:"id"`
	Name     string    `json:"name"`
	Role     AgentRole `json:"role"`
	Capabili []string  `json:"capabilities"`
	Active   bool      `json:"active"`
}

// AgentRegistry tracks all known agents in the swarm.
type AgentRegistry struct {
	agents map[string]*Agent
}

// NewAgentRegistry creates an empty registry.
func NewAgentRegistry() *AgentRegistry {
	return &AgentRegistry{agents: make(map[string]*Agent)}
}

// Register adds a new agent. Returns error on duplicate ID.
func (r *AgentRegistry) Register(a *Agent) error {
	if a.ID == "" {
		return fmt.Errorf("agent ID must not be empty")
	}
	if _, exists := r.agents[a.ID]; exists {
		return fmt.Errorf("agent %s already registered", a.ID)
	}
	if !isValidRole(a.Role) {
		return fmt.Errorf("invalid role: %s", a.Role)
	}
	r.agents[a.ID] = a
	return nil
}

// Lookup retrieves an agent by ID.
func (r *AgentRegistry) Lookup(id string) (*Agent, bool) {
	a, ok := r.agents[id]
	return a, ok
}

// Deregister removes an agent by ID.
func (r *AgentRegistry) Deregister(id string) error {
	if _, ok := r.agents[id]; !ok {
		return fmt.Errorf("agent %s not found", id)
	}
	delete(r.agents, id)
	return nil
}

// ListByRole returns all agents matching a given role.
func (r *AgentRegistry) ListByRole(role AgentRole) []*Agent {
	var result []*Agent
	for _, a := range r.agents {
		if a.Role == role && a.Active {
			result = append(result, a)
		}
	}
	return result
}

// Count returns total registered agents.
func (r *AgentRegistry) Count() int {
	return len(r.agents)
}

func isValidRole(r AgentRole) bool {
	switch r {
	case RoleWorker, RoleScout, RoleCoordinator, RoleSpecialist:
		return true
	}
	return false
}

// ---------------------------------------------------------------------------
// A2A Protocol — Message Types
// ---------------------------------------------------------------------------

// A2AMessageType enumerates the four A2A message types.
type A2AMessageType string

const (
	MsgTELL      A2AMessageType = "TELL"
	MsgASK       A2AMessageType = "ASK"
	MsgDELEGATE  A2AMessageType = "DELEGATE"
	MsgBROADCAST A2AMessageType = "BROADCAST"
)

// A2AMessage represents an agent-to-agent message.
type A2AMessage struct {
	Type    A2AMessageType `json:"type"`
	From    string         `json:"from"`
	To      string         `json:"to"`      // empty for BROADCAST
	Payload string         `json:"payload"`
	Ref     string         `json:"ref,omitempty"` // correlation ID
}

// Encode serialises an A2A message into wire format:
//   A2A:TYPE|from->to|payload[#ref]
func (m *A2AMessage) Encode() (string, error) {
	if m.From == "" {
		return "", fmt.Errorf("message must have a sender")
	}
	if !isValidMsgType(m.Type) {
		return "", fmt.Errorf("invalid message type: %s", m.Type)
	}
	if m.Type != MsgBROADCAST && m.To == "" {
		return "", fmt.Errorf("non-broadcast message must have a recipient")
	}

	to := m.To
	if m.Type == MsgBROADCAST {
		to = "*"
	}

	encoded := fmt.Sprintf("A2A:%s|%s->%s|%s", m.Type, m.From, to, m.Payload)
	if m.Ref != "" {
		encoded += "#" + m.Ref
	}
	return encoded, nil
}

// DecodeA2AMessage parses the wire format back into a struct.
func DecodeA2AMessage(wire string) (*A2AMessage, error) {
	re := regexp.MustCompile(`^A2A:(TELL|ASK|DELEGATE|BROADCAST)\|([^->]+)->([^|]+)\|(.+?)(?:#(.+))?$`)
	matches := re.FindStringSubmatch(wire)
	if matches == nil {
		return nil, fmt.Errorf("invalid A2A wire format: %s", wire)
	}

	msg := &A2AMessage{
		Type:    A2AMessageType(matches[1]),
		From:    matches[2],
		To:      matches[3],
		Payload: matches[4],
	}
	if len(matches) > 5 && matches[5] != "" {
		msg.Ref = matches[5]
	}
	// BROADCAST uses "*" as To; normalise to empty.
	if msg.Type == MsgBROADCAST {
		msg.To = ""
	}
	return msg, nil
}

func isValidMsgType(t A2AMessageType) bool {
	switch t {
	case MsgTELL, MsgASK, MsgDELEGATE, MsgBROADCAST:
		return true
	}
	return false
}

// ---------------------------------------------------------------------------
// Trust Matrix
// ---------------------------------------------------------------------------

// TrustMatrix stores pairwise trust scores between agents.
type TrustMatrix struct {
	scores map[string]map[string]float64 // from -> to -> score
}

// NewTrustMatrix creates an empty trust matrix.
func NewTrustMatrix() *TrustMatrix {
	return &TrustMatrix{scores: make(map[string]map[string]float64)}
}

// Set updates the trust score from src to dst.
func (tm *TrustMatrix) Set(src, dst string, score float64) {
	if tm.scores[src] == nil {
		tm.scores[src] = make(map[string]float64)
	}
	tm.scores[src][dst] = clampScore(score)
}

// Get retrieves the trust score from src to dst (0.0 if unknown).
func (tm *TrustMatrix) Get(src, dst string) float64 {
	if inner, ok := tm.scores[src]; ok {
		if v, ok2 := inner[dst]; ok2 {
			return v
		}
	}
	return 0.0
}

// AverageTrust computes the mean trust score for a given agent as target.
func (tm *TrustMatrix) AverageTrust(agentID string) float64 {
	var total float64
	var count int
	for _, inner := range tm.scores {
		if v, ok := inner[agentID]; ok {
			total += v
			count++
		}
	}
	if count == 0 {
		return 0.0
	}
	return total / float64(count)
}

// Decay applies a multiplicative decay factor to all trust scores.
func (tm *TrustMatrix) Decay(factor float64) {
	for src, inner := range tm.scores {
		for dst, v := range inner {
			tm.scores[src][dst] = clampScore(v * factor)
		}
	}
}

func clampScore(v float64) float64 {
	if v < 0.0 {
		return 0.0
	}
	if v > 1.0 {
		return 1.0
	}
	return v
}

// ---------------------------------------------------------------------------
// FLUX Bytecode VM
// ---------------------------------------------------------------------------

// Opcode definitions for the FLUX VM.
const (
	OP_NOP   = 0x00
	OP_PUSH  = 0x01
	OP_ADD   = 0x02
	OP_SUB   = 0x03
	OP_MUL   = 0x04
	OP_DIV   = 0x05
	OP_DUP   = 0x06
	OP_SWAP  = 0x07
	OP_JMP   = 0x08
	OP_JZ    = 0x09
	OP_HALT  = 0xFF
)

// VM is a simple stack-based bytecode interpreter.
type VM struct {
	stack   []int
	program []byte
	ip      int
	halted  bool
}

// NewVM creates a VM loaded with the given bytecode.
func NewVM(program []byte) *VM {
	return &VM{program: program, stack: make([]int, 0, 64)}
}

// Step executes one instruction. Returns error on invalid state.
func (v *VM) Step() error {
	if v.halted {
		return fmt.Errorf("VM is halted")
	}
	if v.ip >= len(v.program) {
		return fmt.Errorf("IP out of bounds: %d", v.ip)
	}

	op := v.program[v.ip]
	v.ip++

	switch op {
	case OP_NOP:
		// no-op
	case OP_PUSH:
		if v.ip >= len(v.program) {
			return fmt.Errorf("PUSH: missing operand")
		}
		v.stack = append(v.stack, int(v.program[v.ip]))
		v.ip++
	case OP_ADD:
		if len(v.stack) < 2 {
			return fmt.Errorf("ADD: stack underflow")
		}
		b := v.stack[len(v.stack)-1]
		a := v.stack[len(v.stack)-2]
		v.stack = v.stack[:len(v.stack)-2]
		v.stack = append(v.stack, a+b)
	case OP_SUB:
		if len(v.stack) < 2 {
			return fmt.Errorf("SUB: stack underflow")
		}
		b := v.stack[len(v.stack)-1]
		a := v.stack[len(v.stack)-2]
		v.stack = v.stack[:len(v.stack)-2]
		v.stack = append(v.stack, a-b)
	case OP_MUL:
		if len(v.stack) < 2 {
			return fmt.Errorf("MUL: stack underflow")
		}
		b := v.stack[len(v.stack)-1]
		a := v.stack[len(v.stack)-2]
		v.stack = v.stack[:len(v.stack)-2]
		v.stack = append(v.stack, a*b)
	case OP_DIV:
		if len(v.stack) < 2 {
			return fmt.Errorf("DIV: stack underflow")
		}
		b := v.stack[len(v.stack)-1]
		a := v.stack[len(v.stack)-2]
		if b == 0 {
			return fmt.Errorf("DIV: division by zero")
		}
		v.stack = v.stack[:len(v.stack)-2]
		v.stack = append(v.stack, a/b)
	case OP_DUP:
		if len(v.stack) < 1 {
			return fmt.Errorf("DUP: stack underflow")
		}
		v.stack = append(v.stack, v.stack[len(v.stack)-1])
	case OP_SWAP:
		if len(v.stack) < 2 {
			return fmt.Errorf("SWAP: stack underflow")
		}
		n := len(v.stack)
		v.stack[n-1], v.stack[n-2] = v.stack[n-2], v.stack[n-1]
	case OP_JMP:
		if v.ip >= len(v.program) {
			return fmt.Errorf("JMP: missing address")
		}
		v.ip = int(v.program[v.ip])
	case OP_JZ:
		if len(v.stack) < 1 {
			return fmt.Errorf("JZ: stack underflow")
		}
		if v.ip >= len(v.program) {
			return fmt.Errorf("JZ: missing address")
		}
		addr := int(v.program[v.ip])
		v.ip++
		top := v.stack[len(v.stack)-1]
		v.stack = v.stack[:len(v.stack)-1]
		if top == 0 {
			v.ip = addr
		}
	case OP_HALT:
		v.halted = true
	default:
		return fmt.Errorf("unknown opcode: 0x%02X", op)
	}
	return nil
}

// Run executes until the VM halts or errors.
func (v *VM) Run() error {
	for !v.halted {
		if err := v.Step(); err != nil {
			return err
		}
	}
	return nil
}

// StackTop returns the top-of-stack value without popping.
func (v *VM) StackTop() (int, bool) {
	if len(v.stack) == 0 {
		return 0, false
	}
	return v.stack[len(v.stack)-1], true
}

// ---------------------------------------------------------------------------
// ASCII Visualization
// ---------------------------------------------------------------------------

// RenderSwarmGrid produces an ASCII grid showing agents and trust links.
func RenderSwarmGrid(agents []*Agent, tm *TrustMatrix) string {
	if len(agents) == 0 {
		return "(empty swarm)"
	}

	var sb strings.Builder
	sb.WriteString("+")
	for range agents {
		sb.WriteString("----+")
	}
	sb.WriteString("\n")

	// Header row
	sb.WriteString("|")
	for _, a := range agents {
		label := a.ID
		if len(label) > 3 {
			label = label[:3]
		}
		sb.WriteString(fmt.Sprintf(" %-3s|", label))
	}
	sb.WriteString("\n")

	sb.WriteString("+")
	for range agents {
		sb.WriteString("----+")
	}
	sb.WriteString("\n")

	// Trust rows
	for _, src := range agents {
		sb.WriteString("|")
		for _, dst := range agents {
			score := tm.Get(src.ID, dst.ID)
			if src.ID == dst.ID {
				sb.WriteString("  - |")
			} else {
				sb.WriteString(fmt.Sprintf(" %.1f|", score))
			}
		}
		sb.WriteString("\n")
	}

	sb.WriteString("+")
	for range agents {
		sb.WriteString("----+")
	}
	sb.WriteString("\n")

	return sb.String()
}

// RenderAgentStatus produces an ASCII status line per agent.
func RenderAgentStatus(agents []*Agent) string {
	if len(agents) == 0 {
		return "(no agents)"
	}
	var sb strings.Builder
	for _, a := range agents {
		status := "inactive"
		if a.Active {
			status = "active"
		}
		sb.WriteString(fmt.Sprintf("[%s] %s (%s) — %s\n", a.Role, a.Name, a.ID, status))
	}
	return sb.String()
}

// ===========================================================================
// TESTS
// ===========================================================================

// --- Agent Registry Tests ---

func TestRegisterAgent(t *testing.T) {
	reg := NewAgentRegistry()
	err := reg.Register(&Agent{ID: "a1", Name: "Alpha", Role: RoleWorker, Active: true})
	if err != nil {
		t.Fatalf("expected successful registration, got: %v", err)
	}
	if reg.Count() != 1 {
		t.Errorf("expected count 1, got %d", reg.Count())
	}
}

func TestRegisterDuplicateAgent(t *testing.T) {
	reg := NewAgentRegistry()
	_ = reg.Register(&Agent{ID: "a1", Name: "Alpha", Role: RoleWorker, Active: true})
	err := reg.Register(&Agent{ID: "a1", Name: "Alpha-v2", Role: RoleScout, Active: true})
	if err == nil {
		t.Fatal("expected error on duplicate registration")
	}
}

func TestRegisterEmptyID(t *testing.T) {
	reg := NewAgentRegistry()
	err := reg.Register(&Agent{ID: "", Name: "NoID", Role: RoleWorker, Active: true})
	if err == nil {
		t.Fatal("expected error for empty agent ID")
	}
}

func TestRegisterInvalidRole(t *testing.T) {
	reg := NewAgentRegistry()
	err := reg.Register(&Agent{ID: "bad", Name: "BadRole", Role: AgentRole("overlord"), Active: true})
	if err == nil {
		t.Fatal("expected error for invalid role")
	}
}

func TestRegisterAllRoles(t *testing.T) {
	reg := NewAgentRegistry()
	roles := []AgentRole{RoleWorker, RoleScout, RoleCoordinator, RoleSpecialist}
	for i, role := range roles {
		err := reg.Register(&Agent{ID: fmt.Sprintf("r%d", i), Name: fmt.Sprintf("Role-%d", i), Role: role, Active: true})
		if err != nil {
			t.Errorf("failed to register role %s: %v", role, err)
		}
	}
	if reg.Count() != 4 {
		t.Errorf("expected 4 agents, got %d", reg.Count())
	}
}

func TestLookupAgent(t *testing.T) {
	reg := NewAgentRegistry()
	_ = reg.Register(&Agent{ID: "x1", Name: "X1", Role: RoleScout, Active: true})
	a, ok := reg.Lookup("x1")
	if !ok {
		t.Fatal("expected to find agent x1")
	}
	if a.Name != "X1" {
		t.Errorf("expected name X1, got %s", a.Name)
	}
	_, ok = reg.Lookup("missing")
	if ok {
		t.Error("expected not to find missing agent")
	}
}

func TestDeregisterAgent(t *testing.T) {
	reg := NewAgentRegistry()
	_ = reg.Register(&Agent{ID: "z1", Name: "Z1", Role: RoleWorker, Active: true})
	err := reg.Deregister("z1")
	if err != nil {
		t.Fatalf("deregister failed: %v", err)
	}
	if reg.Count() != 0 {
		t.Errorf("expected 0 agents, got %d", reg.Count())
	}
}

func TestDeregisterMissingAgent(t *testing.T) {
	reg := NewAgentRegistry()
	err := reg.Deregister("ghost")
	if err == nil {
		t.Fatal("expected error deregistering unknown agent")
	}
}

func TestListByRole(t *testing.T) {
	reg := NewAgentRegistry()
	_ = reg.Register(&Agent{ID: "w1", Name: "W1", Role: RoleWorker, Active: true})
	_ = reg.Register(&Agent{ID: "w2", Name: "W2", Role: RoleWorker, Active: false}) // inactive
	_ = reg.Register(&Agent{ID: "s1", Name: "S1", Role: RoleScout, Active: true})
	workers := reg.ListByRole(RoleWorker)
	if len(workers) != 1 {
		t.Errorf("expected 1 active worker, got %d", len(workers))
	}
	scouts := reg.ListByRole(RoleScout)
	if len(scouts) != 1 {
		t.Errorf("expected 1 scout, got %d", len(scouts))
	}
	coordinators := reg.ListByRole(RoleCoordinator)
	if len(coordinators) != 0 {
		t.Errorf("expected 0 coordinators, got %d", len(coordinators))
	}
}

// --- A2A Message Tests ---

func TestEncodeTELL(t *testing.T) {
	msg := &A2AMessage{Type: MsgTELL, From: "a1", To: "a2", Payload: "hello"}
	encoded, err := msg.Encode()
	if err != nil {
		t.Fatalf("encode failed: %v", err)
	}
	expected := "A2A:TELL|a1->a2|hello"
	if encoded != expected {
		t.Errorf("expected %q, got %q", expected, encoded)
	}
}

func TestEncodeASK(t *testing.T) {
	msg := &A2AMessage{Type: MsgASK, From: "a1", To: "a2", Payload: "status?"}
	encoded, err := msg.Encode()
	if err != nil {
		t.Fatalf("encode failed: %v", err)
	}
	expected := "A2A:ASK|a1->a2|status?"
	if encoded != expected {
		t.Errorf("expected %q, got %q", expected, encoded)
	}
}

func TestEncodeDELEGATE(t *testing.T) {
	msg := &A2AMessage{Type: MsgDELEGATE, From: "coordinator", To: "worker1", Payload: "task-42"}
	encoded, err := msg.Encode()
	if err != nil {
		t.Fatalf("encode failed: %v", err)
	}
	expected := "A2A:DELEGATE|coordinator->worker1|task-42"
	if encoded != expected {
		t.Errorf("expected %q, got %q", expected, encoded)
	}
}

func TestEncodeBROADCAST(t *testing.T) {
	msg := &A2AMessage{Type: MsgBROADCAST, From: "coordinator", Payload: "swarm-update"}
	encoded, err := msg.Encode()
	if err != nil {
		t.Fatalf("encode failed: %v", err)
	}
	expected := "A2A:BROADCAST|coordinator->*|swarm-update"
	if encoded != expected {
		t.Errorf("expected %q, got %q", expected, encoded)
	}
}

func TestEncodeWithRef(t *testing.T) {
	msg := &A2AMessage{Type: MsgTELL, From: "a1", To: "a2", Payload: "data", Ref: "corr-99"}
	encoded, err := msg.Encode()
	if err != nil {
		t.Fatalf("encode failed: %v", err)
	}
	if !strings.Contains(encoded, "#corr-99") {
		t.Errorf("expected ref #corr-99 in %q", encoded)
	}
}

func TestEncodeNoSender(t *testing.T) {
	msg := &A2AMessage{Type: MsgTELL, From: "", To: "a2", Payload: "x"}
	_, err := msg.Encode()
	if err == nil {
		t.Fatal("expected error for empty sender")
	}
}

func TestEncodeNoRecipientNonBroadcast(t *testing.T) {
	msg := &A2AMessage{Type: MsgTELL, From: "a1", To: "", Payload: "x"}
	_, err := msg.Encode()
	if err == nil {
		t.Fatal("expected error for missing recipient on TELL")
	}
}

func TestEncodeInvalidType(t *testing.T) {
	msg := &A2AMessage{Type: A2AMessageType("INVALID"), From: "a1", To: "a2", Payload: "x"}
	_, err := msg.Encode()
	if err == nil {
		t.Fatal("expected error for invalid message type")
	}
}

func TestDecodeRoundTrip(t *testing.T) {
	cases := []struct {
		name string
		msg  *A2AMessage
	}{
		{"TELL", &A2AMessage{Type: MsgTELL, From: "a1", To: "a2", Payload: "hi"}},
		{"ASK", &A2AMessage{Type: MsgASK, From: "a1", To: "a2", Payload: "q?"}},
		{"DELEGATE", &A2AMessage{Type: MsgDELEGATE, From: "c1", To: "w1", Payload: "task"}},
		{"BROADCAST", &A2AMessage{Type: MsgBROADCAST, From: "c1", Payload: "alert"}},
		{"WITH_REF", &A2AMessage{Type: MsgTELL, From: "a1", To: "a2", Payload: "data", Ref: "r1"}},
	}
	for _, tc := range cases {
		t.Run(tc.name, func(t *testing.T) {
			encoded, err := tc.msg.Encode()
			if err != nil {
				t.Fatalf("encode: %v", err)
			}
			decoded, err := DecodeA2AMessage(encoded)
			if err != nil {
				t.Fatalf("decode: %v", err)
			}
			if decoded.Type != tc.msg.Type {
				t.Errorf("type mismatch: want %s, got %s", tc.msg.Type, decoded.Type)
			}
			if decoded.From != tc.msg.From {
				t.Errorf("from mismatch: want %s, got %s", tc.msg.From, decoded.From)
			}
			expectedTo := tc.msg.To
			if tc.msg.Type == MsgBROADCAST {
				expectedTo = ""
			}
			if decoded.To != expectedTo {
				t.Errorf("to mismatch: want %q, got %q", expectedTo, decoded.To)
			}
			if decoded.Payload != tc.msg.Payload {
				t.Errorf("payload mismatch: want %q, got %q", tc.msg.Payload, decoded.Payload)
			}
			if decoded.Ref != tc.msg.Ref {
				t.Errorf("ref mismatch: want %q, got %q", tc.msg.Ref, decoded.Ref)
			}
		})
	}
}

func TestDecodeInvalidWire(t *testing.T) {
	_, err := DecodeA2AMessage("garbage")
	if err == nil {
		t.Fatal("expected error decoding garbage input")
	}
}

// --- Trust Matrix Tests ---

func TestTrustSetGet(t *testing.T) {
	tm := NewTrustMatrix()
	tm.Set("a", "b", 0.85)
	if v := tm.Get("a", "b"); v != 0.85 {
		t.Errorf("expected 0.85, got %f", v)
	}
}

func TestTrustDefaultZero(t *testing.T) {
	tm := NewTrustMatrix()
	if v := tm.Get("x", "y"); v != 0.0 {
		t.Errorf("expected 0.0 for unknown pair, got %f", v)
	}
}

func TestTrustClampHigh(t *testing.T) {
	tm := NewTrustMatrix()
	tm.Set("a", "b", 2.5)
	if v := tm.Get("a", "b"); v != 1.0 {
		t.Errorf("expected clamped to 1.0, got %f", v)
	}
}

func TestTrustClampLow(t *testing.T) {
	tm := NewTrustMatrix()
	tm.Set("a", "b", -0.5)
	if v := tm.Get("a", "b"); v != 0.0 {
		t.Errorf("expected clamped to 0.0, got %f", v)
	}
}

func TestTrustOverwrite(t *testing.T) {
	tm := NewTrustMatrix()
	tm.Set("a", "b", 0.5)
	tm.Set("a", "b", 0.9)
	if v := tm.Get("a", "b"); v != 0.9 {
		t.Errorf("expected 0.9 after overwrite, got %f", v)
	}
}

func TestAverageTrust(t *testing.T) {
	tm := NewTrustMatrix()
	tm.Set("a", "c", 0.8)
	tm.Set("b", "c", 0.6)
	avg := tm.AverageTrust("c")
	expected := (0.8 + 0.6) / 2.0
	if avg != expected {
		t.Errorf("expected average %f, got %f", expected, avg)
	}
}

func TestAverageTrustNoScores(t *testing.T) {
	tm := NewTrustMatrix()
	if v := tm.AverageTrust("unknown"); v != 0.0 {
		t.Errorf("expected 0.0, got %f", v)
	}
}

func TestTrustDecay(t *testing.T) {
	tm := NewTrustMatrix()
	tm.Set("a", "b", 1.0)
	tm.Set("c", "d", 0.5)
	tm.Decay(0.9)
	if v := tm.Get("a", "b"); v != 0.9 {
		t.Errorf("expected 0.9 after decay, got %f", v)
	}
	if v := tm.Get("c", "d"); v != 0.45 {
		t.Errorf("expected 0.45 after decay, got %f", v)
	}
}

func TestTrustDecayClampsToZero(t *testing.T) {
	tm := NewTrustMatrix()
	tm.Set("a", "b", 0.01)
	tm.Decay(0.0)
	if v := tm.Get("a", "b"); v != 0.0 {
		t.Errorf("expected 0.0 after zero decay, got %f", v)
	}
}

func TestTrustAsymmetric(t *testing.T) {
	tm := NewTrustMatrix()
	tm.Set("a", "b", 0.9)
	tm.Set("b", "a", 0.3)
	if tm.Get("a", "b") == tm.Get("b", "a") {
		t.Error("trust should be asymmetric")
	}
}

func TestTrustSelfScore(t *testing.T) {
	tm := NewTrustMatrix()
	tm.Set("a", "a", 1.0)
	if v := tm.Get("a", "a"); v != 1.0 {
		t.Errorf("expected self-trust 1.0, got %f", v)
	}
}

// --- VM Tests ---

func TestVMPushHalt(t *testing.T) {
	vm := NewVM([]byte{OP_PUSH, 42, OP_HALT})
	err := vm.Run()
	if err != nil {
		t.Fatalf("VM run failed: %v", err)
	}
	if top, ok := vm.StackTop(); !ok || top != 42 {
		t.Errorf("expected stack top 42, got %d", top)
	}
}

func TestVMAdd(t *testing.T) {
	vm := NewVM([]byte{OP_PUSH, 3, OP_PUSH, 4, OP_ADD, OP_HALT})
	err := vm.Run()
	if err != nil {
		t.Fatalf("VM run failed: %v", err)
	}
	if top, ok := vm.StackTop(); !ok || top != 7 {
		t.Errorf("expected 7, got %d", top)
	}
}

func TestVMSub(t *testing.T) {
	vm := NewVM([]byte{OP_PUSH, 10, OP_PUSH, 3, OP_SUB, OP_HALT})
	err := vm.Run()
	if err != nil {
		t.Fatalf("VM run failed: %v", err)
	}
	if top, ok := vm.StackTop(); !ok || top != 7 {
		t.Errorf("expected 7, got %d", top)
	}
}

func TestVMMul(t *testing.T) {
	vm := NewVM([]byte{OP_PUSH, 6, OP_PUSH, 7, OP_MUL, OP_HALT})
	err := vm.Run()
	if err != nil {
		t.Fatalf("VM run failed: %v", err)
	}
	if top, ok := vm.StackTop(); !ok || top != 42 {
		t.Errorf("expected 42, got %d", top)
	}
}

func TestVMDiv(t *testing.T) {
	vm := NewVM([]byte{OP_PUSH, 20, OP_PUSH, 4, OP_DIV, OP_HALT})
	err := vm.Run()
	if err != nil {
		t.Fatalf("VM run failed: %v", err)
	}
	if top, ok := vm.StackTop(); !ok || top != 5 {
		t.Errorf("expected 5, got %d", top)
	}
}

func TestVMDivByZero(t *testing.T) {
	vm := NewVM([]byte{OP_PUSH, 10, OP_PUSH, 0, OP_DIV})
	err := vm.Run()
	if err == nil {
		t.Fatal("expected division by zero error")
	}
}

func TestVMDup(t *testing.T) {
	vm := NewVM([]byte{OP_PUSH, 7, OP_DUP, OP_ADD, OP_HALT})
	err := vm.Run()
	if err != nil {
		t.Fatalf("VM run failed: %v", err)
	}
	if top, ok := vm.StackTop(); !ok || top != 14 {
		t.Errorf("expected 14, got %d", top)
	}
}

func TestVMSwap(t *testing.T) {
	// push 2, push 5, swap, sub => 5-2=3 (sub: a-b where a is deeper)
	vm := NewVM([]byte{OP_PUSH, 2, OP_PUSH, 5, OP_SWAP, OP_SUB, OP_HALT})
	err := vm.Run()
	if err != nil {
		t.Fatalf("VM run failed: %v", err)
	}
	if top, ok := vm.StackTop(); !ok || top != 3 {
		t.Errorf("expected 3, got %d", top)
	}
}

func TestVMNOP(t *testing.T) {
	vm := NewVM([]byte{OP_NOP, OP_PUSH, 1, OP_HALT})
	err := vm.Run()
	if err != nil {
		t.Fatalf("VM run failed: %v", err)
	}
	if top, ok := vm.StackTop(); !ok || top != 1 {
		t.Errorf("expected 1, got %d", top)
	}
}

func TestVMJump(t *testing.T) {
	// PUSH 1, JMP to 5 (the HALT at index 5), PUSH 99 (skipped)
	prog := []byte{OP_PUSH, 1, OP_JMP, 5, OP_PUSH, 99, OP_HALT}
	vm := NewVM(prog)
	err := vm.Run()
	if err != nil {
		t.Fatalf("VM run failed: %v", err)
	}
	if top, ok := vm.StackTop(); !ok || top != 1 {
		t.Errorf("expected 1 (PUSH 99 skipped), got %d", top)
	}
}

func TestVMJumpIfZero(t *testing.T) {
	// PUSH 0, JZ to 5 (HALT), PUSH 99 (skipped when 0)
	prog := []byte{OP_PUSH, 0, OP_JZ, 5, OP_PUSH, 99, OP_HALT}
	vm := NewVM(prog)
	err := vm.Run()
	if err != nil {
		t.Fatalf("VM run failed: %v", err)
	}
	// stack should be empty (0 was popped by JZ, 99 was skipped)
	if _, ok := vm.StackTop(); ok {
		t.Error("expected empty stack after JZ jump")
	}
}

func TestVMJZNotTaken(t *testing.T) {
	// PUSH 5, JZ to 6 (not taken), PUSH 10, HALT
	prog := []byte{OP_PUSH, 5, OP_JZ, 6, OP_PUSH, 10, OP_HALT}
	vm := NewVM(prog)
	err := vm.Run()
	if err != nil {
		t.Fatalf("VM run failed: %v", err)
	}
	if top, ok := vm.StackTop(); !ok || top != 10 {
		t.Errorf("expected 10, got %d", top)
	}
}

func TestVMStackUnderflow(t *testing.T) {
	vm := NewVM([]byte{OP_ADD})
	err := vm.Run()
	if err == nil {
		t.Fatal("expected stack underflow error")
	}
}

func TestVMUnknownOpcode(t *testing.T) {
	vm := NewVM([]byte{0xFE})
	err := vm.Run()
	if err == nil {
		t.Fatal("expected unknown opcode error")
	}
}

func TestVMAlreadyHalted(t *testing.T) {
	vm := NewVM([]byte{OP_HALT})
	_ = vm.Run()
	err := vm.Step()
	if err == nil {
		t.Fatal("expected error stepping halted VM")
	}
}

func TestVMEmptyProgram(t *testing.T) {
	vm := NewVM([]byte{})
	err := vm.Run()
	if err == nil {
		t.Fatal("expected error for empty program")
	}
}

func TestVMComplexProgram(t *testing.T) {
	// Compute (3 + 4) * 2 = 14
	prog := []byte{
		OP_PUSH, 3,
		OP_PUSH, 4,
		OP_ADD,
		OP_PUSH, 2,
		OP_MUL,
		OP_HALT,
	}
	vm := NewVM(prog)
	err := vm.Run()
	if err != nil {
		t.Fatalf("VM run failed: %v", err)
	}
	if top, ok := vm.StackTop(); !ok || top != 14 {
		t.Errorf("expected 14, got %d", top)
	}
}

func TestVMFactorial(t *testing.T) {
	// Compute 3! = 6 using a loop:
	// Start with acc=1, counter=3
	// Loop: DUP counter, JZ to end, MUL acc*counter, DEC counter (via PUSH 1 SUB), JMP loop
	// Simplified: manually unrolled
	prog := []byte{
		OP_PUSH, 1,       // acc = 1
		OP_PUSH, 3,       // counter = 3
		OP_MUL,           // acc = 3
		OP_PUSH, 2,       // counter = 2
		OP_MUL,           // acc = 6
		OP_PUSH, 1,       // counter = 1
		OP_MUL,           // acc = 6
		OP_HALT,
	}
	vm := NewVM(prog)
	err := vm.Run()
	if err != nil {
		t.Fatalf("VM run failed: %v", err)
	}
	if top, ok := vm.StackTop(); !ok || top != 6 {
		t.Errorf("expected 6, got %d", top)
	}
}

// --- ASCII Visualization Tests ---

func TestRenderEmptySwarm(t *testing.T) {
	out := RenderSwarmGrid(nil, NewTrustMatrix())
	if out != "(empty swarm)" {
		t.Errorf("unexpected empty swarm output: %q", out)
	}
}

func TestRenderSingleAgent(t *testing.T) {
	agents := []*Agent{{ID: "a1", Name: "A1", Role: RoleWorker, Active: true}}
	tm := NewTrustMatrix()
	out := RenderSwarmGrid(agents, tm)
	if !strings.Contains(out, "a1") {
		t.Error("expected agent ID in grid output")
	}
	if !strings.Contains(out, "-") {
		t.Error("expected self-cell marker '-' in grid")
	}
}

func TestRenderMultipleAgents(t *testing.T) {
	agents := []*Agent{
		{ID: "alpha", Name: "Alpha", Role: RoleWorker, Active: true},
		{ID: "beta", Name: "Beta", Role: RoleScout, Active: true},
	}
	tm := NewTrustMatrix()
	tm.Set("alpha", "beta", 0.7)
	tm.Set("beta", "alpha", 0.5)
	out := RenderSwarmGrid(agents, tm)
	if !strings.Contains(out, "0.7") {
		t.Error("expected trust score 0.7 in grid")
	}
	if !strings.Contains(out, "0.5") {
		t.Error("expected trust score 0.5 in grid")
	}
	// Check table structure
	lines := strings.Split(strings.TrimSpace(out), "\n")
	if len(lines) < 5 { // header + sep + agent rows + sep + bottom sep
		t.Errorf("expected multi-line grid, got %d lines", len(lines))
	}
}

func TestRenderAgentStatus(t *testing.T) {
	agents := []*Agent{
		{ID: "w1", Name: "Worker1", Role: RoleWorker, Active: true},
		{ID: "s1", Name: "Scout1", Role: RoleScout, Active: false},
	}
	out := RenderAgentStatus(agents)
	if !strings.Contains(out, "active") {
		t.Error("expected 'active' in status output")
	}
	if !strings.Contains(out, "inactive") {
		t.Error("expected 'inactive' in status output")
	}
	if !strings.Contains(out, "worker") {
		t.Error("expected role 'worker' in status output")
	}
	if !strings.Contains(out, "scout") {
		t.Error("expected role 'scout' in status output")
	}
}

func TestRenderAgentStatusEmpty(t *testing.T) {
	out := RenderAgentStatus(nil)
	if out != "(no agents)\n" && out != "(no agents)" {
		t.Errorf("unexpected empty status output: %q", out)
	}
}

func TestGridIDTruncation(t *testing.T) {
	agents := []*Agent{
		{ID: "verylongid", Name: "LongID", Role: RoleCoordinator, Active: true},
	}
	tm := NewTrustMatrix()
	out := RenderSwarmGrid(agents, tm)
	if !strings.Contains(out, "ver") {
		t.Error("expected truncated ID 'ver' in grid header")
	}
}

// --- Integration: Full Swarm Scenario ---

func TestFullSwarmScenario(t *testing.T) {
	// Register agents
	reg := NewAgentRegistry()
	agents := []*Agent{
		{ID: "coord", Name: "Coordinator", Role: RoleCoordinator, Active: true},
		{ID: "w1", Name: "Worker-1", Role: RoleWorker, Active: true},
		{ID: "w2", Name: "Worker-2", Role: RoleWorker, Active: true},
		{ID: "sc1", Name: "Scout-1", Role: RoleScout, Active: true},
	}
	for _, a := range agents {
		if err := reg.Register(a); err != nil {
			t.Fatalf("register %s: %v", a.ID, err)
		}
	}

	// Build trust
	tm := NewTrustMatrix()
	tm.Set("coord", "w1", 0.9)
	tm.Set("coord", "w2", 0.8)
	tm.Set("w1", "coord", 0.85)
	tm.Set("w2", "coord", 0.75)
	tm.Set("sc1", "coord", 0.95)

	// Send DELEGATE from coordinator
	msg := &A2AMessage{Type: MsgDELEGATE, From: "coord", To: "w1", Payload: "compute-42", Ref: "task-001"}
	encoded, err := msg.Encode()
	if err != nil {
		t.Fatalf("encode delegate: %v", err)
	}
	decoded, err := DecodeA2AMessage(encoded)
	if err != nil {
		t.Fatalf("decode delegate: %v", err)
	}
	if decoded.Payload != "compute-42" {
		t.Errorf("payload mismatch: %q", decoded.Payload)
	}

	// Execute FLUX program on "worker"
	prog := []byte{OP_PUSH, 6, OP_PUSH, 7, OP_MUL, OP_HALT}
	vm := NewVM(prog)
	if err := vm.Run(); err != nil {
		t.Fatalf("VM: %v", err)
	}
	result, _ := vm.StackTop()
	if result != 42 {
		t.Errorf("expected 42, got %d", result)
	}

	// Visualize
	grid := RenderSwarmGrid(agents, tm)
	if grid == "(empty swarm)" {
		t.Error("grid should not be empty")
	}

	// Verify trust metrics
	if tm.AverageTrust("coord") < 0.8 {
		t.Error("coordinator trust average too low")
	}

	// Send BROADCAST result
	resp := &A2AMessage{Type: MsgBROADCAST, From: "coord", Payload: "task-001-complete"}
	_, err = resp.Encode()
	if err != nil {
		t.Fatalf("encode broadcast: %v", err)
	}
}
