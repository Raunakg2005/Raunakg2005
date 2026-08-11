#!/usr/bin/env python3
"""Render each featured project as its own card SVG.

Previously these were <td> cells in an HTML table, which GitHub styles as a
plain bordered grid. Drawing the cards ourselves gives consistent height,
a language dot, live star counts, tech chips and a hover-free "live" marker —
and unlike the pin-card services it cannot run out of API quota.
"""

import pathlib

import gh

OUT_DIR = pathlib.Path(__file__).resolve().parent.parent / "assets" / "cards"

W, H = 424, 208

# slug, display title, language, [chips], one-line description, live?
PROJECTS = [
    ("quantum-debugger", "quantum-debugger", "Python", ["Qiskit", "Simulation"],
     "Debugging and inspection tooling for quantum circuits — step through a circuit, "
     "inspect intermediate state, and find where the algorithm actually breaks.", True),
    ("quantum-crypto-chat-BB84", "quantum-crypto-chat", "TypeScript", ["Next.js", "QKD"],
     "Chat secured by the BB84 quantum key distribution protocol — key exchange, "
     "eavesdropper detection and real-time encrypted messaging.", True),
    ("qubit-pilot", "qubit-pilot", "TypeScript", ["Circuits", "Visualiser"],
     "A quantum circuit workbench — build, run and visualise circuits "
     "straight from the browser.", True),
    ("astra-crime-intelligence", "astra-crime-intelligence", "Python", ["ML", "NLP", "GeoSpatial"],
     "AI crime analytics for the Karnataka State Police — geospatial hotspots, "
     "criminal-network link analysis and predictive models.", False),
    ("F-Shield", "F-Shield", "TypeScript", ["Security", "Dashboard"],
     "Fraud and threat detection platform with a live analyst dashboard.", True),
    ("Savaaree-Ride-App", "Savaaree", "JavaScript", ["Solidity", "Web3"],
     "Blockchain ride-sharing DApp — smart-contract settlement "
     "and real-time ride matching.", False),
    ("ResoRoute", "ResoRoute", "Dart", ["Flutter", "Mobile"],
     "Cross-platform routing and resource-navigation app built in Flutter.", True),
    ("ios-exp-2", "Campus Connect", "Swift", ["SwiftUI", "iOS"],
     "Native SwiftUI college companion app — a full iOS build, not a web wrapper.", False),
    ("VR_Shooting_Gallery", "VR Shooting Gallery", "C#", ["Unity", "VR"],
     "Room-scale VR shooting range built in Unity with custom shaders.", False),
    ("chem-ar", "Chem AR", "C#", ["Unity", "ARCore"],
     "Augmented-reality chemistry visualiser — molecules rendered into the real world.", False),
]


def build(slug, title, lang, chips, desc, live, stars) -> str:
    colour = gh.lang_colour(lang)
    lines = gh.wrap(desc, W - 56, 12.5)[:4]
    body = "\n".join(
        f'    <text x="26" y="{112 + i * 18}" class="d-{slug}">{gh.esc(t)}</text>'
        for i, t in enumerate(lines)
    )

    chip_parts, x = [], 26
    for chip in chips:
        cw = len(chip) * 6.6 + 20
        chip_parts.append(
            f'    <rect x="{x}" y="{H - 42}" width="{cw:.0f}" height="22" rx="11" '
            f'fill="{colour}" fill-opacity="0.12" stroke="{colour}" stroke-opacity="0.45"/>\n'
            f'    <text x="{x + cw / 2:.0f}" y="{H - 27}" class="c-{slug}" '
            f'text-anchor="middle">{gh.esc(chip)}</text>'
        )
        x += cw + 8

    star_block = ""
    if stars:
        star_block = (
            f'  <path d="M{W - 74} 30 l3.2 6.6 7.2 1-5.2 5.1 1.2 7.2-6.4-3.4-6.4 3.4 '
            f'1.2-7.2-5.2-5.1 7.2-1z" fill="{gh.AMBER}" opacity="0.95"/>\n'
            f'  <text x="{W - 26}" y="42" class="s-{slug}" text-anchor="end">{stars}</text>'
        )

    live_block = ""
    if live:
        live_block = (
            f'  <circle cx="{W - 30}" cy="{H - 31}" r="4" fill="{gh.TEAL}">\n'
            f'    <animate attributeName="opacity" values="1;0.25;1" dur="2.2s" '
            f'repeatCount="indefinite"/>\n  </circle>\n'
            f'  <text x="{W - 40}" y="{H - 27}" class="l-{slug}" text-anchor="end">LIVE</text>'
        )

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}"
     role="img" aria-label="{gh.esc(title)} — {gh.esc(lang)} project">
  <title>{gh.esc(title)}</title>
  <defs>
    <linearGradient id="bg-{slug}" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{gh.BG0}"/><stop offset="100%" stop-color="{gh.BG1}"/>
    </linearGradient>
    <linearGradient id="top-{slug}" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{colour}"/>
      <stop offset="100%" stop-color="{colour}" stop-opacity="0.05"/>
    </linearGradient>
    <style>
      .t-{slug} {{ font-family:"Segoe UI",Inter,Helvetica,sans-serif; font-size:17px;
                   font-weight:700; fill:#ffffff; }}
      .g-{slug} {{ font-family:"JetBrains Mono",Consolas,monospace; font-size:10.5px;
                   fill:{colour}; letter-spacing:0.6px; }}
      .d-{slug} {{ font-family:"Segoe UI",Inter,Helvetica,sans-serif; font-size:12.5px;
                   fill:{gh.MUTED}; }}
      .c-{slug} {{ font-family:"JetBrains Mono",Consolas,monospace; font-size:10px;
                   font-weight:600; fill:{colour}; }}
      .s-{slug} {{ font-family:"JetBrains Mono",Consolas,monospace; font-size:12.5px;
                   font-weight:700; fill:{gh.AMBER}; }}
      .l-{slug} {{ font-family:"JetBrains Mono",Consolas,monospace; font-size:9.5px;
                   font-weight:700; fill:{gh.TEAL}; letter-spacing:1.2px; }}
    </style>
  </defs>

  <rect width="{W}" height="{H}" rx="14" fill="url(#bg-{slug})"/>
  <rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="13" fill="none"
        stroke="{gh.LINE}" stroke-width="2"/>
  <path d="M14 1h{W - 28}a13 13 0 0 1 13 13v2H1v-2a13 13 0 0 1 13-13z" fill="url(#top-{slug})"/>

  <text x="26" y="46" class="t-{slug}">{gh.esc(title)}</text>
  <circle cx="31" cy="66" r="5" fill="{colour}"/>
  <text x="43" y="70" class="g-{slug}">{gh.esc(lang)}</text>
{star_block}

{body}

{chr(10).join(chip_parts)}
{live_block}
</svg>
'''


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for slug, title, lang, chips, desc, live in PROJECTS:
        try:
            stars = gh.api(f"repos/{gh.USER}/{slug}").get("stargazers_count", 0)
        except Exception:
            stars = 0
        path = OUT_DIR / f"{slug}.svg"
        path.write_text(build(slug, title, lang, chips, desc, live, stars), encoding="utf-8")
        print(f"wrote {path.name} (stars={stars})")


if __name__ == "__main__":
    main()
