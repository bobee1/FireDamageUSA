# SootMend — Record Register

A dated log of every step. Newest entries at the bottom. Status: Done / In progress / Planned.

| # | Date | Build | Step | Status | Notes |
| --- | --- | --- | --- | --- | --- |
| 1 | 2026-11-16 | Plan | Nationwide fire damage build plan written | Done | Claude doc "Nationwide Fire Damage Local Services Site — Build Plan"; Semrush: 13 core terms ≈ 251,300 searches/mo |
| 2 | 2026-11-19 | 1 | Read site criteria and blog criteria docs | Done | Rules applied to every page |
| 3 | 2026-11-19 | 1 | Brand names checked with DNS (Cloudflare DoH) | Done | No records: sootmend.us/.com/.net, ashtohome, cindercall, sootlift, emberrestore, sootswift; firemend.com taken |
| 4 | 2026-11-19 | 1 | Brand chosen: SootMend, domain sootmend.us | Done | Short, fire-specific, unused name; .us per owner |
| 5 | 2026-11-19 | 1 | Owner decisions recorded | Done | Own-business routing; 24/7; 10+ years; owner Anjam Javed; toll-free 1-800-555-0199 |
| 6 | 2026-11-19 | 1 | GitHub repo connected | Done | github.com/bobee1/FireDamageUSA (was empty) |
| 7 | 2026-11-19 | 1 | Generator forked from DryFlare engine and adapted | Done | `build.py`; modules for locations/guides optional until later builds |
| 8 | 2026-11-19 | 1 | Design system "Soot + Ember" | Done | Soot #211c1b, ember #c42b20, accent #b3261e, clean #2f6b5a; contrast checked |
| 9 | 2026-11-19 | 1 | Logo, app icons, favicon, social image | Done | `scripts/make_logo.py`, `scripts/make_brand_png.py` |
| 10 | 2026-11-19 | 1 | Pexels photos downloaded, cropped 3:2, converted to WebP | Done | IDs 10252682, 10252687, 12736402, 16931595, 16931859, 19832605, 25490577, 27639887, 4127692; 1200 + 800 px; all < 180 KB |
| 11 | 2026-11-19 | 1 | Sources checked for safety steps | Done | American Red Cross (stay out until fire officials clear the home), USFA "After the Fire" (report number, insurer), EPA (24–48 h drying) |
| 12 | 2026-11-19 | 1 | Trust and legal pages written | Done | About, Contact, Privacy, Terms, Disclaimer, Editorial policy, Accessibility, 404 |
| 13 | 2026-11-19 | 1 | "How a call works" SVG illustration | Done | Horizontal on desktop, vertical on phones |
| 14 | 2026-11-19 | 1 | Contact form endpoint | Done | `functions/api/lead.js` (Resend; needs env vars) |
| 15 | 2026-11-19 | 1 | Audit fixes | Done | Audit now ignores inline SVG `<title>`; 3 meta descriptions shortened |
| 16 | 2026-11-19 | 1 | Audit + readability + site audit | Done | 0 issues; FK 6.0–6.4 (legal exempt); home `/` pending (Build 3) |
| 17 | 2026-11-19 | 1 | Responsive check 360/768/1280/1440 | Done | No overflow, no console errors, menu works |
| 18 | 2026-11-19 | 1 | STATUS.md + record register written; committed and pushed | Done | Branch `main` |
| 19 | 2026-11-19 | 2 | Owner confirmed ANSI/IICRC S700 claim; phone kept until after deployment; owner hosts after Build 2 push | Done | |
| 20 | 2026-11-19 | 2 | Semrush: 60 service keywords (volume, CPC, KD, intent) | Done | `research/01-service-keywords.csv` (600 units) |
| 21 | 2026-11-19 | 2 | Semrush: 100 city terms + 20 state terms | Done | `research/02-city-demand.csv`, `03-state-terms.csv`; 62 cities ≥110/mo; states mostly 0–480 |
| 22 | 2026-11-19 | 2 | Semrush: question keywords (fire damage, smoke damage, house fire, soot) + 30 guide terms | Done | `research/04-guide-keywords.csv` |
| 23 | 2026-11-19 | 2 | Semrush top-10 SERPs: fire damage restoration, smoke damage restoration, smoke odor removal, fire damage restoration denver | Done | `research/05-competitors.csv` |
| 24 | 2026-11-19 | 2 | Competitor pages read: SERVPRO (~4,500–5,000 words), PuroClean (~3,500 unique), BELFOR | Done | Term list for service pages (soot types, S700, HEPA, fogging, hydroxyl, ozone, lead/asbestos, ALE) |
| 25 | 2026-11-19 | 2 | Site plan doc written for owner approval | Done | https://claude.ai/artifact/5DcSVz4eh8dK1rEX8g8TCo |
| 26 | 2026-11-19 | 2 | STATUS.md and register updated; committed and pushed | Done | Branch `main` |
| 27 | — | 3 | Home, services hub, 8 service pages | Planned | Starts after plan approval |
