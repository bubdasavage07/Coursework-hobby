# Vulnerability Assessment Report

Target: `https://thevault.ryansnavely.com/login`  
Execution environment: `multipass shell ubuntu-agent` (Ubuntu 24.04)  
Date: 2026-03-04

## Scope and approach
I tested the public web app and discovered API surface from the frontend bundle, then validated each endpoint with direct HTTP method probing. I prioritized this order to avoid noisy blind scanning and to focus on realistic attack paths:
1. Fingerprint app + headers
2. Extract API routes from shipped JavaScript
3. Probe auth/vault endpoints for auth bypass, CORS, method abuse, and rate-limit behavior
4. Run targeted scanner checks (`nikto`, `nmap` scripts) for transport/header gaps

## Findings

### 1. Missing key security headers on HTML pages (Medium)
Affected:
- `GET /`
- `GET /login`

Evidence:
- Response headers do **not** include `Content-Security-Policy`, `X-Frame-Options`, or `Strict-Transport-Security`.
- Confirmed with:
  - `curl -sk -D - https://thevault.ryansnavely.com/ -o /dev/null`
  - `curl -sk -D - https://thevault.ryansnavely.com/login -o /dev/null`
  - `nmap --script http-security-headers ...` also reported HSTS missing.

Risk:
- Increased XSS blast radius (no CSP), potential clickjacking risk (no frame policy), and weaker HTTPS downgrade protection (no HSTS).

Recommendation:
- Add headers at edge/origin:
  - `Strict-Transport-Security: max-age=31536000; includeSubDomains; preload`
  - `Content-Security-Policy` (start strict, tune for required scripts)
  - `X-Frame-Options: DENY` (or CSP `frame-ancestors 'none'`)
  - Keep/extend `X-Content-Type-Options: nosniff`, `Referrer-Policy` on HTML too.

### 2. Legacy TLS versions exposed at edge (Medium)
Affected: TLS endpoint for `thevault.ryansnavely.com:443` (Cloudflare edge)

Evidence:
- `nmap -Pn -p 443 --script ssl-enum-ciphers thevault.ryansnavely.com`
- Reported support for TLSv1.0 and TLSv1.1 ciphers.

Risk:
- Older protocol compatibility can weaken transport posture and compliance (PCI/NIST expectations generally require disabling TLS 1.0/1.1).

Recommendation:
- At Cloudflare SSL/TLS settings, set minimum TLS version to `1.2` (or `1.3` where possible).

### 3. Production API CORS allowlist includes localhost origin (Low)
Affected:
- `POST /api/auth/login`
- `POST /api/auth/register`

Evidence:
- Response headers contain:
  - `Access-Control-Allow-Origin: http://localhost:5173`
  - `Access-Control-Allow-Credentials: true`
- Verified via:
  - `curl -X POST ... -H 'Origin: http://localhost:5173' ...`

Risk:
- Trusting localhost in production can create unnecessary attack surface in edge cases (malicious local services/dev tooling abuse).

Recommendation:
- Remove localhost origins from production CORS config.
- Use environment-specific allowlists.

### 4. HTTP endpoint does not enforce HTTPS redirect (Medium)
Affected:
- `GET http://thevault.ryansnavely.com/` (port 80)

Evidence:
- Requesting the cleartext endpoint returns `404 Not Found` directly over HTTP instead of a `301/302` redirect to HTTPS.
- Verified with:
  - `curl -s -D - http://thevault.ryansnavely.com/ -o /dev/null`
- Observed response status line:
  - `HTTP/1.1 404 Not Found`

Risk:
- Users who enter or follow an `http://` URL do not get upgraded automatically. Combined with missing HSTS, this increases downgrade/SSL-stripping exposure on hostile networks.

Recommendation:
- Enforce HTTP->HTTPS redirect at edge/origin for all host/path variants.
- Keep HSTS enabled on HTTPS responses to harden future visits.

### 5. Soft-404 behavior on nonexistent frontend paths (Low)
Affected:
- Arbitrary unknown non-API routes under `/` (SPA path handling)

Evidence:
- Random nonexistent path returned `200` with the same HTML shell as `/`:
  - Example tested path: `/nonexistent-1772665152-18254`
  - `curl -sk -D - https://thevault.ryansnavely.com/nonexistent-1772665152-18254 -o body`
  - Response: `HTTP/2 200`, `content-type: text/html`
  - Body hash matched `/` page hash in testing.
- By contrast, unknown API paths correctly returned `404`:
  - `curl -sk -D - https://thevault.ryansnavely.com/api/nope-... -o /dev/null`

