"""Comprehensive tests for the Agent Bootcamp Engine (bootcamp.py)."""

import sys
import os
import json
import tempfile
import shutil
import unittest
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))


class TestWeakSpot(unittest.TestCase):
    """Test WeakSpot dataclass."""

    def test_create_weak_spot(self):
        from bootcamp import WeakSpot
        ws = WeakSpot(path="src/main.py", function_name="calculate",
                      kind="untested", severity=7, context="def calculate():")
        self.assertEqual(ws.path, "src/main.py")
        self.assertEqual(ws.function_name, "calculate")
        self.assertEqual(ws.kind, "untested")
        self.assertEqual(ws.severity, 7)

    def test_weak_spot_fields_are_settable(self):
        from bootcamp import WeakSpot
        ws = WeakSpot(path="", function_name="", kind="", severity=1, context="")
        ws.severity = 10
        ws.kind = "long_function"
        self.assertEqual(ws.severity, 10)
        self.assertEqual(ws.kind, "long_function")


class TestChallenge(unittest.TestCase):
    """Test Challenge dataclass."""

    def test_create_challenge(self):
        from bootcamp import Challenge, WeakSpot
        spot = WeakSpot(path="a.py", function_name="f", kind="untested",
                        severity=7, context="def f():")
        ch = Challenge(target=spot, task="Write tests for f", difficulty=3,
                       time_limit_minutes=30.0, verification="Run tests")
        self.assertEqual(ch.difficulty, 3)
        self.assertEqual(ch.task, "Write tests for f")
        self.assertFalse(ch.blind)

    def test_blind_challenge(self):
        from bootcamp import Challenge, WeakSpot
        spot = WeakSpot(path="", function_name="f", kind="", severity=1, context="")
        ch = Challenge(target=spot, task="t", difficulty=5,
                       time_limit_minutes=60, verification="v", blind=True)
        self.assertTrue(ch.blind)


class TestEstimate(unittest.TestCase):
    """Test Estimate dataclass."""

    def test_create_estimate(self):
        from bootcamp import Estimate
        est = Estimate(minutes=15.0, confidence=0.8, similar_tasks=3, calibration=1.0)
        self.assertAlmostEqual(est.minutes, 15.0)
        self.assertAlmostEqual(est.confidence, 0.8)
        self.assertEqual(est.similar_tasks, 3)


class TestTaskEstimator(unittest.TestCase):
    """Test TaskEstimator class."""

    def test_initial_calibration(self):
        from bootcamp import TaskEstimator
        est = TaskEstimator()
        self.assertAlmostEqual(est.calibration, 1.0)

    def test_estimate_without_history(self):
        from bootcamp import TaskEstimator
        est = TaskEstimator()
        result = est.estimate("Write tests", {"kind": "testing"})
        self.assertAlmostEqual(result.minutes, 10.0)  # default base
        self.assertAlmostEqual(result.confidence, 0.0)  # no similar tasks

    def test_estimate_with_history(self):
        from bootcamp import TaskEstimator
        est = TaskEstimator()
        est.calibrate("task1", "testing", 10.0, 20.0)
        est.calibrate("task2", "testing", 10.0, 25.0)
        est.calibrate("task3", "testing", 10.0, 15.0)
        result = est.estimate("new task", {"kind": "testing"})
        # Should be based on average of similar tasks * calibration
        self.assertAlmostEqual(result.similar_tasks, 3)

    def test_calibrate_actual_over_estimated(self):
        from bootcamp import TaskEstimator
        est = TaskEstimator()
        initial = est.calibration
        est.calibrate("task", "testing", 10.0, 30.0)  # actual > estimated
        self.assertGreater(est.calibration, initial)  # should increase

    def test_calibrate_actual_under_estimated(self):
        from bootcamp import TaskEstimator
        est = TaskEstimator()
        initial = est.calibration
        est.calibrate("task", "testing", 30.0, 10.0)  # actual < estimated
        self.assertLess(est.calibration, initial)  # should decrease

    def test_calibration_bounds(self):
        from bootcamp import TaskEstimator
        est = TaskEstimator()
        # Run many calibrations to test bounds
        for _ in range(100):
            est.calibrate("t", "k", 10.0, 100.0)
        self.assertGreaterEqual(est.calibration, 0.5)
        self.assertLessEqual(est.calibration, 2.0)

    def test_unfamiliar_context_multiplier(self):
        from bootcamp import TaskEstimator
        est = TaskEstimator()
        normal = est.estimate("task", {"kind": "testing"})
        unfamiliar = est.estimate("task", {"kind": "testing", "unfamiliar": True})
        self.assertGreater(unfamiliar.minutes, normal.minutes)

    def test_cross_language_multiplier(self):
        from bootcamp import TaskEstimator
        est = TaskEstimator()
        normal = est.estimate("task", {"kind": "testing"})
        cross = est.estimate("task", {"kind": "testing", "cross_language": True})
        self.assertGreater(cross.minutes, normal.minutes)

    def test_confidence_capped(self):
        from bootcamp import TaskEstimator
        est = TaskEstimator()
        for i in range(50):
            est.calibrate(f"task_{i}", "testing", 10.0, 15.0)
        result = est.estimate("task", {"kind": "testing"})
        self.assertLessEqual(result.confidence, 0.95)


