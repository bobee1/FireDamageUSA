"""City pages for SootMend: /locations/<state>/<city>/ (Wave 1 = top 50 cities by search demand).

Inputs:
  research/12-city-acs.json                 Census ACS housing data for each city
  research/10-city-heating-fuel.json        Census ACS B25040 heating fuel for each city
  research/11-county-fire-declarations.json OpenFEMA fire declarations by county since 2000
  src/metros/meta.json                      city, state, county, ZIP codes, neighborhoods, nearby cities, Semrush figures
  src/metros/content/<slug>.json            hand-written copy: lead, risks, why, problems, tips, insurance note, FAQ
A page is built only when its content file exists, so cities go live batch by batch.
"""
import json
from pathlib import Path

import states as S

ROOT = Path(__file__).parent
ACS = json.loads((ROOT / "research" / "12-city-acs.json").read_text())["places"]
FUEL = json.loads((ROOT / "research" / "10-city-heating-fuel.json").read_text())["places"]
FEMA = json.loads((ROOT / "research" / "11-county-fire-declarations.json").read_text())["counties"]
MMETA = json.loads((ROOT / "src" / "metros" / "meta.json").read_text())
CDIR = ROOT / "src" / "metros" / "content"
TYPE = {"FM": "fire management assistance", "DR": "major disaster", "EM": "emergency"}


def live(slug):
    return (CDIR / f"{slug}.json").exists()


def mpath(slug):
    m = MMETA[slug]
    return f"/locations/{S.META[m['st']]['slug']}/{m['url']}/"


def mlink(slug, text=None):
    return f'<a href="{mpath(slug)}">{text or MMETA[slug]["city"]}</a>'


def metros_in_state(ab):
    return sorted([k for k, v in MMETA.items() if v["st"] == ab and live(k)], key=lambda k: MMETA[k]["city"])


def fuel(slug):
    return dict(zip(S.FUEL_LABELS, FUEL[MMETA[slug]["fuel"]][:7]))


def county_fire(slug):
    """Total fire declarations across the city's counties, and the latest one."""
    n, latest = 0, None
    for key in MMETA[slug]["fema"]:
        if key in FEMA:
            c, lt = FEMA[key]
            n += c
            if not latest or lt[0] > latest[0]:
                latest = lt
    return n, latest


def title_case(s):
    small = {"and", "of", "the"}
    return " ".join(w.capitalize() if i == 0 or w.lower() not in small else w.lower() for i, w in enumerate(s.lower().split()))


def glance(slug):
    m = MMETA[slug]
    pop, units, med, pre80, pre40, own, mobile = ACS[m["acs"]]
    f = fuel(slug)
    top = max(S.FUEL_LABELS[:6], key=lambda k: f[k])
    n, latest = county_fire(slug)
    rows = [("Population", S.fmt(pop)), ("Housing units", S.fmt(units)), ("Median year built", str(med)),
            ("Homes built before 1980", f"{pre80:g}%"), ("Homes built before 1940", f"{pre40:g}%"),
            ("Owner-occupied homes", f"{own:g}%"), ("Most common heating fuel", f"{top} ({f[top]:g}%)"),
            ("County", m["county"]),
            ("County fire declarations since 2000", str(n) if n else "None")]
    if latest:
        rows.append(("Latest county fire declaration", f"{title_case(latest[2])} ({S.month_year(latest[0])})"))
    rows.append(("Sample ZIP codes", ", ".join(m["zips"])))
    trs = "".join(f'<tr><th scope="row">{k}</th><td>{v}</td></tr>' for k, v in rows)
    return f'<div class="table-scroll"><table class="facts"><tbody>{trs}</tbody></table></div>'


def housing_line(slug):
    m = MMETA[slug]
    pop, units, med, pre80, pre40, own, mobile = ACS[m["acs"]]
    c = m["city"]
    if pre40 >= 25:
        s = S.pick(slug, [f"{pre40:g}% of homes in {c} were built before 1940. Plaster walls, balloon framing and old wiring change how fire and smoke spread, and how repairs are done.",
                          f"{c} has old housing: {pre40:g}% of homes predate 1940. Fire can climb inside balloon-framed walls, and plaster holds smoke odor."], "hl")
    elif pre80 >= 50:
        s = S.pick(slug, [f"About {pre80:g}% of {c} homes were built before 1980, so lead paint and older wiring often come up during fire repairs.",
                          f"More than half of {c}'s housing ({pre80:g}%) went up before 1980. Older wiring and paint that may contain lead shape how repairs are done."], "hl")
    else:
        s = S.pick(slug, [f"Housing in {c} is newer, with a median build year of {med}. Open floor plans and attached garages let smoke travel fast.",
                          f"With a median build year of {med}, most {c} homes are newer. Smoke spreads quickly through open layouts, ducts and attics."], "hl")
    if own < 45:
        s += f" Only {own:g}% of homes are owner-occupied, so many fire calls come from renters, landlords and property managers."
    return f"<p>{s}</p>"


def heating_line(slug):
    f = fuel(slug)
    c = MMETA[slug]["city"]
    if f["Electricity"] >= 55:
        s = f"Electricity heats {f['Electricity']:g}% of {c} homes, so space heaters, cords and outlets drive most winter fire calls."
    elif f["Utility gas"] >= 55:
        s = f"Natural gas heats {f['Utility gas']:g}% of {c} homes. Furnaces, boilers and water heaters need yearly service, and storage should stay clear of them."
    else:
        s = f"{c} homes split between gas ({f['Utility gas']:g}%) and electric heat ({f['Electricity']:g}%)."
    if f["Fuel oil or kerosene"] >= 2.5:
        s += f" About {f['Fuel oil or kerosene']:g}% still burn fuel oil, which brings a risk of oily <a href=\"/services/soot-removal/\">puff-back soot</a>."
    if f["No heating fuel"] >= 4:
        s += f" In the mild climate, {f['No heating fuel']:g}% of homes use no heating fuel at all."
    return f"<p>{s}</p>"


def fuel_chart(slug):
    f = fuel(slug)
    c = MMETA[slug]["city"]
    rows = sorted(((k, v) for k, v in f.items() if v >= 0.5 and k != "Coal"), key=lambda kv: -kv[1])
    bars = "".join(f'<li><span class="bar-label">{k}</span><span class="bar-track"><span class="bar-fill" style="width:{max(v, 1):g}%"></span></span>'
                   f'<span class="bar-val">{v:g}%</span></li>' for k, v in rows)
    return (f'<figure class="bars" aria-label="How homes in {c} are heated"><figcaption><strong>How homes in {c} are heated</strong> '
            f'(share of occupied homes, Census ACS 2020–2024)</figcaption><ul>{bars}</ul></figure>')


