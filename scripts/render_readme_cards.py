#!/usr/bin/env python3
"""Render animated Light/Dark SVG profile cards for Rangga11268 GitHub README."""

from __future__ import annotations

import base64
import datetime as dt
import json
import os
import re
import urllib.error
import urllib.request
from collections import defaultdict
from html.parser import HTMLParser
from pathlib import Path
from xml.sax.saxutils import escape

USERNAME = os.environ.get("GITHUB_USERNAME", "Rangga11268")
STATIC_MODE = os.environ.get("STATIC", "0") == "1"

ROOT = Path(__file__).resolve().parent.parent
CARDS_DIR = ROOT / "cards"
DATA_DIR = ROOT / "data"
FONTS_DIR = Path(__file__).resolve().parent / "fonts"
DATA_FILE = DATA_DIR / "contributions.json"

LANG_COLORS = {
    "Python": ("#2563eb", "#60a5fa"),
    "TypeScript": ("#0284c7", "#38bdf8"),
    "PHP": ("#4f46e5", "#818cf8"),
    "JavaScript": ("#d97706", "#fbbf24"),
    "Blade": ("#e11d48", "#fb7185"),
    "HTML": ("#ea580c", "#fb923c"),
    "CSS": ("#7c3aed", "#a78bfa"),
    "Jupyter Notebook": ("#ea580c", "#fb923c"),
    "Go": ("#0891b2", "#22d3ee"),
    "Shell": ("#059669", "#34d399"),
}

THEMES = {
    "light": {
        "bg": "#fafafa",
        "bg_alt": "#f4f4f5",
        "ink": "#09090b",
        "muted": "#52525b",
        "subtle": "#71717a",
        "border": "#e4e4e7",
        "accent": "#2563eb",
        "accent_soft": "#dbeafe",
        "emerald": "#10b981",
        "amber": "#d97706",
        "shine_a": "#09090b",
        "shine_b": "#2563eb",
        "bar_dim": "#d4d4d8",
        "heat": ["#ebedf0", "#bfdbfe", "#60a5fa", "#2563eb", "#1d4ed8"],
        "track": "#e4e4e7",
    },
    "dark": {
        "bg": "#09090b",
        "bg_alt": "#18181b",
        "ink": "#fafafa",
        "muted": "#a1a1aa",
        "subtle": "#71717a",
        "border": "#27272a",
        "accent": "#3b82f6",
        "accent_soft": "#1e3a8a",
        "emerald": "#34d399",
        "amber": "#fbbf24",
        "shine_a": "#fafafa",
        "shine_b": "#60a5fa",
        "bar_dim": "#27272a",
        "heat": ["#18181b", "#172554", "#1d4ed8", "#3b82f6", "#60a5fa"],
        "track": "#27272a",
    },
}


class ContributionParser(HTMLParser):
    """Parse GitHub's /users/<username>/contributions HTML fragment."""

    def __init__(self) -> None:
        super().__init__()
        self.days_by_id: dict[str, dict[str, object]] = {}
        self.tooltips: dict[str, str] = {}
        self._cur_tip_id: str | None = None
        self._cur_tip_buf: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_map = dict(attrs)
        if tag == "td" and "ContributionCalendar-day" in (attr_map.get("class") or ""):
            day_id = attr_map.get("id")
            date_str = attr_map.get("data-date")
            level_str = attr_map.get("data-level") or "0"
            if day_id and date_str:
                self.days_by_id[day_id] = {
                    "date": date_str,
                    "level": int(level_str),
                    "count": 0,
                }
        elif tag == "tool-tip" and attr_map.get("for"):
            self._cur_tip_id = attr_map["for"]
            self._cur_tip_buf = []

    def handle_data(self, data: str) -> None:
        if self._cur_tip_id is not None:
            self._cur_tip_buf.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "tool-tip" and self._cur_tip_id is not None:
            self.tooltips[self._cur_tip_id] = "".join(self._cur_tip_buf).strip()
            self._cur_tip_id = None
            self._cur_tip_buf = []


def _http_get(url: str, headers: dict[str, str] | None = None) -> bytes:
    req_headers = {"User-Agent": "Rangga11268-Readme-Renderer/1.0"}
    if headers:
        req_headers.update(headers)
    req = urllib.request.Request(url, headers=req_headers)
    with urllib.request.urlopen(req, timeout=20) as resp:
        return resp.read()


