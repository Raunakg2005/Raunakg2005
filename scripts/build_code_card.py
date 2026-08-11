#!/usr/bin/env python3
"""Render the "about me" snippet as a terminal window instead of a plain code fence.

GitHub's own syntax highlighting is fine but visually flat, and it cannot show
window chrome, line numbers, or a blinking cursor. Drawing it ourselves gives
the section a real editor look that matches the other cards.
"""

import pathlib

import gh

OUT = pathlib.Path(__file__).resolve().parent.parent / "assets" / "about-code.svg"

KW, VAR, STR, NUM, PUN, CMT, PROP = (
    "#FF7B72", "#79C0FF", "#A5D6FF", "#F0A868", "#8B949E", "#6E7A91", "#7EE7C7",
)

# (indent, [(text, colour), ...]) — tokenised by hand so the colours are exact.
LINES = [
    [("const", KW), (" raunak", VAR), (" = ", PUN), ("{", PUN)],
    [("  role", PROP), (": ", PUN), ('"Full Stack · App · AI/ML · DevOps · Web3 · Quantum"', STR), (",", PUN)],
    [("  location", PROP), (": ", PUN), ('"Mumbai, India"', STR), (",", PUN)],
    [("  building", PROP), (": ", PUN), ("[", PUN), ('"quantum tooling"', STR), (", ", PUN),
     ('"apps"', STR), (", ", PUN), ('"AI platforms"', STR), (", ", PUN), ('"DApps"', STR), ("],", PUN)],
    [("  ops", PROP), (": ", PUN), ("[", PUN), ('"Docker"', STR), (", ", PUN), ('"Kubernetes"', STR),
     (", ", PUN), ('"Jenkins"', STR), (", ", PUN), ('"MLflow"', STR), (", ", PUN),
     ('"Airflow"', STR), ("],", PUN)],
    [("  languages", PROP), (": ", PUN), ("30", NUM), (",", PUN),
     ("        // across 54 public repos", CMT)],
    [("  stack", PROP), (": ", PUN), ("[", PUN), ('"TypeScript"', STR), (", ", PUN),
     ('"Python"', STR), (", ", PUN), ('"Flutter"', STR), (", ", PUN),
     ('"Swift"', STR), (", ", PUN), ('"Solidity"', STR), ("],", PUN)],
    [("  philosophy", PROP), (": ", PUN),
     ('"Build it, run it, measure it — then ship it."', STR), (",", PUN)],
    [("  openTo", PROP), (": ", PUN), ("[", PUN), ('"collabs"', STR), (", ", PUN),
     ('"OSS"', STR), (", ", PUN), ('"hard problems"', STR), ("],", PUN)],
    [("}", PUN), (" as", KW), (" const", KW), (";", PUN)],
]

CHAR_W = 7.22  # advance width of the mono stack at 12px
FONT = 12
TOP = 62
LEADING = 19.5
W = 860
H = TOP + len(LINES) * LEADING + 26


def build() -> str:
    rows = []
    for i, tokens in enumerate(LINES):
        y = TOP + i * LEADING
        col = 0
        spans = []
        for text, colour in tokens:
            spans.append(
                f'<tspan x="{62 + col * CHAR_W:.1f}" fill="{colour}">{gh.esc(text)}</tspan>'
            )
            col += len(text)
        rows.append(
            f'    <text y="{y:.1f}" class="ln">'
            f'<tspan x="30" fill="#4d5b7c">{i + 1:>2}</tspan>{"".join(spans)}</text>'
        )

    cursor_x = 62 + len(LINES[-1][0][0]) * CHAR_W + 4 * CHAR_W
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H:.0f}"
     role="img" aria-label="About Raunak, as a TypeScript object">
  <title>const raunak = {{ ... }}</title>
  <defs>
    <linearGradient id="cbg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{gh.BG0}"/><stop offset="100%" stop-color="{gh.BG1}"/>
    </linearGradient>
    <linearGradient id="cac" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#6929C4"/><stop offset="50%" stop-color="#1F6FEB"/>
      <stop offset="100%" stop-color="#00D4AA"/>
    </linearGradient>
    <style>
      .ln  {{ font-family:"JetBrains Mono","SFMono-Regular",Consolas,monospace;
              font-size:{FONT}px; }}
      .tab {{ font-family:"JetBrains Mono",Consolas,monospace; font-size:11.5px;
              fill:{gh.MUTED}; }}
    </style>
  </defs>

  <rect width="{W}" height="{H:.0f}" rx="12" fill="url(#cbg)"/>
  <rect x="1" y="1" width="{W - 2}" height="{H - 2:.0f}" rx="11" fill="none"
        stroke="url(#cac)" stroke-opacity="0.4" stroke-width="2"/>

  <!-- window chrome -->
  <path d="M1 13a12 12 0 0 1 12-12h834a12 12 0 0 1 12 12v25H1z" fill="#0b0e14" fill-opacity="0.8"/>
  <line x1="1" y1="38" x2="859" y2="38" stroke="{gh.LINE}"/>
  <circle cx="24" cy="20" r="5.5" fill="#FF5F57"/>
  <circle cx="43" cy="20" r="5.5" fill="#FEBC2E"/>
  <circle cx="62" cy="20" r="5.5" fill="#28C840"/>
  <text x="86" y="24" class="tab">raunak.ts</text>
  <text x="838" y="24" class="tab" text-anchor="end">TypeScript</text>

{chr(10).join(rows)}

  <rect x="{cursor_x:.1f}" y="{TOP + (len(LINES) - 1) * LEADING - 10:.1f}" width="8" height="14" fill="{gh.TEAL}">
    <animate attributeName="opacity" values="1;1;0;0" dur="1.1s" repeatCount="indefinite"/>
  </rect>
</svg>
'''


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(build(), encoding="utf-8")
    print(f"wrote {OUT.name}")


if __name__ == "__main__":
    main()
