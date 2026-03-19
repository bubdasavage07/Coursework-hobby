# The Vault Assessment

Date: 2026-03-17
Target: `https://thevault.ryansnavely.com`
Test source: Kali VM controlled by the owner
Scope used: unauthenticated HTTP/API testing plus two isolated test accounts created for authenticated vault checks

## Executive Summary

I did not find an auth bypass, IDOR, or unauthenticated vault access issue.

I did confirm two weaker but real issues:

1. Account enumeration through `POST /api/auth/register`
2. Production CORS configuration still allows `http://localhost:5173` on auth responses

I also confirmed several non-findings:

- Unauthenticated access to `/api/vault` is blocked with `401`
- Cross-account update/delete on another user's vault entry returns `404`
- Malformed JSON on auth endpoints is handled cleanly with `400`

## Findings

### 1. Account Enumeration via Registration

Severity: Medium

`POST /api/auth/register` returns a distinct `409` with `{"error":"Email already registered"}` for an existing account.

Confirmed behavior:

- New email returns `201` and creates an account
- Reusing the same email returns `409`

Example response observed:

```http
HTTP/2 409
content-type: application/json

{"error":"Email already registered"}
```

Impact:

- An attacker can verify whether an email address already has an account
- That is useful for targeted phishing, credential stuffing, and privacy leakage

Recommendation:

- Return a generic registration response for both cases
- Example: always return `200`/`202` with a neutral message like "If the account can be created, further steps will follow"
- Move exact duplicate handling to logs/telemetry, not the public response body

### 2. Production API Sends CORS Headers for `http://localhost:5173`

Severity: Low to Medium

Auth responses from production included:

```http
Access-Control-Allow-Origin: http://localhost:5173
Access-Control-Allow-Credentials: true
Access-Control-Allow-Headers: Content-Type,Authorization
Access-Control-Allow-Methods: GET,POST,PUT,DELETE,OPTIONS
```

This was present on live `register` and `login` responses.

Impact:

- This looks like dev CORS configuration left enabled in production
- It is not a trivial internet-wide exploit because browsers still enforce origin matching, and your refresh cookie is `SameSite=Strict`
- It does expand trust to any code running from `http://localhost:5173`, which is unnecessary for production and weakens the boundary around auth endpoints

Recommendation:

- Remove `http://localhost:5173` from production CORS allowlists
- If you need local development, gate it by environment
- Only emit `Access-Control-Allow-Origin` for origins that must exist in production

## Confirmed Non-Findings

### Vault API Requires Auth

Both:

```http
GET /api/vault
POST /api/vault
```

returned:

```http
HTTP/2 401
{"error":"Unauthorized"}
```

### No Cross-Account Vault Entry Access

I created one vault entry under test account A, then attempted to update and delete it using test account B.

Both operations returned:

```http
HTTP/2 404
{"error":"Entry not found"}
```

That indicates object ownership checks are working for those routes.

### Malformed JSON Handling Is Clean

Malformed JSON sent to:

- `POST /api/auth/login`
- `POST /api/auth/register`

returned:

```http
HTTP/2 400
{"error":"Invalid JSON"}
```

No parser crash or verbose stack trace was exposed.

## Other Notes

### HTML Security Headers Are Thin

Your SPA HTML response did not include stronger browser-enforced headers like CSP or HSTS in the responses I observed. The page includes a meta `X-Content-Type-Options`, but that is not a substitute for server-set policy headers.

This is more hygiene than an exploit by itself, but for a password manager it is worth tightening.

Suggested additions:

- `Content-Security-Policy`
- `Strict-Transport-Security`
- `X-Content-Type-Options: nosniff` as a real header

### API Trusts Client-Side Password Policy

The frontend enforces a 12-character master password and client-side KDF derivation, but the backend will accept arbitrary `authKeyHash`, `kdfSalt`, and `kdfParams` values directly over the API.

That did not let me break into another account, but it does mean:

- password policy is effectively optional for anyone bypassing the UI
- server-side bounds checking for KDF parameters appears weak or absent

Recommendation:

- Validate acceptable `kdfParams` ranges server-side
- Enforce expected `authKeyHash` format/length
- If you want a real password policy, enforce it in backend terms the API can actually verify

## Test Artifacts

I created two temporary test accounts and one dummy vault entry during authenticated testing.

Emails used:

- `test1773764177@example.com`
- `test1773764222-b@example.com`

Cleanup was attempted, but by the end of testing the login endpoint was returning:

```json
{"error":"Too many requests"}
```

so I could not complete deletion in the same pass.

## Next Steps

1. Fix registration enumeration
2. Remove localhost CORS from production
3. Add real response security headers for the SPA and API
4. Add server-side validation for registration KDF/auth material
5. Manually remove the two temporary accounts if desired once rate limiting clears

## Full Step-By-Step Log

This section lists every substantive command I ran during the assessment, why I ran it, and what it accomplished.

### 1. SSH into the Kali VM

Command:

```bash
ssh -i /Users/ethan/kali-openclaw root@187.124.86.179
```

Why:

- The local sandbox could not resolve the target hostname
- You explicitly told me to run the assessment from your Kali VM

What it accomplished:

- Established an interactive shell on the VM so all subsequent testing came from that host

### 2. Fetch the root page

Command:

```bash
curl -i -sS https://thevault.ryansnavely.com/
```

Why:

- To identify the app type, headers, CDN/proxy behavior, and any immediately exposed frontend resources

What it accomplished:

- Confirmed the app is served through Cloudflare
- Confirmed the root serves a SPA HTML shell
- Identified the frontend JS bundle: `/assets/index-BB3QmwPU.js`

### 3. Fetch the login page

Command:

```bash
curl -i -sS https://thevault.ryansnavely.com/login
```

Why:

- To see whether `/login` was server-rendered, distinct from `/`, or just another SPA route

What it accomplished:

- Confirmed `/login` also falls through to the same SPA shell

### 4. Check `robots.txt`

Command:

```bash
curl -i -sS https://thevault.ryansnavely.com/robots.txt
```

Why:

- To see if standard public files leaked deployment details or paths

What it accomplished:

- Confirmed `/robots.txt` also falls through to the SPA HTML instead of a real robots file

### 5. Check `sitemap.xml`

Command:

```bash
curl -i -sS https://thevault.ryansnavely.com/sitemap.xml
```

Why:

- To look for route disclosure or deployment artifacts

What it accomplished:

- Confirmed `/sitemap.xml` also falls through to the SPA HTML

### 6. Download the frontend JavaScript bundle

Command:

```bash
curl -sS https://thevault.ryansnavely.com/assets/index-BB3QmwPU.js > /tmp/thevault-app.js
```

Why:

- To extract the real API routes and client-side auth logic directly from the bundle

What it accomplished:

- Saved the production JS locally on the VM for string extraction and code inspection

### 7. Attempt route extraction with `rg`

Command:

```bash
rg -n "api/|/auth|login|register|vault|fetch\(|axios|localStorage|sessionStorage|csrf|token" /tmp/thevault-app.js | sed -n '1,220p'
```

Why:

- `rg` is the fastest way to extract API references

What it accomplished:

- Nothing useful; `rg` was not installed on the VM

### 8. Extract API routes with `grep`

Commands:

```bash
/usr/bin/grep -aoE '/api/[A-Za-z0-9_./?-]+' /tmp/thevault-app.js | sort -u | sed -n '1,200p'
/usr/bin/grep -aoE '/[A-Za-z0-9_-]+/(login|register|auth|vault|entries|notes|passwords)[A-Za-z0-9_./?-]*' /tmp/thevault-app.js | sort -u | sed -n '1,200p'
```

Why:

- To recover the app’s real API endpoints without relying on guesswork

What it accomplished:

- Identified these routes:
  - `/api/auth/account`
  - `/api/auth/kdf-params`
  - `/api/auth/login`
  - `/api/auth/logout`
  - `/api/auth/refresh`
  - `/api/auth/register`
  - `/api/vault`
  - `/api/vault/`
  - `/api/vault/export`
  - `/api/vault/import`

### 9. Probe auth and vault endpoints for basic behavior

Commands:

```bash
curl -i -sS https://thevault.ryansnavely.com/api/auth/kdf-params
curl -i -sS https://thevault.ryansnavely.com/api/auth/account
curl -i -sS -X OPTIONS https://thevault.ryansnavely.com/api/auth/login
curl -i -sS -X OPTIONS https://thevault.ryansnavely.com/api/vault
curl -i -sS -H 'Content-Type: application/json' -X POST https://thevault.ryansnavely.com/api/auth/login --data '{}'
curl -i -sS -H 'Content-Type: application/json' -X POST https://thevault.ryansnavely.com/api/auth/register --data '{}'
```

