#!/usr/bin/env python3
"""Shared helpers for the README asset generators: GitHub API access and SVG text utilities."""

import html
import http.client
import json
import os
import time
import urllib.error
import urllib.request

USER = "Raunakg2005"

# Shared palette so every generated card looks like it came from the same set.
BG0, BG1 = "#0d1117", "#161b28"
LINE = "#30363D"
TEXT, MUTED, DIM = "#C9D1D9", "#8B949E", "#6E7A91"
PURPLE, BLUE, TEAL, AMBER = "#B191FF", "#79C0FF", "#7EE7C7", "#F0A868"

LANG_COLOURS = {
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
FALLBACK_COLOUR = "#8B949E"


def _request(url: str, data: bytes | None = None, extra: dict | None = None):
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "readme-builder",
        **(extra or {}),
    }
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return urllib.request.Request(url, data=data, headers=headers)


def _send(req, attempts: int = 4):
    for attempt in range(attempts):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read())
        except urllib.error.HTTPError:
            raise  # a real answer (404 on an empty repo) — let the caller decide
        except (urllib.error.URLError, http.client.HTTPException, OSError):
            # The API drops connections now and then; retry rather than fail the
            # build and leave a stale asset committed.
            if attempt == attempts - 1:
                raise
            time.sleep(2 * (attempt + 1))


def api(path: str):
    """GET a REST endpoint, e.g. api("repos/owner/name")."""
    return _send(_request(f"https://api.github.com/{path}"))


def graphql(query: str, variables: dict):
    payload = json.dumps({"query": query, "variables": variables}).encode()
    data = _send(
        _request(
            "https://api.github.com/graphql",
            data=payload,
            extra={"Content-Type": "application/json"},
        )
    )
    if "errors" in data:
        raise SystemExit(f"GraphQL error: {data['errors']}")
    return data["data"]


def lang_colour(name: str) -> str:
    return LANG_COLOURS.get(name, FALLBACK_COLOUR)


def esc(text: str) -> str:
    """Escape for embedding inside an SVG text node."""
    return html.escape(str(text), quote=True)


def wrap(text: str, width_px: float, font_px: float) -> list[str]:
    """Greedy word wrap using an average glyph-width estimate.

    SVG has no auto-wrapping, and we cannot measure text without a renderer,
    so approximate: ~0.52em average advance for this UI font at these sizes.
    """
    limit = max(int(width_px / (font_px * 0.52)), 8)
    lines, line = [], ""
    for word in text.split():
        candidate = f"{line} {word}".strip()
        if len(candidate) <= limit:
            line = candidate
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines
