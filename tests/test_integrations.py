import unittest
from scripts.integrations import sanitize_url

class TestSanitizeUrl(unittest.TestCase):
    def test_valid_root_relative_urls(self):
        self.assertEqual(sanitize_url('/integrations/'), '/integrations/')
        self.assertEqual(sanitize_url('/assets/icon.svg'), '/assets/icon.svg')

    def test_valid_absolute_urls(self):
        self.assertEqual(sanitize_url('http://example.com'), 'http://example.com')
        self.assertEqual(sanitize_url('https://example.com/icon.png'), 'https://example.com/icon.png')
        self.assertEqual(sanitize_url('   https://example.com  '), 'https://example.com')

    def test_protocol_relative_urls_rejected(self):
        self.assertEqual(sanitize_url('//evil.com'), '#')
        self.assertEqual(sanitize_url('//evil.com/path'), '#')
        self.assertEqual(sanitize_url('/\\evil.com'), '#')

    def test_unsafe_schemes_rejected(self):
        self.assertEqual(sanitize_url('javascript:alert(1)'), '#')
        self.assertEqual(sanitize_url('JAVASCRIPT:alert(1)'), '#')
        self.assertEqual(sanitize_url('data:text/html,<script>alert(1)</script>'), '#')
        self.assertEqual(sanitize_url('vbscript:msgbox(1)'), '#')
        self.assertEqual(sanitize_url('file:///etc/passwd'), '#')

    def test_empty_or_none(self):
        self.assertEqual(sanitize_url(''), '#')
        self.assertEqual(sanitize_url(None), '#')

if __name__ == '__main__':
    unittest.main()
