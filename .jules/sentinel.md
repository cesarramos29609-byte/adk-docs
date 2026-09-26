# Sentinel Journal

## 2026-09-26 - Markdown Frontmatter Icon URI Sanitization
**Vulnerability:** Unsanitized `catalog_icon` URLs in markdown frontmatter could allow URI scheme-based XSS (e.g. `javascript:` or `data:` schemes).
**Learning:** `html.escape()` escapes HTML special characters like `<`, `>`, `&`, and `"` but leaves URI schemes like `javascript:` intact when inserted into HTML `src` or `href` attributes.
**Prevention:** Validate URL schemes explicitly against an allowlist (`http://`, `https://`, or root-relative paths starting with `/`) before rendering into template attributes.
