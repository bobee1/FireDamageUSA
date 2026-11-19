# SootMend — Build Status

Nationwide fire, smoke and soot damage restoration site. Brand **SootMend**, domain **sootmend.us** (no DNS records on 2026-11-19, so very likely unregistered; not yet purchased).
Plan: "Nationwide Fire Damage Local Services Site — Build Plan" (Claude doc). Rules: "Local Service Site SEO Criteria & AI Prompt" and "Blog Post Criteria & SEO Writing Prompt".
Full step log: [docs/RECORD-REGISTER.md](docs/RECORD-REGISTER.md).

Last updated: 2026-11-19

## Previous
- Plan written and approved (2026-11-16): one national brand, Home → State → City structure, wave rollout, Cloudflare hosting.
- Owner decisions (2026-11-19): brand SootMend (picked by Claude, approved by owner via repo name); domain sootmend.us; own-business call routing; 24/7; 10+ years in business; legal owner Anjam Javed; toll-free 1-800-555-0199; repo github.com/bobee1/FireDamageUSA.

## Current — Build 1: Foundation, trust and legal pages (done)
- **Generator:** `build.py` (static site generator forked from the DryFlare engine; locations and guides modules plug in later). JSON front matter + HTML body per page, shared layout, JSON-LD graph (Organization with publishingPrinciples, WebSite, WebPage, BreadcrumbList), sitemap and robots on build.
- **Design system:** "Soot + Ember" palette, set apart from DryFlare (graphite + orange) and the owner's navy/amber city sites. Soot #211c1b, ember #c42b20 (white text 5.65:1), accent text #b3261e (6.54:1), clean green #2f6b5a for checks. Dark hero band, squarer buttons, red numbered steps. All text pairs ≥ 4.5:1.
- **Brand:** logo (house + ember flame + "mended" sparkle, Inter Display ExtraBold wordmark outlined), reversed logo, mark, app icons, favicon, 1200×630 social image. Built by `scripts/make_logo.py` and `scripts/make_brand_png.py`.
- **Pages (8):** About (with a "how a call works" illustration, horizontal on desktop and vertical on phones), Contact (call + form → Pages Function → Resend), Privacy Policy, Terms of Service, Disclaimer, Editorial Policy, Accessibility, 404. Legal pages name Anjam Javed, carry a unique "Document:" line, the effective date, and fire-specific terms (board-up authorizations, release by fire officials, lead/asbestos testing, insurance records).
- **Images:** 9 Pexels photos converted to WebP (1200 px + 800 px, all under 180 KB), library in `src/photos.json`. 2 used now (About, Contact); 7 held for later builds so no photo repeats.
- **Technical:** `_headers` (CSP, HSTS, noindex on *.pages.dev), `_redirects`, web manifest, `functions/api/lead.js`, mobile call bar, sticky header call button, skip link, breadcrumbs.
- **Checks:** `scripts/audit.py` PASS 0 issues (home `/` is the only pending link target); readability FK 6.0–6.4 on About/Contact (legal pages exempt, 6.4–8.7); no repeated paragraphs; no overflow at 360/768/1280/1440 px; no console errors; mobile menu works.

## Coming
| Build | Scope | Needs from owner |
| --- | --- | --- |
| 2 | Semrush keyword research: service keywords, top city demand (state + city), question keywords for guides, top-10 SERP and competitor benchmark. Site plan doc (sitemap, keyword map, clusters, blog map) for approval. | Approve the plan |
| 3 | Home page (1,200–1,800 words), services hub, 7–8 service pages (fire damage restoration, smoke damage restoration, soot removal, smoke odor removal, board-up and roof tarping, contents pack-out and cleaning, commercial fire damage, possibly wildfire smoke damage), with FAQ, Service and business schema, sources, illustrations. | — |
| 4 | Locations hub + state pages (Census housing data, USFA fire data, state insurance and contractor licensing notes). | — |
| 5 | Guides hub + first 10 guides (what to do after a house fire, smoke damage cleanup, insurance and fire claims, soot removal, smoke smell, etc.) + glossary with auto-links + branded featured images. | — |
| 6 | City scoring (searches × CPC) + first 50 Tier 1 metro pages. | — |
| 7+ | City pages in batches of 25 (Tier 2, then Tier 3 once Wave 1 is indexed). | — |
| Launch | Buy sootmend.us, Cloudflare Pages project, real toll-free number, email, Resend keys, Search Console + analytics. | Domain, number, email, Resend key |

## Open items
- **Phone number:** 1-800-555-0199 is in the 555-01xx range reserved for fiction and cannot receive calls. Replace `phone_display` / `phone_e164` in `src/site.json` before launch.
- **Domain:** buy sootmend.us soon (sootmend.com and sootmend.net also had no DNS records on 2026-11-19).
- **Email:** add to `src/site.json` once the domain is bought.
- **Resend env vars** for the contact form: `RESEND_API_KEY`, `LEAD_TO_EMAIL`, `LEAD_FROM_EMAIL`.
- **Process claims to confirm:** About page says crews follow ANSI/IICRC S700 cleaning steps and test suspect materials in older homes. Confirm these match how your crews work.

## Deployment
- Cloudflare Pages (to be created by owner): connect `bobee1/FireDamageUSA`, branch `main`, framework preset None, no build command, build output directory `public`. `functions/` is picked up automatically for the contact form.
- Staging address `*.pages.dev` sends `X-Robots-Tag: noindex` (set in `_headers`) until sootmend.us is connected.

## How to build
```
python3 build.py                 # writes public/
python3 scripts/audit.py         # must print "PASS: 0 issues"
python3 scripts/readability.py   # reading grade <= 9, no repeated paragraphs
python3 scripts/siteaudit.py     # whole-site link, title, canonical, sitemap check
python3 scripts/make_logo.py src/static/img/brand && python3 scripts/make_brand_png.py   # after a logo change
```