def page(slug):
    if not live(slug):
        return None
    c = json.loads((CDIR / f"{slug}.json").read_text())
    m = MMETA[slug]
    st = S.META[m["st"]]
    city, ab = m["city"], m["st"]
    disp = f"{city}, {ab}"
    sp = S.state_path(ab)
    title = f"Fire Damage Restoration {city}, {ab} | SootMend"
    if len(title) > 60:
        title = f"Fire Damage Restoration {city} | SootMend"
    desc = f"Fire damage restoration in {disp}: {c['risk_short']}. Board-up, soot, smoke odor and repairs. Call 1-800-555-0199."
    if len(desc) > 155:
        desc = f"Fire damage restoration in {disp}: {c['risk_short']}. Call SootMend at 1-800-555-0199."
    if len(desc) > 155:
        desc = f"Fire damage restoration in {disp}: {c['risk_short']}. Call 1-800-555-0199."
    near = [n for n in m["nearby"] if live(n)]
    back = sorted(k for k, v in MMETA.items() if slug in v["nearby"] and k not in near and live(k))
    near = (near + back)[:5]
    nb = S.pick(slug, [f"SootMend also covers nearby {S.join_list([mlink(n) for n in near])}.",
                       f"Crews also work in {S.join_list([mlink(n) for n in near])}.",
                       f"Fire damage help is also available in {S.join_list([mlink(n) for n in near])}."], "nb") if near else ""
    quick = S.pick(slug, [f"Fire damage restoration in {disp} covers board-up, soot and smoke cleanup, odor removal, contents cleaning and repairs.",
                          f"In {city}, fire damage restoration means securing the property, cleaning soot and smoke, removing odor and rebuilding.",
                          f"Fire damage restoration in {city} starts with board-up and water removal, then soot cleanup, deodorizing and repairs."], "q")
    quick += f" The main local risks are {c['risk']}. SootMend covers all of {m['county']}, including ZIP codes {', '.join(m['zips'][:3])}."
    doi, doiu = st["doi"]
    ins = S.pick(slug, [f'Home insurance in {city} is regulated by the <a href="{doiu}">{doi}</a>, which takes complaints if a claim stalls. ',
                        f'The <a href="{doiu}">{doi}</a> oversees insurance for {city} homeowners and renters. '], "i")
    ins += c.get("insurance", "")
    if st.get("contractor"):
        ins += f' Check repair contractors with the <a href="{st["contractor"][1]}">{st["contractor"][0]}</a>, and expect city building permits for structural, roofing and electrical work.'
    else:
        ins += f" {st['name']} has no statewide general contractor license, so {city}'s building department sets permit and contractor rules for repairs."
    ins += f" The {S.short(ab)} page has more on state insurance and licensing: see <a href=\"{sp}\">fire damage restoration in {S.short(ab)}</a>."
    cta1 = S.pick(slug, [f"Fire or smoke damage in {city}? Call SootMend {{{{availability}}}}.",
                         f"Need help after a fire in {city}? Call SootMend at {{{{phone}}}}."], "c1")
    tips_h = S.pick(slug, [f"Fire safety tips for {city} homes", f"Tips for {city} homeowners and renters", f"How {city} owners can limit fire damage"], "t")
    n_fire, _ = county_fire(slug)
    faq = [
        {"q": f"Do you cover all of {city}?",
         "a": f"Yes. SootMend takes fire and smoke damage calls from across {city} and {m['county']}, including {S.join_list(m['hoods'][:5])}, and ZIP codes such as {', '.join(m['zips'][:4])}."},
        {"q": f"How fast should cleanup start after a fire in {city}?",
         "a": S.pick(slug, [f"Start as soon as the fire department lets you back in. The EPA says wet materials should dry within 24 to 48 hours to stop mold. Soot is acidic, so it keeps harming metal, glass and stone in a {city} home.",
                            f"Within a day or two. The EPA says to dry wet materials within 24 to 48 hours to prevent mold. Soot left on surfaces in {city} homes keeps staining and eating into them."], "fq")},
        {"q": f"Does insurance cover fire damage in {city}?",
         "a": S.pick(slug, [f"Usually. Home and renters policies for {city} homes cover sudden fire and smoke damage, wildfire included, up to your limits. Report the loss fast and ask about living expenses. For claim problems, contact the {doi}.",
                            f"In most cases, yes. A standard {city} home or renters policy pays for sudden fire and smoke damage up to its limits. Ask early about living expenses, and contact the {doi} if a claim stalls."], "ins")},
        c["faq"],
    ]
    body = f"""<p class="quick"><strong>Quick answer:</strong> {quick}</p>

<h2>{city} fire risk at a glance</h2>
{glance(slug)}
<p class="small-note">{city} figures: Census ACS 2020–2024 5-year estimates (housing and heating fuel) and OpenFEMA fire declarations for {m['county']}, 2000 to November 2026.</p>
{housing_line(slug)}

<h2>Why fire damage in {city} is different</h2>
{''.join(f'<p>{p}</p>' for p in c['why'])}

<h2>Home heating and fire risk in {city}</h2>
{fuel_chart(slug)}
{heating_line(slug)}

<h2>Common fire damage problems in {city}</h2>
{S.problems_table(c)}
{{{{cta:{cta1}}}}}

<h2>{tips_h}</h2>
<ul>{''.join(f'<li>{t}</li>' for t in c['tips'])}</ul>

<h2>Neighborhoods and areas served in {city}</h2>
<p>{c['areas']} {nb}</p>

<h2>Insurance, permits and licensing in {city}</h2>
<p>{ins}</p>
{{{{cta:Call SootMend for fire, smoke and soot damage help in {city}: {{{{phone}}}}.}}}}

{{{{faq}}}}

<h2>Fire damage restoration services in {city}</h2>
{{{{services_grid}}}}

<h2>More fire damage help near {city}</h2>
<ul class="pills">{''.join(f'<li><a href="{mpath(n)}">Fire damage restoration in {MMETA[n]["city"]}</a></li>' for n in near)}<li><a href="{sp}">All of {S.short(ab)}</a></li><li><a href="/locations/">All locations</a></li></ul>

{{{{helpful_guides:{','.join(S.guide_slugs(slug, c))}}}}}

{{{{sources}}}}
"""
    wiki = "https://en.wikipedia.org/wiki/" + m["wiki"]
    sources = [["U.S. Census Bureau: American Community Survey", "https://www.census.gov/programs-surveys/acs"],
               ["FEMA: Disaster declarations", "https://www.fema.gov/disaster/declarations"],
               ["EPA: A Brief Guide to Mold, Moisture and Your Home", "https://www.epa.gov/mold/brief-guide-mold-moisture-and-your-home"],
               ["NFPA: Home Heating Fires", "https://nfpa92.nfpa.org/News-and-Research/Data-research-and-tools/US-Fire-Problem/Heating-equipment"],
               [doi, doiu]]
    if st.get("contractor"):
        sources.append([st["contractor"][0], st["contractor"][1]])
    sources += c.get("sources", [])
    return {
        "path": mpath(slug), "type": "city", "parents": [["Locations", "/locations/"], [S.short(ab), sp]],
        "title": title, "description": desc, "h1": f"Fire Damage Restoration in {disp}", "crumb": city, "priority": "0.8",
        "lead": c["lead"], "chips": [m["county"], "Homes, rentals and businesses", "24/7 fire damage calls"],
        "service": {"name": f"Fire damage restoration in {disp}", "serviceType": "Fire damage restoration",
                    "areaServed": {"@type": "City", "name": disp, "sameAs": wiki,
                                   "containedInPlace": {"@type": "AdministrativeArea", "name": m["county"]}}},
        "about": [[disp, wiki]],
        "mentions": [["Structure fire", "https://en.wikipedia.org/wiki/Structure_fire"]] + c.get("mentions", []),
        "faq_title": f"Fire damage questions in {city}", "faq": faq, "sources": sources,
        "body": body, "source": f"src/metros/content/{slug}.json",
    }


def all_pages():
    return [p for p in (page(s) for s in sorted(MMETA)) if p]
