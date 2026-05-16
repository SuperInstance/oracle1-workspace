# HN Launch Postmortem — 2026-05-13

**Result:** Flagged. 3 points, 0 comments.
**Link:** https://news.ycombinator.com/item?id=48128177
**Root cause:** DNS changes made hours before posting caused Cloudflare IPv6 proxy to break.

## Timeline

- **19:00 UTC** — Cloudflare proxy enabled for fleet.cocapn.ai (changed from DNS-only to proxied)
- **21:00 UTC** — Proxy disabled and re-enabled multiple times during debugging
- **21:30 UTC** — HN post submitted. fleet.cocapn.ai returning 523 (Origin unreachable via IPv6)
- **22:00-23:00 UTC** — DNS propagation window. Post flagged. 3 points.
- **23:12 UTC** — DNS finally propagated. fleet.cocapn.ai returns 200. Too late.

## What went wrong

1. **DNS changes too close to posting.** Cloudflare proxy was toggled 3+ times in the 3 hours before the post. Each toggle triggered a propagation cycle that left the site in an inconsistent state.

2. **Primary link wasn't tested externally.** The GH Pages fallback (`superinstance.github.io/vessel-room-navigator/`) was working continuously. But the HN post linked to `plato.purplepincher.org` (a different page entirely) and the demo lived at `fleet.cocapn.ai` which was broken.

3. **No pre-flight checklist.** No dry run, no external verification, no fallback URL in the post body.

## What to do differently next time

1. **Freeze infrastructure 24 hours before posting.** No DNS changes, no nginx config changes, no cert renewals. The site must be stable for a full day before posting.

2. **Primary link = GH Pages.** GitHub's CDN is separate from our server. `superinstance.github.io/vessel-room-navigator/` cannot go down even if our entire instance crashes. Next post links here directly.

3. **Pre-flight checklist:**
   - [ ] Load the page from a different machine/network
   - [ ] Load the page from a different browser
   - [ ] Load the page from a mobile device
   - [ ] Check all texture assets load
   - [ ] Verify no hardcoded IPs in the deployed code
   - [ ] Confirm SSL cert is valid for >30 days
   - [ ] Run `curl` from a different server to verify external access

4. **Fallback plan:**
   - If the main URL fails, immediately post a comment with the GH Pages link
   - The comment gets pinned at the top of the thread
   - Have the fallback URL written down beforehand, not scrambed for after

5. **Repost when ready.** The demo works now. The infrastructure is stable. When a clear window opens — no DNS changes for 24+ hours, external verification done — repost with a working link.

## The demo works now

fleet.cocapn.ai returns 200. The 3D viewer loads in 600ms. All 10 textures serve. The Page has 7 AI-generated panoramas, room navigation, alarms, dashboards, and a visualizer. The GH Pages fallback works continuously.

The loss stings but the technology is solid. Next time, the link stays up.