def fetch_contributions(username: str) -> list[dict[str, object]]:
    html = _http_get(f"https://github.com/users/{username}/contributions").decode(
        "utf-8", errors="ignore"
    )
    parser = ContributionParser()
    parser.feed(html)
    for day_id, entry in parser.days_by_id.items():
        tip = parser.tooltips.get(day_id, "")
        m = re.search(r"(\d+)\s+contribution", tip)
        entry["count"] = int(m.group(1)) if m else 0
    days = sorted(parser.days_by_id.values(), key=lambda d: str(d["date"]))
    if not days:
        raise RuntimeError("No contribution calendar days parsed from GitHub.")
    return days


def fetch_repos_and_languages(username: str) -> tuple[int, list[dict[str, object]]]:
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    repos_raw = _http_get(
        f"https://api.github.com/users/{username}/repos?per_page=100&type=owner",
        headers=headers,
    )
    repos = [r for r in json.loads(repos_raw.decode("utf-8")) if not r.get("fork")]
    public_count = len(repos)

    lang_bytes: dict[str, int] = defaultdict(int)
    rate_limited = False
    for repo in repos:
        lang_url = repo.get("languages_url")
        if not lang_url:
            continue
        try:
            data = json.loads(_http_get(lang_url, headers=headers).decode("utf-8"))
            for k, v in data.items():
                lang_bytes[k] += int(v)
        except urllib.error.HTTPError as exc:
            if exc.code in (403, 429):
                rate_limited = True
                break
        except Exception:
            continue

    if rate_limited or not lang_bytes:
        raise RuntimeError("GitHub language byte lookup rate-limited or empty.")

    total = sum(lang_bytes.values()) or 1
    top = sorted(lang_bytes.items(), key=lambda kv: -kv[1])[:5]
    top_sum = sum(v for _, v in top)
    other = total - top_sum
    result = [
        {"name": name, "bytes": val, "pct": round(val * 100.0 / total, 1)}
        for name, val in top
    ]
    if other > 0:
        result.append(
            {"name": "Other", "bytes": other, "pct": round(other * 100.0 / total, 1)}
        )
    return public_count, result


def compute_metrics(days: list[dict[str, object]]) -> dict[str, object]:
    total = sum(int(d["count"]) for d in days)
    active_days = sum(1 for d in days if int(d["count"]) > 0)

    best_day = max(days, key=lambda d: int(d["count"]))
    best_date = dt.date.fromisoformat(str(best_day["date"])).strftime("%b %d")

    longest_streak = 0
    running = 0
    for d in days:
        if int(d["count"]) > 0:
            running += 1
            longest_streak = max(longest_streak, running)
        else:
            running = 0

    current_streak = 0
    idx = len(days) - 1
    if idx >= 0 and int(days[idx]["count"]) == 0:
        idx -= 1
    while idx >= 0 and int(days[idx]["count"]) > 0:
        current_streak += 1
        idx -= 1

    monthly: dict[str, int] = defaultdict(int)
    for d in days:
        ym = str(d["date"])[:7]
        monthly[ym] += int(d["count"])
    months_sorted = sorted(monthly.items())[-12:]
    monthly_list = [
        {
            "ym": ym,
            "label": dt.date.fromisoformat(f"{ym}-01").strftime("%b"),
            "count": count,
        }
        for ym, count in months_sorted
    ]

    return {
        "total_contributions": total,
        "active_days": active_days,
        "total_days": len(days),
        "best_day_count": int(best_day["count"]),
        "best_day_date": best_date,
        "longest_streak": longest_streak,
        "current_streak": current_streak,
        "monthly": monthly_list,
    }


def load_or_refresh_data() -> dict[str, object]:
    cached: dict[str, object] = {}
    if DATA_FILE.exists():
        cached = json.loads(DATA_FILE.read_text(encoding="utf-8"))

    try:
        days = fetch_contributions(USERNAME)
    except Exception:
        days = cached.get("days", [])  # type: ignore[assignment]
        if not days:
            raise

    try:
        public_repos, languages = fetch_repos_and_languages(USERNAME)
    except Exception:
        public_repos = int(cached.get("public_repos", 32))
        languages = cached.get("languages", [])  # type: ignore[assignment]

    metrics = compute_metrics(days)
    payload = {
        "username": USERNAME,
        "updated_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d"),
        "public_repos": public_repos,
        "languages": languages,
        **metrics,
        "days": days,
    }
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload


