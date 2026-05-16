"""Comprehensive tests for the FLUX Research Queue (research_queue.py)."""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))


class TestExperimentDataclass(unittest.TestCase):
    """Test the Experiment dataclass."""

    def test_create_experiment(self):
        from research_queue import Experiment
        exp = Experiment(
            id="test_exp",
            hypothesis="Locks improve consistency",
            method=lambda e: {"result": True},
            model="qwen3-coder",
            cost_est=0.05,
        )
        self.assertEqual(exp.id, "test_exp")
        self.assertEqual(exp.status, "queued")
        self.assertEqual(exp.rounds, 0)
        self.assertEqual(exp.max_rounds, 5)

    def test_experiment_default_values(self):
        from research_queue import Experiment
        exp = Experiment(id="x", hypothesis="h", method=lambda e: {})
        self.assertEqual(exp.model, "qwen3-coder")
        self.assertAlmostEqual(exp.cost_est, 0.01)
        self.assertEqual(exp.result, {})


class TestExtractHex(unittest.TestCase):
    """Test the extract_hex utility function."""

    def setUp(self):
        from research_queue import extract_hex
        self.extract_hex = extract_hex

    def test_extracts_0x_prefixed(self):
        result = self.extract_hex("0x10 0x20 0x01")
        self.assertIn("0x10", result)
        self.assertIn("0x20", result)
        self.assertIn("0x01", result)

    def test_extracts_bare_hex(self):
        result = self.extract_hex("10 20 01")
        self.assertIn("0x10", result)
        self.assertIn("0x20", result)
        self.assertIn("0x01", result)

    def test_normalizes_case(self):
        result = self.extract_hex("0xAB 0xCD")
        self.assertIn("0xab", result)
        self.assertIn("0xcd", result)

    def test_ignores_non_hex(self):
        result = self.extract_hex("hello 0x10 world 0x20")
        self.assertIn("0x10", result)
        self.assertIn("0x20", result)
        self.assertNotIn("hello", result)

    def test_ignores_short_0x(self):
        """Bare hex pairs are extracted."""
        result = self.extract_hex("10 20")
        self.assertIn("0x10", result)
        self.assertIn("0x20", result)

    def test_empty_string(self):
        result = self.extract_hex("")
        self.assertEqual(result, "")

    def test_invalid_hex_ignored(self):
        result = self.extract_hex("0xGH 0x10")
        self.assertIn("0x10", result)
        self.assertNotIn("0xgh", result)

    def test_comma_separated(self):
        result = self.extract_hex("0x10,0x20,0x01")
        self.assertIn("0x10", result)
        self.assertIn("0x20", result)


class TestConsistencyCheck(unittest.TestCase):
    """Test the consistency_check function."""

    def setUp(self):
        from research_queue import consistency_check
        self.consistency_check = consistency_check

    def test_identical_outputs_consistent(self):
        outputs = ["0x10 0x20 0x01"] * 3
        result = self.consistency_check(outputs)
        self.assertTrue(result["consistent"])
        self.assertEqual(result["unique_count"], 1)
        self.assertEqual(result["total"], 3)

    def test_different_outputs_inconsistent(self):
        outputs = ["0x10 0x20", "0x10 0x30", "0x10 0x40"]
        result = self.consistency_check(outputs)
        self.assertFalse(result["consistent"])
        self.assertEqual(result["unique_count"], 3)

    def test_single_output_consistent(self):
        outputs = ["0x10 0x20"]
        result = self.consistency_check(outputs)
        self.assertTrue(result["consistent"])

    def test_empty_outputs(self):
        outputs = []
        result = self.consistency_check(outputs)
        # Empty list edge case - consistent with no unique outputs
        self.assertEqual(result["unique_count"], 0)
        self.assertEqual(result["total"], 0)

    def test_samples_limited(self):
        outputs = [f"0x{i:02x}" for i in range(10)]
        result = self.consistency_check(outputs)
        self.assertLessEqual(len(result["samples"]), 3)


class TestModelsDict(unittest.TestCase):
    """Test the MODELS configuration."""

    def test_models_dict_exists(self):
        from research_queue import MODELS
        self.assertIsInstance(MODELS, dict)

    def test_models_have_provider_and_id(self):
        from research_queue import MODELS
        for name, (provider, model_id) in MODELS.items():
            self.assertIn(provider, ["siliconflow", "deepseek"])
            self.assertIsInstance(model_id, str)
            self.assertTrue(len(model_id) > 0)

    def test_expected_models_present(self):
        from research_queue import MODELS
        self.assertIn("qwen3-coder", MODELS)
        self.assertIn("deepseek-chat", MODELS)
        self.assertIn("glm4-flash", MODELS)


class TestFluxOps(unittest.TestCase):
    """Test FLUX opcode definitions."""

    def test_flux_ops_defined(self):
        from research_queue import FLUX_OPS
        self.assertIsInstance(FLUX_OPS, str)
        self.assertIn("MOVI", FLUX_OPS)
        self.assertIn("HALT", FLUX_OPS)
        self.assertIn("GAUGE", FLUX_OPS)
        self.assertIn("ALERT", FLUX_OPS)
        self.assertIn("EVOLVE", FLUX_OPS)

    def test_test_program_defined(self):
        from research_queue import TEST_PROGRAM
        self.assertIsInstance(TEST_PROGRAM, str)
        self.assertIn("heading", TEST_PROGRAM)
        self.assertIn("halt", TEST_PROGRAM)


class TestExperimentRegistry(unittest.TestCase):
    """Test the EXPERIMENTS registry."""

    def test_experiments_list_exists(self):
        from research_queue import EXPERIMENTS
        self.assertIsInstance(EXPERIMENTS, list)

    def test_at_least_8_experiments(self):
        from research_queue import EXPERIMENTS
        self.assertGreaterEqual(len(EXPERIMENTS), 8)

    def test_all_experiments_have_required_fields(self):
        from research_queue import EXPERIMENTS
        for exp in EXPERIMENTS:
            self.assertTrue(hasattr(exp, 'id'))
            self.assertTrue(hasattr(exp, 'hypothesis'))
            self.assertTrue(hasattr(exp, 'method'))
            self.assertTrue(hasattr(exp, 'model'))
            self.assertTrue(len(exp.id) > 0)
            self.assertTrue(len(exp.hypothesis) > 0)
            self.assertTrue(callable(exp.method))

    def test_lock_mass_experiment(self):
        from research_queue import EXPERIMENTS
        ids = [e.id for e in EXPERIMENTS]
        self.assertIn("lock_mass", ids)

    def test_polyglot_experiment(self):
        from research_queue import EXPERIMENTS
        ids = [e.id for e in EXPERIMENTS]
        self.assertIn("polyglot_consistency", ids)

    def test_temperature_stability_experiment(self):
        from research_queue import EXPERIMENTS
        ids = [e.id for e in EXPERIMENTS]
        self.assertIn("temp_stability", ids)


class TestCallModelReturnType(unittest.TestCase):
    """Test that call_model returns the expected dict structure."""

    def test_call_model_returns_dict(self):
        """call_model returns a dict with expected keys (may error due to network)."""
        from research_queue import call_model
        # This may fail due to network issues, but should return a dict
        result = call_model("qwen3-coder", "Say hello", temp=0.0, max_tokens=10)
        self.assertIsInstance(result, dict)
        self.assertIn("content", result)
        self.assertIn("tokens", result)
        self.assertIn("elapsed", result)
        self.assertIn("error", result)


if __name__ == "__main__":
    unittest.main()
