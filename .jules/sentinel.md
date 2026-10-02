## 2026-08-13 - Path Traversal in Custom MkDocs Macro Glob Processing
**Vulnerability:** `render_catalog` in `scripts/integrations.py` accepted glob patterns in `path_filter` without checking whether resolved file paths stayed within `docs_dir`.
**Learning:** `Path.glob()` can resolve paths traversing outside the specified directory root if relative path components like `..` are included in the glob string.
**Prevention:** Always sanitize input paths or verify `file_path.resolve().is_relative_to(base_dir.resolve())` before opening or processing files retrieved from user or template input.

## 2026-08-14 - Protocol-Relative URL Security Bypass in Custom URL Sanitizer
**Vulnerability:** `sanitize_url` in `scripts/integrations.py` checked if URLs started with `/` to allow root-relative paths, but did not disallow `//` or `/\\`.
**Learning:** `url.startswith('/')` matches protocol-relative URLs (e.g. `//evil.com/payload.js` or `/\evil.com`), which browsers parse as network schemes, enabling open redirect or cross-origin script/resource loading.
**Prevention:** When validating root-relative URLs, explicitly ensure the string starts with `/` AND does NOT start with `//`, `/\\`, or `\\`.
