import unittest
from scripts.integrations import sanitize_url

class TestIntegrations(unittest.TestCase):
    def test_sanitize_url_valid_relative(self):
        self.assertEqual(sanitize_url("/integrations/assets/toolbox.svg"), "/integrations/assets/toolbox.svg")
        self.assertEqual(sanitize_url("/docs/index.html"), "/docs/index.html")

    def test_sanitize_url_valid_http(self):
        self.assertEqual(sanitize_url("http://example.com/logo.png"), "http://example.com/logo.png")
        self.assertEqual(sanitize_url("https://example.com/logo.png"), "https://example.com/logo.png")
        self.assertEqual(sanitize_url("HTTPS://EXAMPLE.COM/LOGO.PNG"), "HTTPS://EXAMPLE.COM/LOGO.PNG")

    def test_sanitize_url_rejects_protocol_relative(self):
        self.assertEqual(sanitize_url("//evil.com/phish"), "#")
        self.assertEqual(sanitize_url("/\\evil.com/phish"), "#")

    def test_sanitize_url_rejects_dangerous_schemes(self):
        self.assertEqual(sanitize_url("javascript:alert(1)"), "#")
        self.assertEqual(sanitize_url("data:text/html,<script>alert(1)</script>"), "#")
        self.assertEqual(sanitize_url("   javascript:void(0)   "), "#")
        self.assertEqual(sanitize_url(""), "#")
        self.assertEqual(sanitize_url(None), "#")

if __name__ == '__main__':
    unittest.main()