def load_font_css() -> str:
    geist_b64 = base64.b64encode((FONTS_DIR / "geist-subset.woff2").read_bytes()).decode("ascii")
    mono_b64 = base64.b64encode((FONTS_DIR / "geist-mono-subset.woff2").read_bytes()).decode("ascii")
    return (
        f"@font-face{{font-family:'Geist';font-weight:100 900;font-style:normal;"
        f"src:url(data:font/woff2;base64,{geist_b64}) format('woff2');}}"
        f"@font-face{{font-family:'Geist Mono';font-weight:100 900;font-style:normal;"
        f"src:url(data:font/woff2;base64,{mono_b64}) format('woff2');}}"
    )


def anim_css(base_rules: str) -> str:
    if STATIC_MODE:
        return (
            base_rules
            + ".fade,.bar,.pop,.cell{opacity:1!important;transform:none!important;}"
        )
    return (
        base_rules
        + """
        @keyframes fadeUp{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:translateY(0)}}
        @keyframes barGrow{from{transform:scaleY(0)}to{transform:scaleY(1)}}
        @keyframes popIn{from{opacity:0;transform:scale(.8)}to{opacity:1;transform:scale(1)}}
        @keyframes pulse{0%,100%{opacity:1;transform:scale(1)}50%{opacity:.45;transform:scale(.82)}}
        @keyframes nudge{0%,100%{transform:translate(0,0)}50%{transform:translate(2px,-2px)}}
        .fade{opacity:0;animation:fadeUp .55s cubic-bezier(.16,1,.3,1) forwards;}
        .bar{transform-origin:bottom;transform-box:fill-box;transform:scaleY(0);animation:barGrow .65s cubic-bezier(.16,1,.3,1) forwards;}
        .pop{opacity:0;transform-origin:center;transform-box:fill-box;animation:popIn .4s cubic-bezier(.16,1,.3,1) forwards;}
        .pulse{transform-origin:center;transform-box:fill-box;animation:pulse 2.2s ease-in-out infinite;}
        .nudge{transform-origin:center;transform-box:fill-box;animation:nudge 2.4s ease-in-out infinite;}
        @media(prefers-reduced-motion:reduce){
          .fade,.bar,.pop,.pulse,.nudge{animation:none!important;opacity:1!important;transform:none!important;}
        }
        """
    )


def render_hero(data: dict[str, object], theme_name: str, font_css: str) -> str:
    t = THEMES[theme_name]
    w, h = 860, 154
    total = f"{int(data['total_contributions']):,}"
    active = data["active_days"]
    streak = data["longest_streak"]
    repos = data["public_repos"]

    shine_anim = (
        ""
        if STATIC_MODE
        else '<animateTransform attributeName="gradientTransform" type="translate" values="-1 0;-1 0;2 0" keyTimes="0;0.55;1" dur="5.2s" repeatCount="indefinite"/>'
    )
    name_fill = t["ink"] if STATIC_MODE else "url(#nameShine)"

    css = anim_css(
        font_css
        + f"""
        .sans{{font-family:'Geist',-apple-system,BlinkMacSystemFont,sans-serif;}}
        .mono{{font-family:'Geist Mono',ui-monospace,SFMono-Regular,monospace;font-variant-numeric:tabular-nums;}}
        """
    )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none">
  <defs>
    <linearGradient id="nameShine" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{t['shine_a']}"/>
      <stop offset="42%" stop-color="{t['shine_a']}"/>
      <stop offset="50%" stop-color="{t['shine_b']}"/>
      <stop offset="58%" stop-color="{t['shine_a']}"/>
      <stop offset="100%" stop-color="{t['shine_a']}"/>
      {shine_anim}
    </linearGradient>
  </defs>
  <style>{css}</style>
  <rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="12" fill="{t['bg']}" stroke="{t['border']}"/>

  <g class="fade" style="animation-delay:0.04s">
    <circle cx="28" cy="30" r="4" fill="{t['emerald']}" class="pulse"/>
    <text x="40" y="34" class="mono" font-size="11" font-weight="500" fill="{t['muted']}" letter-spacing="0.06em">BEKASI, INDONESIA · OPEN TO ENGINEERING ROLES</text>
    <rect x="614" y="18" width="222" height="24" rx="12" fill="{t['bg_alt']}" stroke="{t['border']}"/>
    <text x="725" y="34" text-anchor="middle" class="mono" font-size="10.5" font-weight="600" fill="{t['ink']}">GPA 4.00 · 1ST PLACE IT BOOT CAMP</text>
  </g>

  <g class="fade" style="animation-delay:0.12s">
    <text x="24" y="76" class="sans" font-size="30" font-weight="700" letter-spacing="-0.03em" fill="{name_fill}">Darell Rangga Putra Rachman</text>
    <text x="24" y="102" class="sans" font-size="14.5" font-weight="450" fill="{t['muted']}">Software Engineer · Machine Learning &amp; Distributed Systems Architect</text>
  </g>

  <line x1="24" y1="118" x2="{w-24}" y2="118" stroke="{t['border']}"/>

  <g class="fade" style="animation-delay:0.20s">
    <text x="24" y="138" class="mono" font-size="11" font-weight="500" fill="{t['subtle']}">{escape(total)} CONTRIBUTIONS (1Y)  ·  {active} ACTIVE DAYS  ·  {streak}D MAX STREAK  ·  {repos} PUBLIC REPOS</text>
    <text x="{w-24}" y="138" text-anchor="end" class="mono" font-size="11" font-weight="600" fill="{t['accent']}">darellrangga.me</text>
  </g>
