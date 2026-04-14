"""Comprehensive tests for the Polyglot FLUX-ese Compiler (polyglot_flux_compiler.py)."""

import sys
import os
import unittest

# Add scripts dir to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))


class TestOpcodes(unittest.TestCase):
    """Test the OPCODES instruction set definition."""

    def setUp(self):
        from polyglot_flux_compiler import OPCODES
        self.opcodes = OPCODES

    def test_opcodes_is_dict(self):
        """OPCODES is a dictionary."""
        self.assertIsInstance(self.opcodes, dict)

    def test_nop_opcode(self):
        """NOP has opcode 0x00."""
        self.assertEqual(self.opcodes["NOP"], 0x00)

    def test_halt_opcode(self):
        """HALT has opcode 0x01."""
        self.assertEqual(self.opcodes["HALT"], 0x01)

    def test_movi_opcode(self):
        """MOVI has opcode 0x10."""
        self.assertEqual(self.opcodes["MOVI"], 0x10)

    def test_mov_opcode(self):
        """MOV has opcode 0x11."""
        self.assertEqual(self.opcodes["MOV"], 0x11)

    def test_arithmetic_opcodes(self):
        """Arithmetic opcodes exist and are sequential."""
        self.assertEqual(self.opcodes["IADD"], 0x20)
        self.assertEqual(self.opcodes["ISUB"], 0x21)
        self.assertEqual(self.opcodes["IMUL"], 0x22)
        self.assertEqual(self.opcodes["IDIV"], 0x23)

    def test_jump_opcodes(self):
        """Jump opcodes exist."""
        self.assertEqual(self.opcodes["JMP"], 0x30)
        self.assertEqual(self.opcodes["JZ"], 0x31)
        self.assertEqual(self.opcodes["JNZ"], 0x32)

    def test_cmp_opcode(self):
        """CMP has opcode 0x40."""
        self.assertEqual(self.opcodes["CMP"], 0x40)

    def test_stack_opcodes(self):
        """Stack opcodes exist."""
        self.assertEqual(self.opcodes["PUSH"], 0x50)
        self.assertEqual(self.opcodes["POP"], 0x51)

    def test_call_ret_opcodes(self):
        """CALL and RET opcodes exist."""
        self.assertEqual(self.opcodes["CALL"], 0x60)
        self.assertEqual(self.opcodes["RET"], 0x61)

    def test_io_opcodes(self):
        """I/O opcodes exist in 0x80+ range."""
        self.assertEqual(self.opcodes["SAY"], 0x80)
        self.assertEqual(self.opcodes["TELL"], 0x81)
        self.assertEqual(self.opcodes["YELL"], 0x82)

    def test_sensor_opcodes(self):
        """Sensor opcodes exist in 0x90+ range."""
        self.assertEqual(self.opcodes["GAUGE"], 0x90)
        self.assertEqual(self.opcodes["ALERT"], 0x91)

    def test_evolve_opcode(self):
        """EVOLVE has opcode 0xA0."""
        self.assertEqual(self.opcodes["EVOLVE"], 0xA0)

    def test_at_least_20_opcodes(self):
        """ISA has at least 20 unique opcodes."""
        self.assertGreaterEqual(len(self.opcodes), 20)

    def test_all_opcode_values_are_int(self):
        """All opcode values are integers."""
        for name, value in self.opcodes.items():
            self.assertIsInstance(value, int, f"{name} value is not int")

    def test_all_opcode_values_are_positive(self):
        """All opcode values are non-negative."""
        for name, value in self.opcodes.items():
            self.assertGreaterEqual(value, 0, f"{name} is negative")


