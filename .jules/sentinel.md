## 2026-08-13 - Path Traversal in Custom MkDocs Macro Glob Processing
**Vulnerability:** `render_catalog` in `scripts/integrations.py` accepted glob patterns in `path_filter` without checking whether resolved file paths stayed within `docs_dir`.
**Learning:** `Path.glob()` can resolve paths traversing outside the specified directory root if relative path components like `..` are included in the glob string.
**Prevention:** Always sanitize input paths or verify `file_path.resolve().is_relative_to(base_dir.resolve())` before opening or processing files retrieved from user or template input.

## 2026-08-13 - Protocol-Relative URL Bypass in Custom MkDocs Macro URL Sanitization
**Vulnerability:** `sanitize_url` in `scripts/integrations.py` permitted protocol-relative URLs (`//evil.com`) because `.startswith('/')` evaluates to `True` for leading double slashes.
**Learning:** Checking `.startswith('/')` to validate root-relative links is insufficient because browsers treat `//example.com` as a protocol-relative absolute URL to an external domain.
**Prevention:** Explicitly check `cleaned.startswith('/') and not cleaned.startswith('//')` when enforcing root-relative paths to prevent open redirects or untrusted external URL loading.
