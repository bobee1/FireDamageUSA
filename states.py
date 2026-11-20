"""State hub pages for SootMend: one page per state and DC at /locations/<state>/.

Inputs:
  research/06-state-data.json        Census ACS housing data and largest places
  research/07-heating-fuel.json      Census ACS B25040 house heating fuel
  research/08-fema-fire.json         OpenFEMA fire declarations since 2000
  research/09-usfa-fire-deaths.json  USFA state fire deaths and relative risk (2023)
  src/states/meta.json               names, slugs, neighbors, insurance regulator, contractor board
  src/states/content/<AB>.json       hand-written copy: lead, risks, why, problems, tips, insurance note, FAQ
The templates below only stitch facts together; each page's narrative comes from its own content file.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).parent
R = ROOT / "research"
ACS = json.loads((R / "06-state-data.json").read_text())
FUEL = json.loads((R / "07-heating-fuel.json").read_text())["rows"]
FEMA = json.loads((R / "08-fema-fire.json").read_text())["rows"]
USFA = json.loads((R / "09-usfa-fire-deaths.json").read_text())["rows"]
META = json.loads((ROOT / "src" / "states" / "meta.json").read_text())
CONTENT_DIR = ROOT / "src" / "states" / "content"

WIKI = {"GA": "Georgia_(U.S._state)", "WA": "Washington_(state)", "NY": "New_York_(state)", "DC": "Washington,_D.C."}
SMALL_N = {"DE", "ID", "MT", "NH", "RI", "SD", "VT"}  # USFA: fewer than 20 deaths, rate highly variable
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
          "November", "December"]
FUEL_LABELS = ["Utility gas", "Propane or bottled gas", "Electricity", "Fuel oil or kerosene", "Coal", "Wood",
               "No heating fuel"]


def pick(ab, options, salt=""):
    """Deterministic choice so each state keeps the same wording between builds."""
    h = int(hashlib.md5((ab + salt).encode()).hexdigest(), 16)
    return options[h % len(options)]


def join_list(items):
    items = list(items)
    return items[0] if len(items) == 1 else ", ".join(items[:-1]) + " and " + items[-1]


def fmt(n):
    return f"{n:,}"


def state_path(ab):
    return f"/locations/{META[ab]['slug']}/"


def the(ab):
    return "the District of Columbia" if ab == "DC" else META[ab]["name"]


def short(ab):
    return "Washington, DC" if ab == "DC" else META[ab]["name"]


def load_content(ab):
    f = CONTENT_DIR / f"{ab}.json"
    return json.loads(f.read_text()) if f.exists() else None


def fuel(ab):
    return dict(zip(FUEL_LABELS, FUEL[META[ab]["name"]]))


def fema(ab):
    return FEMA.get(ab, [0, 0, 0, None, None])


def month_year(d):
    y, m, _ = d.split("-")
    return f"{MONTHS[int(m) - 1]} {y}"


def times(rr):
    return f"{rr:g} times"


# ---------------------------------------------------------------- page pieces

def quick_answer(ab, c):
    name = the(ab)
    major, emerg, fmag, latest, lname = fema(ab)
    lead = pick(ab, [
        f"Fire damage restoration in {name} covers board-up, soot and smoke cleanup, odor removal, contents cleaning and repairs.",
        f"In {name}, fire damage restoration means securing the property, cleaning soot and smoke, removing odor and rebuilding.",
        f"Fire damage restoration in {name} starts with board-up and water removal, then soot cleanup, deodorizing and repairs.",
    ], "q")
    if fmag >= 5:
        fact = f"Since 2000, FEMA has approved wildfire aid here {fmag} times."
    else:
        f = fuel(ab)
        top = max(("Utility gas", "Electricity", "Fuel oil or kerosene", "Propane or bottled gas"), key=lambda k: f[k])
        fact = f"Most calls start indoors; {f[top]:g}% of homes here heat with {top.lower()}."
    return f"{lead} The main local risks are {c['risk']}. {fact}"


def glance_table(ab):
    pop, med, own, pre80, pre40, mobile, units = ACS["acs"][ab]
    f = fuel(ab)
    major, emerg, fmag, latest, lname = fema(ab)
    deaths = USFA[META[ab]["name"]]
    if deaths:
        d_txt = f"{fmt(deaths[0])} (relative risk {deaths[2]:.1f}; U.S. = 1.0)"
    else:
        d_txt = "Fewer than 10; too few for a USFA rate"
    top = max(FUEL_LABELS[:6], key=lambda k: f[k])
    rows = [
        ("Population", fmt(pop)),
        ("Housing units", fmt(units)),
        ("Median year built", str(med)),
        ("Homes built before 1980", f"{pre80:g}%"),
        ("Most common heating fuel", f"{top} ({f[top]:g}% of homes)"),
        ("Homes heated with wood", f"{f['Wood']:g}%"),
        ("Homes heated with oil", f"{f['Fuel oil or kerosene']:g}%"),
        ("Mobile homes", f"{mobile:g}% of housing units"),
        ("Fire deaths in 2023", d_txt),
        ("FEMA fire declarations since 2000", "None" if not (fmag or major or emerg) else
         f"{fmag} wildfire aid, {major} major disaster" + ("s" if major != 1 else "")
         + (f", {emerg} emergency" if emerg else "")),
    ]
    if latest:
        rows.append(("Latest FEMA fire declaration", f"{lname[0].upper() + lname[1:]} ({month_year(latest)})"))
    trs = "".join(f'<tr><th scope="row">{k}</th><td>{v}</td></tr>' for k, v in rows)
    return f'<div class="table-scroll"><table class="facts"><tbody>{trs}</tbody></table></div>'


def fuel_chart(ab):
    """Bar chart of home heating fuels, built in HTML so it reflows on phones."""
    f = fuel(ab)
    rows = sorted(((k, v) for k, v in f.items() if v >= 0.5 and k != "Coal"), key=lambda kv: -kv[1])
    bars = "".join(
        f'<li><span class="bar-label">{k}</span><span class="bar-track"><span class="bar-fill" style="width:{max(v, 1):g}%"></span></span>'
        f'<span class="bar-val">{v:g}%</span></li>' for k, v in rows)
    return (f'<figure class="bars" aria-label="How homes in {short(ab)} are heated">'
            f'<figcaption><strong>How homes in {short(ab)} are heated</strong> (share of occupied homes, Census ACS 2024)</figcaption>'
            f'<ul>{bars}</ul></figure>')


def heating_text(ab):
    f = fuel(ab)
    name = the(ab)
    parts = []
    if f["Fuel oil or kerosene"] >= 5:
        parts.append(pick(ab, [
            f"{f['Fuel oil or kerosene']:g}% of homes in {name} still burn fuel oil or kerosene. A misfiring oil burner can cause a "
            f"<a href=\"/services/soot-removal/\">puff-back</a> that coats a whole house in oily soot.",
            f"Oil heat is common here: {f['Fuel oil or kerosene']:g}% of homes use fuel oil or kerosene. That makes furnace "
            f"<a href=\"/services/soot-removal/\">puff-backs</a> and oily soot a regular winter call.",
        ], "oil"))
    if f["Wood"] >= 3:
        parts.append(pick(ab, [
            f"{f['Wood']:g}% of homes heat mainly with wood, well above the national pattern. Creosote in flues and hot ashes cause many chimney and stove fires.",
            f"Wood is the main heat source in {f['Wood']:g}% of homes. Dirty chimneys and ashes stored in the wrong place start many fires.",
        ], "wood"))
    if f["Propane or bottled gas"] >= 10:
        parts.append(f"Propane heats {f['Propane or bottled gas']:g}% of homes, mostly in rural areas where fire crews travel farther.")
    if f["Electricity"] >= 55:
        parts.append(pick(ab, [
            f"Electricity heats {f['Electricity']:g}% of homes. Space heaters and overloaded cords are the usual cold-weather fire starters.",
            f"Most homes ({f['Electricity']:g}%) heat with electricity, so space heaters, cords and outlets drive winter fire calls.",
        ], "elec"))
    if f["Utility gas"] >= 55 and len(parts) < 2:
        parts.append(f"Natural gas heats {f['Utility gas']:g}% of homes. Furnaces and water heaters need yearly service to stay safe.")
    if not parts and f["No heating fuel"] >= 20:
        parts.append(f"{f['No heating fuel']:g}% of homes use no heating fuel at all, so heating fires are rare. Cooking, electrical and smoking fires cause most house fires here.")
    if not parts:
        parts.append(f"Homes here split between gas ({f['Utility gas']:g}%) and electric heat ({f['Electricity']:g}%).")
    lead = pick(ab, ["Heating equipment is the second leading cause of U.S. home fires, according to the NFPA.",
                     "The NFPA ranks heating equipment just behind cooking as a cause of home fires."], "nfpa")
    return f"<p>{lead} {' '.join(parts)}</p>"


def risk_text(ab):
    deaths = USFA[META[ab]["name"]]
    name = the(ab)
    pop, med, own, pre80, pre40, mobile, units = ACS["acs"][ab]
    if not deaths:
        s = (f"{name} had fewer than 10 fire deaths in 2023, too few for the U.S. Fire Administration to compute a rate. "
             f"Most fire damage calls here are for kitchen, heating and electrical fires.")
    else:
        d, rate, rr = deaths
        if rr > 1.05:
            cmp = f"{times(rr)} as likely to die in a fire as the U.S. population as a whole"
        elif rr < 0.95:
            cmp = f"less likely than average to die in a fire (relative risk {rr:g})"
        else:
            cmp = "about as likely as the average American to die in a fire"
        s = pick(ab, [
            f"The U.S. Fire Administration counted {fmt(d)} fire deaths in {name} in 2023. People living here were {cmp}.",
            f"In 2023, {fmt(d)} people died in fires in {name}, according to the U.S. Fire Administration. Residents were {cmp}.",
        ], "d")
        if ab in SMALL_N:
            s += " USFA notes that rates based on so few deaths swing a lot from year to year."
    if pre80 >= 50:
        s += f" {pre80:g}% of homes were built before 1980, so older wiring and paint that may contain lead are common in repairs."
    elif mobile >= 10:
        s += f" Mobile homes make up {mobile:g}% of housing; they burn fast and smoke spreads through them quickly."
    else:
        s += f" Housing is fairly new here: the median home was built in {med}."
    return f"<p>{s}</p>"


def problems_table(c):
    rows = "".join(f"<tr><td>{p}</td><td>{w}</td><td>{h}</td></tr>" for p, w, h in c["problems"])
    return ('<table><thead><tr><th>Problem</th><th>Where it shows up</th><th>What helps</th></tr></thead>'
            f'<tbody>{rows}</tbody></table>')


def insurance_section(ab, c):
    m = META[ab]
    name, sh = the(ab), short(ab)
    doi, doiu = m["doi"]
    p1 = pick(ab, [
        f'The <a href="{doiu}">{doi}</a> regulates home insurance in {name} and takes complaints if a claim stalls.',
        f'Home insurance in {name} is overseen by the <a href="{doiu}">{doi}</a>, which can help when a claim runs into trouble.',
    ], "i") + " " + c["insurance"]
    p2 = pick(ab, [
        f"Standard homeowners policies in {name} usually cover fire and smoke damage, including wildfire. If you cannot live at home, ask about additional living expenses (ALE), which can pay for a hotel or rental during repairs.",
        f"Fire and smoke are covered perils on most {sh} home and renters policies, wildfire included. Keep every receipt if you move out; additional living expenses (ALE) coverage can pay the extra cost.",
        f"Most home policies in {name} pay for fire and smoke damage from any cause, wildfire included, up to your limits. Ask your adjuster early about additional living expenses (ALE) if the house is not livable.",
    ], "ale")
    if c.get("licensing"):
        p3 = c["licensing"]
    elif m.get("contractor"):
        cb, cbu = m["contractor"]
        p3 = pick(ab, [
            f'For rebuild work, check the contractor with the <a href="{cbu}">{cb}</a>. Ask for the license or registration number before work starts.',
            f'The <a href="{cbu}">{cb}</a> licenses or registers builders in {name}. Look up any repair contractor there first.',
        ], "c")
    else:
        p3 = pick(ab, [
            f"{name} has no statewide general contractor license, so cities and counties set the rules. Electricians and plumbers still need state or local licenses.",
            f"There is no statewide general contractor license in {name}. Local building offices handle permits, and electrical work needs a licensed electrician.",
        ], "c")
    return f"<p>{p1}</p>\n<p>{p2}</p>\n<p>{p3}</p>"


def faq(ab, c):
    m = META[ab]
    name = the(ab)
    cities = ACS["cities"][ab]
    if ab == "DC":
        cover = ("Yes. SootMend takes fire and smoke damage calls from every ward of the District, "
                 "and from nearby Maryland and Virginia suburbs.")
    else:
        cover = (f"Yes. SootMend takes fire and smoke damage calls from all of {name}, including {join_list(cities[:5])}, "
                 f"plus small towns and rural counties.")
    ins_a = (f"Usually yes. Standard home policies in {name} cover sudden fire and smoke damage, including wildfire, "
             f"up to your limits. Report the loss quickly, document everything and ask about ALE. "
             f"For claim problems, contact the {m['doi'][0]}.")
    if c.get("licensing_faq"):
        lic_a = c["licensing_faq"]
    elif m.get("contractor"):
        lic_a = (f"Rules depend on the work. Check repair contractors with the {m['contractor'][0]}. "
                 f"Electrical, plumbing and HVAC work need licensed trades, and rebuilds need permits.")
    else:
        lic_a = (f"{name} has no statewide general contractor license, so local rules apply. "
                 f"Electrical and plumbing work still need licensed trades, and rebuilds need permits.")
    return [
        {"q": f"Do you cover all of {name}?", "a": cover},
        {"q": f"Does homeowners insurance cover fire damage in {name}?", "a": ins_a},
        {"q": f"Does a fire restoration company need a license in {name}?", "a": lic_a},
        c["faq"],
    ]


def nearby(ab):
    pills = "".join(f'<li><a href="{state_path(n)}">Fire damage restoration in {short(n)}</a></li>' for n in META[ab]["neighbors"])
    pills += '<li><a href="/locations/">All states</a></li>'
    return f'<ul class="pills">{pills}</ul>'


GUIDE_RULES = [  # (slug, keywords in the page's own copy)
    ("how-to-get-smoke-smell-out-of-house", ("wildfire smoke", "smoke smell", "odor")),
    ("what-to-do-after-a-house-fire", ("house fire", "kitchen", "cooking")),
    ("does-homeowners-insurance-cover-fire-damage", ("insurance", "fair plan", "wildfire")),
    ("does-renters-insurance-cover-fire-damage", ("renter", "apartment", "tenant")),
    ("what-is-soot", ("soot", "puff-back", "oil")),
    ("how-to-clean-soot-off-walls", ("chimney", "wood stove", "candle")),
]


def guide_slugs(ab, c):
    blob = json.dumps(c).lower()
    scored = sorted(((-sum(blob.count(k) for k in kws), i, slug) for i, (slug, kws) in enumerate(GUIDE_RULES)))
    return [s for _, _, s in scored[:3]]


def state_page(ab):
    c = load_content(ab)
    if not c:
        return None
    m = META[ab]
    name, sh = the(ab), short(ab)
    cities = ACS["cities"][ab]
    h1 = f"Fire Damage Restoration in {sh}"
    title = f"Fire Damage Restoration in {sh} | SootMend"
    if len(title) > 60:
        title = f"Fire Damage Restoration {sh} | SootMend"
    desc = f"Fire damage restoration in {sh}: {c['risk_short']}. Board-up, soot, smoke odor and repairs. Call 1-800-555-0199."
    if len(desc) > 155:
        desc = f"Fire damage restoration in {sh}: {c['risk_short']}. Call SootMend at 1-800-555-0199."
    if len(desc) > 155:
        desc = f"Fire damage restoration in {sh}: {c['risk_short']}. Call 1-800-555-0199."
    tips_h = pick(ab, [f"Fire safety tips for {sh} homes", f"Tips for property owners in {sh}", f"Practical fire tips for {sh}"], "t")
    cta1 = pick(ab, [f"Fire or smoke damage in {sh}? Call SootMend {{{{availability}}}}.",
                     f"Need help after a fire in {sh}? Call SootMend at {{{{phone}}}}."], "cta")
    cta2 = f"Call SootMend for fire, smoke and soot damage help anywhere in {sh}: {{{{phone}}}}."
    nb = [f'<a href="{state_path(n)}">{short(n)}</a>' for n in m["neighbors"]]
    nb_line = pick(ab, [f" Calls from neighboring {join_list(nb)} are covered too.",
                        f" SootMend also helps owners next door in {join_list(nb)}.",
                        f" Fire damage help is also available across the line in {join_list(nb)}."], "nb")
    if ab == "DC":
        areas_h = "Neighborhoods served in Washington, DC"
        areas_p = c["areas"] + nb_line
    else:
        areas_h = f"Areas served in {sh}"
        areas_p = (f"SootMend takes fire damage calls across {name}. The largest communities are {join_list(cities)}. "
                   + c.get("areas", "") + nb_line)
    body = f"""<p class="quick"><strong>Quick answer:</strong> {quick_answer(ab, c)}</p>