Why:

- To check method handling, validation quality, and route exposure

What it accomplished:

- Confirmed `kdf-params` requires an email parameter
- Confirmed `/api/auth/account` rejects unsupported methods with `405`
- Confirmed `login` and `vault` advertise expected methods
- Confirmed empty JSON bodies are rejected cleanly with `400`

### 10. Check unauthenticated access and malformed JSON handling

Commands:

```bash
curl -i -sS https://thevault.ryansnavely.com/api/vault
curl -i -sS -X POST https://thevault.ryansnavely.com/api/vault
curl -i -sS -H 'Content-Type: application/json' -X POST https://thevault.ryansnavely.com/api/auth/login --data '{bad json'
curl -i -sS -H 'Content-Type: application/json' -X POST https://thevault.ryansnavely.com/api/auth/register --data '{bad json'
curl -i -sS -X POST https://thevault.ryansnavely.com/api/auth/refresh
curl -i -sS -X POST https://thevault.ryansnavely.com/api/auth/logout
curl -i -sS 'https://thevault.ryansnavely.com/api/auth/kdf-params?email=test@example.com'
```

Why:

- To test unauthorized access, parser robustness, token refresh behavior, and KDF parameter disclosure

What it accomplished:

- Confirmed unauthenticated vault access is blocked with `401`
- Confirmed malformed JSON is handled cleanly with `400 {"error":"Invalid JSON"}`
- Confirmed refresh without cookie returns `401 {"error":"No refresh token"}`
- Confirmed logout is callable unauthenticated and returns a benign success message
- Confirmed `kdf-params` returns KDF settings and a salt for arbitrary emails

### 11. Check whether `kdfSalt` is global or per-email

Commands:

```bash
curl -sS 'https://thevault.ryansnavely.com/api/auth/kdf-params?email=test@example.com'
curl -sS 'https://thevault.ryansnavely.com/api/auth/kdf-params?email=another@example.com'
curl -sS 'https://thevault.ryansnavely.com/api/auth/kdf-params?email=ryan@example.com'
```

Why:

- To determine whether the KDF response leaked shared cryptographic material or simply derived per-account salt

What it accomplished:

- Confirmed the salt changes per email, which reduced concern there

### 12. Inspect frontend auth flow around login/register/vault

Commands:

```bash
python3 - <<'PY'
from pathlib import Path
s=Path('/tmp/thevault-app.js').read_text()
for needle in ['/api/auth/register','/api/auth/login','/api/vault/export','/api/vault/import']:
    i=s.find(needle)
    print('\n---', needle, '---')
    print(s[max(0,i-350):i+500])
PY
```

and

```bash
python3 - <<'PY'
from pathlib import Path
s=Path('/tmp/thevault-app.js').read_text()
for needle in ['Fetching key derivation parameters','Authenticating','Create your vault','register(', 'li.register', 'li.login', 'authKey', 'encryptedKey', 'encrypted_data']:
    i=s.find(needle)
    if i!=-1:
        print('\n---', needle, 'at', i, '---')
        print(s[max(0,i-700):i+1200])
PY
```

Why:

- To recover request shapes from the minified client instead of guessing field names
- To understand whether the backend or frontend performs the key derivation and password policy

What it accomplished:

- Confirmed login uses:
  - `email`
  - `authKeyHash`
- Confirmed registration uses:
  - `email`
  - `authKeyHash`
  - `kdfSalt`
  - `kdfParams`
- Confirmed client-side derivation of `authKey` and encryption key
- Confirmed the API stores/accepts encrypted vault blobs as `encrypted_data`
- Confirmed bearer-token auth for API access and cookie-based refresh flow

### 13. Create test account A

Commands:

```bash
EMAIL=test$(date +%s)@example.com
AUTH=1111111111111111111111111111111111111111111111111111111111111111
curl -i -sS -H 'Content-Type: application/json' -X POST https://thevault.ryansnavely.com/api/auth/register --data '{"email":"'"$EMAIL"'","authKeyHash":"'"$AUTH"'","kdfSalt":"QUFBQUFBQUFBQUFBQUFBQQ==","kdfParams":{"iterations":3,"memory":65536,"parallelism":1}}'
printf '\nEMAIL=%s\nAUTH=%s\n' "$EMAIL" "$AUTH"
curl -i -sS -c /tmp/thevault.cookies -H 'Content-Type: application/json' -X POST https://thevault.ryansnavely.com/api/auth/login --data '{"email":"'"$EMAIL"'","authKeyHash":"'"$AUTH"'"}'
```

