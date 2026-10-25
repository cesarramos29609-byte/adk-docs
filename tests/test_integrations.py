import unittest
from scripts.integrations import sanitize_url

class TestSanitizeUrl(unittest.TestCase):
    def test_safe_urls(self):
        self.assertEqual(sanitize_url("/integrations/assets/toolbox.svg"), "/integrations/assets/toolbox.svg")
        self.assertEqual(sanitize_url("http://example.com/logo.png"), "http://example.com/logo.png")
        self.assertEqual(sanitize_url("https://example.com/logo.png"), "https://example.com/logo.png")

    def test_unsafe_urls(self):
        self.assertEqual(sanitize_url("//evil.com/malicious.js"), "#")
        self.assertEqual(sanitize_url("javascript:alert(1)"), "#")
        self.assertEqual(sanitize_url("data:text/html,<script>alert(1)</script>"), "#")
        self.assertEqual(sanitize_url(""), "#")
        self.assertEqual(sanitize_url(None), "#")

if __name__ == "__main__":
    unittest.main()
