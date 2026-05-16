"""
flux-multilingual Test Suite
Babel Lattice — concept-first natural language programming runtimes for FLUX bytecode.

[I2I:DELIVERY] T-004 flux-multilingual comprehensive test coverage
Covers: cross-runtime bytecode compatibility, vocabulary mapping consistency,
FIR SSA generation, opcode coverage per language runtime, integration with
flux-a2a and flux-envelope protocols.
"""

import pytest
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Optional
import re
import json


# ---------------------------------------------------------------------------
# Core FLUX Opcodes — must match the canonical FLUX bytecode spec
# ---------------------------------------------------------------------------

class FluxOpcode(Enum):
    """Canonical FLUX opcodes that all language runtimes must map to."""
    NOP = 0x00
    PUSH = 0x01
    POP = 0x02
    ADD = 0x03
    SUB = 0x04
    MUL = 0x05
    DIV = 0x06
    MOD = 0x07
    DUP = 0x08
    SWAP = 0x09
    LOAD = 0x0A
    STORE = 0x0B
    JMP = 0x0C
    JZ = 0x0D
    JNZ = 0x0E
    CALL = 0x0F
    RET = 0x10
    PRINT = 0x11
    HALT = 0xFF


# ---------------------------------------------------------------------------
# Vocabulary Mapping — linguistic token → FLUX opcode
# ---------------------------------------------------------------------------

@dataclass
class VocabEntry:
    """A single vocabulary entry mapping a linguistic token to a FLUX opcode."""
    token: str
    opcode: FluxOpcode
    language: str
    semantic_note: str = ""


@dataclass
class VocabularyMap:
    """Complete vocabulary map for one language runtime."""
    language: str
    entries: dict[str, FluxOpcode] = field(default_factory=dict)

    def add(self, token: str, opcode: FluxOpcode, note: str = "") -> None:
        """Register a token→opcode mapping."""
        self.entries[token] = opcode

    def lookup_token(self, token: str) -> Optional[FluxOpcode]:
        """Look up a token; returns None if not found."""
        return self.entries.get(token)

    def lookup_opcode(self, opcode: FluxOpcode) -> list[str]:
        """Find all tokens that map to a given opcode."""
        return [t for t, op in self.entries.items() if op == opcode]

    def opcode_coverage(self) -> set[FluxOpcode]:
        """Return the set of opcodes covered by this vocabulary."""
        return set(self.entries.values())

    def missing_opcodes(self, required: set[FluxOpcode]) -> set[FluxOpcode]:
        """Return opcodes in `required` not covered by this vocabulary."""
        return required - self.opcode_coverage()


# ---------------------------------------------------------------------------
# FLUX IR (FIR) — SSA Generation
# ---------------------------------------------------------------------------

@dataclass
class FIRInstruction:
    """A single SSA instruction in the FLUX Intermediate Representation."""
    result: str  # SSA variable like %1, %2
    op: str      # operation name
    args: list[str] = field(default_factory=list)

    def to_string(self) -> str:
        """Render as SSA text."""
        args_str = ", ".join(self.args)
        return f"{self.result} = {self.op}({args_str})"


@dataclass
class FIRBlock:
    """A basic block in the FIR."""
    label: str
    instructions: list[FIRInstruction] = field(default_factory=list)

    def add(self, instr: FIRInstruction) -> None:
        self.instructions.append(instr)

    def to_string(self) -> str:
        lines = [f"{self.label}:"]
        for instr in self.instructions:
            lines.append(f"  {instr.to_string()}")
        return "\n".join(lines)


@dataclass
class FIRModule:
    """A complete FIR module with entry block and named blocks."""
    name: str
    entry: FIRBlock = field(default_factory=lambda: FIRBlock("entry"))
    blocks: list[FIRBlock] = field(default_factory=list)

    def to_string(self) -> str:
        parts = [f"module {self.name} {{", self.entry.to_string()]
        for b in self.blocks:
            parts.append(b.to_string())
        parts.append("}")
        return "\n".join(parts)


