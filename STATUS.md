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
- Build 4 — Locations hub, 50 state pages and DC (done): `states.py` + hand-written copy per state; ACS heating fuel, OpenFEMA fire declarations and USFA 2023 fire deaths in `research/07`–`09`; heating bar chart; 1,053–1,182 words per state.
- Build 5 — Guides hub, 12 guides and glossary (done): 12 guides (1,368–1,786 words) with branded images, 55-term glossary with auto-links, briefs in `docs/guide-briefs.md`.

## Current — Build 6: Wave 1 city pages, batch 1 of 2 (done)
- **25 city pages** at `/locations/<state>/<city>/` (1,054–1,243 words each): Denver, San Diego, Dallas, Los Angeles, Houston, Colorado Springs, Charlotte, Columbus, Atlanta, Austin, Chicago, Jacksonville, Tampa, Sacramento, Plano, Arlington, Raleigh, San Antonio, Minneapolis, Kansas City (MO), Mesa, Cincinnati, Seattle, Phoenix and Salt Lake City — Wave 1 ranks 1–25 by Semrush demand.
- **Generator:** `metros.py` builds each page from data plus hand-written copy in `src/metros/content/<slug>.json` (source: `scripts/metro_content/batch1.py` → `gen.py`). A city goes live only when its content file exists, so batch 2 just adds files.
- **Each city page has:** quick answer with county and ZIPs; a facts table (population, housing age, owner share, main heating fuel, county FEMA fire declarations since 2000 and the latest one); a housing paragraph; local "why it's different" copy naming real neighborhoods and past fires; a heating bar chart and paragraph; a problems → service table; tips; neighborhoods served with links to nearby city pages; insurance, permit and contractor-board notes linking the state page; 4 FAQs; services grid; nearby links; helpful guides; 6–8 sources; Service schema with `areaServed` and `containedInPlace`.
- **New data (pulled 2026-11-19):** `research/10-city-heating-fuel.json` (ACS 2024 5-year B25040 for all 50 Wave 1 cities), `research/11-county-fire-declarations.json` (OpenFEMA fire declarations by county), `research/12-city-acs.json` (housing data, reused from the sister project). `src/metros/meta.json` holds all 50 Wave 1 cities (batch 1 and 2), with Kansas City, MO and Portland, OR chosen for the ambiguous names.
- **Links:** state pages list their city pages; the locations hub has a "City pages" list; the home page links eight major cities; nearby cities link both ways.
- **Checks:** audit PASS 0 issues (109 pages); reading grade ≤ 9 and no repeated paragraphs; site audit clean (every city has 3+ inbound links); no overflow or console errors at 360/768/1280.

## Coming
| Build | Scope | Needs from owner |
| --- | --- | --- |
| 6b | Wave 1 batch 2: cities 26–50 (Baton Rouge, New York, Fort Worth, Nashville, Durham, Orlando, Philadelphia, Las Vegas, Indianapolis, Portland, Omaha, Louisville, Cleveland, Aurora, Tucson, Boise, Madison, Reno, Miami, Wichita, Baltimore, Memphis, Pittsburgh, Long Beach, Gilbert). | — |
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
python3 scripts/metro_content/gen.py   # after editing city copy
python3 scripts/make_post_images.py      # after adding or retitling a guide
python3 build.py                 # writes public/
python3 scripts/audit.py         # must print "PASS: 0 issues"
python3 scripts/readability.py   # reading grade <= 9, no repeated paragraphs
python3 scripts/siteaudit.py     # whole-site link, title, canonical, sitemap check
python3 scripts/make_logo.py src/static/img/brand && python3 scripts/make_brand_png.py   # after a logo change
```
