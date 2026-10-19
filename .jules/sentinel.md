## 2026-08-13 - Path Traversal in Custom MkDocs Macro Glob Processing
**Vulnerability:** `render_catalog` in `scripts/integrations.py` accepted glob patterns in `path_filter` without checking whether resolved file paths stayed within `docs_dir`.
**Learning:** `Path.glob()` can resolve paths traversing outside the specified directory root if relative path components like `..` are included in the glob string.
**Prevention:** Always sanitize input paths or verify `file_path.resolve().is_relative_to(base_dir.resolve())` before opening or processing files retrieved from user or template input.

## 2026-08-14 - Protocol-Relative URL Bypass in URL Sanitizer
**Vulnerability:** `sanitize_url` in `scripts/integrations.py` validated root-relative paths using `url.startswith('/')`, which allowed protocol-relative URLs starting with `//` (e.g. `//evil.com`).
**Learning:** Checking `url.startswith('/')` alone is insufficient for validating root-relative paths because browsers treat `//example.com` as a protocol-relative scheme pointing to an external domain.
**Prevention:** Ensure root-relative URL checks verify `cleaned.startswith('/') and not cleaned.startswith('//')`.