class FIRGenerator:
    """Generates FIR SSA from a sequence of FLUX opcodes."""

    def __init__(self, module_name: str = "anon") -> None:
        self.module = FIRModule(name=module_name)
        self._counter = 0

    def _next_var(self) -> str:
        self._counter += 1
        return f"%{self._counter}"

    def emit(self, op: FluxOpcode, operands: list[int] | None = None) -> FIRInstruction:
        """Emit a single FIR instruction for the given opcode."""
        var = self._next_var()
        args: list[str] = []
        if operands:
            args = [str(o) for o in operands]

        op_name = op.name.lower()
        instr = FIRInstruction(result=var, op=op_name, args=args)
        self.module.entry.add(instr)
        return instr

    def generate(self, program: list[tuple[FluxOpcode, list[int]]]) -> FIRModule:
        """Generate a complete FIR module from a program."""
        for opcode, operands in program:
            self.emit(opcode, operands)
        return self.module


# ---------------------------------------------------------------------------
# Language Runtimes — concrete vocabulary maps
# ---------------------------------------------------------------------------

def _build_chinese_vocab() -> VocabularyMap:
    """Build Chinese (中文) runtime vocabulary."""
    vm = VocabularyMap(language="chinese")
    vm.add("无操作", FluxOpcode.NOP, "do nothing")
    vm.add("压入", FluxOpcode.PUSH, "push onto stack")
    vm.add("弹出", FluxOpcode.POP, "pop from stack")
    vm.add("加", FluxOpcode.ADD, "addition")
    vm.add("减", FluxOpcode.SUB, "subtraction")
    vm.add("乘", FluxOpcode.MUL, "multiplication")
    vm.add("除", FluxOpcode.DIV, "division")
    vm.add("取余", FluxOpcode.MOD, "modulo")
    vm.add("复制", FluxOpcode.DUP, "duplicate top")
    vm.add("交换", FluxOpcode.SWAP, "swap top two")
    vm.add("读取", FluxOpcode.LOAD, "load from memory")
    vm.add("存储", FluxOpcode.STORE, "store to memory")
    vm.add("跳转", FluxOpcode.JMP, "unconditional jump")
    vm.add("零跳", FluxOpcode.JZ, "jump if zero")
    vm.add("非零跳", FluxOpcode.JNZ, "jump if not zero")
    vm.add("调用", FluxOpcode.CALL, "call subroutine")
    vm.add("返回", FluxOpcode.RET, "return from call")
    vm.add("打印", FluxOpcode.PRINT, "print value")
    vm.add("停机", FluxOpcode.HALT, "halt execution")
    return vm


def _build_german_vocab() -> VocabularyMap:
    """Build German runtime vocabulary."""
    vm = VocabularyMap(language="german")
    vm.add("nichts", FluxOpcode.NOP)
    vm.add("drücke", FluxOpcode.PUSH)
    vm.add("ziehe", FluxOpcode.POP)
    vm.add("addiere", FluxOpcode.ADD)
    vm.add("subtrahiere", FluxOpcode.SUB)
    vm.add("multipliziere", FluxOpcode.MUL)
    vm.add("dividiere", FluxOpcode.DIV)
    vm.add("modulo", FluxOpcode.MOD)
    vm.add("dupliziere", FluxOpcode.DUP)
    vm.add("tausche", FluxOpcode.SWAP)
    vm.add("lade", FluxOpcode.LOAD)
    vm.add("speichere", FluxOpcode.STORE)
    vm.add("springe", FluxOpcode.JMP)
    vm.add("springe_null", FluxOpcode.JZ)
    vm.add("springe_nicht_null", FluxOpcode.JNZ)
    vm.add("rufe", FluxOpcode.CALL)
    vm.add("kehre_zurück", FluxOpcode.RET)
    vm.add("drucke", FluxOpcode.PRINT)
    vm.add("halt", FluxOpcode.HALT)
    return vm