Why:

- To obtain a controlled authenticated account for vault testing

What it accomplished:

- Created test account A
- Logged in successfully
- Captured:
  - bearer `accessToken`
  - `refreshToken` cookie
- Verified auth cookie flags:
  - `HttpOnly`
  - `Secure`
  - `SameSite=Strict`
  - `Path=/api/auth`

### 14. Test authenticated vault access and create a vault entry

Commands:

```bash
EMAIL1=test1773764177@example.com
AUTH1=1111111111111111111111111111111111111111111111111111111111111111
TOKEN1=$(curl -sS -c /tmp/thevault1.cookies -H 'Content-Type: application/json' -X POST https://thevault.ryansnavely.com/api/auth/login --data '{"email":"'"$EMAIL1"'","authKeyHash":"'"$AUTH1"'"}' | jq -r .accessToken)
printf 'TOKEN1=%s\n' "$TOKEN1"
curl -i -sS -H "Authorization: Bearer $TOKEN1" https://thevault.ryansnavely.com/api/vault
curl -i -sS -H 'Content-Type: application/json' -H "Authorization: Bearer $TOKEN1" -X POST https://thevault.ryansnavely.com/api/vault --data '{"encrypted_data":{"iv":"QUFBQUFBQUFBQUFB","ciphertext":"QkJCQkJCQkJCQkJCQkJCQg=="}}'
```

Why:

- To confirm the bearer token worked
- To create one owned object for cross-account authorization testing

What it accomplished:

- Confirmed authenticated `GET /api/vault` returns the account’s entries
- Created one dummy vault entry under account A
- Captured its UUID:
  - `90d75dc7-3efd-4d6c-9a99-beb488f6f838`

### 15. Probe CORS behavior

Commands:

```bash
curl -i -sS -H 'Origin: http://localhost:5173' -H 'Access-Control-Request-Method: POST' -H 'Access-Control-Request-Headers: content-type' -X OPTIONS https://thevault.ryansnavely.com/api/auth/login
curl -i -sS -H 'Origin: https://evil.example' -H 'Access-Control-Request-Method: POST' -H 'Access-Control-Request-Headers: content-type' -X OPTIONS https://thevault.ryansnavely.com/api/auth/login
```

Why:

- To determine whether production CORS was restricted or if dev origins were still allowed

What it accomplished:

- Confirmed the production API had already emitted `Access-Control-Allow-Origin: http://localhost:5173` on real auth responses
- Observed preflight handling that did not strongly validate origin in the response body/headers I saw
- This supported the CORS misconfiguration finding, though not a full cross-origin credential theft exploit by itself

### 16. Create test account B and test cross-account access

Commands:

```bash
ENTRY1=90d75dc7-3efd-4d6c-9a99-beb488f6f838
EMAIL2=test$(date +%s)-b@example.com
AUTH2=2222222222222222222222222222222222222222222222222222222222222222
curl -sS -H 'Content-Type: application/json' -X POST https://thevault.ryansnavely.com/api/auth/register --data '{"email":"'"$EMAIL2"'","authKeyHash":"'"$AUTH2"'","kdfSalt":"QkJCQkJCQkJCQkJCQkJCQg==","kdfParams":{"iterations":3,"memory":65536,"parallelism":1}}' | jq .
TOKEN2=$(curl -sS -H 'Content-Type: application/json' -X POST https://thevault.ryansnavely.com/api/auth/login --data '{"email":"'"$EMAIL2"'","authKeyHash":"'"$AUTH2"'"}' | jq -r .accessToken)
printf 'EMAIL2=%s\nTOKEN2=%s\n' "$EMAIL2" "$TOKEN2"
curl -i -sS -H 'Content-Type: application/json' -H "Authorization: Bearer $TOKEN2" -X PUT https://thevault.ryansnavely.com/api/vault/$ENTRY1 --data '{"encrypted_data":{"iv":"Q0NDQ0NDQ0NDQ0ND","ciphertext":"RERERERERERERERERERERA=="}}'
curl -i -sS -H "Authorization: Bearer $TOKEN2" -X DELETE https://thevault.ryansnavely.com/api/vault/$ENTRY1
curl -i -sS -H "Authorization: Bearer $TOKEN1" https://thevault.ryansnavely.com/api/vault
```

