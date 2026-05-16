"""Comprehensive tests for the Oracle1 Batch Workers (batch.py)."""

import sys
import os
import unittest
from unittest.mock import patch, MagicMock
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))


class TestCallZai(unittest.TestCase):
    """Test the call_zai function."""

    def test_call_zai_exists(self):
        from batch import call_zai
        import inspect
        sig = inspect.signature(call_zai)
        params = list(sig.parameters.keys())
        self.assertIn("prompt", params)
        self.assertIn("model", params)

    def test_call_zai_default_params(self):
        from batch import call_zai
        import inspect
        sig = inspect.signature(call_zai)
        self.assertEqual(sig.parameters["model"].default, "glm-4.7-flashx")
        self.assertEqual(sig.parameters["max_tokens"].default, 4096)


class TestGithubApi(unittest.TestCase):
    """Test github_api function."""

    def test_github_api_exists(self):
        from batch import github_api
        import inspect
        sig = inspect.signature(github_api)
        params = list(sig.parameters.keys())
        self.assertIn("url", params)

    @patch("batch.urlopen")
    def test_github_api_makes_request(self, mock_urlopen):
        from batch import github_api
        mock_resp = MagicMock()
        mock_resp.read.return_value = json.dumps([{"name": "test"}]).encode()
        mock_resp.__enter__ = MagicMock(return_value=mock_resp)
        mock_resp.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = mock_resp
        result = github_api("https://api.github.com/users/test/repos")
        self.assertIsInstance(result, list)


class TestFetchAllRepos(unittest.TestCase):
    """Test fetch_all_repos function."""

    def test_fetch_all_repos_exists(self):
        from batch import fetch_all_repos
        import inspect
        sig = inspect.signature(fetch_all_repos)
        params = list(sig.parameters.keys())
        self.assertIn("owner", params)


class TestGenerateDescriptionsBatch(unittest.TestCase):
    """Test generate_descriptions_batch function."""

    def test_generate_descriptions_batch_exists(self):
        from batch import generate_descriptions_batch
        import inspect
        sig = inspect.signature(generate_descriptions_batch)
        params = list(sig.parameters.keys())
        self.assertIn("repos_with_no_desc", params)
        self.assertIn("batch_size", params)
        self.assertEqual(sig.parameters["batch_size"].default, 30)


class TestCmdFunctions(unittest.TestCase):
    """Test command functions exist."""

    def test_cmd_descriptions_exists(self):
        from batch import cmd_descriptions
        self.assertTrue(callable(cmd_descriptions))

    def test_cmd_analyze_exists(self):
        from batch import cmd_analyze
        self.assertTrue(callable(cmd_analyze))

    def test_cmd_export_exists(self):
        from batch import cmd_export
        self.assertTrue(callable(cmd_export))

    def test_cmd_apply_descriptions_exists(self):
        from batch import cmd_apply_descriptions
        self.assertTrue(callable(cmd_apply_descriptions))


class TestModuleConstants(unittest.TestCase):
    """Test module-level constants."""

    def test_api_key_defined(self):
        from batch import API_KEY
        self.assertIsInstance(API_KEY, str)
        self.assertGreater(len(API_KEY), 0)

    def test_base_url_defined(self):
        from batch import BASE_URL
        self.assertIsInstance(BASE_URL, str)
        self.assertTrue(BASE_URL.startswith("https://"))


class TestModuleImports(unittest.TestCase):
    """Test module can be imported."""

    def test_module_imports(self):
        import batch
        self.assertTrue(hasattr(batch, 'call_zai'))
        self.assertTrue(hasattr(batch, 'github_api'))
        self.assertTrue(hasattr(batch, 'fetch_all_repos'))
        self.assertTrue(hasattr(batch, 'generate_descriptions_batch'))
        self.assertTrue(hasattr(batch, 'cmd_descriptions'))
        self.assertTrue(hasattr(batch, 'cmd_analyze'))
        self.assertTrue(hasattr(batch, 'cmd_export'))


if __name__ == "__main__":
    unittest.main()