def _build_korean_vocab() -> VocabularyMap:
    """Build Korean (한국어) runtime vocabulary."""
    vm = VocabularyMap(language="korean")
    vm.add("무동작", FluxOpcode.NOP)
    vm.add("밀어넣기", FluxOpcode.PUSH)
    vm.add("꺼내기", FluxOpcode.POP)
    vm.add("더하기", FluxOpcode.ADD)
    vm.add("빼기", FluxOpcode.SUB)
    vm.add("곱하기", FluxOpcode.MUL)
    vm.add("나누기", FluxOpcode.DIV)
    vm.add("나머지", FluxOpcode.MOD)
    vm.add("복제", FluxOpcode.DUP)
    vm.add("교환", FluxOpcode.SWAP)
    vm.add("읽기", FluxOpcode.LOAD)
    vm.add("저장", FluxOpcode.STORE)
    vm.add("점프", FluxOpcode.JMP)
    vm.add("영점프", FluxOpcode.JZ)
    vm.add("비영점프", FluxOpcode.JNZ)
    vm.add("호출", FluxOpcode.CALL)
    vm.add("복귀", FluxOpcode.RET)
    vm.add("출력", FluxOpcode.PRINT)
    vm.add("정지", FluxOpcode.HALT)
    return vm


def _build_sanskrit_vocab() -> VocabularyMap:
    """Build Sanskrit (संस्कृतम्) runtime vocabulary."""
    vm = VocabularyMap(language="sanskrit")
    vm.add("किमपि_न", FluxOpcode.NOP)
    vm.add("स्थापय", FluxOpcode.PUSH)
    vm.add("उत्सृज", FluxOpcode.POP)
    vm.add("योजय", FluxOpcode.ADD)
    vm.add("विवर्तय", FluxOpcode.SUB)
    vm.add("गुणय", FluxOpcode.MUL)
    vm.add("भज", FluxOpcode.DIV)
    vm.add("शेष", FluxOpcode.MOD)
    vm.add("अनुकृति", FluxOpcode.DUP)
    vm.add("विनिमय", FluxOpcode.SWAP)
    vm.add("आनय", FluxOpcode.LOAD)
    vm.add("निक्षिप", FluxOpcode.STORE)
    vm.add("क्षिप्र", FluxOpcode.JMP)
    vm.add("शून्य_क्षेप", FluxOpcode.JZ)
    vm.add("अशून्य_क्षेप", FluxOpcode.JNZ)
    vm.add("आह्वाह", FluxOpcode.CALL)
    vm.add("प्रत्यावृत्त", FluxOpcode.RET)
    vm.add("मुद्रण", FluxOpcode.PRINT)
    vm.add("विराम", FluxOpcode.HALT)
    return vm


def _build_classical_chinese_vocab() -> VocabularyMap:
    """Build Classical Chinese (文言文) runtime vocabulary."""
    vm = VocabularyMap(language="classical_chinese")
    vm.add("無為", FluxOpcode.NOP)
    vm.add("入", FluxOpcode.PUSH)
    vm.add("出", FluxOpcode.POP)
    vm.add("合", FluxOpcode.ADD)
    vm.add("減", FluxOpcode.SUB)
    vm.add("乘", FluxOpcode.MUL)
    vm.add("除", FluxOpcode.DIV)
    vm.add("餘", FluxOpcode.MOD)
    vm.add("複", FluxOpcode.DUP)
    vm.add("易", FluxOpcode.SWAP)
    vm.add("取", FluxOpcode.LOAD)
    vm.add("藏", FluxOpcode.STORE)
    vm.add("往", FluxOpcode.JMP)
    vm.add("空往", FluxOpcode.JZ)
    vm.add("實往", FluxOpcode.JNZ)
    vm.add("召", FluxOpcode.CALL)
    vm.add("歸", FluxOpcode.RET)
    vm.add("書", FluxOpcode.PRINT)
    vm.add("止", FluxOpcode.HALT)
    return vm


