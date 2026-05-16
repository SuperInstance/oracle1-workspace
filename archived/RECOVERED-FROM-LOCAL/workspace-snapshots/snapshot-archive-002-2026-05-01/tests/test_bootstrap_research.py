"""Comprehensive tests for the Bootstrap Research Experiment Runner."""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))


class TestFluxOpsDict(unittest.TestCase):
    """Test the FLUX_OPS opcode definitions."""

    def test_flux_ops_is_dict(self):
        from bootstrap_research import FLUX_OPS
        self.assertIsInstance(FLUX_OPS, dict)

    def test_core_opcodes_present(self):
        from bootstrap_research import FLUX_OPS
        self.assertIn("NOP", FLUX_OPS)
        self.assertIn("HALT", FLUX_OPS)
        self.assertIn("MOVI", FLUX_OPS)
        self.assertIn("MOV", FLUX_OPS)
        self.assertIn("IADD", FLUX_OPS)
        self.assertIn("ISUB", FLUX_OPS)
        self.assertIn("JMP", FLUX_OPS)
        self.assertIn("JZ", FLUX_OPS)
        self.assertIn("JNZ", FLUX_OPS)
        self.assertIn("CMP", FLUX_OPS)
        self.assertIn("PUSH", FLUX_OPS)
        self.assertIn("POP", FLUX_OPS)
        self.assertIn("CALL", FLUX_OPS)
        self.assertIn("RET", FLUX_OPS)
        self.assertIn("GAUGE", FLUX_OPS)
        self.assertIn("ALERT", FLUX_OPS)
        self.assertIn("EVOLVE", FLUX_OPS)
        self.assertIn("SAY", FLUX_OPS)

    def test_opcode_values_are_hex_strings(self):
        from bootstrap_research import FLUX_OPS
        for name, value in FLUX_OPS.items():
            self.assertIsInstance(value, str)
            self.assertTrue(value.startswith("0x"), f"{name}: {value}")


class TestModelsConfig(unittest.TestCase):
    """Test the MODELS configuration."""

    def test_models_defined(self):
        from bootstrap_research import MODELS
        self.assertIsInstance(MODELS, dict)

    def test_deepseek_v3(self):
        from bootstrap_research import MODELS
        self.assertIn("deepseek-v3", MODELS)
        self.assertEqual(MODELS["deepseek-v3"], "deepseek-ai/DeepSeek-V3")

    def test_qwen3_coder(self):
        from bootstrap_research import MODELS
        self.assertIn("qwen3-coder", MODELS)

    def test_seed_model(self):
        from bootstrap_research import MODELS
        self.assertIn("seed", MODELS)


class TestCallModelFunction(unittest.TestCase):
    """Test call_model function."""

    def test_call_model_exists(self):
        from bootstrap_research import call_model
        import inspect
        sig = inspect.signature(call_model)
        params = list(sig.parameters.keys())
        self.assertIn("model_id", params)
        self.assertIn("prompt", params)

    def test_call_model_returns_dict(self):
        from bootstrap_research import call_model
        result = call_model("qwen3-coder", "Say OK", temp=0.0, max_tokens=10)
        self.assertIsInstance(result, dict)
        self.assertIn("content", result)
        self.assertIn("tokens", result)
        self.assertIn("model", result)


class TestRunExperiment(unittest.TestCase):
    """Test run_experiment function."""

    def test_run_experiment_exists(self):
        from bootstrap_research import run_experiment
        import inspect
        sig = inspect.signature(run_experiment)
        params = list(sig.parameters.keys())
        self.assertIn("exp_id", params)
        self.assertIn("prompt", params)

    def test_run_experiment_default_params(self):
        from bootstrap_research import run_experiment
        import inspect
        sig = inspect.signature(run_experiment)
        # models and temps have defaults
        self.assertIn("models", sig.parameters)
        self.assertIn("temps", sig.parameters)


class TestAnalyzeConsistency(unittest.TestCase):
    """Test analyze_consistency function."""

    def test_analyze_consistency(self):
        from bootstrap_research import analyze_consistency
        results = [
            {"model": "qwen3-coder", "content": "0x10 0x20 0x01"},
            {"model": "qwen3-coder", "content": "0x10 0x20 0x01"},
            {"model": "qwen3-coder", "content": "0x10 0x20 0x01"},
        ]
        analysis = analyze_consistency(results)
        self.assertIsInstance(analysis, dict)
        self.assertIn("qwen3-coder", analysis)
        self.assertTrue(analysis["qwen3-coder"]["consistent"])

    def test_analyze_consistency_inconsistent(self):
        from bootstrap_research import analyze_consistency
        results = [
            {"model": "qwen3-coder", "content": "0x10 0x20"},
            {"model": "qwen3-coder", "content": "0x10 0x30"},
            {"model": "qwen3-coder", "content": "0x10 0x40"},
        ]
        analysis = analyze_consistency(results)
        self.assertFalse(analysis["qwen3-coder"]["consistent"])
        self.assertEqual(analysis["qwen3-coder"]["unique_outputs"], 3)

    def test_analyze_consistency_empty(self):
        from bootstrap_research import analyze_consistency
        analysis = analyze_consistency([])
        self.assertIsInstance(analysis, dict)
        self.assertEqual(len(analysis), 0)


class TestGenerateNextRound(unittest.TestCase):
    """Test generate_next_round function."""

    def test_generate_next_round_exists(self):
        from bootstrap_research import generate_next_round
        import inspect
        sig = inspect.signature(generate_next_round)
        params = list(sig.parameters.keys())
        self.assertIn("prev_results", params)
        self.assertIn("round_num", params)


class TestModuleImports(unittest.TestCase):
    """Test module can be imported."""

    def test_module_imports(self):
        import bootstrap_research
        self.assertTrue(hasattr(bootstrap_research, 'FLUX_OPS'))
        self.assertTrue(hasattr(bootstrap_research, 'MODELS'))
        self.assertTrue(hasattr(bootstrap_research, 'call_model'))
        self.assertTrue(hasattr(bootstrap_research, 'run_experiment'))
        self.assertTrue(hasattr(bootstrap_research, 'analyze_consistency'))


if __name__ == "__main__":
    unittest.main()