Why:

- To test for IDOR or broken object-level authorization

What it accomplished:

- Confirmed account B could not modify or delete account A’s vault entry
- Both update and delete returned `404 {"error":"Entry not found"}`
- Verified account A’s entry still existed afterward

### 17. Run `nmap` method check

Command:

```bash
nmap --script http-methods -p 443 thevault.ryansnavely.com
```

Why:

- To do a fast server-level method exposure check separate from the app’s route-level behavior

What it accomplished:

- Confirmed the edge server itself only exposed `GET` and `HEAD` at the HTTP-service level in that scan context
- This was not very informative for the app API because Cloudflare and route logic sit in front

### 18. Start `nikto`

Command:

```bash
nikto -host https://thevault.ryansnavely.com -ask no -nointeractive
```

Why:

- To see if a generic web scanner surfaced anything I had not already seen manually

What it accomplished:

- Nothing useful before I stopped it
- The manual testing already had better signal than waiting on scanner noise

### 19. Stop the lingering scan

Command:

```text
Ctrl-C
```

Why:

- The scan was taking longer than necessary and was not producing higher-value data

What it accomplished:

- Returned the shell promptly so I could finish with targeted checks instead

### 20. Confirm account enumeration explicitly

Commands:

```bash
curl -i -sS -H 'Content-Type: application/json' -X POST https://thevault.ryansnavely.com/api/auth/register --data '{"email":"test1773764177@example.com","authKeyHash":"1111111111111111111111111111111111111111111111111111111111111111","kdfSalt":"QUFBQUFBQUFBQUFBQUFBQQ==","kdfParams":{"iterations":3,"memory":65536,"parallelism":1}}'
curl -i -sS https://thevault.ryansnavely.com/ | sed -n '1,40p'
```

Why:

- To verify that duplicate registration returned a distinct, user-enumerating response
- To quickly re-check the HTML headers one more time

What it accomplished:

- Confirmed duplicate registration returns:
  - `409`
  - `{"error":"Email already registered"}`
- Confirmed the main HTML still lacked stronger response security headers in the observed response

### 21. Attempt cleanup of test artifacts

Commands:

```bash
TOKEN1=$(curl -sS -H 'Content-Type: application/json' -X POST https://thevault.ryansnavely.com/api/auth/login --data '{"email":"test1773764177@example.com","authKeyHash":"1111111111111111111111111111111111111111111111111111111111111111"}' | jq -r .accessToken)
TOKEN2=$(curl -sS -H 'Content-Type: application/json' -X POST https://thevault.ryansnavely.com/api/auth/login --data '{"email":"test1773764222-b@example.com","authKeyHash":"2222222222222222222222222222222222222222222222222222222222222222"}' | jq -r .accessToken)
curl -i -sS -H "Authorization: Bearer $TOKEN1" -X DELETE https://thevault.ryansnavely.com/api/vault/90d75dc7-3efd-4d6c-9a99-beb488f6f838
curl -i -sS -H "Authorization: Bearer $TOKEN1" -X DELETE https://thevault.ryansnavely.com/api/auth/account
curl -i -sS -H "Authorization: Bearer $TOKEN2" -X DELETE https://thevault.ryansnavely.com/api/auth/account
```

Why:

- To remove the two test accounts and the dummy vault entry after testing

What it accomplished:

- Cleanup did not succeed
- Those delete attempts returned `401`

### 22. Retry cleanup with fresh cookie-backed auth

Commands:

```bash
RESP1=$(curl -sS -c /tmp/t1.cookies -H 'Content-Type: application/json' -X POST https://thevault.ryansnavely.com/api/auth/login --data '{"email":"test1773764177@example.com","authKeyHash":"1111111111111111111111111111111111111111111111111111111111111111"}')
TOKEN1=$(printf '%s' "$RESP1" | jq -r .accessToken)
printf 'RESP1=%s\nTOKEN1=%s\n' "$RESP1" "$TOKEN1"
curl -i -sS -H "Authorization: Bearer $TOKEN1" https://thevault.ryansnavely.com/api/vault
curl -i -sS -b /tmp/t1.cookies -H "Authorization: Bearer $TOKEN1" -X DELETE https://thevault.ryansnavely.com/api/vault/90d75dc7-3efd-4d6c-9a99-beb488f6f838
curl -i -sS -b /tmp/t1.cookies -H "Authorization: Bearer $TOKEN1" -X DELETE https://thevault.ryansnavely.com/api/auth/account
```

