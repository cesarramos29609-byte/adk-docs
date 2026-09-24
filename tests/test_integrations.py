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
        self.macros = {}
        self.conf = {'docs_dir': docs_dir}

    def macro(self, func):
        self.macros[func.__name__] = func
        return func


class TestIntegrationsMacro(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.docs_dir = Path(self.temp_dir)
        self.env = MockEnv(str(self.docs_dir))
        define_env(self.env)
        self.render_catalog = self.env.macros['render_catalog']

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_unsafe_icon_schemes_replaced(self):
        # Create test markdown file with unsafe catalog_icon
        tool_file = self.docs_dir / "tool_unsafe.md"
        tool_file.write_text(
            "---\n"
            "title: Unsafe Tool\n"
            "catalog_icon: 'javascript:alert(1)'\n"
            "catalog_tags: ['security']\n"
            "---\n"
            "# Unsafe Tool Description\n",
            encoding='utf-8'
        )

        html_out = self.render_catalog("*.md")
        self.assertNotIn('javascript:alert(1)', html_out)
        self.assertIn('/integrations/assets/toolbox.svg', html_out)

    def test_safe_icon_urls_preserved(self):
        tool_file = self.docs_dir / "tool_safe.md"
        tool_file.write_text(
            "---\n"
            "title: Safe Tool\n"
            "catalog_icon: 'https://example.com/icon.png'\n"
            "catalog_tags: ['safe']\n"
            "---\n"
            "# Safe Tool\n",
            encoding='utf-8'
        )

        html_out = self.render_catalog("*.md")
        self.assertIn('https://example.com/icon.png', html_out)

    def test_relative_icon_url(self):
        tool_file = self.docs_dir / "tool_rel.md"
        tool_file.write_text(
            "---\n"
            "title: Relative Icon Tool\n"
            "catalog_icon: 'assets/icon.svg'\n"
            "---\n",
            encoding='utf-8'
        )

        html_out = self.render_catalog("*.md")
        self.assertIn('/assets/icon.svg', html_out)


if __name__ == '__main__':
    unittest.main()