<h2>{sh} fire risk at a glance</h2>
{glance_table(ab)}
<p class="small-note">{sh} figures: Census ACS (housing 2020–2024, heating fuel 2024), U.S. Fire Administration (2023 deaths) and OpenFEMA (declarations 2000 to November 2026). USFA warns against ranking states on crude death rates, because age mix differs.</p>
{risk_text(ab)}

<h2>Why fire damage in {sh} is different</h2>
{''.join(f'<p>{p}</p>' for p in c['why'])}

<h2>Home heating and fire risk in {sh}</h2>
{fuel_chart(ab)}
{heating_text(ab)}

<h2>Common fire damage problems in {sh}</h2>
{problems_table(c)}
{{{{cta:{cta1}}}}}

<h2>{tips_h}</h2>
<ul>{''.join(f'<li>{t}</li>' for t in c['tips'])}</ul>

<h2>Insurance and licensing in {sh}</h2>
{insurance_section(ab, c)}
{{{{cta:{cta2}}}}}

<h2>{areas_h}</h2>
<p>{areas_p}</p>

{{{{faq}}}}

<h2>Fire damage restoration services in {sh}</h2>
{{{{services_grid}}}}

<h2>Fire damage help in nearby states</h2>
{nearby(ab)}

{{{{helpful_guides:{','.join(guide_slugs(ab, c))}}}}}

