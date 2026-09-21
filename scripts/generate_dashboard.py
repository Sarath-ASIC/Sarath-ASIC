#!/usr/bin/env python3
import os, urllib.parse, urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

USER = os.getenv("GITHUB_USER", "Sarath-ASIC")
TOKEN = os.getenv("GITHUB_TOKEN", "")
OUT = Path("assets/engineering_dashboard.svg")

def get(url):
    req = urllib.request.Request(url)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    if TOKEN:
        req.add_header("Authorization", f"Bearer {TOKEN}")
    with urllib.request.urlopen(req, timeout=20) as r:
        import json
        return json.load(r)

def esc(x):
    return (str(x).replace("&","&amp;").replace("<","&lt;")
            .replace(">","&gt;").replace('"',"&quot;"))

def main():
    u = urllib.parse.quote(USER)
    profile = get(f"https://api.github.com/users/{u}")

    repos, page = [], 1
    while True:
        data = get(f"https://api.github.com/users/{u}/repos?per_page=100&page={page}&type=owner")
        if not data:
            break
        repos.extend(data)
        if len(data) < 100:
            break
        page += 1

    public_repos = profile.get("public_repos", len(repos))
    followers = profile.get("followers", 0)
    stars = sum(int(r.get("stargazers_count", 0)) for r in repos)

    since = (datetime.now(timezone.utc) - timedelta(days=30)).strftime("%Y-%m-%d")
    q = urllib.parse.quote(f"author:{USER} committer-date:>{since}")
    try:
        commits = get(f"https://api.github.com/search/commits?q={q}").get("total_count", 0)
    except Exception:
        commits = 0

    now = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M")

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 610" role="img">
<defs><style>
.m{{font-family:ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,monospace}}
.t{{font-size:26px;font-weight:700;fill:#f8fafc}}
.l{{font-size:14px;fill:#94a3b8}}
.v{{font-size:18px;fill:#e2e8f0;font-weight:600}}
.a{{fill:#67e8f9}}
.line{{stroke:#334155;stroke-width:1}}
.p{{animation:pulse 1.8s ease-in-out infinite}}
@keyframes pulse{{0%,100%{{opacity:.35}}50%{{opacity:1}}}}
</style></defs>
<rect width="1200" height="610" rx="18" fill="#0b1020"/>
<rect x="20" y="20" width="1160" height="570" rx="14" fill="none" stroke="#334155"/>
<text x="50" y="62" class="m t">SARATH-ASIC :: ENGINEERING TERMINAL</text>
<text x="1135" y="62" text-anchor="end" class="m l">● LIVE TELEMETRY</text>
<line x1="50" y1="82" x2="1150" y2="82" class="line"/>

<g transform="translate(70,125)">
<rect width="350" height="290" rx="16" fill="#0f172a" stroke="#475569"/>
<text x="25" y="35" class="m l">$ ./silicon_core</text>
<rect x="92" y="70" width="166" height="125" rx="14" fill="#111827" stroke="#67e8f9"/>
<text x="175" y="126" text-anchor="middle" class="m t">RTL</text>
<text x="175" y="153" text-anchor="middle" class="m l">DESIGN CORE</text>
<g stroke="#67e8f9" stroke-width="4" class="p">
<path d="M92 92H55 M92 123H45 M92 154H55 M258 92H295 M258 123H305 M258 154H295"/>
<path d="M120 70V40 M153 70V30 M186 70V40 M219 70V30"/>
<path d="M120 195V225 M153 195V235 M186 195V225 M219 195V235"/>
</g>
<text x="25" y="250" class="m l">VERILOG / SYSTEMVERILOG</text>
<text x="25" y="272" class="m l">FPGA / SoC / VERIFICATION</text>
</g>

<g transform="translate(475,125)">
<text y="20" class="m l">$ ./system-info</text>
<text y="55" class="m l">DOMAIN</text><text x="180" y="55" class="m v">RTL / DV / FPGA</text>
<text y="88" class="m l">SPECIALTY</text><text x="180" y="88" class="m v">Digital Design</text>
<text y="121" class="m l">SIMULATION</text><text x="180" y="121" class="m v">QuestaSim</text>
<text y="154" class="m l">FPGA FLOW</text><text x="180" y="154" class="m v">Vivado / Libero</text>
<text y="187" class="m l">SCRIPTING</text><text x="180" y="187" class="m v">Python / TCL / C</text>
<text y="220" class="m l">STATUS</text><text x="180" y="220" class="m v a">BUILDING</text>
</g>

<g transform="translate(475,370)">
<text class="m l">$ ./active-work</text>
<text y="34" class="m v">01  Runtime Verification</text>
<text y="64" class="m v">02  AHB / MSS / FPGA Integration</text>
<text y="94" class="m v">03  CXL.mem → LPDDR5X</text>
</g>

<g transform="translate(70,450)">
<text class="m l">$ ./github-telemetry</text>
<line y1="18" x2="1080" y2="18" class="line"/>
<text y="55" class="m l">PUBLIC REPOS</text><text x="155" y="55" class="m v">{esc(public_repos)}</text>
<text x="300" y="55" class="m l">FOLLOWERS</text><text x="420" y="55" class="m v">{esc(followers)}</text>
<text x="555" y="55" class="m l">STARS</text><text x="625" y="55" class="m v">{esc(stars)}</text>
<text x="760" y="55" class="m l">COMMITS / 30D</text><text x="900" y="55" class="m v">{esc(commits)}</text>
<text y="88" class="m l">LAST REFRESH: {esc(now)}</text>
<circle cx="1060" cy="82" r="5" fill="#67e8f9" class="p"/>
</g>
</svg>"""

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(svg, encoding="utf-8")
    print("Wrote", OUT)

if __name__ == "__main__":
    main()