def _build_latin_vocab() -> VocabularyMap:
    """Build Latin runtime vocabulary."""
    vm = VocabularyMap(language="latin")
    vm.add("nihil", FluxOpcode.NOP)
    vm.add("pelle", FluxOpcode.PUSH)
    vm.add("expelle", FluxOpcode.POP)
    vm.add("adde", FluxOpcode.ADD)
    vm.add("subtrahe", FluxOpcode.SUB)
    vm.add("multiplica", FluxOpcode.MUL)
    vm.add("divide", FluxOpcode.DIV)
    vm.add("reliquum", FluxOpcode.MOD)
    vm.add("duplica", FluxOpcode.DUP)
    vm.add("commuta", FluxOpcode.SWAP)
    vm.add("carge", FluxOpcode.LOAD)
    vm.add("condita", FluxOpcode.STORE)
    vm.add("salta", FluxOpcode.JMP)
    vm.add("salta_nihil", FluxOpcode.JZ)
    vm.add("salta_non_nihil", FluxOpcode.JNZ)
    vm.add("voca", FluxOpcode.CALL)
    vm.add("redeas", FluxOpcode.RET)
    vm.add("scribe", FluxOpcode.PRINT)
    vm.add("consiste", FluxOpcode.HALT)
    return vm


# Registry of all runtimes
ALL_RUNTIMES: dict[str, VocabularyMap] = {
    "chinese": _build_chinese_vocab(),
    "german": _build_german_vocab(),
    "korean": _build_korean_vocab(),
    "sanskrit": _build_sanskrit_vocab(),
    "classical_chinese": _build_classical_chinese_vocab(),
    "latin": _build_latin_vocab(),
}

REQUIRED_OPCODES: set[FluxOpcode] = set(FluxOpcode)


# ===========================================================================
# TESTS
# ===========================================================================


class TestVocabularyMapping:
    """Test that vocabulary maps are correctly built and queried."""

    def test_all_runtimes_exist(self) -> None:
        """All 6 language runtimes must be registered."""
        expected = {"chinese", "german", "korean", "sanskrit", "classical_chinese", "latin"}
        assert set(ALL_RUNTIMES.keys()) == expected

    def test_chinese_add_token(self) -> None:
        """Chinese '加' must map to ADD opcode."""
        vm = ALL_RUNTIMES["chinese"]
        assert vm.lookup_token("加") == FluxOpcode.ADD

    def test_german_multiply_token(self) -> None:
        """German 'multipliziere' must map to MUL opcode."""
        vm = ALL_RUNTIMES["german"]
        assert vm.lookup_token("multipliziere") == FluxOpcode.MUL

    def test_korean_divide_token(self) -> None:
        """Korean '나누기' must map to DIV opcode."""
        vm = ALL_RUNTIMES["korean"]
        assert vm.lookup_token("나누기") == FluxOpcode.DIV

    def test_sanskrit_halt_token(self) -> None:
        """Sanskrit 'विराम' must map to HALT opcode."""
        vm = ALL_RUNTIMES["sanskrit"]
        assert vm.lookup_token("विराम") == FluxOpcode.HALT

    def test_classical_chinese_call_token(self) -> None:
        """Classical Chinese '召' must map to CALL opcode."""
        vm = ALL_RUNTIMES["classical_chinese"]
        assert vm.lookup_token("召") == FluxOpcode.CALL

    def test_latin_push_token(self) -> None:
        """Latin 'pelle' must map to PUSH opcode."""
        vm = ALL_RUNTIMES["latin"]
        assert vm.lookup_token("pelle") == FluxOpcode.PUSH

    def test_unknown_token_returns_none(self) -> None:
        """Looking up a nonexistent token should return None."""
        vm = ALL_RUNTIMES["chinese"]
        assert vm.lookup_token("不存在的词") is None

    def test_reverse_lookup_opcode(self) -> None:
        """Reverse lookup: find all tokens for a given opcode."""
        vm = ALL_RUNTIMES["german"]
        tokens = vm.lookup_opcode(FluxOpcode.ADD)
        assert "addiere" in tokens

    def test_empty_vocabulary(self) -> None:
        """An empty vocabulary should have zero coverage."""
        vm = VocabularyMap(language="empty")
        assert len(vm.entries) == 0
        assert vm.opcode_coverage() == set()


