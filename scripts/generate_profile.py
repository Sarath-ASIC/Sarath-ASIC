#!/usr/bin/env python3
"""Generate the live VLSI engineering section of README.md."""

import json
import os
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
CONFIG = ROOT / "profile.yml"
DATA = ROOT / "profile-data/profile-data.json"
START = "<!-- PROFILE:START -->"
END = "<!-- PROFILE:END -->"


def config():
    # This intentionally supports the simple YAML shipped with this project.
    # PyYAML is used when installed; otherwise the lists are parsed directly.
    try:
        import yaml
        return yaml.safe_load(CONFIG.read_text()) or {}
    except ImportError:
        out, section, current = {}, None, None
        for raw in CONFIG.read_text().splitlines():
            s = raw.strip()
            if not s or s.startswith("#"):
                continue
            if not raw.startswith(" "):
                if ":" in s:
                    k, v = s.split(":", 1)
                    k, v = k.strip(), v.strip()
                    if v:
                        out[k] = v.strip("'\"")
                        section = None
                    else:
                        out[k] = []
                        section = k
                        current = out[k]
            elif s.startswith("- ") and isinstance(current, list):
                current.append(s[2:].strip("'\""))
        return out


def api(path, token=None):
    h = {"Accept": "application/vnd.github+json", "User-Agent": "Sarath-ASIC-profile"}
    if token:
        h["Authorization"] = "Bearer " + token
    req = urllib.request.Request("https://api.github.com" + path, headers=h)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())


def age(ts):
    if not ts:
        return "unknown"
    dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
    d = datetime.now(timezone.utc) - dt
    if d.days == 0:
        h = d.seconds // 3600
        return f"{h}h ago" if h else "today"
    if d.days < 30:
        return f"{d.days}d ago"
    if d.days < 365:
        return f"{d.days//30}mo ago"
    return f"{d.days//365}y ago"


def main():
    cfg = config()
    user = cfg.get("username", "Sarath-ASIC")
    token = os.getenv("GITHUB_TOKEN")
    excluded = set(cfg.get("excluded_repositories", ["Sarath-ASIC"]))
    max_repos = int(cfg.get("max_repositories", 30))

    profile = api("/users/" + urllib.parse.quote(user), token)
    repos = api("/users/" + urllib.parse.quote(user) +
                "/repos?per_page=100&sort=updated", token)
    repos = [r for r in repos if not r.get("fork") and r["name"] not in excluded]
    repos.sort(key=lambda r: r.get("updated_at") or "", reverse=True)
    repos = repos[:max_repos]

    # Evidence detection from repository metadata. We deliberately avoid
    # claiming proficiency or assigning skill scores.
    signatures = {
        "SystemVerilog": [".sv", ".svh", "systemverilog"],
        "Verilog": [".v", ".vh", "verilog"],
        "SVA": ["assert property", "assertion", "cover property", "$past", "$rose", "$fell", "disable iff"],
        "Functional Coverage": ["covergroup", "coverpoint", "cross coverage", "illegal_bins"],
        "UVM": ["uvm", "uvm_test", "uvm_component", "uvm_sequence"],
        "CXL": ["cxl", "cxl.mem", "cxl_mem"],
        "LPDDR5X": ["lpddr5x", "lpddr5"],
        "Memory Verification": ["memory verification", "mem verification", "memory test"],
        "Testbench": ["testbench", "verification"],
    }

    evidence = {k: [] for k in signatures}
    languages = {}
    activity = []

    for r in repos:
        text = " ".join([
            r.get("name", ""),
            r.get("description", "") or "",
            " ".join(r.get("topics", []) or []),
            r.get("language", "") or ""
        ]).lower()

        for tech, patterns in signatures.items():
            if any(p.lower() in text for p in patterns):
                evidence[tech].append(r["name"])

        if r.get("language"):
            languages[r["language"]] = languages.get(r["language"], 0) + 1

        try:
            commits = api("/repos/%s/%s/commits?per_page=3" % (user, r["name"]), token)
            for c in commits:
                ci = c.get("commit", {})
                author = ci.get("author") or {}
                activity.append({
                    "repo": r["name"],
                    "message": (ci.get("message") or "").splitlines()[0][:100],
                    "date": author.get("date"),
                    "url": c.get("html_url")
                })
        except Exception:
            pass

    activity.sort(key=lambda x: x.get("date") or "", reverse=True)

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        "## LIVE ENGINEERING STATUS",
        "",
        f"> Generated from public GitHub evidence. Last refresh: **{now}**.",
        "",
        "### Current Focus",
        ""
    ]
    for x in cfg.get("current_focus", []):
        lines.append("- " + x)
    lines += ["", "### Learning Path", ""]
    for x in cfg.get("learning", []):
        lines.append("- " + x)

    lines += [
        "", "## ENGINEERING EVIDENCE", "",
        f"- **{profile.get('public_repos', 0)}** public repositories",
        f"- **{profile.get('followers', 0)}** GitHub followers",
        f"- **{len(repos)}** repositories inspected",
        "",
        "### Detected Toolchain & Concepts",
        "",
        "| Area | Repository evidence |",
        "|---|---:|"
    ]

    order = ["SystemVerilog", "Verilog", "SVA", "Functional Coverage",
             "UVM", "CXL", "LPDDR5X", "Memory Verification", "Testbench"]
    for tech in order:
        if evidence[tech]:
            lines.append(f"| {tech} | {len(evidence[tech])} repo(s) |")

    lines += [
        "",
        "> Counts represent repository evidence, not proficiency scores.",
        "",
        "### Repository Languages",
        "",
        "| Language | Repositories |",
        "|---|---:|"
    ]
    for lang, count in sorted(languages.items(), key=lambda x: (-x[1], x[0])):
        lines.append(f"| {lang} | {count} |")

    lines += ["", "## RECENT BUILD LOG", ""]
    if activity:
        lines += ["| Time | Repository | Commit |", "|---|---|---|"]
        for a in activity[:8]:
            repo = f"[{a['repo']}]({a['url']})" if a["url"] else a["repo"]
            msg = a["message"].replace("|", "\\|")
            lines.append(f"| {age(a['date'])} | {repo} | {msg} |")
    else:
        lines.append("No recent public commit activity was available.")

    lines += ["", "## ACTIVE PROJECTS", "",
              "| Repository | Language | Stars | Last update |",
              "|---|---|---:|---|"]
    featured = cfg.get("featured_repositories", [])
    selected = [r for r in repos if r["name"] in featured] if featured else repos[:6]
    for r in selected:
        name = f"[{r['name']}]({r['html_url']})"
        lines.append(f"| {name} | {r.get('language') or '—'} | {r.get('stargazers_count', 0)} | {age(r.get('updated_at'))} |")

    generated = "\n".join(lines).rstrip()
    old = README.read_text(encoding="utf-8")
    a, b = old.find(START), old.find(END)
    if a < 0 or b < a:
        raise RuntimeError("README.md is missing PROFILE:START/PROFILE:END markers.")
    README.write_text(old[:a] + START + "\n" + generated + "\n" + old[b+len(END):], encoding="utf-8")

    DATA.parent.mkdir(exist_ok=True)
    DATA.write_text(json.dumps({
        "generated_at": now,
        "public_repositories": profile.get("public_repos", 0),
        "followers": profile.get("followers", 0),
        "languages": languages,
        "technology_evidence": evidence,
        "recent_activity": activity[:10]
    }, indent=2), encoding="utf-8")

    print("Profile updated:", README)
    print("Generated data:", DATA)


if __name__ == "__main__":
    main()
