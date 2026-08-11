#!/usr/bin/env python3
"""Build the section-header banners used across the profile README.

Plain markdown `##` headings looked bare next to the rest of the page. These
render as one banner per section: an accent-gradient rule, a vector glyph, and
a title. Glyphs are drawn as geometry rather than emoji, because emoji inside
an SVG depend on whatever font the viewer's machine happens to have.
"""

import pathlib

OUT_DIR = pathlib.Path(__file__).resolve().parent.parent / "assets" / "sections"

W, H = 860, 78

# slug, title, kicker, accent, glyph geometry (drawn inside a 0..24 box)
SECTIONS = [
    (
        "about", "About Me", "WHO I AM AND WHAT I BUILD", "#B191FF",
        '<circle cx="12" cy="8.5" r="4.2" fill="none" stroke="currentColor" stroke-width="2"/>'
        '<path d="M4.2 20.5c0-4.3 3.5-6.6 7.8-6.6s7.8 2.3 7.8 6.6" fill="none" '
        'stroke="currentColor" stroke-width="2" stroke-linecap="round"/>',
    ),
    (
        "stack", "Tech Stack", "LANGUAGES, FRAMEWORKS, INFRASTRUCTURE", "#79C0FF",
        '<path d="M12 2.6 22 8l-10 5.4L2 8z" fill="none" stroke="currentColor" '
        'stroke-width="2" stroke-linejoin="round"/>'
        '<path d="M2 13.2 12 18.6l10-5.4" fill="none" stroke="currentColor" '
        'stroke-width="2" stroke-linejoin="round"/>'
        '<path d="M2 18.2 12 23.6l10-5.4" fill="none" stroke="currentColor" '
        'stroke-width="2" stroke-linejoin="round" opacity="0.55"/>',
    ),
    (
        "quantum", "Quantum Computing", "SHIPPED, DEPLOYED, PUBLICLY USABLE", "#B191FF",
        '<circle cx="12" cy="12" r="2.6" fill="currentColor"/>'
        '<ellipse cx="12" cy="12" rx="10.4" ry="4.4" fill="none" stroke="currentColor" stroke-width="1.8"/>'
        '<ellipse cx="12" cy="12" rx="10.4" ry="4.4" fill="none" stroke="currentColor" '
        'stroke-width="1.8" transform="rotate(60 12 12)"/>'
        '<ellipse cx="12" cy="12" rx="10.4" ry="4.4" fill="none" stroke="currentColor" '
        'stroke-width="1.8" transform="rotate(120 12 12)"/>',
    ),
    (
        "apps", "App Development · AR / VR", "NATIVE, CROSS-PLATFORM, IMMERSIVE", "#7EE7C7",
        '<rect x="3" y="2.6" width="11" height="18.8" rx="2.4" fill="none" '
        'stroke="currentColor" stroke-width="2"/>'
        '<line x1="6.6" y1="18.4" x2="10.4" y2="18.4" stroke="currentColor" '
        'stroke-width="2" stroke-linecap="round"/>'
        '<path d="M16.4 8.6h3.4a2 2 0 0 1 2 2v3.6a2 2 0 0 1-2 2h-1l-1.4 2-1.4-2h-.6" '
        'fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>',
    ),
    (
        "projects", "Featured Projects", "THINGS THAT ACTUALLY RUN", "#F0A868",
        '<rect x="2.6" y="2.6" width="8.2" height="8.2" rx="1.8" fill="none" '
        'stroke="currentColor" stroke-width="2"/>'
        '<rect x="13.2" y="2.6" width="8.2" height="8.2" rx="1.8" fill="currentColor" opacity="0.85"/>'
        '<rect x="2.6" y="13.2" width="8.2" height="8.2" rx="1.8" fill="currentColor" opacity="0.85"/>'
        '<rect x="13.2" y="13.2" width="8.2" height="8.2" rx="1.8" fill="none" '
        'stroke="currentColor" stroke-width="2"/>',
    ),
    (
        "stats", "By the Numbers", "PULLED LIVE FROM THE GITHUB API", "#79C0FF",
        '<line x1="3" y1="21.4" x2="21" y2="21.4" stroke="currentColor" '
        'stroke-width="2" stroke-linecap="round"/>'
        '<rect x="4.4" y="13" width="3.8" height="6" rx="1.2" fill="currentColor"/>'
        '<rect x="10.1" y="8" width="3.8" height="11" rx="1.2" fill="currentColor"/>'
        '<rect x="15.8" y="3.4" width="3.8" height="15.6" rx="1.2" fill="currentColor"/>',
    ),
    (
        "snake", "Contribution Snake", "WATCH IT EAT A YEAR OF COMMITS", "#7EE7C7",
        '<rect x="2.4" y="9.6" width="4.6" height="4.6" rx="1.2" fill="currentColor" opacity="0.4"/>'
        '<rect x="8.2" y="9.6" width="4.6" height="4.6" rx="1.2" fill="currentColor" opacity="0.7"/>'
        '<rect x="14" y="9.6" width="4.6" height="4.6" rx="1.2" fill="currentColor"/>'
        '<circle cx="21.2" cy="11.9" r="1.5" fill="currentColor"/>',
    ),
    (
        "connect", "Connect", "OPEN TO COLLABORATION", "#F0A868",
        '<circle cx="6.4" cy="12" r="3.6" fill="none" stroke="currentColor" stroke-width="2"/>'
        '<circle cx="17.6" cy="6.6" r="3.2" fill="none" stroke="currentColor" stroke-width="2"/>'
        '<circle cx="17.6" cy="17.4" r="3.2" fill="none" stroke="currentColor" stroke-width="2"/>'
        '<line x1="9.6" y1="10.4" x2="14.6" y2="7.9" stroke="currentColor" stroke-width="2"/>'
        '<line x1="9.6" y1="13.6" x2="14.6" y2="16.1" stroke="currentColor" stroke-width="2"/>',
    ),
]