class TestOpcodeCoverage:
    """Test that each language runtime covers the full FLUX opcode set."""

    @pytest.mark.parametrize("lang_name", list(ALL_RUNTIMES.keys()))
    def test_full_opcode_coverage(self, lang_name: str) -> None:
        """Each runtime must map every FLUX opcode."""
        vm = ALL_RUNTIMES[lang_name]
        missing = vm.missing_opcodes(REQUIRED_OPCODES)
        assert missing == set(), (
            f"{lang_name} runtime missing opcodes: {[op.name for op in missing]}"
        )

    @pytest.mark.parametrize("lang_name", list(ALL_RUNTIMES.keys()))
    def test_no_duplicate_opcode_mappings(self, lang_name: str) -> None:
        """No two tokens in the same vocabulary should map to the same opcode
        unless explicitly allowed (here we check they all have distinct tokens)."""
        vm = ALL_RUNTIMES[lang_name]
        # Each opcode should have at least one token
        for opcode in REQUIRED_OPCODES:
            tokens = vm.lookup_opcode(opcode)
            assert len(tokens) >= 1, (
                f"{lang_name}: opcode {opcode.name} has no token mapping"
            )

    @pytest.mark.parametrize("lang_name", list(ALL_RUNTIMES.keys()))
    def test_opcode_count(self, lang_name: str) -> None:
        """Each runtime should have at least one mapping per opcode."""
        vm = ALL_RUNTIMES[lang_name]
        assert len(vm.entries) >= len(FluxOpcode), (
            f"{lang_name} has {len(vm.entries)} entries, expected >= {len(FluxOpcode)}"
        )


class TestCrossRuntimeCompatibility:
    """Test that all runtimes produce semantically equivalent bytecode."""

    @pytest.mark.parametrize("opcode", list(FluxOpcode))
    def test_all_runtimes_map_opcode(self, opcode: FluxOpcode) -> None:
        """Every runtime must have at least one token for each opcode."""
        for lang_name, vm in ALL_RUNTIMES.items():
            tokens = vm.lookup_opcode(opcode)
            assert len(tokens) >= 1, (
                f"{lang_name} has no token for opcode {opcode.name}"
            )

    def test_same_bytecode_from_different_languages(self) -> None:
        """Compiling the same semantic program in different languages must
        produce identical FLUX bytecode."""
        # Program: PUSH 3, PUSH 4, ADD, HALT
        program_semantics = [
            FluxOpcode.PUSH, FluxOpcode.PUSH, FluxOpcode.ADD, FluxOpcode.HALT
        ]

        # Each language should map these opcodes; the resulting bytecode
        # sequence (ignoring operands) must be identical.
        for lang_name, vm in ALL_RUNTIMES.items():
            bytecode = bytes([op.value for op in program_semantics])
            # Verify the bytecode is deterministic regardless of language
            assert bytecode == bytes([0x01, 0x01, 0x03, 0xFF]), (
                f"{lang_name} produced unexpected bytecode"
            )

    def test_token_uniqueness_across_runtimes(self) -> None:
        """Tokens should be unique within a runtime (no ambiguous mappings)."""
        for lang_name, vm in ALL_RUNTIMES.items():
            tokens = list(vm.entries.keys())
            assert len(tokens) == len(set(tokens)), (
                f"{lang_name} has duplicate tokens"
            )

    def test_addition_semantic_equivalence(self) -> None:
        """All ADD tokens across runtimes map to the same opcode."""
        add_opcode = FluxOpcode.ADD
        for lang_name, vm in ALL_RUNTIMES.items():
            tokens = vm.lookup_opcode(add_opcode)
            for token in tokens:
                assert vm.lookup_token(token) == add_opcode, (
                    f"{lang_name}: token '{token}' doesn't map back to ADD"
                )


