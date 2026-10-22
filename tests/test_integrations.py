import unittest
from scripts.integrations import sanitize_url

class TestIntegrationsSanitizeUrl(unittest.TestCase):

    def test_safe_urls(self):
        self.assertEqual(sanitize_url("http://example.com/icon.png"), "http://example.com/icon.png")
        self.assertEqual(sanitize_url("https://example.com/icon.png"), "https://example.com/icon.png")
        self.assertEqual(sanitize_url("/assets/icon.png"), "/assets/icon.png")
        self.assertEqual(sanitize_url("assets/icon.png"), "/assets/icon.png")

    def test_unsafe_urls(self):
        self.assertEqual(sanitize_url("javascript:alert(1)"), "#")
        self.assertEqual(sanitize_url("  javascript:alert(1)  "), "#")
        self.assertEqual(sanitize_url("data:text/html,<script>alert(1)</script>"), "#")
        self.assertEqual(sanitize_url("vbscript:msgbox(1)"), "#")
        self.assertEqual(sanitize_url("//attacker.com/malicious.png"), "#")
        self.assertEqual(sanitize_url(""), "#")
        self.assertEqual(sanitize_url(None), "#")

if __name__ == "__main__":
    unittest.main()
