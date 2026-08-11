#!/usr/bin/env python3
"""Build a self-hosted contribution-streak SVG for the profile README.

streak-stats.demolab.com answers a direct request fine but is slow enough that
GitHub's camo image proxy gives up with a 504, so the card renders broken on
the profile. This computes the same figures from the GraphQL contributions
calendar and commits a static SVG instead.
"""

import datetime as dt
import pathlib

import gh

OUT = pathlib.Path(__file__).resolve().parent.parent / "assets" / "streak.svg"

QUERY = """
query($login:String!, $from:DateTime!, $to:DateTime!) {
  user(login:$login) {
    createdAt
    contributionsCollection(from:$from, to:$to) {
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount } }
      }
    }
  }
}
"""


def graphql(variables: dict) -> dict:
    return gh.graphql(QUERY, variables)["user"]


def collect_days() -> dict[dt.date, int]:
    """Walk year-sized windows from account creation to today.

    contributionsCollection caps each query at one year, so a single call
    cannot see a streak that started earlier.
    """
    today = dt.date.today()
    first = graphql(
        {
            "login": gh.USER,
            "from": f"{today.year}-01-01T00:00:00Z",
            "to": f"{today.isoformat()}T00:00:00Z",
        }
    )
    created = dt.datetime.fromisoformat(first["createdAt"].replace("Z", "+00:00")).date()

    days: dict[dt.date, int] = {}
    start = dt.date(created.year, 1, 1)
    while start <= today:
        end = min(dt.date(start.year, 12, 31), today)
        data = graphql(
            {
                "login": gh.USER,
                "from": f"{start.isoformat()}T00:00:00Z",
                "to": f"{end.isoformat()}T23:59:59Z",
            }
        )
        for week in data["contributionsCollection"]["contributionCalendar"]["weeks"]:
            for day in week["contributionDays"]:
                days[dt.date.fromisoformat(day["date"])] = day["contributionCount"]
        start = dt.date(start.year + 1, 1, 1)
    return days


def streaks(days: dict[dt.date, int]) -> dict:
    today = dt.date.today()
    ordered = sorted(d for d in days if d <= today)
    total = sum(days[d] for d in ordered)

    # longest run of consecutive active days
    longest = run = 0
    l_start = l_end = run_start = None
    prev = None
    for d in ordered:
        if days[d] > 0:
            if prev is not None and (d - prev).days == 1 and run > 0:
                run += 1
            else:
                run, run_start = 1, d
            if run > longest:
                longest, l_start, l_end = run, run_start, d
            prev = d
        else:
            run, prev = 0, d

    # current streak — today not yet committed does not break it
    current, c_start = 0, None
    cursor = today
    if days.get(today, 0) == 0:
        cursor = today - dt.timedelta(days=1)
    while days.get(cursor, 0) > 0:
        current += 1
        c_start = cursor
        cursor -= dt.timedelta(days=1)

    return {
        "total": total,
        "first": ordered[0] if ordered else today,
        "current": current,
        "c_start": c_start,
        "c_end": today if current else None,
        "longest": longest,
        "l_start": l_start,
        "l_end": l_end,
    }


def fmt(d) -> str:
    # Built by hand rather than with %-d, which is a glibc extension and
    # raises ValueError on Windows.
    return f"{d:%b} {d.day}, {d.year}" if d else "—"


def build(s: dict) -> str:
    ring = 54
    circ = 2 * 3.14159265 * ring
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 300" width="520" height="300"
     role="img" aria-label="Contribution streak">
  <title>Contributions — {s["total"]} total, {s["current"]}-day current streak</title>
  <defs>
    <linearGradient id="sbg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0d1117"/><stop offset="100%" stop-color="#161b28"/>
    </linearGradient>
    <linearGradient id="sac" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#6929C4"/><stop offset="50%" stop-color="#1F6FEB"/>
      <stop offset="100%" stop-color="#00D4AA"/>
    </linearGradient>
    <filter id="sglow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="4" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <style>
      .big {{ font-family:"JetBrains Mono",Consolas,monospace; font-size:34px;
              font-weight:800; fill:#ffffff; }}
      .mid {{ font-family:"JetBrains Mono",Consolas,monospace; font-size:27px;
              font-weight:700; fill:#79C0FF; }}
      .lbl {{ font-family:"Segoe UI",Inter,Helvetica,sans-serif; font-size:12px;
              font-weight:600; fill:#C9D1D9; letter-spacing:0.4px; }}
      .sub {{ font-family:"Segoe UI",Inter,Helvetica,sans-serif; font-size:10px; fill:#6E7A91; }}
      .ttl {{ font-family:"Segoe UI",Inter,Helvetica,sans-serif; font-size:16px;
              font-weight:700; fill:#7EE7C7; }}
    </style>
  </defs>

  <rect width="520" height="300" rx="12" fill="url(#sbg)"/>
  <rect x="1" y="1" width="518" height="298" rx="11" fill="none"
        stroke="url(#sac)" stroke-opacity="0.4" stroke-width="2"/>

  <text x="22" y="34" class="ttl">◈ Contribution Streak</text>

  <!-- total -->
  <g>
    <text x="92" y="132" class="big" text-anchor="middle">{s["total"]}</text>
    <text x="92" y="156" class="lbl" text-anchor="middle">Total Contributions</text>
    <text x="92" y="174" class="sub" text-anchor="middle">{fmt(s["first"])} — Present</text>
  </g>
  <line x1="178" y1="70" x2="178" y2="230" stroke="#30363D" stroke-width="1"/>

  <!-- current streak, ringed -->
  <g>
    <circle cx="260" cy="128" r="{ring}" fill="none" stroke="#21262D" stroke-width="6"/>
    <circle cx="260" cy="128" r="{ring}" fill="none" stroke="#00D4AA" stroke-width="6"
            stroke-linecap="round" filter="url(#sglow)"
            stroke-dasharray="{circ:.1f}" stroke-dashoffset="{circ:.1f}"
            transform="rotate(-90 260 128)">
      <animate attributeName="stroke-dashoffset" from="{circ:.1f}"
               to="{circ * 0.12:.1f}" dur="1.2s" fill="freeze"/>
    </circle>
    <text x="260" y="122" class="big" text-anchor="middle">{s["current"]}</text>
    <text x="260" y="146" class="sub" text-anchor="middle">🔥 day streak</text>
    <text x="260" y="204" class="lbl" text-anchor="middle">Current Streak</text>
    <text x="260" y="222" class="sub" text-anchor="middle">{fmt(s["c_start"])} — {fmt(s["c_end"])}</text>
  </g>
  <line x1="342" y1="70" x2="342" y2="230" stroke="#30363D" stroke-width="1"/>

  <!-- longest streak -->
  <g>
    <text x="430" y="132" class="mid" text-anchor="middle">{s["longest"]}</text>
    <text x="430" y="156" class="lbl" text-anchor="middle">Longest Streak</text>
    <text x="430" y="174" class="sub" text-anchor="middle">{fmt(s["l_start"])} — {fmt(s["l_end"])}</text>
  </g>

  <line x1="22" y1="256" x2="498" y2="256" stroke="#30363D" stroke-width="1"/>
  <text x="260" y="278" class="sub" text-anchor="middle">generated in-repo from the GitHub contributions API</text>
</svg>
'''


def main() -> None:
    stats = streaks(collect_days())
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(build(stats), encoding="utf-8")
    print(
        f"wrote {OUT} — total={stats['total']} "
        f"current={stats['current']} longest={stats['longest']}"
    )


if __name__ == "__main__":
    main()
