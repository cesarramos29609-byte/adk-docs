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
import shutil
from pathlib import Path
from scripts.integrations import define_env

class MockEnv:
    def __init__(self, docs_dir):
        self.conf = {'docs_dir': docs_dir}
        self.macros = {}

    def macro(self, func):
        self.macros[func.__name__] = func
        return func

class TestIntegrations(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.docs_dir = Path(self.temp_dir)
        self.env = MockEnv(str(self.docs_dir))
        define_env(self.env)
        self.render_catalog = self.env.macros['render_catalog']

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_unsafe_icon_protocol_sanitized(self):
        doc_path = self.docs_dir / "tool_unsafe.md"
        doc_path.write_text("""---
title: Unsafe Tool
catalog_tags: [test]
catalog_icon: "javascript:alert('xss')"
---
# Unsafe Tool
Description
""", encoding='utf-8')

        output = self.render_catalog("*.md")
        self.assertNotIn("javascript:alert", output)
        self.assertIn("/integrations/assets/toolbox.svg", output)

    def test_tag_html_escaping(self):
        doc_path = self.docs_dir / "tool_escape.md"
        doc_path.write_text("""---
title: Escape Tool
catalog_tags: ["<script>"]
---
# Escape Tool
Description
""", encoding='utf-8')

        output = self.render_catalog("*.md")
        self.assertNotIn("&Lt;Script&Gt;", output)
        self.assertIn('&lt;Script&gt;', output)
        self.assertIn('data-filter="&lt;script&gt;"', output)

    def test_safe_icon_url_handled(self):
        doc_path = self.docs_dir / "tool_safe.md"
        doc_path.write_text("""---
title: Safe Tool
catalog_icon: "https://example.com/icon.svg"
catalog_tags: [mcp]
---
# Safe Tool
Description
""", encoding='utf-8')

        output = self.render_catalog("*.md")
        self.assertIn('src="https://example.com/icon.svg"', output)
        self.assertIn('>MCP</button>', output)

if __name__ == '__main__':
    unittest.main()