Risk:
- Soft-404 responses reduce monitoring fidelity, create ambiguity for scanners and logging pipelines, and can hide broken links or mistyped endpoints during security triage.

Recommendation:
- Return real `404` for unknown routes at the edge (or include explicit not-found signaling in app/router plus compatible edge rules).
- Keep SPA fallback limited to intended client routes and exclude clearly invalid patterns.

### 6. Verbose auth validation error leaks request schema details (Low)
Affected:
- `POST /api/auth/login`

Evidence:
- Sending malformed login JSON returned a specific field-level validation message:
  - Request body: `{"username":"nosuchuser_20260304","password":"WrongPass123!"}`
  - Response: `HTTP/2 400` with `{"error":"Missing required field: email"}`
- Captured in `/tmp/vaultscan2/login_attempt_headers.txt` and `/tmp/vaultscan2/login_attempt_body.json`.

Risk:
- Detailed validation messages help attackers tune request formats faster during credential stuffing or auth abuse testing by disclosing exact expected schema and field names.

Recommendation:
- Return generic validation failures on auth endpoints (for example, `Invalid request`) and log full details server-side only.
- Keep fine-grained validation feedback for trusted/internal contexts only.

### 7. Auth endpoint responses lack explicit anti-cache directives (Low)
Affected:
- `POST /api/auth/login` (error responses)
- `POST /api/auth/refresh`
- `POST /api/auth/logout`

Evidence:
- Observed auth API responses without explicit `Cache-Control`/`Pragma` no-store directives in captured headers:
  - `/tmp/vaultscan2/login_attempt_headers.txt`
  - `/tmp/vaultscan2/refresh_headers.txt`
  - `/tmp/vaultscan2/logout_headers.txt`

Risk:
- Missing explicit no-store controls on authentication-related responses can increase risk of unintended caching by misconfigured intermediaries or client environments, potentially exposing auth metadata.

Recommendation:
- Add strict cache controls on auth endpoints:
  - `Cache-Control: no-store, no-cache, must-revalidate, private`
  - `Pragma: no-cache`
  - `Expires: 0`

## Additional observations (not confirmed vulnerabilities)
- API routes discovered from frontend bundle:
  - `/api/auth/{kdf-params,login,logout,refresh,register,account}`
  - `/api/vault{,/import,/export}`
- Unauthorized access checks were generally correct (`401`) for protected vault/account actions.
- `POST /api/auth/logout` returns `200 {"message":"Logged out"}` even when unauthenticated; this is usually low impact/no-op but worth confirming intended behavior.
- `POST /api/auth/login` and `POST /api/auth/register` were consistently rate-limited (`429`) from the test IP, which limited deeper auth-flow testing in this run.

## Commands used (core)
- `multipass shell ubuntu-agent`
- `curl` method/header probes across discovered endpoints
- JS route extraction from frontend bundle (`/assets/index-BB3QmwPU.js`)
- `nikto -h https://thevault.ryansnavely.com ...`
- `nmap -Pn -p 443 --script http-security-headers,ssl-enum-ciphers thevault.ryansnavely.com`
- Additional targeted probes:
  - HTTP redirect validation on port 80 (`curl -s -D - http://thevault.ryansnavely.com/`)
  - Randomized path soft-404 validation (`curl ... /nonexistent-*`)
  - Login/register rate-limit sampling (`25x POST /api/auth/login`)
  - Malformed auth payload validation/error probing (`POST /api/auth/login`)

## Files/artifacts generated in VM
- `/tmp/vaultscan/api_paths.txt`
- `/tmp/vaultscan/api_probe.txt`
- `/tmp/vaultscan/html_headers_full.txt`
- `/tmp/vaultscan/cors_headers.txt`
- `/tmp/vaultscan/localhost_cors.txt`
- `/tmp/vaultscan/nmap_headers_tls.txt`
- `/tmp/vaultscan/nikto.txt`
- `/tmp/vaultscan2/*` (extended method/CORS/path probes)
- `/tmp/vaultscan3/http_root_headers.txt`
- `/tmp/vaultscan3/soft404_headers.txt`
- `/tmp/vaultscan3/soft404_path.txt`
- `/tmp/vaultscan3/login_rate_sample.txt`
- `/tmp/vaultscan2/login_attempt_headers.txt`
- `/tmp/vaultscan2/login_attempt_body.json`

## What I would test next (if you want a phase 2)
1. Authenticated testing with a test account (IDOR/object-level auth on vault item CRUD).
2. CSRF validation with real session cookies and browser-based PoCs.
3. Rate-limit resilience and bypass analysis with controlled cooldown windows.
4. Dependency and client-side crypto review from source (not just minified bundle).
