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

## Current — Build 3: Home, services hub and 8 service pages (done)
- **Home** (`/`, 1,498 words): "fire damage restoration" focus, services grid, how a call works, "what a house fire leaves behind" illustration (desktop + mobile versions), process, where we work, cost factors, signs, first steps, 7 FAQs, 6 sources.
- **Services hub** (`/services/`): CollectionPage, scenario → service table, "what to ask a fire damage restoration company" checklist.
- **8 service pages** (1,103–1,304 words each), one per keyword in the approved map: fire damage cleanup, smoke damage restoration, soot removal, smoke odor removal, board-up and roof tarping, contents cleaning and pack-out, fire damage repair, commercial fire damage restoration. Each has a 40–60 word quick answer, checklist, comparison table, steps, competitor-gap sections (soot types, dry chemical sponges, HEPA, thermal fogging, hydroxyl, EPA ozone cautions, puff-backs, wildfire ash, lead RRP and asbestos testing, permits, ALE, business interruption), cost factors without prices, DIY vs pro, insurance notes, 5–6 FAQs (FAQPage schema), Service schema, Wikipedia entities, 4–6 primary sources and 3 related-service links.
- **Photos:** 10 Pexels photos as WebP (800 + 1200 px), each used once; alt text in `src/photos.json`.
- **Guide and "near you" blocks** are written into each page and appear automatically once Builds 4 and 5 add the locations and blog modules.
- **Build fix:** tables now sit in a scroll box on phones (no page overflow at 360 px).
- **Checks:** audit PASS 0 issues; reading grade 5.9–8.9; site audit clean; no horizontal overflow at 360/768/1280.

## Coming
| Build | Scope | Needs from owner |
| --- | --- | --- |
| 4 | Locations hub + 50 state pages + DC (Census housing data, USFA fire data, state insurance and contractor licensing notes). | — |
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
python3 build.py                 # writes public/
python3 scripts/audit.py         # must print "PASS: 0 issues"
python3 scripts/readability.py   # reading grade <= 9, no repeated paragraphs
python3 scripts/siteaudit.py     # whole-site link, title, canonical, sitemap check
python3 scripts/make_logo.py src/static/img/brand && python3 scripts/make_brand_png.py   # after a logo change
```