</svg>
"""


def render_tile(
    *,
    theme_name: str,
    font_css: str,
    delay: float,
    eyebrow: str,
    dot_color_key: str,
    headline: str,
    sublabel: str,
    footer: str,
    highlight_bar: str | None = None,
) -> str:
    t = THEMES[theme_name]
    w, h = 280, 142
    dot = t[dot_color_key]
    css = anim_css(
        font_css
        + f"""
        .sans{{font-family:'Geist',-apple-system,BlinkMacSystemFont,sans-serif;}}
        .mono{{font-family:'Geist Mono',ui-monospace,SFMono-Regular,monospace;font-variant-numeric:tabular-nums;}}
        """
    )
    bar_el = (
        f'<rect x="18" y="0" width="52" height="2.5" rx="1.25" fill="{highlight_bar or dot}"/>'
    )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none">
  <style>{css}</style>
  <rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="10" fill="{t['bg']}" stroke="{t['border']}"/>
  {bar_el}
  <g class="fade" style="animation-delay:{delay:.2f}s">
    <circle cx="24" cy="25" r="3.5" fill="{dot}" class="pulse"/>
    <text x="34" y="29" class="mono" font-size="10.5" font-weight="600" fill="{t['muted']}" letter-spacing="0.06em">{escape(eyebrow)}</text>
    <text x="{w-22}" y="29" text-anchor="end" class="mono nudge" font-size="13" font-weight="600" fill="{t['subtle']}">↗</text>

    <text x="18" y="72" class="sans" font-size="27" font-weight="700" letter-spacing="-0.03em" fill="{t['ink']}">{escape(headline)}</text>
    <text x="18" y="94" class="sans" font-size="13" font-weight="500" fill="{t['muted']}">{escape(sublabel)}</text>

    <line x1="18" y1="110" x2="{w-18}" y2="110" stroke="{t['border']}"/>
    <text x="18" y="128" class="mono" font-size="10.5" font-weight="500" fill="{t['subtle']}">{escape(footer)}</text>
  </g>
</svg>
"""


