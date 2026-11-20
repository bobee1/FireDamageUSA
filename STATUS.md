# SootMend — Build Status

Nationwide fire, smoke and soot damage restoration site. Brand **SootMend**, domain **sootmend.us** (no DNS records on 2026-11-19, so very likely unregistered; not yet purchased).
Plan: "Nationwide Fire Damage Local Services Site — Build Plan" (Claude doc). Rules: "Local Service Site SEO Criteria & AI Prompt" and "Blog Post Criteria & SEO Writing Prompt".
Full step log: [docs/RECORD-REGISTER.md](docs/RECORD-REGISTER.md).

Last updated: 2026-11-19

## Previous
- Plan written and approved (2026-11-16): one national brand, Home → State → City structure, wave rollout, Cloudflare hosting.
- Owner decisions (2026-11-19): brand SootMend; domain sootmend.us; own-business call routing; 24/7; 10+ years in business; legal owner Anjam Javed; toll-free 1-800-555-0199 (kept until after deployment); ANSI/IICRC S700 confirmed; repo github.com/bobee1/FireDamageUSA.
- Build 1 — Foundation, trust and legal pages (done): generator `build.py` (forked from the DryFlare engine), "Soot + Ember" design system, logo set and icons, 9 Pexels photos as WebP (2 used, 7 held), About (with "how a call works" illustration), Contact (form → Pages Function → Resend), Privacy, Terms, Disclaimer, Editorial Policy, Accessibility, 404; `_headers`, `_redirects`, manifest; audit 0 issues; FK 6.0–6.4; responsive clean at 360/768/1280/1440.
- Build 2 — Keyword research and site plan (done, approved 2026-11-19): plan doc https://claude.ai/artifact/5DcSVz4eh8dK1rEX8g8TCo; Semrush data in `research/01`–`05`; keyword map for home + 8 services, Wave 1 = top 50 cities (Nashville included), 12-guide blog map.
- Build 2b — Logo set and design system (done): design system artifact https://claude.ai/artifact/Y1stA843hy3x3heukjyA8n with tokens, brand book, 9 logo versions and 14 components; site CSS reads the new tokens.
- Build 3 — Home, services hub and 8 service pages (done): home (1,498 words), services hub, 8 service pages (1,103–1,304 words) per the keyword map; 10 Pexels photos; tables scroll on phones; audit 0 issues, FK 5.9–8.9.

## Current — Build 4: Locations hub, 50 state pages and DC (done)
- **Locations hub** (`/locations/`, 821 words): CollectionPage, state cards grouped by Census region, a national patterns table (most FEMA wildfire aid, highest USFA fire death risk, most oil heat, most wood heat), what each state page covers, 3 FAQs, Pexels photo 942560.
- **51 state pages** (`/locations/<state>/`, 1,053–1,182 words each), built by `states.py` from data plus hand-written copy in `src/states/content/<AB>.json` (source: `scripts/state_content/batch*.py` → `gen.py`). Each page has a quick answer, a "fire risk at a glance" facts table, a fire-death risk paragraph, local "why it's different" copy, a heating-fuel bar chart (HTML, reflows on phones), a heating paragraph, a problems → service table, state safety tips, insurance regulator and contractor board links, areas served, 4 FAQs, services grid, neighboring-state links and 5–8 sources. Service schema with `areaServed`.
- **New data** (pulled 2026-11-19 through the browser):
  - `research/07-heating-fuel.json` — Census ACS 2024 B25040 house heating fuel, all states + DC.
  - `research/08-fema-fire.json` — OpenFEMA fire declarations since 2000 (major, emergency, fire management assistance) and the latest one per state.
  - `research/09-usfa-fire-deaths.json` — USFA 2023 fire deaths, rate and relative risk.
  - Reused from the sister project: `research/06-state-data.json` (ACS housing, largest places) and `src/states/meta.json` (slugs, neighbors, insurance regulator, contractor board).
- **Site-wide:** "Locations" now shows in the nav and footer; every service page gained a "<service> near you" block linking all 51 state pages.
- **Waiting on later builds:** each state page has a "Helpful guides" block (shows after Build 5) and will list its cities after Build 6.
- **Checks:** audit PASS 0 issues; reading grade ≤ 9 on every page, no repeated paragraphs; site audit clean (70 pages); no horizontal overflow at 360/768/1280.

## Coming
| Build | Scope | Needs from owner |
| --- | --- | --- |
| 5 | Guides hub + 12 guides from the blog map + glossary (50+ terms) with auto-links + branded featured images. | — |
| 6 | Wave 1: top 50 city pages from the approved list (Nashville included), in batches of 25. | — |
| 7+ | Cities 51–62, then suburbs scored from a second Semrush pull, 25 at a time, once 70%+ of Wave 1 is indexed. | Search Console access |
| Launch | Buy sootmend.us, Cloudflare Pages project, real toll-free number, email, Resend keys, Search Console + analytics. | Domain, number, email, Resend key |

## Open items
- **Phone number:** 1-800-555-0199 is in the 555-01xx range reserved for fiction and cannot receive calls. Owner will swap it after deployment: change `phone_display` / `phone_e164` in `src/site.json`, rebuild and push.
- **Domain:** buy sootmend.us soon (sootmend.com and sootmend.net also had no DNS records on 2026-11-19).
- **Email:** add to `src/site.json` once the domain is bought.
- **Resend env vars** for the contact form: `RESEND_API_KEY`, `LEAD_TO_EMAIL`, `LEAD_FROM_EMAIL`.

## Deployment
- Cloudflare Pages (owner sets this up after the Build 2 push): connect `bobee1/FireDamageUSA`, branch `main`, framework preset None, no build command, build output directory `public`. `functions/` is picked up automatically for the contact form.
- Staging address `*.pages.dev` sends `X-Robots-Tag: noindex` (set in `_headers`) until sootmend.us is connected.

## How to build
```
python3 scripts/state_content/gen.py   # after editing state copy
python3 build.py                 # writes public/
python3 scripts/audit.py         # must print "PASS: 0 issues"
python3 scripts/readability.py   # reading grade <= 9, no repeated paragraphs
python3 scripts/siteaudit.py     # whole-site link, title, canonical, sitemap check
python3 scripts/make_logo.py src/static/img/brand && python3 scripts/make_brand_png.py   # after a logo change
```
