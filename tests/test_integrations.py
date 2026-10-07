# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import html
import unittest
from scripts.integrations import sanitize_url

class TestIntegrations(unittest.TestCase):

    def test_sanitize_url_safe_urls(self):
        self.assertEqual(sanitize_url('/docs/integrations/'), '/docs/integrations/')
        self.assertEqual(sanitize_url('https://google.com'), 'https://google.com')
        self.assertEqual(sanitize_url('http://example.com/icon.png'), 'http://example.com/icon.png')

    def test_sanitize_url_unsafe_schemes(self):
        self.assertEqual(sanitize_url('javascript:alert(1)'), '#')
        self.assertEqual(sanitize_url('data:text/html,<script>alert(1)</script>'), '#')
        self.assertEqual(sanitize_url('vbscript:msgbox(1)'), '#')

    def test_sanitize_url_protocol_relative(self):
        self.assertEqual(sanitize_url('//evil.com/phish'), '#')
        self.assertEqual(sanitize_url('/\\evil.com'), '#')
        self.assertEqual(sanitize_url('\\\\evil.com'), '#')

    def test_sanitize_url_empty_or_none(self):
        self.assertEqual(sanitize_url(''), '#')
        self.assertEqual(sanitize_url(None), '#')
        self.assertEqual(sanitize_url('   '), '#')

    def test_tag_display_escaping(self):
        tag = "q&a"
        raw_display = "MCP" if tag.lower() == "mcp" else tag.title()
        safe_display = html.escape(raw_display)
        self.assertEqual(safe_display, 'Q&amp;A')

        tag_quote = "don't"
        raw_display_quote = "MCP" if tag_quote.lower() == "mcp" else tag_quote.title()
        safe_display_quote = html.escape(raw_display_quote)
        self.assertNotIn('&#X27;', safe_display_quote)

if __name__ == '__main__':
    unittest.main()
