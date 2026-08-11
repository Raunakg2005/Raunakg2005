#!/usr/bin/env python3
"""Build a self-hosted language-mix SVG for the profile README.

The usual github-readme-stats instances share one GitHub API quota and answer
with "Something went wrong! Maximum retries exceeded" once it runs dry. This
computes the same numbers from the API directly, using the workflow's own
GITHUB_TOKEN, and commits a static SVG — so there is no third party left to
rate-limit us.
"""

import collections
import json
import os
import pathlib
import urllib.error
import urllib.request

USER = "Raunakg2005"
OUT = pathlib.Path(__file__).resolve().parent.parent / "assets" / "lang-stats.svg"
TOP_N = 8

# Language -> brand colour, matching GitHub's linguist palette.
COLOURS = {
    "TypeScript": "#3178C6", "JavaScript": "#F1E05A", "Python": "#3572A5",
    "CSS": "#563D7C", "HTML": "#E34C26", "C#": "#178600", "Swift": "#F05138",
    "Dart": "#00B4AB", "C++": "#F34B7D", "C": "#555555", "Java": "#B07219",
    "Kotlin": "#A97BFF", "PHP": "#4F5D95", "Solidity": "#AA6746",
    "ShaderLab": "#222C37", "HLSL": "#AACE60", "Jupyter Notebook": "#DA5B0B",
    "Dockerfile": "#384D54", "Shell": "#89E051", "Mathematica": "#DD1100",
    "Objective-C": "#438EFF", "Jac": "#8A3FFC", "TeX": "#3D6117",
    "PowerShell": "#012456", "CMake": "#DA3434", "Hack": "#878787",
    "Batchfile": "#C1F12E", "Wolfram Language": "#DD1100", "Mako": "#7E858D",
    "Procfile": "#6E7681",
}
FALLBACK = "#8B949E"


def api(path: str):
    req = urllib.request.Request(
        f"https://api.github.com/{path}",
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "readme-builder",
        },
    )
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read())


def collect() -> tuple[collections.Counter, int, int]:
    totals: collections.Counter = collections.Counter()
    repos, stars, page = 0, 0, 1
    while True:
        batch = api(f"users/{USER}/repos?per_page=100&page={page}&type=owner")
        if not batch:
            break
        for repo in batch:
            if repo.get("fork"):
                continue
            repos += 1
            stars += repo.get("stargazers_count", 0)
            try:
                totals.update(api(f"repos/{USER}/{repo['name']}/languages"))
            except urllib.error.HTTPError:
                pass  # empty or inaccessible repo — just skip it
        page += 1
    return totals, repos, stars


def build(totals: collections.Counter, repos: int, stars: int) -> str:
    grand = sum(totals.values()) or 1
    top = totals.most_common(TOP_N)
    other = grand - sum(v for _, v in top)
    rows = [(name, val / grand * 100) for name, val in top]
    if other > 0:
        rows.append(("Other", other / grand * 100))

    # stacked bar
    bar, x = [], 22.0
    width = 476.0
    for i, (name, pct) in enumerate(rows):
        w = max(width * pct / 100, 1.5)
        colour = COLOURS.get(name, FALLBACK)
        radius = ' rx="4"' if i in (0, len(rows) - 1) else ""
        bar.append(
            f'    <rect x="{x:.1f}" y="74" width="{w:.1f}" height="16"{radius} fill="{colour}">\n'
            f'      <animate attributeName="height" values="0;16" dur="0.7s" '
            f'begin="{i * 0.07:.2f}s" fill="freeze"/>\n'
            f'      <animate attributeName="y" values="90;74" dur="0.7s" '
            f'begin="{i * 0.07:.2f}s" fill="freeze"/>\n'
            f"    </rect>"
        )
        x += w

    # two-column legend
    legend = []
    for i, (name, pct) in enumerate(rows):
        col, row = i % 2, i // 2
        lx = 22 + col * 250
        ly = 124 + row * 26
        colour = COLOURS.get(name, FALLBACK)
        label = name if len(name) <= 16 else name[:15] + "…"
        legend.append(
            f'    <g opacity="0">\n'
            f'      <animate attributeName="opacity" values="0;1" dur="0.45s" '
            f'begin="{0.25 + i * 0.06:.2f}s" fill="freeze"/>\n'
            f'      <circle cx="{lx + 5}" cy="{ly - 4}" r="5.5" fill="{colour}"/>\n'
            f'      <text x="{lx + 18}" y="{ly}" class="lg">{label}</text>\n'
            f'      <text x="{lx + 218}" y="{ly}" class="pc" text-anchor="end">{pct:.1f}%</text>\n'
            f"    </g>"
        )

    langs = len(totals)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 300" width="520" height="300"
     role="img" aria-label="Language mix across {repos} public repositories">
  <title>Language mix — {repos} public repos, {langs} languages</title>
  <defs>
    <linearGradient id="lbg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0d1117"/><stop offset="100%" stop-color="#161b28"/>
    </linearGradient>
    <linearGradient id="lac" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#6929C4"/><stop offset="50%" stop-color="#1F6FEB"/>
      <stop offset="100%" stop-color="#00D4AA"/>
    </linearGradient>
    <style>
      .ttl {{ font-family:"Segoe UI",Inter,Helvetica,sans-serif; font-size:16px;
              font-weight:700; fill:#7EE7C7; }}
      .lg  {{ font-family:"Segoe UI",Inter,Helvetica,sans-serif; font-size:12.5px; fill:#C9D1D9; }}
      .pc  {{ font-family:"JetBrains Mono",Consolas,monospace; font-size:12px; fill:#8B949E; }}
      .kv  {{ font-family:"JetBrains Mono",Consolas,monospace; font-size:19px;
              font-weight:700; fill:#79C0FF; }}
      .kl  {{ font-family:"Segoe UI",Inter,Helvetica,sans-serif; font-size:10px;
              fill:#6E7A91; letter-spacing:1.1px; }}
    </style>
  </defs>

  <rect width="520" height="300" rx="12" fill="url(#lbg)"/>
  <rect x="1" y="1" width="518" height="298" rx="11" fill="none"
        stroke="url(#lac)" stroke-opacity="0.4" stroke-width="2"/>

  <text x="22" y="34" class="ttl">◈ Language Mix</text>
  <text x="22" y="56" class="pc">across {repos} public repositories</text>

{chr(10).join(bar)}

{chr(10).join(legend)}

  <line x1="22" y1="236" x2="498" y2="236" stroke="#30363D" stroke-width="1"/>
  <g>
    <text x="60"  y="266" class="kv" text-anchor="middle">{repos}</text>
    <text x="60"  y="282" class="kl" text-anchor="middle">REPOS</text>
    <text x="200" y="266" class="kv" text-anchor="middle">{langs}</text>
    <text x="200" y="282" class="kl" text-anchor="middle">LANGUAGES</text>
    <text x="340" y="266" class="kv" text-anchor="middle">{stars}</text>
    <text x="340" y="282" class="kl" text-anchor="middle">STARS</text>
    <text x="460" y="266" class="kv" text-anchor="middle">{grand // 1_000_000}M</text>
    <text x="460" y="282" class="kl" text-anchor="middle">BYTES</text>
  </g>
</svg>
'''


def main() -> None:
    totals, repos, stars = collect()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(build(totals, repos, stars), encoding="utf-8")
    print(f"wrote {OUT} — {repos} repos, {len(totals)} languages, {stars} stars")


if __name__ == "__main__":
    main()
