#!/usr/bin/env python3
"""Render the two remaining markdown tables as cards.

Everything else on the profile is a generated card now, which left GitHub's
default table styling — plain borders, flat header row — looking out of place
inside the "A bit more" and "More app & XR builds" sections.
"""

import pathlib

import gh

ROOT = pathlib.Path(__file__).resolve().parent.parent
W = 860
MONO = "'JetBrains Mono','SFMono-Regular',Consolas,monospace"
SANS = "'Segoe UI',Inter,Helvetica,Arial,sans-serif"

# ── "A bit more": lead phrase, supporting detail, accent ──
POINTS = [
    ("Full stack, genuinely end to end",
     "Next.js and React on the front, Node/FastAPI/Laravel behind it, "
     "Postgres or Mongo underneath, Dockerised and deployed.", gh.BLUE),
    ("App developer across Flutter, SwiftUI and Kotlin",
     "Native iOS, native Android and cross-platform — shipped to real devices.", gh.TEAL),
    ("Quantum is shipped work, not a hobby",
     "Debugging tooling, QKD protocol implementations and circuit simulators "
     "that are live on the web right now.", gh.PURPLE),
    ("AI/ML that gets deployed",
     "Geospatial crime analytics, NLP pipelines, fraud detection and LLM-backed products.",
     "#FF7B72"),
    ("Solidity smart contracts and DApps",
     "Real Web3 integration, not a wrapper around someone else's contract.", gh.AMBER),
    ("AR / VR / game dev in Unity",
     "C#, custom HLSL and ShaderLab shaders, and a handful of shipped VR builds.", "#F0A868"),
    ("DevOps & MLOps",
     "Dockerised services, Jenkins and GitHub Actions pipelines, Kubernetes, and ML that "
     "gets versioned, tracked and served rather than left in a notebook.", "#A5D6FF"),
    ("The boring parts matter",
     "Tests, CI, monitoring, and code the next person can actually read.", gh.TEAL),
]

# ── "More app & XR builds": name, what it is, language, chips ──
XR_ROWS = [
    ("Block Blast", "Puzzle game build", "TypeScript", ["TypeScript"]),
    ("VR Beat Box", "Rhythm experience in VR", "C++", ["C++", "Unity"]),
    ("2048 iOS", "Native iOS take on 2048", "Swift", ["Swift"]),
    ("echoscape", "Swift Playgrounds audio app", "Swift", ["Swift", "Audio"]),
    ("AtomicQR", "AR chemistry QR compound viewer", "C#", ["C#", "Unity"]),
    ("Faculty Timetable", "Timetable builder app", "Dart", ["Dart", "Flutter"]),
]