class TestPolyglotMap(unittest.TestCase):
    """Test the POLYGLOT_MAP keyword mapping."""

    def setUp(self):
        from polyglot_flux_compiler import POLYGLOT_MAP
        self.pmap = POLYGLOT_MAP

    def test_polyglot_map_is_dict(self):
        """POLYGLOT_MAP is a dictionary."""
        self.assertIsInstance(self.pmap, dict)

    def test_english_keywords(self):
        """English maritime keywords map to correct opcodes."""
        self.assertEqual(self.pmap["navigate"], "JMP")
        self.assertEqual(self.pmap["steer"], "MOV")
        self.assertEqual(self.pmap["anchor"], "HALT")
        self.assertEqual(self.pmap["sail"], "CALL")
        self.assertEqual(self.pmap["knots"], "IMUL")

    def test_japanese_keywords(self):
        """Japanese navigation keywords map correctly."""
        self.assertEqual(self.pmap["航海"], "CALL")
        self.assertEqual(self.pmap["舵"], "MOV")
        self.assertEqual(self.pmap["ノット"], "IMUL")
        self.assertEqual(self.pmap["回す"], "JNZ")
        self.assertEqual(self.pmap["着く"], "RET")

    def test_french_keywords(self):
        """French keywords map correctly."""
        self.assertEqual(self.pmap["fonction"], "CALL")
        self.assertEqual(self.pmap["vitesse"], "IMUL")
        self.assertEqual(self.pmap["jusque"], "JNZ")
        self.assertEqual(self.pmap["si"], "JZ")

    def test_german_keywords(self):
        """German keywords map correctly."""
        self.assertEqual(self.pmap["wiederhole"], "JNZ")
        self.assertEqual(self.pmap["funktion"], "CALL")
        self.assertEqual(self.pmap["setze"], "MOVI")

    def test_chinese_keywords(self):
        """Chinese keywords map correctly."""
        self.assertEqual(self.pmap["函数"], "CALL")
        self.assertEqual(self.pmap["循环"], "JNZ")
        self.assertEqual(self.pmap["如果"], "JZ")
        self.assertEqual(self.pmap["返回"], "RET")

    def test_spanish_keywords(self):
        """Spanish keywords map correctly."""
        self.assertEqual(self.pmap["función"], "CALL")
        self.assertEqual(self.pmap["mientras"], "JNZ")
        self.assertEqual(self.pmap["velocidad"], "IMUL")

    def test_russian_keywords(self):
        """Russian keywords map correctly."""
        self.assertEqual(self.pmap["функция"], "CALL")
        self.assertEqual(self.pmap["пока"], "JNZ")
        self.assertEqual(self.pmap["вернуть"], "RET")

    def test_arabic_keywords(self):
        """Arabic keywords map correctly."""
        self.assertEqual(self.pmap["دالة"], "CALL")
        self.assertEqual(self.pmap["حتى"], "CMP")
        self.assertEqual(self.pmap["سرعة"], "IMUL")

    def test_universal_programming_keywords(self):
        """Universal programming keywords map correctly."""
        self.assertEqual(self.pmap["loop"], "JNZ")
        self.assertEqual(self.pmap["if"], "JZ")
        self.assertEqual(self.pmap["else"], "JMP")
        self.assertEqual(self.pmap["return"], "RET")
        self.assertEqual(self.pmap["set"], "MOVI")
        self.assertEqual(self.pmap["add"], "IADD")
        self.assertEqual(self.pmap["sub"], "ISUB")
        self.assertEqual(self.pmap["goto"], "JMP")
        self.assertEqual(self.pmap["push"], "PUSH")
        self.assertEqual(self.pmap["pop"], "POP")
        self.assertEqual(self.pmap["say"], "SAY")
        self.assertEqual(self.pmap["gauge"], "GAUGE")
        self.assertEqual(self.pmap["alert"], "ALERT")
        self.assertEqual(self.pmap["evolve"], "EVOLVE")

    def test_maritime_register_keywords(self):
        """Maritime register names map to register numbers."""
        self.assertEqual(self.pmap["captain"], 0x00)
        self.assertEqual(self.pmap["helm"], 0x01)
        self.assertEqual(self.pmap["engine"], 0x02)
        self.assertEqual(self.pmap["compass"], 0x03)
        self.assertEqual(self.pmap["logbook"], 0x04)
        self.assertEqual(self.pmap["watch"], 0x05)

    def test_map_has_at_least_50_entries(self):
        """Polyglot map covers at least 50 keywords."""
        self.assertGreaterEqual(len(self.pmap), 50)

    def test_values_are_either_string_or_int(self):
        """All values are either string (opcode names) or int (registers)."""
        for key, value in self.pmap.items():
            self.assertTrue(
                isinstance(value, (str, int)),
                f"POLYGLOT_MAP[{key!r}] = {value!r} is neither str nor int"
            )


