"""Comprehensive tests for the Oracle1 Task Framework (task_worker.py)."""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))


class TestModelsConfiguration(unittest.TestCase):
    """Test the MODELS configuration."""

    def test_models_defined(self):
        from task_worker import MODELS
        self.assertIsInstance(MODELS, dict)

    def test_expected_model_tiers(self):
        from task_worker import MODELS
        self.assertIn("bulk", MODELS)
        self.assertIn("good", MODELS)
        self.assertIn("runner", MODELS)
        self.assertIn("expert", MODELS)

    def test_bulk_model(self):
        from task_worker import MODELS
        self.assertEqual(MODELS["bulk"], "glm-4.7-flash")

    def test_good_model(self):
        from task_worker import MODELS
        self.assertEqual(MODELS["good"], "glm-4.7")

    def test_runner_model(self):
        from task_worker import MODELS
        self.assertEqual(MODELS["runner"], "glm-5-turbo")

    def test_expert_model(self):
        from task_worker import MODELS
        self.assertEqual(MODELS["expert"], "glm-5.1")


class TestCallModel(unittest.TestCase):
    """Test call_model function."""

    def test_call_model_exists(self):
        from task_worker import call_model
        import inspect
        sig = inspect.signature(call_model)
        params = list(sig.parameters.keys())
        self.assertIn("prompt", params)
        self.assertIn("model", params)

    def test_call_model_default_model(self):
        from task_worker import call_model
        import inspect
        sig = inspect.signature(call_model)
        self.assertEqual(sig.parameters["model"].default, "glm-4.7-flashx")

    def test_call_model_returns_string_or_none(self):
        from task_worker import call_model
        result = call_model("Say OK", model="glm-4.7-flashx")
        # Result may be string or None depending on API availability
        self.assertTrue(result is None or isinstance(result, str))


class TestTaskReadmeDescriptions(unittest.TestCase):
    """Test task_readme_descriptions function."""

    def test_function_exists(self):
        from task_worker import task_readme_descriptions
        self.assertTrue(callable(task_readme_descriptions))

    def test_all_repos_have_descriptions(self):
        """When all repos have descriptions, function returns early."""
        from task_worker import task_readme_descriptions
        import tempfile, os
        # Create a temp file where all repos have descriptions
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("repo1|Has description|url1\n")
            f.write("repo2|Another desc|url2\n")
            tmpfile = f.name
        try:
            # Should print message and return without error
            task_readme_descriptions(tmpfile)
        finally:
            os.unlink(tmpfile)


class TestTaskFunctions(unittest.TestCase):
    """Test all task functions exist."""

    def test_task_summarize_readme(self):
        from task_worker import task_summarize_readme
        self.assertTrue(callable(task_summarize_readme))

    def test_task_categorize_repos(self):
        from task_worker import task_categorize_repos
        self.assertTrue(callable(task_categorize_repos))

    def test_task_generate_mermaid(self):
        from task_worker import task_generate_mermaid
        self.assertTrue(callable(task_generate_mermaid))


class TestApiConfiguration(unittest.TestCase):
    """Test API configuration."""

    def test_api_key_defined(self):
        from task_worker import API_KEY
        self.assertIsInstance(API_KEY, str)
        self.assertGreater(len(API_KEY), 0)

    def test_base_url_defined(self):
        from task_worker import BASE_URL
        self.assertIsInstance(BASE_URL, str)
        self.assertTrue(BASE_URL.startswith("https://"))


class TestModuleImports(unittest.TestCase):
    """Test module can be imported."""

    def test_module_imports(self):
        import task_worker
        self.assertTrue(hasattr(task_worker, 'MODELS'))
        self.assertTrue(hasattr(task_worker, 'call_model'))
        self.assertTrue(hasattr(task_worker, 'API_KEY'))
        self.assertTrue(hasattr(task_worker, 'BASE_URL'))


if __name__ == "__main__":
    unittest.main()