def shell(h, uid, body) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {h}" width="{W}" height="{h}"
     role="img" aria-label="{uid}">
  <defs>
    <linearGradient id="bg{uid}" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{gh.BG0}"/><stop offset="100%" stop-color="{gh.BG1}"/>
    </linearGradient>
    <linearGradient id="ac{uid}" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#6929C4"/><stop offset="50%" stop-color="#1F6FEB"/>
      <stop offset="100%" stop-color="#00D4AA"/>
    </linearGradient>
  </defs>
  <rect width="{W}" height="{h}" rx="13" fill="url(#bg{uid})"/>
  <rect x="1" y="1" width="{W - 2}" height="{h - 2}" rx="12" fill="none"
        stroke="url(#ac{uid})" stroke-opacity="0.4" stroke-width="2"/>
{body}
</svg>
'''


def about_list() -> str:
    lead_px, desc_px, desc_lead = 14, 12.5, 17
    rows, y = [], 62
    for i, (lead, desc, colour) in enumerate(POINTS):
        lines = gh.wrap(desc, W - 132, desc_px)
        row_h = 24 + len(lines) * desc_lead + 14
        rows.append(
            f'  <rect x="16" y="{y - 20}" width="{W - 32}" height="{row_h - 6}" rx="8" '
            f'fill="#ffffff" fill-opacity="{0.028 if i % 2 == 0 else 0.008}"/>'
            f'<rect x="26" y="{y - 14}" width="3" height="{row_h - 22}" rx="1.5" fill="{colour}"/>'
            f'<circle cx="27.5" cy="{y - 5}" r="4.5" fill="{colour}">'
            f'<animate attributeName="opacity" values="0.35;1;0.35" dur="3s" '
            f'begin="{i * 0.25:.2f}s" repeatCount="indefinite"/></circle>'
            f'<text x="46" y="{y}" style="font:700 {lead_px}px {SANS};fill:#ffffff">'
            f'{gh.esc(lead)}</text>'
        )
        for j, line in enumerate(lines):
            rows.append(
                f'  <text x="46" y="{y + 22 + j * desc_lead}" '
                f'style="font:400 {desc_px}px {SANS};fill:{gh.MUTED}">{gh.esc(line)}</text>'
            )
        y += row_h

    height = y + 44
    head = (
        f'  <text x="26" y="36" style="font:700 16px {SANS};fill:{gh.TEAL}">◈ A bit more</text>'
        f'<text x="{W - 26}" y="36" text-anchor="end" '
        f'style="font:600 10px {MONO};fill:{gh.DIM};letter-spacing:1.6px">WHAT I ACTUALLY DO</text>'
        f'<line x1="26" y1="46" x2="{W - 26}" y2="46" stroke="{gh.LINE}"/>'
    )
    foot = (
        f'  <line x1="26" y1="{y + 2}" x2="{W - 26}" y2="{y + 2}" stroke="{gh.LINE}"/>'
        f'<text x="26" y="{y + 26}" style="font:600 12.5px {MONO};fill:{gh.TEAL}">'
        f'✉ raunakg2005@gmail.com</text>'
        f'<text x="{W - 26}" y="{y + 26}" text-anchor="end" '
        f'style="font:400 11.5px {SANS};fill:{gh.MUTED}">Open to collaboration</text>'
    )
    return shell(height, "about-list", head + "\n" + "\n".join(rows) + "\n" + foot)


def xr_table() -> str:
    top, row_h = 96, 38
    cols = (26, 292, 604)
    rows = []
    for i, (name, what, lang, chips) in enumerate(XR_ROWS):
        y = top + i * row_h
        colour = gh.lang_colour(lang)
        if i % 2 == 0:
            rows.append(
                f'  <rect x="16" y="{y - 24}" width="{W - 32}" height="{row_h}" rx="7" '
                f'fill="#ffffff" fill-opacity="0.025"/>'
            )
        rows.append(
            f'  <circle cx="{cols[0] + 6}" cy="{y - 5}" r="4.6" fill="{colour}"/>'
            f'<text x="{cols[0] + 20}" y="{y}" '
            f'style="font:600 13.5px {SANS};fill:#ffffff">{gh.esc(name)}</text>'
            f'<text x="{cols[1]}" y="{y}" '
            f'style="font:400 12.5px {SANS};fill:{gh.MUTED}">{gh.esc(what)}</text>'
        )
        x = cols[2]
        for chip in chips:
            cw = len(chip) * 6.6 + 20
            rows.append(
                f'  <rect x="{x:.0f}" y="{y - 15}" width="{cw:.0f}" height="21" rx="10.5" '
                f'fill="{colour}" fill-opacity="0.12" stroke="{colour}" stroke-opacity="0.45"/>'
                f'<text x="{x + cw / 2:.0f}" y="{y - 1}" text-anchor="middle" '
                f'style="font:600 10px {MONO};fill:{colour}">{gh.esc(chip)}</text>'
            )
            x += cw + 7

    height = top + len(XR_ROWS) * row_h + 16
    head = (
        f'  <text x="26" y="38" style="font:700 16px {SANS};fill:{gh.TEAL}">'
        f'◈ More App &amp; XR Builds</text>'
        f'<text x="{cols[0]}" y="72" style="font:700 10px {MONO};fill:{gh.DIM};'
        f'letter-spacing:1.5px">PROJECT</text>'
        f'<text x="{cols[1]}" y="72" style="font:700 10px {MONO};fill:{gh.DIM};'
        f'letter-spacing:1.5px">WHAT IT IS</text>'
        f'<text x="{cols[2]}" y="72" style="font:700 10px {MONO};fill:{gh.DIM};'
        f'letter-spacing:1.5px">STACK</text>'
        f'<line x1="22" y1="80" x2="{W - 22}" y2="80" stroke="{gh.LINE}"/>'
    )
    return shell(height, "xr-index", head + "\n" + "\n".join(rows))


def main() -> None:
    out = ROOT / "assets"
    out.mkdir(parents=True, exist_ok=True)
    (out / "about-list.svg").write_text(about_list(), encoding="utf-8")
    (out / "xr-index.svg").write_text(xr_table(), encoding="utf-8")
    print("wrote about-list.svg and xr-index.svg")


if __name__ == "__main__":
    main()
