"""Writes src/states/content/<AB>.json from the batch files in this folder.

Each batch file defines S = {"AB": {...}}. Problem rows end with a service key from L,
which becomes a link to that service page.
"""
import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE.parent.parent / "src" / "states" / "content"
L = {
    "board": ("board-up-and-roof-tarping", "Board-up and roof tarping"),
    "cleanup": ("fire-damage-cleanup", "Fire damage cleanup"),
    "smoke": ("smoke-damage-restoration", "Smoke damage restoration"),
    "soot": ("soot-removal", "Soot removal"),
    "odor": ("smoke-odor-removal", "Smoke odor removal"),
    "contents": ("contents-cleaning", "Contents cleaning and pack-out"),
    "repair": ("fire-damage-repair", "Fire damage repair"),
    "commercial": ("commercial-fire-damage-restoration", "Commercial fire restoration"),
}


def link(key):
    slug, text = L[key]
    return f'<a href="/services/{slug}/">{text}</a>'


def main(files):
    OUT.mkdir(parents=True, exist_ok=True)
    n = 0
    for f in files:
        spec = importlib.util.spec_from_file_location(Path(f).stem, f)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        for ab, c in mod.S.items():
            c = dict(c)
            c["problems"] = [[p, w, link(k)] for p, w, k in c["problems"]]
            q, a = c["faq"]
            c["faq"] = {"q": q, "a": a}
            (OUT / f"{ab}.json").write_text(json.dumps(c, indent=1, ensure_ascii=False) + "\n")
            n += 1
    print(f"wrote {n} state content files")


if __name__ == "__main__":
    main(sys.argv[1:] or sorted(str(p) for p in HERE.glob("batch*.py")))
