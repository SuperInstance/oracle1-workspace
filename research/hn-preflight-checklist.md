# HN Pre-Flight Checklist

**Private. Casey runs this. I verify every line.**

---

## T-24h: Infrastructure Freeze

- [ ] No DNS changes — Cloudflare records must be untouched for 24h prior
- [ ] No nginx config changes — no new server blocks, locations, or certs
- [ ] No certbot runs — SSL certs must be valid with >30 days remaining
- [ ] No new service deployments — no systemd restarts, no new containers
- [ ] No Cloudflare proxy toggling — must be stable for 24h

## T-1h: External Verification

From a machine OUTSIDE the Oracle Cloud network:

- [ ] `curl -sI https://fleet.cocapn.ai/` returns 200
- [ ] `curl -sI https://superinstance.github.io/vessel-room-navigator/` returns 200
- [ ] First load completes in <3 seconds from cold cache
- [ ] Textures load: `curl -sI https://fleet.cocapn.ai/textures/pano_wheelhouse.jpg` returns 200
- [ ] All images load: `for t in wheelhouse galley foredeck aft_cockpit engine_room wheelhouse_roof crows_nest; do curl -sI .../$t.jpg; done`
- [ ] Three.js CDN loads from unpkg/jsdelivr
- [ ] Page renders in browser — drag to look around works
- [ ] Warp keys 2-9 work (test at least 3 rooms)
- [ ] Side panel opens
- [ ] Mobile responsive viewport works
- [ ] iOS Safari loads without errors
- [ ] Textures serve with `Cache-Control: public, immutable` headers

## T-30m: Content Check

- [ ] HN post title starts with "Show HN:" (if demo) or just describes what it IS
- [ ] No marketing language in the title — no "amazing," "revolutionary," "proves"
- [ ] URL links directly to the working demo
- [ ] URL is NOT localhost, NOT an IP address, NOT our server's raw IP
- [ ] URL is `https://superinstance.github.io/vessel-room-navigator/` (GH Pages)
- [ ] GitHub Pages URL has been verified externally
- [ ] fleet.cocapn.ai is a secondary mention, not the primary link
- [ ] Post body (if any) describes what it does, not what it proves
- [ ] No Cloudflare IPs in the URL path

## T-5m: Last Look

- [ ] Read the post title aloud. Does it sound like marketing?
- [ ] Click the link. Does it load?
- [ ] Is there a visible demo immediately, or do I need to scroll?
- [ ] What would a skeptic say in the first comment?

## Post-Submission

- [ ] Monitor the page for the first 15 minutes
- [ ] If first comments mention broken links, post the fallback URL immediately
- [ ] If 523 or 5xx errors appear, post the GH Pages URL as a reply
- [ ] Do NOT touch DNS, nginx, or Cloudflare for the next 4 hours

---

## The One Rule

**The last change before posting must be at least 24 hours old.** If you changed anything — DNS, nginx, code, certs — wait 24 hours from that change before submitting. The only exception is a trivial README edit that doesn't affect the deployed site.

---

*Filed 2026-05-13 after the 523 incident.*