{{{{sources}}}}
"""
    wiki = "https://en.wikipedia.org/wiki/" + WIKI.get(ab, m["name"].replace(" ", "_"))
    sources = [
        ["U.S. Fire Administration: State Fire Death Risk", "https://www.usfa.fema.gov/statistics/deaths-injuries/states.html"],
        ["FEMA: Disaster declarations", "https://www.fema.gov/disaster/declarations"],
        ["U.S. Census Bureau: American Community Survey", "https://www.census.gov/programs-surveys/acs"],
        ["NFPA: Home Heating Fires", "https://nfpa92.nfpa.org/News-and-Research/Data-research-and-tools/US-Fire-Problem/Heating-equipment"],
        [m["doi"][0], m["doi"][1]],
    ]
    if m.get("contractor"):
        sources.append([m["contractor"][0], m["contractor"][1]])
    sources += c.get("sources", [])
    return {
        "path": state_path(ab), "type": "state", "parents": [["Locations", "/locations/"]],
        "title": title, "description": desc, "h1": h1, "crumb": sh, "priority": "0.8",
        "lead": c["lead"],
        "chips": [f"All of {sh}" if ab != "DC" else "Every DC ward", "Homes, rentals and businesses", "24/7 fire damage calls"],
        "service": {"name": f"Fire damage restoration in {sh}", "serviceType": "Fire damage restoration",
                    "areaServed": {"@type": "State" if ab != "DC" else "City", "name": sh, "sameAs": wiki}},
        "about": [[sh, wiki]],
        "mentions": [["Structure fire", "https://en.wikipedia.org/wiki/Structure_fire"],
                     ["Wildfire", "https://en.wikipedia.org/wiki/Wildfire"]],
        "faq_title": f"Fire damage questions in {sh}",
        "faq": faq(ab, c), "sources": sources,
        "body": body, "source": f"src/states/content/{ab}.json", "state": ab,
    }


def all_state_pages():
    return [p for p in (state_page(ab) for ab in sorted(META, key=lambda a: META[a]["name"])) if p]


REGIONS = {
    "Northeast": ["CT", "ME", "MA", "NH", "NJ", "NY", "PA", "RI", "VT"],
    "Midwest": ["IL", "IN", "IA", "KS", "MI", "MN", "MO", "NE", "ND", "OH", "SD", "WI"],
    "South": ["AL", "AR", "DE", "DC", "FL", "GA", "KY", "LA", "MD", "MS", "NC", "OK", "SC", "TN", "TX", "VA", "WV"],
    "West": ["AK", "AZ", "CA", "CO", "HI", "ID", "MT", "NV", "NM", "OR", "UT", "WA", "WY"],
}


def states_grid():
    """Cards for the locations hub, grouped by Census region."""
    out = []
    for reg, abs_ in REGIONS.items():
        cards = "".join(
            f'<li><a class="state-card" href="{state_path(a)}"><span class="state-name">{short(a)}</span>'
            f'<span class="state-cities">{", ".join(ACS["cities"][a][:3]) if a != "DC" else "All eight wards"}</span></a></li>'
            for a in sorted(abs_, key=lambda x: META[x]["name"]) if load_content(a))
        out.append(f'<h3>{reg}</h3><ul class="state-grid">{cards}</ul>')
    return "\n".join(out)


def state_pills():
    pills = "".join(f'<li><a href="{state_path(a)}">{short(a)}</a></li>'
                    for a in sorted(META, key=lambda x: META[x]["name"]) if load_content(a))
    return f'<ul class="pills pills-sm">{pills}</ul>'
