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

## Current — Build 5: Guides hub, 12 guides and glossary (done)
- **12 guides** in `src/pages/blog/` (1,368–1,786 words, FK 4.6–8.3), one per approved blog-map keyword, each tied to a money page. Briefs (Semrush top-10 SERPs pulled 2026-11-19, competitor estimates, money page, word counts) in `docs/guide-briefs.md`.
  - First Steps: what to do after a house fire (with checklist table).
  - Smoke & Odor: smoke smell out of a house; smoke smell out of clothes; hydroxyl generator vs. ozone vs. thermal fogging; what is considered smoke damage.
  - Soot & Cleaning: what is soot; how to clean soot off walls.
  - Insurance & Claims: homeowners insurance and fire; renters insurance and fire; dealing with the adjuster.
  - Restoration Basics: the restoration process; what drives restoration cost (factors only, no prices).
- **Every guide has:** keyword in title, meta, H1, short answer, an H2 and slug; "Short answer" box; money-page link in the first 150 words; tables and steps; mid-article CTA; prevention section; "Local note" with 3–5 state links; "Related reading"; closing "When should you call…" section; 4–5 FAQs (FAQPage); 3–6 opened primary sources; author box; 2 related cards; BlogPosting schema with citations.
- **New sources opened this build:** NAIC homeowners and renters consumer pages, Maryland Insurance Administration renters page, United Policyholders (partial-loss fire tips, contents tips), EPA PM basics, EPA ash and wildfire IAQ pages, National Cancer Institute soot page, Red Cross cleaning page (re-read for exact figures).
- **Featured images:** 12 branded 1200×630 graphics (WebP + JPG, 20–25 KB WebP) from `scripts/make_post_images.py`.
- **Guides hub** (`/blog/`) grouped by category; **glossary** (`/glossary/`) with 55 fire terms and DefinedTermSet schema; glossary terms auto-link (max 4 per page) on service, state and guide pages.
- **Internal links:** "Helpful guides" now shows on all 8 service pages and 51 state pages; sidebar "Popular guides" on every page; home page links the process, cost and first-steps guides; each guide links 3–6 other guides.
- **Checks:** audit PASS 0 issues (84 pages); reading grade ≤ 9, no repeated paragraphs; site audit clean; no overflow or console errors at 360/768/1280.

## Coming
| Build | Scope | Needs from owner |
| --- | --- | --- |
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
python3 scripts/make_post_images.py      # after adding or retitling a guide
python3 build.py                 # writes public/
python3 scripts/audit.py         # must print "PASS: 0 issues"
python3 scripts/readability.py   # reading grade <= 9, no repeated paragraphs
python3 scripts/siteaudit.py     # whole-site link, title, canonical, sitemap check
python3 scripts/make_logo.py src/static/img/brand && python3 scripts/make_brand_png.py   # after a logo change
```
