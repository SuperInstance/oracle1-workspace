# cocapn.ai SSL Fix - 2026-05-03

## Problem
cocapn.ai had no SSL certificate (`https_certificate: null` on GitHub Pages). purplepincher.org worked via Cloudflare proxy.

## Root Cause
The CNAME record for cocapn.ai was set to `superinstance.github.io` with `proxied: false`. Without Cloudflare proxy, GitHub Pages doesn't serve HTTPS for custom domains unless configured (which it wasn't).

## Fix Applied
Updated the existing CNAME record to enable Cloudflare proxy:

**Record:** `cocapn.ai` → `superinstance.github.io` (CNAME)
- **Before:** `proxied: false`
- **After:** `proxied: true`

## Verification

### DNS (Cloudflare)
```
cocapn.ai CNAME superinstance.github.io proxied=true TTL=1
```

### SSL Certificate (Cloudflare Universal)
```
Status: active
Certificate: *.cocapn.ai (Google Trust Services)
Valid: Apr 30 2026 → Jul 29 2026
```

### HTTPS Response
```
curl -sI https://cocapn.ai
HTTP/2 200
server: cloudflare
```

## Technical Details

### Why this works
- Cloudflare acts as a reverse proxy between visitors and GitHub Pages
- Cloudflare provides the SSL certificate (Universal SSL / Let's Encrypt)
- GitHub Pages sees requests coming from Cloudflare IPs, not directly from visitors
- GitHub Pages doesn't need its own cert for the custom domain

### Before vs After

| Aspect | Before | After |
|--------|--------|-------|
| DNS | Direct to GitHub | Cloudflare proxied |
| SSL | None (insecure) | Cloudflare Universal |
| Certificate | N/A | Google Trust Services *.cocapn.ai |
| Response headers | No server header | `server: cloudflare` |

## Cloudflare Zone Info
- **Zone ID:** 146d6a9d6c949b646e8b0145913d49bc
- **Account ID:** 049ff5e84ecf636b53b162cbb580aae6
- **DNS Token:** [CF_ZONE_TOKEN_REDACTED] (zone-scoped, DNS+SSL permissions)

## Comparison with purplepincher.org

| Domain | Type | Content | Proxied | SSL |
|--------|------|---------|---------|-----|
| cocapn.ai | CNAME | superinstance.github.io | ✅ true | ✅ Cloudflare Universal |
| purplepincher.org | CNAME | superinstance.github.io/purplepincher.org | ✅ true | ✅ Cloudflare Universal |

## Notes
- The CNAME target stays as `superinstance.github.io` (GitHub Pages origin)
- Cloudflare handles SSL termination; GitHub Pages receives plain HTTP from Cloudflare
- TTL is set to 1 (auto) which is appropriate for proxied records
- No DNS A records were needed or used — only the CNAME with proxy enabled