def build(slug: str, title: str, kicker: str, accent: str, glyph: str) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}"
     role="img" aria-label="{title}">
  <title>{title}</title>
  <defs>
    <linearGradient id="bg-{slug}" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%"   stop-color="{accent}" stop-opacity="0.16"/>
      <stop offset="55%"  stop-color="#0d1117" stop-opacity="0.55"/>
      <stop offset="100%" stop-color="#0d1117" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="rule-{slug}" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%"   stop-color="{accent}"/>
      <stop offset="60%"  stop-color="{accent}" stop-opacity="0.35"/>
      <stop offset="100%" stop-color="{accent}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="badge-{slug}" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%"   stop-color="{accent}" stop-opacity="0.30"/>
      <stop offset="100%" stop-color="{accent}" stop-opacity="0.08"/>
    </linearGradient>
    <filter id="soft-{slug}" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur stdDeviation="3.4" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <style>
      .t-{slug} {{ font-family:"Segoe UI",Inter,Helvetica,Arial,sans-serif;
                   font-size:27px; font-weight:800; fill:#ffffff; letter-spacing:-0.2px; }}
      .k-{slug} {{ font-family:"JetBrains Mono","SFMono-Regular",Consolas,monospace;
                   font-size:11px; font-weight:600; fill:{accent};
                   fill-opacity:0.75; letter-spacing:2px; }}
    </style>
  </defs>

  <rect x="0" y="0" width="{W}" height="{H}" rx="12" fill="url(#bg-{slug})"/>

  <!-- accent badge + vector glyph -->
  <rect x="14" y="19" width="40" height="40" rx="11" fill="url(#badge-{slug})"
        stroke="{accent}" stroke-opacity="0.45"/>
  <g transform="translate(22 27) scale(1.12)" color="{accent}" opacity="0.95">
    <g>{glyph}</g>
  </g>

  <text x="70" y="36" class="t-{slug}">{title}</text>
  <text x="71" y="55" class="k-{slug}">{kicker}</text>

  <!-- trailing rule with a travelling highlight -->
  <rect x="70" y="66" width="{W - 108}" height="2" rx="1" fill="url(#rule-{slug})" opacity="0.5"/>
  <rect y="66" width="90" height="2" rx="1" fill="{accent}" filter="url(#soft-{slug})">
    <animate attributeName="x" values="70;{W - 190};70" dur="7s"
             keyTimes="0;0.5;1" calcMode="spline"
             keySplines="0.45 0 0.55 1;0.45 0 0.55 1" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="0.15;0.75;0.15" dur="7s" repeatCount="indefinite"/>
  </rect>
</svg>
'''


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for slug, title, kicker, accent, glyph in SECTIONS:
        path = OUT_DIR / f"{slug}.svg"
        path.write_text(build(slug, title, kicker, accent, glyph), encoding="utf-8")
        print(f"wrote {path.name}")


if __name__ == "__main__":
    main()
