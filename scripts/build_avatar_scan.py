#!/usr/bin/env python3
"""Build the animated avatar-scanner SVG for the profile README.

GitHub renders README images through camo, and an SVG loaded via <img> is not
allowed to fetch external resources. So the avatar has to be inlined as a
base64 data URI. This script pulls the live GitHub avatar and bakes it in,
which means the banner refreshes itself whenever the avatar changes.
"""

import base64
import pathlib
import urllib.request

USER = "Raunakg2005"
AVATAR_URL = f"https://github.com/{USER}.png?size=460"
OUT = pathlib.Path(__file__).resolve().parent.parent / "assets" / "avatar-scan.svg"

# Sweep chips shown to the right of the portrait.
CHIPS = [
    ("QUANTUM", "#B191FF"),
    ("AI / ML", "#7EE7C7"),
    ("WEB3", "#F0A868"),
    ("FULL STACK", "#79C0FF"),
]

READOUT = [
    "> init scan --target profile",
    "> resolving stack .............. 29 langs",
    "> repositories ................. 59 public",
    "> status ....................... SHIPPING",
]


def fetch_avatar_data_uri() -> str:
    req = urllib.request.Request(AVATAR_URL, headers={"User-Agent": "readme-builder"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        raw = resp.read()
    return "data:image/png;base64," + base64.b64encode(raw).decode("ascii")


def build(avatar_uri: str) -> str:
    cx, cy, r = 168, 160, 96

    chips = []
    for i, (label, colour) in enumerate(CHIPS):
        x = 320 + (i % 2) * 168
        y = 196 + (i // 2) * 38
        delay = f"{i * 0.18:.2f}s"
        chips.append(
            f'''    <g opacity="0">
      <animate attributeName="opacity" values="0;1" dur="0.5s" begin="{delay}" fill="freeze"/>
      <rect x="{x}" y="{y}" width="150" height="27" rx="13.5"
            fill="{colour}" fill-opacity="0.10" stroke="{colour}" stroke-opacity="0.55"/>
      <text x="{x + 75}" y="{y + 18}" text-anchor="middle" class="chip" fill="{colour}">{label}</text>
    </g>'''
        )

    readout = []
    for i, line in enumerate(READOUT):
        y = 96 + i * 21
        begin = f"{0.5 + i * 0.35:.2f}s"
        readout.append(
            f'''    <text x="320" y="{y}" class="mono" opacity="0">{line}
      <animate attributeName="opacity" values="0;0.85" dur="0.4s" begin="{begin}" fill="freeze"/>
    </text>'''
        )

    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
     viewBox="0 0 860 320" width="860" height="320" role="img"
     aria-label="Raunak Kumar Gupta — animated profile scan">
  <title>Raunak Kumar Gupta — profile scan</title>

  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%"   stop-color="#0d1117"/>
      <stop offset="55%"  stop-color="#131a2b"/>
      <stop offset="100%" stop-color="#1b1330"/>
    </linearGradient>

    <linearGradient id="edge" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%"   stop-color="#6929C4"/>
      <stop offset="50%"  stop-color="#1F6FEB"/>
      <stop offset="100%" stop-color="#00D4AA"/>
    </linearGradient>

    <linearGradient id="beam" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%"   stop-color="#00D4AA" stop-opacity="0"/>
      <stop offset="45%"  stop-color="#00D4AA" stop-opacity="0.85"/>
      <stop offset="55%"  stop-color="#7EE7C7" stop-opacity="1"/>
      <stop offset="100%" stop-color="#00D4AA" stop-opacity="0"/>
    </linearGradient>

    <radialGradient id="vig" cx="50%" cy="50%" r="70%">
      <stop offset="60%"  stop-color="#000" stop-opacity="0"/>
      <stop offset="100%" stop-color="#000" stop-opacity="0.55"/>
    </radialGradient>

    <pattern id="grid" width="26" height="26" patternUnits="userSpaceOnUse">
      <path d="M26 0H0V26" fill="none" stroke="#1F6FEB" stroke-opacity="0.13" stroke-width="1"/>
    </pattern>

    <pattern id="scanlines" width="4" height="4" patternUnits="userSpaceOnUse">
      <rect width="4" height="1.4" fill="#7EE7C7" fill-opacity="0.16"/>
    </pattern>

    <clipPath id="portrait">
      <circle cx="{cx}" cy="{cy}" r="{r}"/>
    </clipPath>

    <clipPath id="card">
      <rect x="0" y="0" width="860" height="320" rx="20"/>
    </clipPath>

    <filter id="glow" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur stdDeviation="5" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>

    <!-- The moving window that the scan beam reveals through. -->
    <mask id="sweep">
      <rect x="0" y="0" width="860" height="320" fill="black"/>
      <rect x="0" width="860" height="46" fill="url(#beam)">
        <animate attributeName="y" values="52;222;52" dur="4.6s"
                 keyTimes="0;0.5;1" calcMode="spline"
                 keySplines="0.45 0 0.55 1;0.45 0 0.55 1" repeatCount="indefinite"/>
      </rect>
    </mask>

    <style>
      .mono {{ font-family: "JetBrains Mono","SFMono-Regular",Consolas,monospace;
               font-size: 13px; fill: #7EE7C7; }}
      .chip {{ font-family: "JetBrains Mono","SFMono-Regular",Consolas,monospace;
               font-size: 11.5px; font-weight: 700; letter-spacing: 1.2px; }}
      .name {{ font-family: "Segoe UI",Inter,Helvetica,Arial,sans-serif;
               font-size: 38px; font-weight: 800; fill: #ffffff; letter-spacing: -0.5px; }}
      .role {{ font-family: "Segoe UI",Inter,Helvetica,Arial,sans-serif;
               font-size: 14.5px; font-weight: 600; fill: #A9B6D0; letter-spacing: 2.6px; }}
      .tick {{ font-family: "JetBrains Mono",Consolas,monospace; font-size: 9px; fill: #4d5b7c; }}
    </style>
  </defs>

  <g clip-path="url(#card)">
    <rect width="860" height="320" fill="url(#bg)"/>
    <rect width="860" height="320" fill="url(#grid)"/>
    <rect width="860" height="320" fill="url(#vig)"/>

    <!-- ── left: the scanned portrait ── -->
    <g>
      <!-- dim base pass -->
      <image xlink:href="{avatar_uri}" x="{cx - r}" y="{cy - r}" width="{r * 2}" height="{r * 2}"
             clip-path="url(#portrait)" opacity="0.38" preserveAspectRatio="xMidYMid slice"/>

      <!-- bright pass, revealed only inside the travelling beam -->
      <g mask="url(#sweep)">
        <image xlink:href="{avatar_uri}" x="{cx - r}" y="{cy - r}" width="{r * 2}" height="{r * 2}"
               clip-path="url(#portrait)" preserveAspectRatio="xMidYMid slice"/>
        <circle cx="{cx}" cy="{cy}" r="{r}" fill="#00D4AA" fill-opacity="0.22"/>
      </g>

      <circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#scanlines)" clip-path="url(#portrait)" opacity="0.5"/>

      <!-- the beam edge itself -->
      <g clip-path="url(#portrait)">
        <rect x="{cx - r}" width="{r * 2}" height="2.2" fill="#7EE7C7" filter="url(#glow)">
          <animate attributeName="y" values="{cy - r};{cy + r};{cy - r}" dur="4.6s"
                   keyTimes="0;0.5;1" calcMode="spline"
                   keySplines="0.45 0 0.55 1;0.45 0 0.55 1" repeatCount="indefinite"/>
        </rect>
      </g>

      <!-- rim + counter-rotating reticles -->
      <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="url(#edge)" stroke-width="2.5"/>
      <circle cx="{cx}" cy="{cy}" r="{r + 11}" fill="none" stroke="#1F6FEB" stroke-opacity="0.5"
              stroke-width="1.4" stroke-dasharray="16 10">
        <animateTransform attributeName="transform" type="rotate"
                          from="0 {cx} {cy}" to="360 {cx} {cy}" dur="16s" repeatCount="indefinite"/>
      </circle>
      <circle cx="{cx}" cy="{cy}" r="{r + 20}" fill="none" stroke="#6929C4" stroke-opacity="0.42"
              stroke-width="1.2" stroke-dasharray="3 13">
        <animateTransform attributeName="transform" type="rotate"
                          from="360 {cx} {cy}" to="0 {cx} {cy}" dur="24s" repeatCount="indefinite"/>
      </circle>

      <!-- targeting brackets -->
      <g stroke="#00D4AA" stroke-width="2.2" fill="none" stroke-linecap="round" opacity="0.9">
        <path d="M{cx - r - 28} {cy - r + 4} v-26 h26"/>
        <path d="M{cx + r + 28} {cy - r + 4} v-26 h-26"/>
        <path d="M{cx - r - 28} {cy + r - 4} v26 h26"/>
        <path d="M{cx + r + 28} {cy + r - 4} v26 h-26"/>
        <animate attributeName="opacity" values="0.9;0.35;0.9" dur="2.6s" repeatCount="indefinite"/>
      </g>

      <text x="{cx}" y="{cy + r + 44}" text-anchor="middle" class="tick">◈ SCANNING ◈</text>
    </g>

    <!-- ── right: identity readout ── -->
    <text x="320" y="56" class="name">Raunak Kumar Gupta</text>
    <text x="322" y="76" class="role">FULL STACK · AI/ML · WEB3 · QUANTUM</text>

{chr(10).join(readout)}

{chr(10).join(chips)}

    <!-- travelling underline -->
    <rect x="320" y="286" width="470" height="2" rx="1" fill="#1F6FEB" fill-opacity="0.25"/>
    <rect y="286" width="120" height="2" rx="1" fill="url(#edge)">
      <animate attributeName="x" values="320;670;320" dur="4.6s"
               keyTimes="0;0.5;1" calcMode="spline"
               keySplines="0.45 0 0.55 1;0.45 0 0.55 1" repeatCount="indefinite"/>
    </rect>

    <rect x="1" y="1" width="858" height="318" rx="19" fill="none"
          stroke="url(#edge)" stroke-opacity="0.45" stroke-width="2"/>
  </g>
</svg>
'''


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(build(fetch_avatar_data_uri()), encoding="utf-8")
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
