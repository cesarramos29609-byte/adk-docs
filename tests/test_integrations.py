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

import unittest
import tempfile
from pathlib import Path
from scripts.integrations import sanitize_url, define_env


class MockEnv:
    def __init__(self, docs_dir):
        self.conf = {'docs_dir': docs_dir}

    def macro(self, func):
        return func


class TestIntegrations(unittest.TestCase):

    def test_sanitize_url_safe(self):
        self.assertEqual(sanitize_url("https://example.com/logo.png"), "https://example.com/logo.png")
        self.assertEqual(sanitize_url("http://example.com/logo.png"), "http://example.com/logo.png")
        self.assertEqual(sanitize_url("/integrations/assets/toolbox.svg"), "/integrations/assets/toolbox.svg")

    def test_sanitize_url_unsafe(self):
        self.assertEqual(sanitize_url("javascript:alert(1)"), "#")
        self.assertEqual(sanitize_url("data:text/html,<script>alert(1)</script>"), "#")
        self.assertEqual(sanitize_url("//evil.com/phish"), "#")
        self.assertEqual(sanitize_url(""), "#")

    def test_render_catalog_macro(self):
        with tempfile.TemporaryDirectory() as tmp_docs:
            docs_dir = Path(tmp_docs)
            env = MockEnv(str(docs_dir))

            # Create a sample test doc
            sample_doc = docs_dir / "sample.md"
            sample_doc.write_text("""---
catalog_title: "Test Tool & Special"
catalog_description: "A test description"
catalog_tags: ["mcp", "a&b", "<script>"]
---
# Title
""", encoding='utf-8')

            # define_env attaches macro functions, but returns None in mkdocs-macros-plugin.
            # In scripts/integrations.py:
            # env.macro(render_catalog)
            # So we can capture the macro function inside MockEnv.
            captured = {}
            def macro_decorator(func):
                captured['render_catalog'] = func
                return func
            env.macro = macro_decorator

            define_env(env)
            render_catalog = captured['render_catalog']
            html_output = render_catalog("*.md")

            # Check HTML output escaping
            self.assertIn('data-filter="mcp">MCP</button>', html_output)
            self.assertIn('data-filter="a&amp;b">A&amp;B</button>', html_output)
            self.assertIn('data-filter="&lt;script&gt;">&lt;Script&gt;</button>', html_output)
            self.assertIn('Test Tool &amp; Special', html_output)


if __name__ == '__main__':
    unittest.main()
