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

class TestIntegrationsSanitizeUrl(unittest.TestCase):

    def test_sanitize_url_valid_root_relative(self):
        self.assertEqual(sanitize_url("/integrations/assets/toolbox.svg"), "/integrations/assets/toolbox.svg")
        self.assertEqual(sanitize_url("/docs/test/"), "/docs/test/")

    def test_sanitize_url_valid_http_https(self):
        self.assertEqual(sanitize_url("http://example.com"), "http://example.com")
        self.assertEqual(sanitize_url("https://example.com/logo.png"), "https://example.com/logo.png")

    def test_sanitize_url_rejects_protocol_relative(self):
        self.assertEqual(sanitize_url("//evil.com"), "#")
        self.assertEqual(sanitize_url("//attacker.com/malicious.png"), "#")

    def test_sanitize_url_rejects_javascript_and_data(self):
        self.assertEqual(sanitize_url("javascript:alert(1)"), "#")
        self.assertEqual(sanitize_url("data:text/html,<script>alert(1)</script>"), "#")

    def test_sanitize_url_empty_and_whitespace(self):
        self.assertEqual(sanitize_url(""), "#")
        self.assertEqual(sanitize_url(None), "#")
        self.assertEqual(sanitize_url("   "), "#")

if __name__ == "__main__":
    unittest.main()
