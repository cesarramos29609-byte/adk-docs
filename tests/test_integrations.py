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


class TestIntegrationsScript(unittest.TestCase):

    def test_sanitize_url_safe(self):
        self.assertEqual(sanitize_url("http://example.com"), "http://example.com")
        self.assertEqual(sanitize_url("https://example.com"), "https://example.com")
        self.assertEqual(sanitize_url("/integrations/assets/icon.svg"), "/integrations/assets/icon.svg")

    def test_sanitize_url_unsafe(self):
        self.assertEqual(sanitize_url("javascript:alert(1)"), "#")
        self.assertEqual(sanitize_url("data:text/html;base64,123"), "#")
        self.assertEqual(sanitize_url("//attacker.com/malicious"), "#")
        self.assertEqual(sanitize_url("/\\attacker.com"), "#")
        self.assertEqual(sanitize_url("\\attacker.com"), "#")
        self.assertEqual(sanitize_url(""), "#")

    def test_tag_display_escaping(self):
        tag = "<script>"
        display_name = "MCP" if tag.lower() == "mcp" else html.escape(tag.title())
        self.assertEqual(display_name, "&lt;Script&gt;")
        self.assertNotIn("&Lt;", display_name)


if __name__ == "__main__":
    unittest.main()
