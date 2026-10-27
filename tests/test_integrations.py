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
from scripts.integrations import sanitize_url

class TestIntegrations(unittest.TestCase):
    def test_sanitize_url_safe_root_relative(self):
        self.assertEqual(sanitize_url("/integrations/assets/toolbox.svg"), "/integrations/assets/toolbox.svg")
        self.assertEqual(sanitize_url("/docs/page/"), "/docs/page/")

    def test_sanitize_url_safe_http_https(self):
        self.assertEqual(sanitize_url("http://example.com"), "http://example.com")
        self.assertEqual(sanitize_url("https://example.com/asset.png"), "https://example.com/asset.png")

    def test_sanitize_url_protocol_relative_blocked(self):
        self.assertEqual(sanitize_url("//attacker.com"), "#")
        self.assertEqual(sanitize_url("//attacker.com/payload.js"), "#")
        self.assertEqual(sanitize_url("/\\attacker.com"), "#")

    def test_sanitize_url_javascript_data_schemes_blocked(self):
        self.assertEqual(sanitize_url("javascript:alert(1)"), "#")
        self.assertEqual(sanitize_url("data:text/html,<script>alert(1)</script>"), "#")

    def test_sanitize_url_empty_or_none(self):
        self.assertEqual(sanitize_url(""), "#")
        self.assertEqual(sanitize_url(None), "#")

if __name__ == '__main__':
    unittest.main()
