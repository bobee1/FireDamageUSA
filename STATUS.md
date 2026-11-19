# SootMend — Build Status

Nationwide fire, smoke and soot damage restoration site. Brand **SootMend**, domain **sootmend.us** (no DNS records on 2026-11-19, so very likely unregistered; not yet purchased).
Plan: "Nationwide Fire Damage Local Services Site — Build Plan" (Claude doc). Rules: "Local Service Site SEO Criteria & AI Prompt" and "Blog Post Criteria & SEO Writing Prompt".
Full step log: [docs/RECORD-REGISTER.md](docs/RECORD-REGISTER.md).

Last updated: 2026-11-19

## Previous
- Plan written and approved (2026-11-16): one national brand, Home → State → City structure, wave rollout, Cloudflare hosting.
- Owner decisions (2026-11-19): brand SootMend; domain sootmend.us; own-business call routing; 24/7; 10+ years in business; legal owner Anjam Javed; toll-free 1-800-555-0199 (kept until after deployment); ANSI/IICRC S700 confirmed; repo github.com/bobee1/FireDamageUSA.
- Build 1 — Foundation, trust and legal pages (done): generator `build.py` (forked from the DryFlare engine), "Soot + Ember" design system, logo set and icons, 9 Pexels photos as WebP (2 used, 7 held), About (with "how a call works" illustration), Contact (form → Pages Function → Resend), Privacy, Terms, Disclaimer, Editorial Policy, Accessibility, 404; `_headers`, `_redirects`, manifest; audit 0 issues; FK 6.0–6.4; responsive clean at 360/768/1280/1440.

## Current — Build 2: Keyword research and site plan (done, waiting for approval)
- **Plan doc:** "SootMend Site Plan — Build 2 Keyword Research" (Claude doc): https://claude.ai/artifact/5DcSVz4eh8dK1rEX8g8TCo
- **Semrush (US, 19 Nov 2026, ~5,400 units; 33,760 left):** 60 service terms, 100 city terms, 20 state terms, 30 guide terms, question keywords for 4 seeds, top-10 SERPs for 4 keywords. Raw data in `research/01`–`05`.
- **Keyword map:** home = "fire damage restoration" (110,000/mo, KD 33) + near me, fire restoration, fire restoration company. 8 service pages: fire damage repair (9,900), fire damage cleanup (8,100), smoke damage restoration (9,900), smoke odor removal (6,600), soot removal (1,000), board-up and roof tarping (fire board up 1,900), contents cleaning and pack-out (590), commercial fire damage restoration (4,400).
- **Locations:** state names are barely searched (top: Arizona 480/mo), so state pages are hubs. 62 of 100 cities get ≥110 searches/mo; Wave 1 = top 50 (14,830 searches/mo combined; Denver 720 leads).
- **Blog map:** 12 guides (~29,800 searches/mo across primary + secondary terms), e.g. how to get smoke smell out of a house (4,400), does renters insurance cover fire damage (2,900), smoke smell out of clothes (2,400), what is soot (4,400).
- **Competitors:** national SERP held by BELFOR, SERVPRO, ServiceMaster, ATI, a Home Depot guide and Yelp; "smoke odor removal" is a shopping/DIY SERP. Gaps: soot types, standards, lead/asbestos testing, state insurance and licensing, wildfire and heating-season local detail.
- **Waiting on owner:** approve the plan; decide whether SootMend covers Nashville (default: skip, since Nashville Fire Removal Pros targets it; Washington, DC takes slot 50).

## Coming
| Build | Scope | Needs from owner |
| --- | --- | --- |
| 3 | Home page (1,200–1,800 words), services hub, 8 service pages per the approved keyword map (repair, cleanup, smoke damage, smoke odor, soot, board-up and tarping, contents, commercial), with competitor term coverage, FAQ, Service and business schema, sources, illustrations and photos. | Plan approval (Build 2) |
| 4 | Locations hub + state pages (Census housing data, USFA fire data, state insurance and contractor licensing notes). | — |
| 5 | Guides hub + 12 guides from the blog map + glossary (50+ terms) with auto-links + branded featured images. | — |
| 6 | Wave 1: top 50 city pages from the approved list, in batches of 25. | Nashville decision |
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
