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


class TestSanitizeUrl(unittest.TestCase):

    def test_valid_urls(self):
        self.assertEqual(sanitize_url("https://example.com"), "https://example.com")
        self.assertEqual(sanitize_url("http://example.com/path"), "http://example.com/path")
        self.assertEqual(sanitize_url("/integrations/assets/tool.svg"), "/integrations/assets/tool.svg")

    def test_case_insensitive_schemes(self):
        self.assertEqual(sanitize_url("HTTPS://EXAMPLE.COM"), "HTTPS://EXAMPLE.COM")
        self.assertEqual(sanitize_url("Http://example.com"), "Http://example.com")

    def test_protocol_relative_and_bypass_urls(self):
        self.assertEqual(sanitize_url("//evil.com/malicious.js"), "#")
        self.assertEqual(sanitize_url("/\\evil.com/malicious.js"), "#")

    def test_xss_javascript_and_data_schemes(self):
        self.assertEqual(sanitize_url("javascript:alert(1)"), "#")
        self.assertEqual(sanitize_url("JAVASCRIPT:alert(1)"), "#")
        self.assertEqual(sanitize_url("data:text/html,<script>alert(1)</script>"), "#")

    def test_empty_and_whitespace_urls(self):
        self.assertEqual(sanitize_url(""), "#")
        self.assertEqual(sanitize_url("   "), "#")
        self.assertEqual(sanitize_url(None), "#")


if __name__ == "__main__":
    unittest.main()
