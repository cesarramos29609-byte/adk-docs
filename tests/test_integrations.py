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

    def test_allowed_urls(self):
        self.assertEqual(sanitize_url("/integrations/assets/toolbox.svg"), "/integrations/assets/toolbox.svg")
        self.assertEqual(sanitize_url("https://google.github.io/"), "https://google.github.io/")
        self.assertEqual(sanitize_url("http://example.com/icon.png"), "http://example.com/icon.png")

    def test_protocol_relative_urls_rejected(self):
        self.assertEqual(sanitize_url("//evil.com/malicious.js"), "#")
        self.assertEqual(sanitize_url("  //attacker.com  "), "#")

    def test_unsafe_schemes_rejected(self):
        self.assertEqual(sanitize_url("javascript:alert(1)"), "#")
        self.assertEqual(sanitize_url("data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg=="), "#")

    def test_empty_or_none(self):
        self.assertEqual(sanitize_url(""), "#")
        self.assertEqual(sanitize_url(None), "#")


if __name__ == "__main__":
    unittest.main()
