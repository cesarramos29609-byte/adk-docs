import unittest
from scripts.integrations import sanitize_url

class TestSanitizeUrl(unittest.TestCase):
    def test_valid_root_relative_urls(self):
        self.assertEqual(sanitize_url("/integrations/assets/toolbox.svg"), "/integrations/assets/toolbox.svg")
        self.assertEqual(sanitize_url("/path/to/page/"), "/path/to/page/")

    def test_valid_http_urls(self):
        self.assertEqual(sanitize_url("http://example.com/icon.png"), "http://example.com/icon.png")
        self.assertEqual(sanitize_url("https://example.com/icon.png"), "https://example.com/icon.png")
        self.assertEqual(sanitize_url("HTTPS://EXAMPLE.COM/ICON.PNG"), "HTTPS://EXAMPLE.COM/ICON.PNG")

    def test_protocol_relative_urls_rejected(self):
        self.assertEqual(sanitize_url("//attacker.com/evil.js"), "#")
        self.assertEqual(sanitize_url(" //evil.com"), "#")

    def test_dangerous_schemes_rejected(self):
        self.assertEqual(sanitize_url("javascript:alert(1)"), "#")
        self.assertEqual(sanitize_url("data:text/html,<script>alert(1)</script>"), "#")
        self.assertEqual(sanitize_url("vbscript:msgbox"), "#")

    def test_empty_and_whitespace(self):
        self.assertEqual(sanitize_url(""), "#")
        self.assertEqual(sanitize_url(None), "#")
        self.assertEqual(sanitize_url("   "), "#")

if __name__ == "__main__":
    unittest.main()