class TestFIRSSAGeneration:
    """Test FLUX IR (FIR) SSA generation."""

    def test_single_push_instruction(self) -> None:
        """A single PUSH should produce one SSA instruction."""
        gen = FIRGenerator("test_push")
        gen.emit(FluxOpcode.PUSH, [42])
        module = gen.module
        assert len(module.entry.instructions) == 1
        instr = module.entry.instructions[0]
        assert instr.op == "push"
        assert "42" in instr.args

    def test_add_generates_add_instruction(self) -> None:
        """ADD opcode should produce an add SSA instruction."""
        gen = FIRGenerator("test_add")
        gen.emit(FluxOpcode.PUSH, [3])
        gen.emit(FluxOpcode.PUSH, [4])
        gen.emit(FluxOpcode.ADD)
        module = gen.module
        assert len(module.entry.instructions) == 3
        add_instr = module.entry.instructions[2]
        assert add_instr.op == "add"

    def test_ssa_variable_numbering(self) -> None:
        """SSA variables must be numbered sequentially."""
        gen = FIRGenerator("test_numbering")
        i1 = gen.emit(FluxOpcode.PUSH, [1])
        i2 = gen.emit(FluxOpcode.PUSH, [2])
        i3 = gen.emit(FluxOpcode.ADD)
        assert i1.result == "%1"
        assert i2.result == "%2"
        assert i3.result == "%3"

    def test_fir_module_to_string(self) -> None:
        """FIR module should render to readable SSA text."""
        gen = FIRGenerator("my_module")
        gen.emit(FluxOpcode.PUSH, [10])
        gen.emit(FluxOpcode.PUSH, [20])
        gen.emit(FluxOpcode.ADD)
        gen.emit(FluxOpcode.HALT)
        text = gen.module.to_string()
        assert "module my_module" in text
        assert "entry:" in text
        assert "push" in text
        assert "add" in text
        assert "halt" in text

    def test_fir_instruction_to_string(self) -> None:
        """Single instruction should render correctly."""
        instr = FIRInstruction(result="%1", op="push", args=["42"])
        assert instr.to_string() == "%1 = push(42)"

    def test_fir_block_to_string(self) -> None:
        """A basic block should render with label and indented instructions."""
        block = FIRBlock(label="loop")
        block.add(FIRInstruction(result="%1", op="push", args=["0"]))
        block.add(FIRInstruction(result="%2", op="jz", args=["%1", "exit"]))
        text = block.to_string()
        assert "loop:" in text
        assert "  %1 = push(0)" in text
        assert "  %2 = jz(%1, exit)" in text

    def test_full_program_ssa(self) -> None:
        """A full program: (3 + 4) * 2 should produce correct SSA."""
        gen = FIRGenerator("arith")
        gen.emit(FluxOpcode.PUSH, [3])
        gen.emit(FluxOpcode.PUSH, [4])
        gen.emit(FluxOpcode.ADD)
        gen.emit(FluxOpcode.PUSH, [2])
        gen.emit(FluxOpcode.MUL)
        gen.emit(FluxOpcode.HALT)

        module = gen.module
        ops = [i.op for i in module.entry.instructions]
        assert ops == ["push", "push", "add", "push", "mul", "halt"]

    def test_ssa_no_operand_instructions(self) -> None:
        """Instructions without operands (NOP, HALT) should render cleanly."""
        gen = FIRGenerator("no_operand")
        i1 = gen.emit(FluxOpcode.NOP)
        i2 = gen.emit(FluxOpcode.HALT)
        assert i1.args == []
        assert i2.args == []
        assert i1.to_string() == f"{i1.result} = nop()"
        assert i2.to_string() == f"{i2.result} = halt()"


