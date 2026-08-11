#!/usr/bin/env python3
"""Render the full project index as a table SVG.

A markdown table on a profile is just borders and left-aligned text. Drawing
it gives zebra rows, a language dot per project, live star counts and a status
column that all line up.
"""

import pathlib

import gh

OUT = pathlib.Path(__file__).resolve().parent.parent / "assets" / "project-index.svg"

# slug, display name, domain, language, stack summary, live?
ROWS = [
    ("quantum-debugger", "quantum-debugger", "Quantum", "Python", "Python · Qiskit", True),
    ("quantum-crypto-chat-BB84", "quantum-crypto-chat-BB84", "Quantum crypto", "TypeScript",
     "Next.js · TypeScript", True),
    ("qubit-pilot", "qubit-pilot", "Quantum tooling", "TypeScript", "TypeScript", True),
    ("astra-crime-intelligence", "astra-crime-intelligence", "AI / ML", "Python",
     "Python · ML · NLP", False),
    ("F-Shield", "F-Shield", "Security", "TypeScript", "TypeScript", True),
    ("Savaaree-Ride-App", "Savaaree", "Web3", "JavaScript", "Node · Web3.js · Solidity", False),
    ("ResoRoute", "ResoRoute", "App", "Dart", "Flutter · Dart", True),
    ("ios-exp-2", "Campus Connect", "iOS", "Swift", "Swift · SwiftUI", False),
    ("VR_Shooting_Gallery", "VR Shooting Gallery", "XR", "C#", "Unity · C#", False),
    ("chem-ar", "Chem AR", "AR", "C#", "Unity · C#", False),
    ("choices-anti-drug-vite", "choices-anti-drug", "AI product", "JavaScript",
     "Vite · React · MongoDB", False),
    ("Novadiff-jac", "Novadiff", "Experimental", "Jac", "Jac", False),
]

W = 860
HEAD, ROW_H, TOP = 74, 34, 96
COLS = (26, 300, 452, 700, 800)  # project, domain, stack, stars, status


def build(stars: dict) -> str:
    height = TOP + len(ROWS) * ROW_H + 20
    body = []
    for i, (slug, name, domain, lang, stack, live) in enumerate(ROWS):
        y = TOP + i * ROW_H
        colour = gh.lang_colour(lang)
        if i % 2 == 0:
            body.append(
                f'  <rect x="14" y="{y - 22}" width="{W - 28}" height="{ROW_H}" rx="6" '
                f'fill="#ffffff" fill-opacity="0.022"/>'
            )
        body.append(f'  <circle cx="{COLS[0] + 6}" cy="{y - 5}" r="4.6" fill="{colour}"/>')
        body.append(f'  <text x="{COLS[0] + 20}" y="{y}" class="nm">{gh.esc(name)}</text>')
        body.append(f'  <text x="{COLS[1]}" y="{y}" class="dm">{gh.esc(domain)}</text>')
        body.append(f'  <text x="{COLS[2]}" y="{y}" class="st">{gh.esc(stack)}</text>')

        n = stars.get(slug, 0)
        if n:
            body.append(
                f'  <path d="M{COLS[3]} {y - 12} l2.6 5.3 5.8.8-4.2 4.1 1 5.8-5.2-2.7'
                f'-5.2 2.7 1-5.8-4.2-4.1 5.8-.8z" fill="{gh.AMBER}"/>'
                f'<text x="{COLS[3] + 20}" y="{y}" class="sc">{n}</text>'
            )
        else:
            body.append(f'  <text x="{COLS[3] + 2}" y="{y}" class="dash">—</text>')

        if live:
            body.append(
                f'  <circle cx="{COLS[4] + 6}" cy="{y - 5}" r="4" fill="{gh.TEAL}">'
                f'<animate attributeName="opacity" values="1;0.25;1" dur="2.4s" '
                f'begin="{i * 0.12:.2f}s" repeatCount="indefinite"/></circle>'
                f'<text x="{COLS[4] + 18}" y="{y}" class="lv">live</text>'
            )
        else:
            body.append(f'  <text x="{COLS[4] + 2}" y="{y}" class="dash">—</text>')

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {height}"
     width="{W}" height="{height}" role="img" aria-label="Full project index">
  <title>Full project index</title>
  <defs>
    <linearGradient id="ibg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{gh.BG0}"/><stop offset="100%" stop-color="{gh.BG1}"/>
    </linearGradient>
    <linearGradient id="iac" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#6929C4"/><stop offset="50%" stop-color="#1F6FEB"/>
      <stop offset="100%" stop-color="#00D4AA"/>
    </linearGradient>
    <style>
      .ttl  {{ font-family:"Segoe UI",Inter,Helvetica,sans-serif; font-size:16px;
               font-weight:700; fill:{gh.TEAL}; }}
      .hd   {{ font-family:"JetBrains Mono",Consolas,monospace; font-size:10px;
               font-weight:700; fill:{gh.DIM}; letter-spacing:1.4px; }}
      .nm   {{ font-family:"Segoe UI",Inter,Helvetica,sans-serif; font-size:13.5px;
               font-weight:600; fill:#ffffff; }}
      .dm   {{ font-family:"Segoe UI",Inter,Helvetica,sans-serif; font-size:12.5px;
               fill:{gh.BLUE}; }}
      .st   {{ font-family:"JetBrains Mono",Consolas,monospace; font-size:11.5px;
               fill:{gh.MUTED}; }}
      .sc   {{ font-family:"JetBrains Mono",Consolas,monospace; font-size:12px;
               font-weight:700; fill:{gh.AMBER}; }}
      .lv   {{ font-family:"JetBrains Mono",Consolas,monospace; font-size:10.5px;
               font-weight:700; fill:{gh.TEAL}; }}
      .dash {{ font-family:"JetBrains Mono",Consolas,monospace; font-size:12px; fill:#3d4759; }}
    </style>
  </defs>

  <rect width="{W}" height="{height}" rx="12" fill="url(#ibg)"/>
  <rect x="1" y="1" width="{W - 2}" height="{height - 2}" rx="11" fill="none"
        stroke="url(#iac)" stroke-opacity="0.4" stroke-width="2"/>

  <text x="26" y="38" class="ttl">◈ Project Index</text>

  <text x="{COLS[0]}" y="{HEAD}" class="hd">PROJECT</text>
  <text x="{COLS[1]}" y="{HEAD}" class="hd">DOMAIN</text>
  <text x="{COLS[2]}" y="{HEAD}" class="hd">STACK</text>
  <text x="{COLS[3]}" y="{HEAD}" class="hd">STARS</text>
  <text x="{COLS[4]}" y="{HEAD}" class="hd">STATUS</text>
  <line x1="22" y1="{HEAD + 10}" x2="{W - 22}" y2="{HEAD + 10}" stroke="{gh.LINE}"/>

{chr(10).join(body)}
</svg>
'''


def main() -> None:
    stars = {}
    for slug, *_ in ROWS:
        try:
            stars[slug] = gh.api(f"repos/{gh.USER}/{slug}").get("stargazers_count", 0)
        except Exception:
            stars[slug] = 0
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(build(stars), encoding="utf-8")
    print(f"wrote {OUT.name} — {len(ROWS)} rows")


if __name__ == "__main__":
    main()