def render_activity(data: dict[str, object], theme_name: str, font_css: str) -> str:
    t = THEMES[theme_name]
    w, h = 860, 294
    css = anim_css(
        font_css
        + f"""
        .sans{{font-family:'Geist',-apple-system,BlinkMacSystemFont,sans-serif;}}
        .mono{{font-family:'Geist Mono',ui-monospace,SFMono-Regular,monospace;font-variant-numeric:tabular-nums;}}
        """
    )

    # 1. KPI boxes
    kpis = [
        ("TOTAL (1Y)", f"{int(data['total_contributions']):,}"),
        ("ACTIVE DAYS", f"{data['active_days']} / {data['total_days']}"),
        ("BUSIEST DAY", f"{data['best_day_count']} ({data['best_day_date']})"),
        ("STREAK (CUR / MAX)", f"{data['current_streak']}d / {data['longest_streak']}d"),
    ]
    kpi_svg = []
    box_w = 193
    gap = 13
    for i, (lbl, val) in enumerate(kpis):
        x = 24 + i * (box_w + gap)
        kpi_svg.append(
            f'<g class="fade" style="animation-delay:{0.10 + i * 0.05:.2f}s">'
            f'<rect x="{x}" y="44" width="{box_w}" height="44" rx="8" fill="{t["bg_alt"]}" stroke="{t["border"]}"/>'
            f'<text x="{x+12}" y="60" class="mono" font-size="9.5" font-weight="500" fill="{t["subtle"]}" letter-spacing="0.05em">{escape(lbl)}</text>'
            f'<text x="{x+12}" y="79" class="sans" font-size="15.5" font-weight="700" fill="{t["ink"]}">{escape(val)}</text>'
            f"</g>"
        )

    # 2. Monthly bar chart (left panel: x=24..505, y=104..198)
    months: list[dict[str, object]] = data["monthly"]  # type: ignore[assignment]
    max_m = max((int(m["count"]) for m in months), default=1) or 1
    best_idx = max(range(len(months)), key=lambda i: int(months[i]["count"]))
    bar_svg = []
    chart_x0 = 26
    bar_w = 24
    bar_gap = 15.5
    base_y = 180
    max_bar_h = 46

    for i, m in enumerate(months):
        cnt = int(m["count"])
        bh = max(4, round(cnt * max_bar_h / max_m))
        bx = chart_x0 + i * (bar_w + bar_gap)
        by = base_y - bh
        is_best = i == best_idx
        fill = t["accent"] if is_best else t["bar_dim"]
        delay = 0.25 + i * 0.03
        bar_svg.append(
            f'<rect x="{bx:.1f}" y="{by}" width="{bar_w}" height="{bh}" rx="3" fill="{fill}" class="bar" style="animation-delay:{delay:.2f}s"/>'
        )
        bar_svg.append(
            f'<text x="{bx + bar_w/2:.1f}" y="{base_y + 13}" text-anchor="middle" class="mono" font-size="9.5" fill="{t["ink"] if is_best else t["subtle"]}" font-weight="{600 if is_best else 400}">{escape(str(m["label"]))}</text>'
        )
        if is_best:
            bar_svg.append(
                f'<text x="{bx + bar_w/2:.1f}" y="{by - 5}" text-anchor="middle" class="mono pop" font-size="9.5" font-weight="700" fill="{t["accent"]}" style="animation-delay:{delay + 0.35:.2f}s">{cnt}</text>'
            )

    # 3. Top Languages (right panel: x=530..836)
    langs: list[dict[str, object]] = data["languages"]  # type: ignore[assignment]
    lang_bar_svg = []
    lang_legend_svg = []
    bar_total_w = 296
    cur_x = 532.0
    color_idx = 0 if theme_name == "light" else 1
    for i, lg in enumerate(langs):
        name = str(lg["name"])
        pct = float(lg["pct"])
        seg_w = max(4.0, bar_total_w * pct / 100.0)
        if i == len(langs) - 1:
            seg_w = max(4.0, (532.0 + bar_total_w) - cur_x)
        c = LANG_COLORS.get(name, (t["subtle"], t["muted"]))[color_idx]
        lang_bar_svg.append(
            f'<rect x="{cur_x:.1f}" y="128" width="{seg_w:.1f}" height="8" rx="2" fill="{c}"/>'
        )
        cur_x += seg_w

        col = i % 2
        row = i // 2
        lx = 532 + col * 154
        ly = 152 + row * 18
        lang_legend_svg.append(
            f'<circle cx="{lx+4}" cy="{ly-3.5}" r="3.5" fill="{c}"/>'
            f'<text x="{lx+12}" y="{ly}" class="mono" font-size="10.5" fill="{t["ink"]}">{escape(name)}</text>'
            f'<text x="{lx+142}" y="{ly}" text-anchor="end" class="mono" font-size="10.5" fill="{t["subtle"]}">{pct:.1f}%</text>'
        )

    # 4. Contribution Heatmap (53 cols x 7 rows, flush with x=24..836)
    days: list[dict[str, object]] = data["days"]  # type: ignore[assignment]
    heat_svg = []
    cell = 11.8
    step = 15.38
    hx0 = 24.0
    hy0 = 208.0
    for idx, d in enumerate(days):
        col = idx // 7
        row = idx % 7
        if col >= 53:
            break
        lvl = min(4, max(0, int(d["level"])))
        cx = hx0 + col * step
        cy = hy0 + row * 10.5
        delay = 0.20 + col * 0.012
        heat_svg.append(
            f'<rect x="{cx:.1f}" y="{cy:.1f}" width="{cell:.1f}" height="8.2" rx="1.8" fill="{t["heat"][lvl]}" class="fade" style="animation-delay:{delay:.3f}s"/>'
        )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none">
  <style>{css}</style>
  <rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="12" fill="{t['bg']}" stroke="{t['border']}"/>

  <g class="fade" style="animation-delay:0.04s">
    <text x="24" y="28" class="mono" font-size="11" font-weight="600" fill="{t['ink']}" letter-spacing="0.06em">GITHUB ACTIVITY &amp; CODE TELEMETRY</text>
    <text x="{w-24}" y="28" text-anchor="end" class="mono" font-size="10.5" fill="{t['subtle']}">UPDATED {escape(str(data['updated_at']))}</text>
  </g>

  {''.join(kpi_svg)}

  <g class="fade" style="animation-delay:0.20s">
    <text x="24" y="114" class="mono" font-size="10" font-weight="600" fill="{t['muted']}" letter-spacing="0.05em">MONTHLY CONTRIBUTIONS</text>
    {''.join(bar_svg)}
  </g>

  <line x1="514" y1="104" x2="514" y2="194" stroke="{t['border']}"/>

  <g class="fade" style="animation-delay:0.24s">
    <text x="532" y="114" class="mono" font-size="10" font-weight="600" fill="{t['muted']}" letter-spacing="0.05em">LANGUAGE DISTRIBUTION ({data['public_repos']} REPOS)</text>
    <rect x="532" y="128" width="296" height="8" rx="4" fill="{t['track']}"/>
    {''.join(lang_bar_svg)}
    {''.join(lang_legend_svg)}
  </g>

  <line x1="24" y1="199" x2="{w-24}" y2="199" stroke="{t['border']}"/>
  {''.join(heat_svg)}