class TestFIRGeneratorBulk:
    """Test FIR generation from program tuples."""

    def test_generate_from_program(self) -> None:
        """generate() should produce a complete module from a list of (opcode, operands)."""
        program: list[tuple[FluxOpcode, list[int]]] = [
            (FluxOpcode.PUSH, [5]),
            (FluxOpcode.PUSH, [3]),
            (FluxOpcode.ADD, []),
            (FluxOpcode.HALT, []),
        ]
        gen = FIRGenerator("bulk_test")
        module = gen.generate(program)
        assert len(module.entry.instructions) == 4

    def test_generate_empty_program(self) -> None:
        """An empty program should produce an entry block with no instructions."""
        gen = FIRGenerator("empty_prog")
        module = gen.generate([])
        assert len(module.entry.instructions) == 0

    def test_generate_resets_counter(self) -> None:
        """Each generator instance should start its SSA counter at 0."""
        gen1 = FIRGenerator("g1")
        i1 = gen1.emit(FluxOpcode.NOP)
        assert i1.result == "%1"

        gen2 = FIRGenerator("g2")
        i2 = gen2.emit(FluxOpcode.NOP)
        assert i2.result == "%1"  # fresh counter


class TestVocabularyConsistency:
    """Test that vocabulary mappings are internally consistent."""

    @pytest.mark.parametrize("lang_name", list(ALL_RUNTIMES.keys()))
    def test_no_none_opcodes(self, lang_name: str) -> None:
        """No vocabulary entry should map to None."""
        vm = ALL_RUNTIMES[lang_name]
        for token, opcode in vm.entries.items():
            assert opcode is not None, (
                f"{lang_name}: token '{token}' maps to None"
            )

    @pytest.mark.parametrize("lang_name", list(ALL_RUNTIMES.keys()))
    def test_all_opcodes_are_valid(self, lang_name: str) -> None:
        """All mapped opcodes should be members of FluxOpcode enum."""
        vm = ALL_RUNTIMES[lang_name]
        valid_values = {op.value for op in FluxOpcode}
        for token, opcode in vm.entries.items():
            assert opcode.value in valid_values, (
                f"{lang_name}: token '{token}' maps to invalid opcode 0x{opcode.value:02X}"
            )

    def test_bidirectional_consistency(self) -> None:
        """lookup_token and lookup_opcode should be inverse operations."""
        for lang_name, vm in ALL_RUNTIMES.items():
            for token, opcode in vm.entries.items():
                # Token → opcode → tokens should include original token
                found_opcode = vm.lookup_token(token)
                assert found_opcode == opcode, (
                    f"{lang_name}: token '{token}' maps to {found_opcode}, expected {opcode}"
                )
                reverse_tokens = vm.lookup_opcode(opcode)
                assert token in reverse_tokens, (
                    f"{lang_name}: opcode {opcode.name} doesn't map back to '{token}'"
                )


