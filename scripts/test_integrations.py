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
from scripts.integrations import _is_safe_url, DEFAULT_ICON


class TestIntegrationsSecurity(unittest.TestCase):

    def test_is_safe_url_valid(self):
        valid_urls = [
            "/integrations/assets/toolbox.svg",
            "/assets/icon.png",
            "assets/icon.png",
            "https://example.com/logo.svg",
            "http://example.com/logo.png",
        ]
        for url in valid_urls:
            with self.subTest(url=url):
                self.assertTrue(_is_safe_url(url))

    def test_is_safe_url_invalid(self):
        invalid_urls = [
            "javascript:alert(1)",
            "JAVASCRIPT:alert('xss')",
            "data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==",
            "vbscript:msgbox(1)",
            "file:///etc/passwd",
            "",
            None,
            123,
        ]
        for url in invalid_urls:
            with self.subTest(url=url):
                self.assertFalse(_is_safe_url(url))


if __name__ == "__main__":
    unittest.main()