Why:

- To see whether cleanup required both the bearer token and the refresh/auth cookie context

What it accomplished:

- The login endpoint had started rate limiting by then
- Response observed:

```json
{"error":"Too many requests"}
```

- That prevented cleanup during the same session

### 23. Exit the VM

Command:

```bash
exit
```

Why:

- To close the SSH session after testing

What it accomplished:

- Ended the remote assessment session cleanly

## Follow-Up Testing Ideas

These are the next things I would test if continuing the assessment later. They are ordered roughly by value.

### 1. Retry Cleanup and Confirm Delete Semantics

Why:

- Two test accounts and one dummy entry may still exist
- `DELETE /api/auth/account` returning `401` during cleanup is worth understanding

What to do:

- Wait for login rate limiting to clear
- Re-authenticate both test accounts
- Test deletion with:
  - bearer token only
  - refresh cookie only
  - bearer token plus refresh cookie
- Verify whether account deletion requires a CSRF token, password re-entry, or a different auth path

What to look for:

- Inconsistent auth requirements
- Account deletion that works with only cookie context
- A cleanup path that differs from what the frontend implies

### 2. Test Refresh Token Rotation and Replay

Why:

- The app uses short-lived bearer tokens and cookie-backed refresh
- Rotation bugs are common and high impact

What to do:

- Login once and save the original `refreshToken` cookie
- Call `POST /api/auth/refresh`
- See whether a new cookie is issued
- Try replaying the old refresh cookie after rotation

What to look for:

- Old refresh token still valid after refresh
- Multiple refresh tokens active concurrently for one session
- Missing binding between refresh token and user/session state

### 3. Inspect JWT Validation Edge Cases

Why:

- The app uses bearer JWTs for vault API access

What to do:

- Decode one token locally and inspect claims
- Try:
  - expired token reuse
  - malformed token structure
  - valid token with altered signature
  - token in wrong header casing or duplicated headers

What to look for:

- Anything other than clean `401`
- Leaky errors that expose signing or validation internals

### 4. Fuzz `kdfParams` on Registration

Why:

- The backend appears to accept client-supplied KDF parameters

What to do:

- Register disposable accounts with extreme values for:
  - `iterations`
  - `memory`
  - `parallelism`
- Also try wrong types:
  - strings
  - negative numbers
  - floats
  - huge integers
  - nulls

What to look for:

- Server accepts unsafe values
- Server crashes or slows down badly
- Validation mismatch between frontend expectations and backend acceptance

### 5. Test `authKeyHash` Validation Strictness

Why:

- The backend accepted a dummy repeated hex string during my test account creation

What to do:

- Try registration/login with:
  - short strings
  - oversized strings
  - non-hex strings
  - unicode
  - empty string
  - `null`

What to look for:

- Weak format enforcement
- Parser inconsistencies
- Potential storage or logging edge cases

### 6. Enumerate Rate-Limit Scope and Bypass Potential

Why:

- I hit `{"error":"Too many requests"}` during cleanup

What to do:

- Measure whether rate limiting is keyed by:
  - IP
  - email
  - route
  - account
  - cookie/session
- Compare login, register, and refresh thresholds

What to look for:

- Account lockout abuse potential
- Easy distributed bypass
- Inconsistent treatment of real users vs attackers

### 7. Check Password Reset / Recovery Surface If It Exists

Why:

- Account recovery paths often undercut otherwise decent auth

What to do:

- Search the frontend bundle for:
  - `reset`
  - `forgot`
  - `recover`
  - `verify`
  - `email`
- Probe any discovered endpoints

What to look for:

- Account enumeration
- weak token formats
- reset links not bound to session or device context

### 8. Probe Import/Export More Aggressively

Why:

- Import/export endpoints frequently have validation and resource-consumption issues

What to do:

- With an authenticated test account:
  - call `GET /api/vault/export`
  - call `POST /api/vault/import` with malformed arrays
  - send oversized payloads
  - send duplicate entries
  - send entries with missing nested fields

What to look for:

- Broken schema validation
- unbounded resource use
- server-side trust of client object structure

### 9. Check for Stored XSS in Decrypted Vault Data Rendering

Why:

- Even encrypted-at-rest systems can be vulnerable after client-side decryption and rendering

What to do:

- Create vault items whose decrypted fields contain:
  - raw HTML
  - event handlers
  - SVG payloads
  - long markdown-like strings
- Then load the real UI and inspect render behavior

What to look for:

- Execution in the browser after decrypt/render
- unsafe `dangerouslySetInnerHTML` behavior
- DOM injection in item titles, notes, or metadata

### 10. Verify CSP and Other Response Headers on API and HTML

Why:

- The root HTML response I saw lacked stronger browser security headers

What to do:

- Re-check both HTML and API routes for:
  - `Content-Security-Policy`
  - `Strict-Transport-Security`
  - `X-Content-Type-Options`
  - `Cross-Origin-Resource-Policy`
  - `Cross-Origin-Opener-Policy`
  - `Permissions-Policy`

What to look for:

- Missing or inconsistent headers between static and API responses
- policy gaps that matter for a password manager frontend

### 11. Verify CORS Behavior in a Real Browser Context

Why:

- I confirmed production responses include `Access-Control-Allow-Origin: http://localhost:5173`
- I did not complete a full browser-origin exploit chain

What to do:

- Serve a minimal page from `http://localhost:5173`
- From that origin, try:
  - `fetch()` to login
  - credentialed `fetch()` to refresh
  - reading JSON responses

What to look for:

- Whether browsers actually expose response bodies to JS from that origin
- whether credentialed cross-origin refresh is possible at all with `SameSite=Strict`

### 12. Search the Bundle for Hidden or Admin Routes

Why:

- SPA bundles often reveal endpoints not reachable from the normal UI

What to do:

- Extract additional strings from the JS bundle for:
  - `/admin`
  - `/debug`
  - `/health`
  - `/metrics`
  - `/internal`
  - `/users`
  - feature flags

What to look for:

- Hidden maintenance routes
- debug behaviors left exposed in production

### 13. Confirm Whether `kdf-params` Enables Useful Enumeration Beyond Registration

Why:

- I saw per-email salts returned for arbitrary addresses
- That may or may not differ for registered vs unregistered accounts

What to do:

- Compare `kdf-params` responses for:
  - known-existing emails
  - definitely-nonexistent emails
- Check for differences in:
  - status
  - timing
  - salt format
  - response length

What to look for:

- Silent account enumeration through timing or payload shape

### 14. Test Logout and Refresh CSRF Assumptions

Why:

- `logout` is callable without much ceremony
- refresh relies on cookie context

What to do:

- From a separate origin, test whether browser form posts or JS requests can trigger:
  - logout
  - refresh

What to look for:

- Cross-site logout CSRF
- refresh behavior that depends only on ambient cookies

### 15. Build a Minimal Regression Checklist

Why:

- If you patch the issues, you need a quick repeatable verification set

Suggested checklist:

1. Duplicate registration returns generic response
2. Production no longer emits localhost CORS headers
3. Unauthenticated vault still returns `401`
4. Cross-account vault entry mutation still fails
5. Malformed JSON still returns safe `400`
6. Cleanup of disposable test accounts works predictably

## Regression Checklist Commands

Run these from your Kali VM.

Set target first:

```bash
TARGET="https://thevault.ryansnavely.com"
```

### 1. Duplicate Registration Should Return a Generic Response

Replace the email with an account you know already exists.

```bash
EMAIL="replace-with-existing-account@example.com"
AUTH="1111111111111111111111111111111111111111111111111111111111111111"

curl -i -sS -H 'Content-Type: application/json' \
  -X POST "$TARGET/api/auth/register" \
  --data '{"email":"'"$EMAIL"'","authKeyHash":"'"$AUTH"'","kdfSalt":"QUFBQUFBQUFBQUFBQUFBQQ==","kdfParams":{"iterations":3,"memory":65536,"parallelism":1}}'
```

Expected after fix:

- No account-existence-specific message like `Email already registered`

### 2. Production Should Not Emit Localhost CORS