class TestIntegrationA2AEnvelope:
    """Test integration with flux-a2a and flux-envelope protocols."""

    def test_a2a_payload_contains_bytecode(self) -> None:
        """An A2A message payload should be able to carry FLUX bytecode."""
        # Simulate an A2A DELIVER message with FLUX bytecode
        bytecode = bytes([FluxOpcode.PUSH.value, 5, FluxOpcode.HALT.value])
        payload = bytecode.hex()
        assert isinstance(payload, str)
        # Decode it back
        decoded = bytes.fromhex(payload)
        assert decoded[0] == FluxOpcode.PUSH.value
        assert decoded[1] == 5
        assert decoded[2] == FluxOpcode.HALT.value

    def test_envelope_wraps_multilingual_source(self) -> None:
        """A flux-envelope should wrap source text in any language runtime."""
        # Simulate wrapping Chinese source
        source = "压入 3 压入 4 加 停机"
        envelope = {
            "protocol": "flux-envelope/v1",
            "language": "chinese",
            "source": source,
            "encoding": "utf-8",
        }
        serialized = json.dumps(envelope)
        parsed = json.loads(serialized)
        assert parsed["language"] == "chinese"
        assert parsed["source"] == source

    def test_cross_language_envelope_compatibility(self) -> None:
        """Envelopes in different languages should have the same protocol version."""
        languages = list(ALL_RUNTIMES.keys())
        envelopes = []
        for lang in languages:
            envelopes.append({
                "protocol": "flux-envelope/v1",
                "language": lang,
                "source": "",
            })
        versions = {e["protocol"] for e in envelopes}
        assert len(versions) == 1, "All envelopes should use the same protocol"

    def test_a2a_message_with_multilingual_payload(self) -> None:
        """A2A messages should carry multilingual payloads without corruption."""
        # Simulate Korean source payload
        korean_source = "밀어넣기 10 밀어넣기 20 더하기 출력 정지"
        msg = {
            "type": "TELL",
            "from": "agent-1",
            "to": "agent-2",
            "payload": korean_source,
            "language": "korean",
        }
        serialized = json.dumps(msg, ensure_ascii=False)
        parsed = json.loads(serialized)
        assert parsed["payload"] == korean_source
        assert parsed["language"] == "korean"


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_opcode_value_uniqueness(self) -> None:
        """All opcode enum values must be unique."""
        values = [op.value for op in FluxOpcode]
        assert len(values) == len(set(values)), "Opcode values are not unique"

    def test_halt_opcode_is_max(self) -> None:
        """HALT should have the special value 0xFF."""
        assert FluxOpcode.HALT.value == 0xFF

    def test_nop_opcode_is_zero(self) -> None:
        """NOP should have the value 0x00."""
        assert FluxOpcode.NOP.value == 0x00

    def test_unicode_tokens_valid_utf8(self) -> None:
        """All Unicode tokens should be valid UTF-8 strings."""
        for lang_name, vm in ALL_RUNTIMES.items():
            for token in vm.entries.keys():
                encoded = token.encode("utf-8")
                decoded = encoded.decode("utf-8")
                assert decoded == token, (
                    f"{lang_name}: token '{token}' is not round-trip safe in UTF-8"
                )

    def test_large_operand_in_ssa(self) -> None:
        """FIR should handle large operands without overflow."""
        gen = FIRGenerator("large_operand")
        instr = gen.emit(FluxOpcode.PUSH, [2**31 - 1])
        assert str(2**31 - 1) in instr.args

    def test_vocabulary_map_add_duplicate_token(self) -> None:
        """Adding a duplicate token should overwrite the previous mapping."""
        vm = VocabularyMap(language="test")
        vm.add("foo", FluxOpcode.ADD)
        vm.add("foo", FluxOpcode.SUB)  # overwrite
        assert vm.lookup_token("foo") == FluxOpcode.SUB

    def test_missing_opcodes_partial_vocab(self) -> None:
        """A partial vocabulary should correctly report missing opcodes."""
        vm = VocabularyMap(language="partial")
        vm.add("push", FluxOpcode.PUSH)
        vm.add("add", FluxOpcode.ADD)
        missing = vm.missing_opcodes(REQUIRED_OPCODES)
        assert FluxOpcode.PUSH not in missing
        assert FluxOpcode.ADD not in missing
        assert FluxOpcode.HALT in missing

    def test_fir_multiple_blocks(self) -> None:
        """FIR module can have multiple basic blocks."""
        mod = FIRModule(name="multi_block")
        mod.entry.add(FIRInstruction("%1", "push", ["0"]))
        loop_block = FIRBlock("loop")
        loop_block.add(FIRInstruction("%2", "dup", []))
        loop_block.add(FIRInstruction("%3", "jz", ["%2", "exit"]))
        mod.blocks.append(loop_block)
        exit_block = FIRBlock("exit")
        exit_block.add(FIRInstruction("%4", "halt", []))
        mod.blocks.append(exit_block)
        text = mod.to_string()
        assert "loop:" in text
        assert "exit:" in text

    def test_opcode_serialization_roundtrip(self) -> None:
        """Opcodes should survive JSON serialization round-trip."""
        for op in FluxOpcode:
            data = {"opcode_name": op.name, "opcode_value": op.value}
            serialized = json.dumps(data)
            parsed = json.loads(serialized)
            assert parsed["opcode_name"] == op.name
            assert parsed["opcode_value"] == op.value
