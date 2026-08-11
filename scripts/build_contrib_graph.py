#!/usr/bin/env python3
"""Render the last year of contributions as a heatmap calendar.

The third-party activity-graph service draws a line chart, which says very
little. A real calendar grid shows the actual shape of a year's work, and
building it here keeps it on-brand and independent of anyone else's uptime.
"""

import datetime as dt
import pathlib

import gh

OUT = pathlib.Path(__file__).resolve().parent.parent / "assets" / "contrib-graph.svg"

QUERY = """
query($login:String!, $from:DateTime!, $to:DateTime!) {
  user(login:$login) {
    contributionsCollection(from:$from, to:$to) {
      contributionCalendar {
        totalContributions
        weeks { firstDay contributionDays { date weekday contributionCount } }
      }
    }
  }
}
"""

CELL, GAP = 12, 3
LEFT, TOP = 46, 62
EMPTY = "#1b2130"
STEPS = ["#0e4429", "#1c7a52", "#2ea97a", "#7EE7C7"]
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def fetch():
    today = dt.date.today()
    start = today - dt.timedelta(days=364)
    data = gh.graphql(
        QUERY,
        {
            "login": gh.USER,
            "from": f"{start.isoformat()}T00:00:00Z",
            "to": f"{today.isoformat()}T23:59:59Z",
        },
    )
    cal = data["user"]["contributionsCollection"]["contributionCalendar"]
    return cal["weeks"], cal["totalContributions"]


def shade(count: int, peak: int) -> str:
    if count <= 0:
        return EMPTY
    # Quartiles of the busiest day, so the scale adapts to the actual range.
    for i, cut in enumerate((0.25, 0.5, 0.75)):
        if count <= max(peak * cut, i + 1):
            return STEPS[i]
    return STEPS[3]


def build(weeks, total) -> str:
    peak = max(
        (d["contributionCount"] for w in weeks for d in w["contributionDays"]), default=1
    ) or 1
    width = LEFT + len(weeks) * (CELL + GAP) + 22
    height = TOP + 7 * (CELL + GAP) + 56

    cells, months, seen = [], [], set()
    for wi, week in enumerate(weeks):
        x = LEFT + wi * (CELL + GAP)
        first = dt.date.fromisoformat(week["firstDay"])
        if first.month not in seen and first.day <= 7:
            seen.add(first.month)
            months.append(
                f'  <text x="{x}" y="{TOP - 10}" class="mo">{MONTHS[first.month - 1]}</text>'
            )
        for day in week["contributionDays"]:
            y = TOP + day["weekday"] * (CELL + GAP)
            n = day["contributionCount"]
            delay = (wi * 7 + day["weekday"]) * 0.0016
            cells.append(
                f'  <rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2.6" '
                f'fill="{shade(n, peak)}" opacity="0">'
                f'<animate attributeName="opacity" values="0;1" dur="0.35s" '
                f'begin="{delay:.3f}s" fill="freeze"/>'
                f'<title>{n} on {day["date"]}</title></rect>'
            )

    legend_x = width - 178
    legend = [
        f'  <rect x="{legend_x + 34 + i * 16}" y="{height - 30}" width="{CELL}" '
        f'height="{CELL}" rx="2.6" fill="{c}"/>'
        for i, c in enumerate([EMPTY, *STEPS])
    ]

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}"
     width="{width}" height="{height}" role="img"
     aria-label="{total} contributions in the last year">
  <title>{total} contributions in the last year</title>
  <defs>
    <linearGradient id="gbg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{gh.BG0}"/><stop offset="100%" stop-color="{gh.BG1}"/>
    </linearGradient>
    <linearGradient id="gac" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#6929C4"/><stop offset="50%" stop-color="#1F6FEB"/>
      <stop offset="100%" stop-color="#00D4AA"/>
    </linearGradient>
    <style>
      .ttl {{ font-family:"Segoe UI",Inter,Helvetica,sans-serif; font-size:16px;
              font-weight:700; fill:{gh.TEAL}; }}
      .sub {{ font-family:"JetBrains Mono",Consolas,monospace; font-size:11.5px; fill:{gh.MUTED}; }}
      .mo  {{ font-family:"Segoe UI",Inter,Helvetica,sans-serif; font-size:10.5px; fill:{gh.DIM}; }}
      .dy  {{ font-family:"Segoe UI",Inter,Helvetica,sans-serif; font-size:10px; fill:{gh.DIM}; }}
      .lg  {{ font-family:"Segoe UI",Inter,Helvetica,sans-serif; font-size:10px; fill:{gh.DIM}; }}
    </style>
  </defs>

  <rect width="{width}" height="{height}" rx="12" fill="url(#gbg)"/>
  <rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="11" fill="none"
        stroke="url(#gac)" stroke-opacity="0.4" stroke-width="2"/>

  <text x="22" y="32" class="ttl">◈ Contribution Calendar</text>
  <text x="{width - 22}" y="32" class="sub" text-anchor="end">{total} in the last year</text>

{chr(10).join(months)}

  <text x="20" y="{TOP + CELL - 2}" class="dy">M</text>
  <text x="20" y="{TOP + 2 * (CELL + GAP) + CELL - 2}" class="dy">W</text>
  <text x="20" y="{TOP + 4 * (CELL + GAP) + CELL - 2}" class="dy">F</text>

{chr(10).join(cells)}

  <text x="{legend_x}" y="{height - 20}" class="lg">Less</text>
{chr(10).join(legend)}
  <text x="{legend_x + 124}" y="{height - 20}" class="lg">More</text>
</svg>
'''


def main() -> None:
    weeks, total = fetch()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(build(weeks, total), encoding="utf-8")
    print(f"wrote {OUT.name} — {total} contributions across {len(weeks)} weeks")


if __name__ == "__main__":
    main()
