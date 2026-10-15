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
from scripts.integrations import sanitize_url, define_env


class TestIntegrationsScript(unittest.TestCase):

    def test_sanitize_url_valid(self):
        self.assertEqual(sanitize_url("/integrations/agentmail/"), "/integrations/agentmail/")
        self.assertEqual(sanitize_url("http://example.com/logo.png"), "http://example.com/logo.png")
        self.assertEqual(sanitize_url("https://example.com/logo.png"), "https://example.com/logo.png")
        self.assertEqual(sanitize_url("HTTP://EXAMPLE.COM/LOGO.PNG"), "HTTP://EXAMPLE.COM/LOGO.PNG")

    def test_sanitize_url_invalid_or_malicious(self):
        self.assertEqual(sanitize_url(""), "#")
        self.assertEqual(sanitize_url(None), "#")
        self.assertEqual(sanitize_url("javascript:alert(1)"), "#")
        self.assertEqual(sanitize_url("data:text/html,test"), "#")
        self.assertEqual(sanitize_url("//evil.com/phishing"), "#")
        self.assertEqual(sanitize_url("/\\evil.com/phishing"), "#")

    def test_define_env_macro_registration(self):
        class MockEnv:
            def __init__(self):
                self.macros = {}

            def macro(self, func):
                self.macros[func.__name__] = func
                return func

        env = MockEnv()
        define_env(env)
        self.assertIn("render_catalog", env.macros)


if __name__ == "__main__":
    unittest.main()