```bash
curl -i -sS -H 'Content-Type: application/json' \
  -X POST "$TARGET/api/auth/login" \
  --data '{"email":"nobody@example.com","authKeyHash":"1111111111111111111111111111111111111111111111111111111111111111"}' \
  | sed -n '1,40p'

curl -i -sS -H 'Origin: http://localhost:5173' \
  -H 'Access-Control-Request-Method: POST' \
  -H 'Access-Control-Request-Headers: content-type' \
  -X OPTIONS "$TARGET/api/auth/login"
```

Expected after fix:

- No `Access-Control-Allow-Origin: http://localhost:5173` in production

### 3. Unauthenticated Vault Must Still Return `401`

```bash
curl -i -sS "$TARGET/api/vault"
curl -i -sS -X POST "$TARGET/api/vault"
```

Expected:

- `401 Unauthorized`

### 4. Cross-Account Vault Mutation Must Fail

```bash
EMAIL1="testa$(date +%s)@example.com"
AUTH1="1111111111111111111111111111111111111111111111111111111111111111"
EMAIL2="testb$(date +%s)@example.com"
AUTH2="2222222222222222222222222222222222222222222222222222222222222222"

curl -sS -H 'Content-Type: application/json' -X POST "$TARGET/api/auth/register" \
  --data '{"email":"'"$EMAIL1"'","authKeyHash":"'"$AUTH1"'","kdfSalt":"QUFBQUFBQUFBQUFBQUFBQQ==","kdfParams":{"iterations":3,"memory":65536,"parallelism":1}}' | jq .

TOKEN1=$(curl -sS -H 'Content-Type: application/json' -X POST "$TARGET/api/auth/login" \
  --data '{"email":"'"$EMAIL1"'","authKeyHash":"'"$AUTH1"'"}' | jq -r .accessToken)

ENTRY_ID=$(curl -sS -H 'Content-Type: application/json' -H "Authorization: Bearer $TOKEN1" \
  -X POST "$TARGET/api/vault" \
  --data '{"encrypted_data":{"iv":"QUFBQUFBQUFBQUFB","ciphertext":"QkJCQkJCQkJCQkJCQkJCQg=="}}' | jq -r .id)

curl -sS -H 'Content-Type: application/json' -X POST "$TARGET/api/auth/register" \
  --data '{"email":"'"$EMAIL2"'","authKeyHash":"'"$AUTH2"'","kdfSalt":"QkJCQkJCQkJCQkJCQkJCQg==","kdfParams":{"iterations":3,"memory":65536,"parallelism":1}}' | jq .

TOKEN2=$(curl -sS -H 'Content-Type: application/json' -X POST "$TARGET/api/auth/login" \
  --data '{"email":"'"$EMAIL2"'","authKeyHash":"'"$AUTH2"'"}' | jq -r .accessToken)

curl -i -sS -H 'Content-Type: application/json' -H "Authorization: Bearer $TOKEN2" \
  -X PUT "$TARGET/api/vault/$ENTRY_ID" \
  --data '{"encrypted_data":{"iv":"Q0NDQ0NDQ0NDQ0ND","ciphertext":"RERERERERERERERERERERA=="}}'

curl -i -sS -H "Authorization: Bearer $TOKEN2" \
  -X DELETE "$TARGET/api/vault/$ENTRY_ID"
```

Expected:

- Update/delete from account 2 should fail

### 5. Malformed JSON Should Still Return Safe `400`

```bash
curl -i -sS -H 'Content-Type: application/json' \
  -X POST "$TARGET/api/auth/login" \
  --data '{bad json'

curl -i -sS -H 'Content-Type: application/json' \
  -X POST "$TARGET/api/auth/register" \
  --data '{bad json'
```

Expected:

- `400`
- Generic parse error such as `Invalid JSON`

### 6. Cleanup of Disposable Test Accounts Should Work Predictably

```bash
curl -i -sS -H "Authorization: Bearer $TOKEN1" \
  -X DELETE "$TARGET/api/vault/$ENTRY_ID"

curl -i -sS -H "Authorization: Bearer $TOKEN1" \
  -X DELETE "$TARGET/api/auth/account"

curl -i -sS -H "Authorization: Bearer $TOKEN2" \
  -X DELETE "$TARGET/api/auth/account"
```

Expected:

- Cleanup succeeds without confusing auth failures
