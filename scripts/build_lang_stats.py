#!/usr/bin/env python3
"""Build a self-hosted language-mix SVG for the profile README.

The usual github-readme-stats instances share one GitHub API quota and answer
with "Something went wrong! Maximum retries exceeded" once it runs dry. This
computes the same numbers from the API directly, using the workflow's own
GITHUB_TOKEN, and commits a static SVG — so there is no third party left to
rate-limit us.
"""

import collections
import pathlib
import urllib.error

import gh

OUT = pathlib.Path(__file__).resolve().parent.parent / "assets" / "lang-stats.svg"
TOP_N = 8





def collect() -> tuple[collections.Counter, int, int]:
    """Weight every repo equally instead of summing raw bytes.

    Raw byte totals are meaningless here: a single Unity project vendors a
    ~650MB C++ engine SDK, which alone was rendering the card as "85% C++".
    Normalising within each repo first, then averaging, means one repo full of
    third-party code cannot drown out the other fifty-odd.
    """
    totals: collections.Counter = collections.Counter()
    repos, stars, page = 0, 0, 1
    while True:
        batch = gh.api(f"users/{gh.USER}/repos?per_page=100&page={page}&type=owner")
        if not batch:
            break
        for repo in batch:
            if repo.get("fork"):
                continue
            repos += 1
            stars += repo.get("stargazers_count", 0)
            try:
                langs = gh.api(f"repos/{gh.USER}/{repo['name']}/languages")
            except urllib.error.HTTPError:
                continue  # empty or inaccessible repo — just skip it
            repo_bytes = sum(langs.values())
            if not repo_bytes:
                continue
            for name, size in langs.items():
                totals[name] += size / repo_bytes  # this repo's share, capped at 1.0
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
        colour = gh.lang_colour(name)
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
        colour = gh.lang_colour(name)
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
      .tl  {{ font-family:"JetBrains Mono",Consolas,monospace; font-size:15px;
              font-weight:700; fill:#79C0FF; }}
    </style>
  </defs>

  <rect width="520" height="300" rx="12" fill="url(#lbg)"/>
  <rect x="1" y="1" width="518" height="298" rx="11" fill="none"
        stroke="url(#lac)" stroke-opacity="0.4" stroke-width="2"/>

  <text x="22" y="34" class="ttl">◈ Language Mix</text>
  <text x="22" y="56" class="pc">{repos} public repos · each weighted equally</text>

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
    <text x="460" y="264" class="tl" text-anchor="middle">{rows[0][0]}</text>
    <text x="460" y="282" class="kl" text-anchor="middle">MOST USED</text>
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
