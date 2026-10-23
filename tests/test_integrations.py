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
        self.assertEqual(sanitize_url("http://example.com/foo"), "http://example.com/foo")
        self.assertEqual(sanitize_url("/valid/relative/path"), "/valid/relative/path")

    def test_unsafe_urls(self):
        self.assertEqual(sanitize_url("javascript:alert(1)"), "#")
        self.assertEqual(sanitize_url("data:text/html,<script>alert(1)</script>"), "#")
        self.assertEqual(sanitize_url("//attacker.com/evil.js"), "#")
        self.assertEqual(sanitize_url("/\\attacker.com/evil.js"), "#")
        self.assertEqual(sanitize_url(""), "#")
        self.assertEqual(sanitize_url("   "), "#")


if __name__ == "__main__":
    unittest.main()