class TestProjectScanner(unittest.TestCase):
    """Test ProjectScanner class."""

    def setUp(self):
        from bootcamp import ProjectScanner
        self.tmpdir = Path(tempfile.mkdtemp())
        # Create a minimal source file
        src = self.tmpdir / "src"
        src.mkdir()
        (src / "main.py").write_text(
            'def hello():\n'
            '    print("hello")\n\n'
            'def calculate(x):\n'
            '    return x * 2\n'
        )
        self.scanner = ProjectScanner(str(self.tmpdir))

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_scan_returns_list(self):
        result = self.scanner.scan()
        self.assertIsInstance(result, list)

    def test_scan_sorted_by_severity(self):
        result = self.scanner.scan()
        if len(result) > 1:
            for i in range(len(result) - 1):
                self.assertGreaterEqual(result[i].severity, result[i + 1].severity)

    def test_find_untested(self):
        spots = self.scanner._find_untested()
        self.assertIsInstance(spots, list)
        # All spots should have kind "untested"
        for s in spots:
            self.assertEqual(s.kind, "untested")

    def test_find_undocumented(self):
        spots = self.scanner._find_undocumented()
        self.assertIsInstance(spots, list)
        for s in spots:
            self.assertEqual(s.kind, "undocumented")

    def test_find_long_functions(self):
        # Create a long function
        src = self.tmpdir / "src"
        (src / "long.py").write_text(
            'def long_function():\n' +
            '    x = 1\n' * 60
        )
        spots = self.scanner._find_long_functions()
        self.assertIsInstance(spots, list)

    def test_find_missing_error_handling(self):
        # Create a file with I/O but no error handling
        src = self.tmpdir / "src"
        (src / "io.py").write_text(
            'def fetch_data():\n'
            '    f = open("data.txt")\n'
            '    return f.read()\n'
        )
        spots = self.scanner._find_missing_error_handling()
        self.assertIsInstance(spots, list)