class TestCompileFluxEse(unittest.TestCase):
    """Test the compile_flux_ese function."""

    def setUp(self):
        from polyglot_flux_compiler import compile_flux_ese, OPCODES
        self.compile = compile_flux_ese
        self.opcodes = OPCODES

    def test_simple_set_halt(self):
        """A simple 'set 1 halt' compiles to MOVI, 1, HALT."""
        code = "set 1 halt"
        result = self.compile(code)
        self.assertIsInstance(result, bytes)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], self.opcodes["MOVI"])
        self.assertEqual(result[1], 1)
        self.assertEqual(result[2], self.opcodes["HALT"])

    def test_compilation_includes_trailing_halt(self):
        """Every compilation ends with HALT."""
        code = "set 42"
        result = self.compile(code)
        self.assertEqual(result[-1], self.opcodes["HALT"])

    def test_empty_source_produces_only_halt(self):
        """Empty source produces only HALT."""
        result = self.compile("")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], self.opcodes["HALT"])

    def test_comment_lines_ignored(self):
        """Lines starting with # are ignored."""
        code = "# this is a comment\nhalt"
        result = self.compile(code)
        # Should have: HALT (from source) + HALT (appended)
        self.assertEqual(result[-1], self.opcodes["HALT"])

    def test_multiple_instructions(self):
        """Multiple instructions on separate lines compile correctly."""
        code = "set 1\nset 2\nhalt"
        result = self.compile(code)
        self.assertGreaterEqual(len(result), 4)  # MOVI, 1, MOVI, 2, HALT

    def test_japanese_navigation_compiles(self):
        """Japanese keywords compile to correct opcodes."""
        code = "航海 着く"
        result = self.compile(code)
        self.assertEqual(result[0], self.opcodes["CALL"])  # 航海
        self.assertEqual(result[1], self.opcodes["RET"])   # 着く
        self.assertEqual(result[2], self.opcodes["HALT"])  # trailing

    def test_french_keywords_compiles(self):
        """French keywords compile to correct opcodes."""
        code = "si 1"
        result = self.compile(code)
        self.assertEqual(result[0], self.opcodes["JZ"])  # si

    def test_loop_keyword_compiles(self):
        """Loop keyword compiles to JNZ."""
        code = "loop"
        result = self.compile(code)
        self.assertEqual(result[0], self.opcodes["JNZ"])

    def test_evolve_keyword_compiles(self):
        """Evolve keyword compiles correctly."""
        code = "evolve"
        result = self.compile(code)
        self.assertEqual(result[0], self.opcodes["EVOLVE"])

    def test_numeric_immediate_values(self):
        """Numeric tokens compile as immediate byte values."""
        code = "set 255"
        result = self.compile(code)
        # MOVI 0xFF & HALT
        self.assertEqual(result[1], 255)

    def test_hex_immediate_values(self):
        """Hex tokens compile as immediate byte values."""
        code = "set 0x0A"
        result = self.compile(code)
        self.assertEqual(result[1], 0x0A)

    def test_large_numbers_masked_to_byte(self):
        """Numbers larger than 255 are masked to a single byte."""
        code = "set 300"
        result = self.compile(code)
        self.assertEqual(result[1], 300 & 0xFF)

    def test_unknown_tokens_ignored(self):
        """Unknown tokens are silently skipped."""
        code = "zzzzz halt"
        result = self.compile(code)
        self.assertEqual(result[-1], self.opcodes["HALT"])

    def test_verbose_flag(self):
        """Verbose mode doesn't change the output bytes."""
        code = "set 1 halt"
        result_quiet = self.compile(code)
        result_verbose = self.compile(code, verbose=True)
        self.assertEqual(result_quiet, result_verbose)

    def test_multilingual_program(self):
        """A multilingual program compiles successfully."""
        code = "set 東 ノット loop gauge alert evolve halt"
        result = self.compile(code)
        self.assertIsInstance(result, bytes)
        self.assertGreater(len(result), 1)


