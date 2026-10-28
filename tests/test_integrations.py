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

import os
import tempfile
import unittest
from pathlib import Path
from scripts.integrations import sanitize_url, define_env


class TestIntegrations(unittest.TestCase):

    def test_sanitize_url(self):
        self.assertEqual(sanitize_url("/path/to/page"), "/path/to/page")
        self.assertEqual(sanitize_url("https://example.com"), "https://example.com")
        self.assertEqual(sanitize_url("http://example.com"), "http://example.com")
        self.assertEqual(sanitize_url("javascript:alert(1)"), "#")
        self.assertEqual(sanitize_url("data:text/html,<script>alert(1)</script>"), "#")
        self.assertEqual(sanitize_url(""), "#")

    def test_render_catalog_html_escaping(self):
        class MockEnv:
            def __init__(self, docs_dir):
                self.conf = {'docs_dir': str(docs_dir)}
                self.macros = {}

            def macro(self, func):
                self.macros[func.__name__] = func
                return func

        with tempfile.TemporaryDirectory() as tmp_dir:
            docs_dir = Path(tmp_dir)
            # Create a test markdown file with special characters in catalog_tags
            test_file = docs_dir / "test_tool.md"
            test_file.write_text(
                "---\n"
                "catalog_title: Test Tool\n"
                "catalog_description: A test tool\n"
                "catalog_tags:\n"
                "  - mcp\n"
                "  - 'a\"b'\n"
                "  - 'c&d'\n"
                "---\n"
                "# Test Tool\n",
                encoding="utf-8"
            )

            env = MockEnv(docs_dir)
            define_env(env)
            render_catalog = env.macros['render_catalog']

            rendered_html = render_catalog("*.md")

            # Check that "mcp" displays as "MCP"
            self.assertIn('>MCP</button>', rendered_html)

            # Check that tag with quotes 'a"b' is escaped as &quot; and display is A&quot;B, NOT A&Quot;B
            self.assertIn('data-filter="a&quot;b"', rendered_html)
            self.assertIn('>A&quot;B</button>', rendered_html)
            self.assertNotIn('&Quot;', rendered_html)

            # Check that tag with ampersand 'c&d' is escaped as &amp; and display is C&amp;D, NOT C&Amp;D
            self.assertIn('data-filter="c&amp;d"', rendered_html)
            self.assertIn('>C&amp;D</button>', rendered_html)
            self.assertNotIn('&Amp;', rendered_html)


if __name__ == '__main__':
    unittest.main()
