#!/usr/bin/env python3
"""Build the About-Me card. Four styles; pick one with --style.

    python scripts/build_about_card.py --style circuit --out assets/about-card.svg

Every style is a self-contained animated SVG so it works through GitHub's
image proxy, which runs no scripts and loads no external resources.
"""

import argparse
import pathlib

import gh

NAME = "Raunak Kumar Gupta"
# Single-quoted family names: these land inside double-quoted style="" attributes,
# and nesting double quotes there is not well-formed XML.
MONO = "'JetBrains Mono','SFMono-Regular',Consolas,monospace"
SANS = "'Segoe UI',Inter,Helvetica,Arial,sans-serif"
W = 860


def frame(h, uid, body, extra_defs="") -> str:
    """Shared shell: rounded dark panel with the gradient edge every card uses."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {h}" width="{W}" height="{h}"
     role="img" aria-label="About {NAME}">
  <title>{NAME} — full stack, app, AI/ML, DevOps, Web3 and quantum</title>
  <defs>
    <linearGradient id="bg{uid}" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{gh.BG0}"/><stop offset="100%" stop-color="{gh.BG1}"/>
    </linearGradient>
    <linearGradient id="ac{uid}" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#6929C4"/><stop offset="50%" stop-color="#1F6FEB"/>
      <stop offset="100%" stop-color="#00D4AA"/>
    </linearGradient>
    <filter id="gl{uid}" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur stdDeviation="3.2" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
{extra_defs}
  </defs>
  <rect width="{W}" height="{h}" rx="14" fill="url(#bg{uid})"/>
  <rect x="1" y="1" width="{W - 2}" height="{h - 2}" rx="13" fill="none"
        stroke="url(#ac{uid})" stroke-opacity="0.45" stroke-width="2"/>
{body}
</svg>
'''


# ─────────────────────────────  1. quantum circuit  ─────────────────────────────

def circuit() -> str:
    h = 330
    wires = [
        ("FULL STACK", "TypeScript · Next.js · Node", gh.BLUE, "H"),
        ("APP / MOBILE", "Flutter · SwiftUI · Kotlin", gh.TEAL, "X"),
        ("AI / ML", "PyTorch · TensorFlow", "#FF7B72", "H"),
        ("WEB3", "Solidity · Ethereum", gh.AMBER, "Z"),
        ("QUANTUM", "Qiskit · QKD · BB84", gh.PURPLE, "H"),
        ("DEVOPS / MLOPS", "Docker · K8s · MLflow", "#A5D6FF", "X"),
    ]
    top, step = 76, 38
    x_gate, x_ctrl, x_box, x_meter = 108, 168, 214, 470

    parts = [
        f'  <text x="26" y="34" style="font:700 17px {SANS};fill:{gh.TEAL}">◈ whoami()</text>',
        f'  <text x="{W - 26}" y="34" text-anchor="end" '
        f'style="font:600 11px {MONO};fill:{gh.DIM};letter-spacing:1.6px">'
        f'6-QUBIT IDENTITY REGISTER</text>',
    ]

    for i, (label, sub, colour, gate) in enumerate(wires):
        y = top + i * step
        d = i * 0.14
        parts.append(
            f'  <text x="26" y="{y + 4}" style="font:600 12px {MONO};fill:{gh.DIM}">|0⟩</text>\n'
            f'  <line x1="56" y1="{y}" x2="{W - 30}" y2="{y}" stroke="{gh.LINE}" stroke-width="1.6"/>'
        )
        # a pulse travelling down the wire
        parts.append(
            f'  <circle cy="{y}" r="3.4" fill="{colour}" filter="url(#gl1)" opacity="0.9">'
            f'<animate attributeName="cx" values="56;{W - 30}" dur="3.6s" '
            f'begin="{d:.2f}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0;1;1;0" dur="3.6s" '
            f'begin="{d:.2f}s" repeatCount="indefinite"/></circle>'
        )
        # single-qubit gate
        parts.append(
            f'  <g opacity="0"><animate attributeName="opacity" values="0;1" dur="0.4s" '
            f'begin="{d:.2f}s" fill="freeze"/>'
            f'<rect x="{x_gate}" y="{y - 13}" width="26" height="26" rx="5" '
            f'fill="{colour}" fill-opacity="0.16" stroke="{colour}" stroke-width="1.5"/>'
            f'<text x="{x_gate + 13}" y="{y + 5}" text-anchor="middle" '
            f'style="font:700 13px {MONO};fill:{colour}">{gate}</text></g>'
        )
        # entangling control dots, alternating
        if i % 2 == 0 and i + 1 < len(wires):
            parts.append(
                f'  <g opacity="0"><animate attributeName="opacity" values="0;1" dur="0.4s" '
                f'begin="{d + 0.2:.2f}s" fill="freeze"/>'
                f'<circle cx="{x_ctrl}" cy="{y}" r="4.6" fill="{colour}"/>'
                f'<line x1="{x_ctrl}" y1="{y}" x2="{x_ctrl}" y2="{y + step}" '
                f'stroke="{colour}" stroke-width="1.8"/>'
                f'<circle cx="{x_ctrl}" cy="{y + step}" r="7" fill="none" '
                f'stroke="{colour}" stroke-width="1.8"/>'
                f'<line x1="{x_ctrl - 7}" y1="{y + step}" x2="{x_ctrl + 7}" y2="{y + step}" '
                f'stroke="{colour}" stroke-width="1.8"/></g>'
            )
        # the labelled domain box
        parts.append(
            f'  <g opacity="0"><animate attributeName="opacity" values="0;1" dur="0.45s" '
            f'begin="{d + 0.35:.2f}s" fill="freeze"/>'
            f'<rect x="{x_box}" y="{y - 15}" width="236" height="30" rx="7" '
            f'fill="{colour}" fill-opacity="0.10" stroke="{colour}" stroke-opacity="0.5"/>'
            f'<text x="{x_box + 12}" y="{y + 4}" '
            f'style="font:700 11.5px {MONO};fill:{colour};letter-spacing:1.1px">{label}</text>'
            f'<text x="{x_meter - 14}" y="{y + 4}" text-anchor="end" '
            f'style="font:400 10.5px {SANS};fill:{gh.MUTED}">{gh.esc(sub)}</text></g>'
        )
        # measurement meter
        bar = 150
        parts.append(
            f'  <rect x="{x_meter + 30}" y="{y - 5}" width="{bar}" height="9" rx="4.5" fill="#1b2130"/>'
            f'<rect x="{x_meter + 30}" y="{y - 5}" width="0" height="9" rx="4.5" fill="{colour}">'
            f'<animate attributeName="width" values="0;{bar - (i % 3) * 12}" dur="1.1s" '
            f'begin="{d + 0.6:.2f}s" fill="freeze"/></rect>'
            f'<path d="M{x_meter} {y + 9} a11 11 0 0 1 22 0" fill="none" stroke="{gh.MUTED}" '
            f'stroke-width="1.6"/>'
            f'<line x1="{x_meter + 11}" y1="{y + 9}" x2="{x_meter + 17}" y2="{y + 1}" '
            f'stroke="{colour}" stroke-width="1.8" stroke-linecap="round"/>'
        )

    y_out = top + len(wires) * step + 6
    parts.append(
        f'  <line x1="26" y1="{y_out}" x2="{W - 26}" y2="{y_out}" stroke="{gh.LINE}"/>'
        f'<text x="26" y="{y_out + 26}" style="font:700 13px {MONO};fill:{gh.TEAL}">'
        f'&gt; measure() →</text>'
        f'<text x="150" y="{y_out + 26}" style="font:800 15px {SANS};fill:#fff">{NAME}</text>'
        f'<text x="{W - 26}" y="{y_out + 26}" text-anchor="end" '
        f'style="font:400 11.5px {MONO};fill:{gh.MUTED}">Mumbai, India · 54 repos · 30 languages</text>'
    )
    return frame(h, "1", "\n".join(parts))


# ─────────────────────────────  2. live terminal  ─────────────────────────────

def terminal() -> str:
    h = 306
    cw, fs = 7.22, 12.5
    lines = [
        ("cmd", "whoami"),
        ("out", "full stack · app · ai/ml · devops · web3 · quantum"),
        ("cmd", "cat stack.json"),
        ("out", "TypeScript  Python  Flutter  Swift  Solidity  Qiskit"),
        ("cmd", "git log --oneline | wc -l"),
        ("out", "917 contributions across 54 public repos"),
        ("cmd", "./ship.sh --production"),
        ("out", "building… tests passed… deployed ✓"),
    ]
    top, lead = 74, 24
    clips, rows, t = [], [], 0.35

    for i, (kind, text) in enumerate(lines):
        y = top + i * lead
        prompt = "raunak@github ~ $ "
        full = prompt + text if kind == "cmd" else "> " + text
        width = len(full) * cw + 8
        dur = len(full) * 0.028 if kind == "cmd" else 0.3
        clips.append(
            f'    <clipPath id="t{i}"><rect x="26" y="{y - 14}" width="0" height="20">'
            f'<animate attributeName="width" values="0;{width:.0f}" dur="{dur:.2f}s" '
            f'begin="{t:.2f}s" fill="freeze"/></rect></clipPath>'
        )
        if kind == "cmd":
            rows.append(
                f'  <g clip-path="url(#t{i})">'
                f'<text x="26" y="{y}" style="font:400 {fs}px {MONO};fill:{gh.TEAL}">{prompt}</text>'
                f'<text x="{26 + len(prompt) * cw:.0f}" y="{y}" '
                f'style="font:600 {fs}px {MONO};fill:#fff">{gh.esc(text)}</text></g>'
            )
        else:
            rows.append(
                f'  <g clip-path="url(#t{i})">'
                f'<text x="26" y="{y}" style="font:400 {fs}px {MONO};fill:{gh.BLUE}">&gt; </text>'
                f'<text x="{26 + 2 * cw:.0f}" y="{y}" '
                f'style="font:400 {fs}px {MONO};fill:{gh.MUTED}">{gh.esc(text)}</text></g>'
            )
        t += dur + (0.18 if kind == "cmd" else 0.42)

    y_last = top + len(lines) * lead
    body = f'''  <path d="M1 14a13 13 0 0 1 13-13h832a13 13 0 0 1 13 13v26H1z" fill="#0b0e14" fill-opacity="0.85"/>
  <line x1="1" y1="40" x2="859" y2="40" stroke="{gh.LINE}"/>
  <circle cx="24" cy="21" r="5.5" fill="#FF5F57"/>
  <circle cx="43" cy="21" r="5.5" fill="#FEBC2E"/>
  <circle cx="62" cy="21" r="5.5" fill="#28C840"/>
  <text x="88" y="25" style="font:400 11.5px {MONO};fill:{gh.MUTED}">raunak@github — zsh</text>
  <text x="{W - 24}" y="25" text-anchor="end"
        style="font:600 10.5px {MONO};fill:{gh.TEAL};letter-spacing:1.4px">● LIVE</text>

{chr(10).join(rows)}

  <text x="26" y="{y_last}" style="font:400 {fs}px {MONO};fill:{gh.TEAL}" opacity="0">
    raunak@github ~ $ <animate attributeName="opacity" values="0;1" dur="0.2s"
      begin="{t:.2f}s" fill="freeze"/></text>
  <rect x="{26 + 18 * cw:.0f}" y="{y_last - 11}" width="8.5" height="15" fill="{gh.TEAL}" opacity="0">
    <animate attributeName="opacity" values="0;1" dur="0.1s" begin="{t:.2f}s" fill="freeze"/>
    <animate attributeName="opacity" values="1;1;0;0" dur="1.1s"
             begin="{t + 0.2:.2f}s" repeatCount="indefinite"/>
  </rect>'''
    return frame(h, "2", body, "\n".join(clips))


# ─────────────────────────────  3. stat sheet  ─────────────────────────────

def stats() -> str:
    h = 300
    skills = [
        ("Frontend", 92, gh.BLUE), ("Backend", 88, gh.TEAL),
        ("App / Mobile", 84, "#A5D6FF"), ("AI / ML", 80, "#FF7B72"),
        ("Quantum", 86, gh.PURPLE), ("Web3", 72, gh.AMBER),
        ("DevOps / MLOps", 78, "#7EE7C7"), ("AR / VR", 65, "#F0A868"),
    ]
    loadout = ["TypeScript", "Python", "Flutter", "Qiskit", "Solidity", "Unity", "Docker"]

    parts = [
        f'  <text x="26" y="38" style="font:800 21px {SANS};fill:#fff">{NAME}</text>',
        f'  <text x="27" y="58" style="font:700 11px {MONO};fill:{gh.TEAL};letter-spacing:2px">'
        f'CLASS · FULL STACK / QUANTUM ENGINEER</text>',
        f'  <rect x="{W - 132}" y="22" width="106" height="42" rx="10" fill="{gh.PURPLE}" '
        f'fill-opacity="0.14" stroke="{gh.PURPLE}" stroke-opacity="0.55"/>',
        f'  <text x="{W - 79}" y="44" text-anchor="middle" '
        f'style="font:800 19px {MONO};fill:{gh.PURPLE}">LVL 21</text>',
        f'  <text x="{W - 79}" y="57" text-anchor="middle" '
        f'style="font:600 8.5px {MONO};fill:{gh.DIM};letter-spacing:1.3px">MUMBAI, IN</text>',
        f'  <line x1="26" y1="76" x2="{W - 26}" y2="76" stroke="{gh.LINE}"/>',
    ]

    bar_w, top, step = 292, 104, 30
    for i, (label, pct, colour) in enumerate(skills):
        col, row = i % 2, i // 2
        x = 26 + col * 420
        y = top + row * step
        parts.append(
            f'  <text x="{x}" y="{y - 8}" style="font:600 12px {SANS};fill:{gh.TEXT}">{label}</text>'
            f'<text x="{x + bar_w + 46}" y="{y - 8}" text-anchor="end" '
            f'style="font:700 11px {MONO};fill:{colour}">{pct}</text>'
            f'<rect x="{x}" y="{y - 2}" width="{bar_w + 46}" height="9" rx="4.5" fill="#1b2130"/>'
            f'<rect x="{x}" y="{y - 2}" width="0" height="9" rx="4.5" fill="{colour}">'
            f'<animate attributeName="width" values="0;{(bar_w + 46) * pct / 100:.0f}" '
            f'dur="1.05s" begin="{i * 0.09:.2f}s" fill="freeze"/></rect>'
        )

    y_load = top + 4 * step + 22
    parts.append(
        f'  <line x1="26" y1="{y_load - 22}" x2="{W - 26}" y2="{y_load - 22}" stroke="{gh.LINE}"/>'
        f'<text x="26" y="{y_load + 4}" '
        f'style="font:700 10px {MONO};fill:{gh.DIM};letter-spacing:1.6px">LOADOUT</text>'
    )
    x = 108
    for i, item in enumerate(loadout):
        cw = len(item) * 6.9 + 22
        parts.append(
            f'  <g opacity="0"><animate attributeName="opacity" values="0;1" dur="0.4s" '
            f'begin="{0.5 + i * 0.07:.2f}s" fill="freeze"/>'
            f'<rect x="{x:.0f}" y="{y_load - 12}" width="{cw:.0f}" height="23" rx="11.5" '
            f'fill="{gh.BLUE}" fill-opacity="0.11" stroke="{gh.BLUE}" stroke-opacity="0.45"/>'
            f'<text x="{x + cw / 2:.0f}" y="{y_load + 4}" text-anchor="middle" '
            f'style="font:600 10.5px {MONO};fill:{gh.BLUE}">{item}</text></g>'
        )
        x += cw + 8
    return frame(h, "3", "\n".join(parts))


# ─────────────────────────────  4. holographic dossier  ─────────────────────────────

def dossier() -> str:
    h = 300
    fields = [
        ("DESIGNATION", NAME, gh.TEAL),
        ("SECTOR", "Mumbai, India", gh.BLUE),
        ("DISCIPLINES", "Full Stack · App · AI/ML · DevOps · Web3 · Quantum", gh.PURPLE),
        ("PRIMARY STACK", "TypeScript · Python · Flutter · Swift · Qiskit", gh.BLUE),
        ("DEPLOYED", "quantum-debugger · BB84 chat · qubit-pilot · F-Shield", gh.TEAL),
    ]
    tiles = [("54", "REPOS"), ("30", "LANGS"), ("917", "COMMITS"), ("6", "DOMAINS")]

    defs = f'''    <pattern id="scan4" width="4" height="4" patternUnits="userSpaceOnUse">
      <rect width="4" height="1.3" fill="{gh.TEAL}" fill-opacity="0.05"/>
    </pattern>
    <linearGradient id="beam4" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{gh.TEAL}" stop-opacity="0"/>
      <stop offset="50%" stop-color="{gh.TEAL}" stop-opacity="0.22"/>
      <stop offset="100%" stop-color="{gh.TEAL}" stop-opacity="0"/>
    </linearGradient>'''

    parts = [f'  <rect x="2" y="2" width="{W - 4}" height="{h - 4}" rx="12" fill="url(#scan4)"/>']
    # corner brackets
    for cx, cy, sx, sy in ((22, 22, 1, 1), (W - 22, 22, -1, 1), (22, h - 22, 1, -1), (W - 22, h - 22, -1, -1)):
        parts.append(
            f'  <path d="M{cx} {cy + 26 * sy} V{cy} H{cx + 26 * sx}" fill="none" '
            f'stroke="{gh.TEAL}" stroke-width="2.2" stroke-linecap="round" opacity="0.85"/>'
        )
    parts.append(
        f'  <rect x="2" width="{W - 4}" height="60" fill="url(#beam4)">'
        f'<animate attributeName="y" values="2;{h - 62};2" dur="5.5s" '
        f'keyTimes="0;0.5;1" calcMode="spline" '
        f'keySplines="0.45 0 0.55 1;0.45 0 0.55 1" repeatCount="indefinite"/></rect>'
    )
    parts.append(
        f'  <text x="52" y="44" style="font:700 12px {MONO};fill:{gh.TEAL};letter-spacing:3px">'
        f'◈ IDENTITY RECORD</text>'
        f'<rect x="{W - 168}" y="28" width="116" height="24" rx="12" fill="{gh.TEAL}" '
        f'fill-opacity="0.14" stroke="{gh.TEAL}" stroke-opacity="0.6"/>'
        f'<circle cx="{W - 152}" cy="40" r="4" fill="{gh.TEAL}">'
        f'<animate attributeName="opacity" values="1;0.2;1" dur="1.9s" repeatCount="indefinite"/></circle>'
        f'<text x="{W - 140}" y="44" style="font:700 10px {MONO};fill:{gh.TEAL};'
        f'letter-spacing:1.6px">VERIFIED</text>'
        f'<line x1="52" y1="58" x2="{W - 52}" y2="58" stroke="{gh.LINE}"/>'
    )

    top, step = 88, 30
    for i, (key, val, colour) in enumerate(fields):
        y = top + i * step
        parts.append(
            f'  <g opacity="0"><animate attributeName="opacity" values="0;1" dur="0.5s" '
            f'begin="{i * 0.16:.2f}s" fill="freeze"/>'
            f'<text x="52" y="{y}" style="font:700 9.5px {MONO};fill:{gh.DIM};'
            f'letter-spacing:1.5px">⬡ {key}</text>'
            f'<text x="228" y="{y}" style="font:600 13px {SANS};fill:{colour}">{gh.esc(val)}</text></g>'
        )

    y_t = top + len(fields) * step + 16
    parts.append(f'  <line x1="52" y1="{y_t - 20}" x2="{W - 52}" y2="{y_t - 20}" stroke="{gh.LINE}"/>')
    for i, (num, lbl) in enumerate(tiles):
        x = 118 + i * 168
        parts.append(
            f'  <text x="{x}" y="{y_t + 8}" text-anchor="middle" '
            f'style="font:800 21px {MONO};fill:#fff">{num}</text>'
            f'<text x="{x}" y="{y_t + 24}" text-anchor="middle" '
            f'style="font:600 9px {MONO};fill:{gh.DIM};letter-spacing:1.5px">{lbl}</text>'
        )
    parts.append(
        f'  <text x="{W - 62}" y="{y_t + 16}" text-anchor="end" '
        f'style="font:700 10px {MONO};fill:{gh.TEAL};letter-spacing:1.4px">STATUS ▶ SHIPPING</text>'
    )
    return frame(h, "4", "\n".join(parts), defs)


STYLES = {"circuit": circuit, "terminal": terminal, "stats": stats, "dossier": dossier}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--style", choices=[*STYLES, "all"], default="circuit")
    ap.add_argument("--out", default="assets/about-card.svg")
    args = ap.parse_args()
    root = pathlib.Path(__file__).resolve().parent.parent

    if args.style == "all":
        out_dir = root / "assets" / "about-previews"
        out_dir.mkdir(parents=True, exist_ok=True)
        for name, fn in STYLES.items():
            (out_dir / f"{name}.svg").write_text(fn(), encoding="utf-8")
            print(f"wrote about-previews/{name}.svg")
        return

    out = root / args.out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(STYLES[args.style](), encoding="utf-8")
    print(f"wrote {out.relative_to(root)} (style={args.style})")


if __name__ == "__main__":
    main()