class TestDisassemble(unittest.TestCase):
    """Test the disassemble function."""

    def setUp(self):
        from polyglot_flux_compiler import disassemble
        self.disassemble = disassemble

    def test_disassemble_empty(self):
        """Empty bytecode produces empty disassembly."""
        result = self.disassemble(b"")
        self.assertEqual(result.strip(), "")

    def test_disassemble_single_nop(self):
        """Single NOP byte disassembles correctly."""
        result = self.disassemble(b"\x00")
        self.assertIn("NOP", result)
        self.assertIn("0x00", result)

    def test_disassemble_halt(self):
        """HALT byte disassembles correctly."""
        result = self.disassemble(b"\x01")
        self.assertIn("HALT", result)

    def test_disassemble_movi(self):
        """MOVI byte disassembles correctly."""
        result = self.disassemble(b"\x10")
        self.assertIn("MOVI", result)

    def test_disassemble_sequence(self):
        """A sequence of bytes disassembles with addresses."""
        result = self.disassemble(b"\x10\x01\x20\x01\x01")
        lines = result.strip().split("\n")
        self.assertEqual(len(lines), 5)
        # Check addresses
        self.assertIn("0000:", lines[0])
        self.assertIn("0001:", lines[1])

    def test_disassemble_unknown_opcodes(self):
        """Unknown opcodes show as DATA."""
        result = self.disassemble(b"\xFF")
        self.assertIn("DATA_0xFF", result)


class TestTranslateToEnglish(unittest.TestCase):
    """Test the translate_to_english function."""

    def setUp(self):
        from polyglot_flux_compiler import translate_to_english
        self.translate = translate_to_english

    def test_english_passthrough(self):
        """English keywords pass through."""
        result = self.translate("set loop halt")
        self.assertIn("movi", result)
        self.assertIn("jnz", result)
        self.assertIn("halt", result)

    def test_japanese_translated(self):
        """Japanese keywords are translated to English."""
        result = self.translate("航海 着く")
        self.assertIn("call", result)
        self.assertIn("ret", result)

    def test_french_translated(self):
        """French keywords are translated."""
        result = self.translate("si alors")
        self.assertIn("jz", result)
        self.assertIn("jmp", result)

    def test_register_keywords_translated(self):
        """Maritime register names translate to R registers."""
        result = self.translate("captain helm")
        self.assertIn("R0", result)
        self.assertIn("R1", result)

    def test_unknown_tokens_passthrough(self):
        """Unknown tokens pass through unchanged."""
        result = self.translate("xyzzy")
        self.assertIn("xyzzy", result)

    def test_empty_input(self):
        """Empty input returns empty string."""
        result = self.translate("")
        self.assertEqual(result, "")

    def test_numbers_preserved(self):
        """Numeric tokens are preserved."""
        result = self.translate("set 42")
        self.assertIn("42", result)


class TestCompilerEdgeCases(unittest.TestCase):
    """Edge case tests for the compiler."""

    def setUp(self):
        from polyglot_flux_compiler import compile_flux_ese, disassemble, OPCODES
        self.compile = compile_flux_ese
        self.disassemble = disassemble
        self.opcodes = OPCODES

    def test_roundtrip_compile_disassemble(self):
        """Compile then disassemble produces readable output."""
        code = "set 1 add 2 halt"
        bytecode = self.compile(code)
        disasm = self.disassemble(bytecode)
        self.assertIn("MOVI", disasm)
        self.assertIn("IADD", disasm)
        self.assertIn("HALT", disasm)

    def test_all_opcodes_compilable(self):
        """All opcode names can be compiled."""
        for name in self.opcodes:
            code = f"{name.lower()}"
            result = self.compile(code)
            self.assertIsInstance(result, bytes, f"Failed to compile: {name}")
            self.assertGreater(len(result), 0)

    def test_arabic_keywords_compilable(self):
        """Arabic keywords compile without error."""
        code = "دالة حتى سرعة"
        result = self.compile(code)
        self.assertIsInstance(result, bytes)
        self.assertGreater(len(result), 1)

    def test_russian_keywords_compilable(self):
        """Russian keywords compile without error."""
        code = "функция пока вернуть"
        result = self.compile(code)
        self.assertIsInstance(result, bytes)
        self.assertGreater(len(result), 1)


if __name__ == "__main__":
    unittest.main()
