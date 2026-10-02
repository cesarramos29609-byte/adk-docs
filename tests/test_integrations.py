import unittest
from scripts.integrations import sanitize_url

class TestSanitizeUrl(unittest.TestCase):
    def test_valid_root_relative_url(self):
        self.assertEqual(sanitize_url("/integrations/assets/toolbox.svg"), "/integrations/assets/toolbox.svg")
        self.assertEqual(sanitize_url("/tools/google-cloud/"), "/tools/google-cloud/")

    def test_valid_http_https_url(self):
        self.assertEqual(sanitize_url("http://example.com/icon.png"), "http://example.com/icon.png")
        self.assertEqual(sanitize_url("https://example.com/icon.png"), "https://example.com/icon.png")

    def test_disallow_protocol_relative_url(self):
        self.assertEqual(sanitize_url("//evil.com/malicious.js"), "#")
        self.assertEqual(sanitize_url("//attacker.com"), "#")

    def test_disallow_backslash_url(self):
        self.assertEqual(sanitize_url("/\\\\evil.com"), "#")
        self.assertEqual(sanitize_url("\\\\evil.com"), "#")

    def test_disallow_javascript_and_data_uris(self):
        self.assertEqual(sanitize_url("javascript:alert(1)"), "#")
        self.assertEqual(sanitize_url("   javascript:alert(1)   "), "#")
        self.assertEqual(sanitize_url("data:text/html,<script>alert(1)</script>"), "#")

    def test_empty_or_none_url(self):
        self.assertEqual(sanitize_url(""), "#")
        self.assertEqual(sanitize_url(None), "#")

if __name__ == "__main__":
    unittest.main()