class TestChallengeGenerator(unittest.TestCase):
    """Test ChallengeGenerator class."""

    def test_generate_challenges(self):
        from bootcamp import ChallengeGenerator, TaskEstimator, WeakSpot
        est = TaskEstimator()
        gen = ChallengeGenerator(est)
        spots = [
            WeakSpot(path="a.py", function_name="f", kind="untested",
                      severity=7, context="def f():"),
            WeakSpot(path="b.py", function_name="g", kind="undocumented",
                      severity=4, context="def g():"),
        ]
        challenges = gen.generate(spots, count=3)
        self.assertGreaterEqual(len(challenges), 2)  # at least as many as spots
        for ch in challenges:
            from bootcamp import Challenge; self.assertIsInstance(ch, Challenge)

    def test_difficulty_increments(self):
        from bootcamp import ChallengeGenerator, TaskEstimator, WeakSpot
        est = TaskEstimator()
        gen = ChallengeGenerator(est)
        spots = [WeakSpot(path="", function_name="f", kind="untested",
                          severity=7, context="")] * 10
        gen.generate(spots, count=5)
        # Difficulty should have increased
        self.assertGreater(gen.difficulty, 1)

    def test_topic_rotation(self):
        from bootcamp import ChallengeGenerator, TaskEstimator, WeakSpot
        est = TaskEstimator()
        gen = ChallengeGenerator(est)
        spots = [WeakSpot(path="", function_name="f", kind="untested",
                          severity=7, context="")] * 10
        gen.generate(spots, count=10)
        # Topics should rotate through the list
        self.assertGreaterEqual(gen.current_topic, 1)


class TestBlindTestRunner(unittest.TestCase):
    """Test BlindTestRunner class."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        state_file = os.path.join(self.tmpdir, "blind_tests.json")
        from bootcamp import BlindTestRunner
        self.runner = BlindTestRunner(state_file=state_file)

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_submit_returns_token(self):
        token = self.runner.submit("agent-1", "challenge-1", "my work here")
        self.assertIsInstance(token, str)
        self.assertIn("agent-1", token)
        self.assertIn("challenge-1", token)

    def test_submit_and_verify(self):
        token = self.runner.submit("agent-1", "ch-1", "work")
        self.runner.verify(token, passed=True, details="Good work")
        tests = self.runner.pickup("agent-1")
        self.assertEqual(len(tests), 1)
        self.assertEqual(tests[0]["status"], "pass")

    def test_verify_failed(self):
        token = self.runner.submit("agent-1", "ch-1", "work")
        self.runner.verify(token, passed=False, details="Needs improvement")
        tests = self.runner.pickup("agent-1")
        self.assertEqual(tests[0]["status"], "fail")

    def test_pickup_only_verified(self):
        self.runner.submit("agent-1", "ch-1", "work")
        self.runner.submit("agent-2", "ch-2", "work")
        token1 = self.runner.submit("agent-1", "ch-1", "work")
        self.runner.verify(token1, True)
        # Only agent-1 should have verified tests
        a1 = self.runner.pickup("agent-1")
        a2 = self.runner.pickup("agent-2")
        self.assertGreaterEqual(len(a1), 1)
        self.assertEqual(len(a2), 0)

    def test_persistence(self):
        """Tests persist across BlindTestRunner instances."""
        token = self.runner.submit("agent-1", "ch-1", "work")
        # Create new runner with same state file
        from bootcamp import BlindTestRunner
        runner2 = BlindTestRunner(state_file=self.runner.state_file)
        self.assertIn(token, runner2.tests)


class TestDojoSession(unittest.TestCase):
    """Test DojoSession class."""

    def test_variants_list(self):
        from bootcamp import DojoSession
        dojo = DojoSession("test-agent")
        self.assertEqual(len(dojo.variants), 5)
        names = [v[0] for v in dojo.variants]
        self.assertIn("Twin-A", names)
        self.assertIn("Twin-E", names)

    def test_variant_configurations(self):
        from bootcamp import DojoSession
        dojo = DojoSession("test-agent")
        # Twin-A: same model, temp 0.0, with context
        self.assertEqual(dojo.variants[0][2], 0.0)
        self.assertTrue(dojo.variants[0][3])
        # Twin-B: same model, temp 0.7
        self.assertEqual(dojo.variants[1][2], 0.7)


if __name__ == "__main__":
    unittest.main()
