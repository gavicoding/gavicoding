"""Gera a animacao do grafico de contribuicoes do perfil (SVG, so CSS + SMIL).

Ciclo de 15 s (cerca de 1 s de pausa antes de recomecar):
  1. "GAVICODING" aparece escrito com os quadradinhos;
  2. um bonequinho percorre o grafico colocando as contribuicoes reais do ano;
  3. a cobrinha vem atras comendo tudo; recomeca.

Uso:
  python scripts/contrib_anim.py --user gavicoding --out dist          (le GITHUB_TOKEN)
  python scripts/contrib_anim.py --sample --out dist                   (dados ficticios)
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import random
import urllib.request
from pathlib import Path

CELL, GAP = 11, 3
PITCH = CELL + GAP
LEFT, TOP = 34, 34
LOOP = 15.0
TXT_END = 4.0
WALK_START, WALK_DUR = 4.3, 7.0
SNAKE_DELAY = 2.5

PALETTES = {
    "dark": {
        "bg": "#0d1117", "empty": "#161b22", "levels": ["#0e4429", "#006d32", "#26a641", "#39d353"],
        "text": "#818cf8", "label": "#8b949e", "snake": "#a5b4fc", "snake_head": "#6366f1",
        "skin": "#f2c9a0", "hair": "#3f3f46", "shirt": "#6366f1", "pants": "#1e293b",
    },
    "light": {
        "bg": "#ffffff", "empty": "#ebedf0", "levels": ["#9be9a8", "#40c463", "#30a14e", "#216e39"],
        "text": "#4f46e5", "label": "#57606a", "snake": "#818cf8", "snake_head": "#4338ca",
        "skin": "#e0ac7e", "hair": "#27272a", "shirt": "#4f46e5", "pants": "#334155",
    },
}

# fonte 4x5 (linhas de cima para baixo)
FONT = {
    "G": [".###", "#...", "#.##", "#..#", ".###"],
    "A": [".##.", "#..#", "####", "#..#", "#..#"],
    "V": ["#..#", "#..#", "#..#", ".##.", ".##."],
    "I": ["###.", ".#..", ".#..", ".#..", "###."],
    "C": [".###", "#...", "#...", "#...", ".###"],
    "O": [".##.", "#..#", "#..#", "#..#", ".##."],
    "D": ["###.", "#..#", "#..#", "#..#", "###."],
    "N": ["#..#", "##.#", "#.##", "#..#", "#..#"],
}
LEVEL_INDEX = {"FIRST_QUARTILE": 0, "SECOND_QUARTILE": 1, "THIRD_QUARTILE": 2, "FOURTH_QUARTILE": 3}


def fetch_calendar(user: str, token: str) -> list[list[dict]]:
    query = """query($login:String!){ user(login:$login){ contributionsCollection{ contributionCalendar{
        totalContributions weeks{ contributionDays{ date contributionCount contributionLevel } } } } } }"""
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": query, "variables": {"login": user}}).encode(),
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json", "User-Agent": "contrib-anim"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.load(resp)
    weeks = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
    return [w["contributionDays"] for w in weeks]


def sample_calendar() -> list[list[dict]]:
    rnd = random.Random(7)
    end = dt.date(2026, 11, 24)
    start = end - dt.timedelta(days=end.weekday() + 1 + 52 * 7)
    weeks, day = [], start
    while day <= end:
        week = []
        for _ in range(7):
            if day > end:
                break
            busy = rnd.random() < (0.55 if day.weekday() < 5 else 0.2)
            n = rnd.randint(1, 14) if busy else 0
            level = "NONE" if n == 0 else ["FIRST_QUARTILE", "SECOND_QUARTILE", "THIRD_QUARTILE", "FOURTH_QUARTILE"][min(3, n // 4)]
            week.append({"date": day.isoformat(), "contributionCount": n, "contributionLevel": level})
            day += dt.timedelta(days=1)
        weeks.append(week)
    return weeks


def build_svg(weeks: list[list[dict]], theme: str) -> str:
    pal = PALETTES[theme]
    ncol = len(weeks)
    width = LEFT + ncol * PITCH + 20
    height = TOP + 7 * PITCH + 34

    def cx(c: int) -> float:
        return LEFT + c * PITCH + CELL / 2

    def cy(r: int) -> float:
        return TOP + r * PITCH + CELL / 2

    # caminho em serpentina (coluna a coluna), igual para o bonequinho e a cobra
    order: list[tuple[int, int]] = []
    for c in range(ncol):
        rows = range(7) if c % 2 == 0 else range(6, -1, -1)
        order.extend((c, r) for r in rows)
    pos = {cell: i for i, cell in enumerate(order)}
    n = len(order) - 1
    # ritmo: passa rapido pelos dias vazios e devagar onde ha contribuicao
    has = {(c, r) for c, week in enumerate(weeks) for r, d in enumerate(week)
           if LEVEL_INDEX.get(d.get("contributionLevel"), -1) >= 0}
    weights = [1.0 if cell in has else 0.12 for cell in order]
    cum, acc = [], 0.0
    for wgt in weights:
        cum.append(acc)
        acc += wgt
    tfrac = [v / cum[-1] if cum[-1] else i / n for i, v in enumerate(cum)]
    path_d = "M " + " L ".join(f"{cx(c):.1f} {cy(r):.1f}" for c, r in order)

    pct = lambda s: f"{100 * s / LOOP:.3f}%"  # noqa: E731
    parts: list[str] = []
    total = 0

    # celulas: base vazia + contribuicoes com tempo proprio
    month_labels = []
    last_month, last_col = None, -10
    for c, week in enumerate(weeks):
        for r, day in enumerate(week):
            x, y = LEFT + c * PITCH, TOP + r * PITCH
            parts.append(f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2" fill="{pal["empty"]}"/>')
            lvl = LEVEL_INDEX.get(day.get("contributionLevel"), -1)
            total += int(day.get("contributionCount", 0))
            if lvl >= 0:
                p = tfrac[pos[(c, r)]]
                delay = p * WALK_DUR - LOOP
                parts.append(
                    f'<rect class="ct" style="animation-delay:{delay:.3f}s" x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2" fill="{pal["levels"][lvl]}"/>'
                )
        if week:
            d = dt.date.fromisoformat(week[0]["date"])
            if d.month != last_month and c - last_col >= 3:
                month_labels.append((c, d.strftime("%b")))
                last_month, last_col = d.month, c
            elif d.month != last_month:
                last_month = d.month

    labels = "".join(
        f'<text x="{LEFT + c * PITCH}" y="{TOP - 10}" class="lbl">{m}</text>' for c, m in month_labels
    )

    # texto GAVICODING
    word = "GAVICODING"
    start_col = max(0, (ncol - len(word) * 5 + 1) // 2)
    txt = []
    for i, ch in enumerate(word):
        for r, line in enumerate(FONT[ch]):
            for k, bit in enumerate(line):
                if bit == "#":
                    c = start_col + i * 5 + k
                    if c < ncol:
                        x, y = LEFT + c * PITCH, TOP + (r + 1) * PITCH
                        txt.append(
                            f'<rect class="tx" style="animation-delay:{c * 0.03:.2f}s" x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2" fill="{pal["text"]}"/>'
                        )

    # tempos de cada fase dentro do ciclo
    s0 = WALK_START + SNAKE_DELAY
    pts = ";".join(f"{i / n:.5f}" for i in range(n + 1))

    def timing(t0: float) -> tuple[str, str]:
        times = ";".join(f"{(t0 + f * WALK_DUR) / LOOP:.5f}" for f in tfrac)
        return f"0;{pts};1", f"0;{times};1"

    kp_walk, kt_walk = timing(WALK_START)
    kp_snake, kt_snake = timing(s0)

    def vis(a: float, b: float) -> str:
        return (
            f'<animate attributeName="opacity" dur="{LOOP}s" repeatCount="indefinite" '
            f'values="0;0;1;1;0;0" keyTimes="0;{(a - 0.2) / LOOP:.4f};{a / LOOP:.4f};{b / LOOP:.4f};{(b + 0.2) / LOOP:.4f};1"/>'
        )

    avatar = f"""
    <g class="mover" opacity="0">
      {vis(WALK_START, WALK_START + WALK_DUR)}
      <animateMotion dur="{LOOP}s" repeatCount="indefinite" calcMode="linear" keyPoints="{kp_walk}" keyTimes="{kt_walk}" path="{path_d}"/>
      <g transform="translate(0 -9)">
        <rect x="-3" y="-8" width="6" height="2" fill="{pal["hair"]}"/>
        <rect x="-3" y="-6" width="6" height="5" rx="1" fill="{pal["skin"]}"/>
        <rect x="-4" y="-1" width="8" height="6" rx="1" fill="{pal["shirt"]}"/>
        <rect x="-3" y="5" width="2" height="4" fill="{pal["pants"]}"/>
        <rect x="1" y="5" width="2" height="4" fill="{pal["pants"]}"/>
        <rect x="4" y="0" width="3" height="3" rx="1" fill="{pal["levels"][2]}"/>
      </g>
    </g>"""

    snake_parts = []
    lag = 0.035
    for i in range(7):
        size = 10 if i == 0 else max(5, 9 - i)
        color = pal["snake_head"] if i == 0 else pal["snake"]
        snake_parts.append(
            f"""<g class="mover" opacity="0">{vis(s0 + i * lag, s0 + WALK_DUR + i * lag)}
      <animateMotion dur="{LOOP}s" begin="{i * lag:.3f}s" repeatCount="indefinite" calcMode="linear" keyPoints="{kp_snake}" keyTimes="{kt_snake}" path="{path_d}"/>
      <rect x="{-size / 2}" y="{-size / 2}" width="{size}" height="{size}" rx="{size / 3:.1f}" fill="{color}"/></g>"""
        )

    a_in = pct(WALK_START)
    a_on = pct(WALK_START + 0.25)
    e_on = pct(WALK_START + SNAKE_DELAY)
    e_off = pct(WALK_START + SNAKE_DELAY + 0.15)
    css = f"""
    .lbl {{ font: 10px -apple-system, "Segoe UI", Helvetica, Arial, sans-serif; fill: {pal["label"]}; }}
    .cap {{ font: 11px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; fill: {pal["label"]}; }}
    .ct {{ opacity: 0; transform-box: fill-box; transform-origin: center; animation: life {LOOP}s linear infinite; }}
    @keyframes life {{
      0% {{ opacity: 0; transform: scale(0.2); }}
      {a_in} {{ opacity: 0; transform: scale(0.2); }}
      {a_on} {{ opacity: 1; transform: scale(1); }}
      {e_on} {{ opacity: 1; transform: scale(1); }}
      {e_off} {{ opacity: 0; transform: scale(0.2); }}
      100% {{ opacity: 0; transform: scale(0.2); }}
    }}
    .tx {{ opacity: 0; animation: txt {LOOP}s ease-out infinite; }}
    @keyframes txt {{
      0% {{ opacity: 0; }} 3% {{ opacity: 1; }} {pct(TXT_END - 0.6)} {{ opacity: 1; }} {pct(TXT_END)} {{ opacity: 0; }} 100% {{ opacity: 0; }}
    }}
    @media (prefers-reduced-motion: reduce) {{
      .ct {{ animation: none; opacity: 1; transform: none; }}
      .tx, .mover {{ display: none; }}
    }}"""

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{total} contributions in the last year, animated">
  <style>{css}</style>
  <rect width="{width}" height="{height}" rx="10" fill="{pal["bg"]}"/>
  {labels}
  {"".join(parts)}
  {"".join(txt)}
  {avatar}
  {"".join(snake_parts)}
  <text x="{LEFT}" y="{height - 12}" class="cap">{total} contributions in the last year</text>
  <text x="{width - 20}" y="{height - 12}" class="cap" text-anchor="end">@gavicoding</text>
</svg>
"""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--user", default="gavicoding")
    ap.add_argument("--out", default="dist")
    ap.add_argument("--sample", action="store_true", help="usa dados ficticios (sem API)")
    args = ap.parse_args()
    token = os.environ.get("GITHUB_TOKEN", "")
    weeks = sample_calendar() if args.sample or not token else fetch_calendar(args.user, token)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    for theme in ("dark", "light"):
        (out / f"contrib-{theme}.svg").write_text(build_svg(weeks, theme), encoding="utf-8")
    print("ok:", out.resolve())


if __name__ == "__main__":
    main()
