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
from pathlib import Path
from tempfile import TemporaryDirectory
from scripts.integrations import sanitize_url, define_env


class TestIntegrations(unittest.TestCase):

    def test_sanitize_url_disallows_protocol_relative(self):
        # Allowed URLs
        self.assertEqual(sanitize_url("/valid/path"), "/valid/path")
        self.assertEqual(sanitize_url("http://example.com"), "http://example.com")
        self.assertEqual(sanitize_url("https://example.com"), "https://example.com")

        # Disallowed URLs (protocol-relative, javascript:, data:, etc.)
        self.assertEqual(sanitize_url("//evil.com/phish"), "#")
        self.assertEqual(sanitize_url("javascript:alert(1)"), "#")
        self.assertEqual(sanitize_url("data:text/html,evil"), "#")
        self.assertEqual(sanitize_url(""), "#")
        self.assertEqual(sanitize_url(None), "#")

    def test_render_catalog_escapes_tags(self):
        with TemporaryDirectory() as tmp_dir:
            docs_dir = Path(tmp_dir)
            tool_file = docs_dir / "test-tool.md"
            tool_file.write_text(
                "---\n"
                "title: Test Tool\n"
                "catalog_tags: ['a&b']\n"
                "---\n"
                "Description text",
                encoding="utf-8"
            )

            # Mock env object with conf
            class MockEnv:
                def __init__(self, d):
                    self.conf = {'docs_dir': str(d)}
                    self.macro_func = None

                def macro(self, func):
                    self.macro_func = func
                    return func

            env = MockEnv(docs_dir)
            define_env(env)

            rendered = env.macro_func("*.md")

            # Check that & in tags is escaped as &amp; and not corrupted to &Amp;
            self.assertIn("&amp;", rendered)
            self.assertNotIn("&Amp;", rendered)


if __name__ == "__main__":
    unittest.main()