</svg>
"""


def main() -> None:
    CARDS_DIR.mkdir(parents=True, exist_ok=True)
    data = load_or_refresh_data()
    font_css = load_font_css()

    for theme in ("light", "dark"):
        (CARDS_DIR / f"hero-{theme}.svg").write_text(
            render_hero(data, theme, font_css), encoding="utf-8"
        )
        (CARDS_DIR / f"tile-aiml-{theme}.svg").write_text(
            render_tile(
                theme_name=theme,
                font_css=font_css,
                delay=0.14,
                eyebrow="01 // AI & SCIML",
                dot_color_key="accent",
                headline="522 Tests",
                sublabel="5 Flagship ML Engines",
                footer="SpecRAG · Conformal · Causal",
                highlight_bar=THEMES[theme]["accent"],
            ),
            encoding="utf-8",
        )
        (CARDS_DIR / f"tile-fullstack-{theme}.svg").write_text(
            render_tile(
                theme_name=theme,
                font_css=font_css,
                delay=0.22,
                eyebrow="02 // FULL-STACK",
                dot_color_key="emerald",
                headline="<25ms p95",
                sublabel="Distributed Web Systems",
                footer="Laravel · FastAPI · Next.js",
                highlight_bar=THEMES[theme]["emerald"],
            ),
            encoding="utf-8",
        )
        (CARDS_DIR / f"tile-portfolio-{theme}.svg").write_text(
            render_tile(
                theme_name=theme,
                font_css=font_css,
                delay=0.30,
                eyebrow="03 // LEADERSHIP",
                dot_color_key="amber",
                headline="1st / 44",
                sublabel="IT Boot Camp 2026 Winner",
                footer="darellrangga.me · 89p HAKI",
                highlight_bar=THEMES[theme]["amber"],
            ),
            encoding="utf-8",
        )
        (CARDS_DIR / f"activity-{theme}.svg").write_text(
            render_activity(data, theme, font_css), encoding="utf-8"
        )

    print(
        f"Rendered 10 SVG cards into {CARDS_DIR} "
        f"(total={data['total_contributions']}, active={data['active_days']}, "
        f"streak={data['longest_streak']}, repos={data['public_repos']}, static={STATIC_MODE})"
    )


if __name__ == "__main__":
    main()
