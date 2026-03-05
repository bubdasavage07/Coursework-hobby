
### 3. Security Misconfiguration: SPA Catch-all Exposure of Sensitive Files

*   Vulnerability: Security Misconfiguration / Information Disclosure (CWE-200)
*   Severity: Medium
*   Description: The SPA catch-all behavior serves the same index.html for requests like /.env, /robots.txt, /sitemap.xml, which may expose environment configuration or sensitive files via unintended paths.
*   Evidence: Observed behavior where requesting paths returns SPA HTML instead of 404s.
*   Impact: Potential exposure of server configuration and sensitive environment data to an attacker who probes discovery endpoints.
*   Remediation: Implement server-side 404 for non-existent files; disable directory listing; ensure sensitive files are blocked or served with proper access controls.

### 4. Authentication & Session Management: Client-Side Only Crypto & Potential Weaknesses

*   Vulnerability: Weak Password Hashing Assumptions / Client-Side Crypto Reliance (CWE-326/CWE-329)
*   Severity: Medium
*   Description: While client-side encryption is used, the security relies on secrecy of client device and proper KDF parameter handling. The kdf-params endpoint disclosure (see 1) exacerbates risk by giving attacker knowledge of KDF config.
*   Evidence: Client derives key using Argon2id with server-provided salt/params; authKeyHash is SHA-256 of authKey; kdf-params endpoint leaks params.
*   Impact: If endpoint allows attacker to learn kdfParams, offline brute-force attacks could be more feasible; if device is compromised, vault content could be exposed.
*   Remediation: Move KDF parameter disclosure behind proper authentication; rotate params per user; consider server-side validation and stricter crypto practices; server should not see plaintext vault data but ensure integrity.

### 5. Rate Limiting & Brute Force Protection: Inconsistent Controls

*   Vulnerability: Rate Limiting / Brute Force Protection (OWASP A05:2021 Security Misconfiguration)
*   Severity: Medium
*   Description: The code references 429 rate limit handling and 423 lockout after 15 minutes; unclear if endpoints implement consistent rate-limiting; absence of explicit rate-limiting headers.
*   Evidence: Mention of 429 in error handling; 423 lockout after repeated failures.
*   Impact: Attackers could enumerate or brute-force account access; denial of service by rapid failed attempts.
*   Remediation: Enforce consistent, global rate limiting; return uniform error messages; implement account lockout with progressive delay; add CAPTCHA or re-auth challenges after failures.

### 6. Information Disclosure: Missing Security Headers (Repeated)

*   Already covered in 2; re-iterating for completeness: ensure all HTTP(S) responses include CSP, HSTS, X-Frame-Options, Referrer-Policy.

### 7. Client-Side Security: SPA Attack Surface (XSS, CSRF)

*   Vulnerability: Client-side rendered SPA may be vulnerable to XSS if untrusted data is rendered; CSRF risk in cookie-based session if state-changing actions are not protected.
*   Severity: Low to Medium depending on implementation
*   Evidence: Frontend uses React with Axios; authentication via cookies; risky if no CSRF tokens and no SameSite=None without Secure flags.
*   Remediation: Use CSRF tokens for state-changing requests; set HttpOnly, Secure, SameSite=strict cookies; validate and sanitize data on server; implement CSP.

### 8. Supply Chain: Dependencies

*   Vulnerability: Third-party dependencies and build tooling (Vite, React, Node) may have known vulnerabilities.
*   Severity: Medium
*   Evidence: Not specifically observed; general risk.
*   Remediation: Run dependency scanning (npm audit, Snyk); lockfile updates; pin versions; enableViv; keep up to date.

### 9. Cloudflare / Hosting Misconfig: Exposure via Cloudflare

*   Vulnerability: Misconfiguration of Cloudflare security settings; server header exposure; lack of Origin Shield, WAF settings.
*   Severity: Medium
*   Evidence: Server header reveals Cloudflare; no secure headers.
*   Remediation: Use Cloudflare security features: WAF, TLS 1.3, HSTS preload, rate limiting, bot management, etc.

---

### Summary Recommendations (Top 6 Quick Wins)
- Remove information leakage via /api/auth/kdf-params by authenticating or genericize error; implement rate limiting.
- Add comprehensive security headers (CSP, HSTS, X-Frame-Options, Referrer-Policy) at Cloudflare or server level.
- Enforce server-side 404 for sensitive paths and disable SPA catch-all behavior for sensitive endpoints.
- Strengthen authentication: ensure consistent rate-limiting, lockout policies, and monitor for brute-force attempts.
- Add CSRF protection, SameSite cookies, and server-side validation.
- Regular dependency vulnerability scanning and patching.

