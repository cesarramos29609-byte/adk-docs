import unittest
import sys
from pathlib import Path

# Add scripts directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from integrations import sanitize_url

class TestSanitizeUrl(unittest.TestCase):
    def test_valid_http_urls(self):
        self.assertEqual(sanitize_url("http://example.com"), "http://example.com")
        self.assertEqual(sanitize_url("https://example.com/foo?bar=1"), "https://example.com/foo?bar=1")

    def test_valid_relative_urls(self):
        self.assertEqual(sanitize_url("/path/to/resource"), "/path/to/resource")
        self.assertEqual(sanitize_url("/index.html"), "/index.html")

    def test_empty_or_none(self):
        self.assertEqual(sanitize_url(""), "#")
        self.assertEqual(sanitize_url("   "), "#")

    def test_javascript_urls(self):
        self.assertEqual(sanitize_url("javascript:alert(1)"), "#")
        self.assertEqual(sanitize_url("  javascript:alert('xss')"), "#")

    def test_protocol_relative_urls(self):
        # Protocol relative URLs should be treated as untrusted external redirects or unsafe URIs
        self.assertEqual(sanitize_url("//evil.com"), "#")
        self.assertEqual(sanitize_url("//evil.com/phishing"), "#")

if __name__ == "__main__":
    unittest.main()
