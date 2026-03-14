#!/usr/bin/env python3
"""Generate profile README from projects.json + GitHub API descriptions."""
import json, subprocess

with open("projects.json") as f:
    projects = json.load(f)

rows = []
for p in projects:
    repo = p["repo"]
    icon = p["icon"]
    tags = p["tags"]
    name = repo.split("/")[1].capitalize()

    result = subprocess.run(
        ["gh", "api", f"repos/{repo}", "--jq", ".description // empty"],
        capture_output=True, text=True
    )
    desc = result.stdout.strip() or "No description"

    rows.append(
        "  <tr>\n"
        "    <td align=\"center\" width=\"80\">\n"
        f"      <a href=\"https://github.com/{repo}\">\n"
        f"        <img src=\"https://raw.githubusercontent.com/{repo}/main/{icon}\" width=\"48\" />\n"
        "      </a>\n"
        "    </td>\n"
        "    <td>\n"
        f"      <b><a href=\"https://github.com/{repo}\">{name}</a></b> — {desc}<br/>\n"
        f"      <sub>{tags}</sub>\n"
        "    </td>\n"
        "  </tr>"
    )

table = "\n".join(rows)

readme = (
    "## Hey, I'm Oleg \U0001f44b\n"
    "\n"
    "I build small apps that solve real problems "
    "— usually for myself first, then share them when they turn out useful.\n"
    "\n"
    "### My projects\n"
    "\n"
    "<table>\n"
    + table + "\n"
    "</table>\n"
    "\n"
    "### Tech I work with\n"
    "\n"
    "<p>\n"
    '  <img src="https://img.shields.io/badge/Rust-000?logo=rust&logoColor=fff" alt="Rust" />\n'
    '  <img src="https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff" alt="Python" />\n'
    '  <img src="https://img.shields.io/badge/Tauri-24C8D8?logo=tauri&logoColor=fff" alt="Tauri" />\n'
    '  <img src="https://img.shields.io/badge/TypeScript-3178C6?logo=typescript&logoColor=fff" alt="TypeScript" />\n'
    '  <img src="https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=fff" alt="Docker" />\n'
    '  <img src="https://img.shields.io/badge/Linux-FCC624?logo=linux&logoColor=000" alt="Linux" />\n'
    "</p>\n"
    "\n"
    "---\n"
    "\n"
    "If any of these save you time, a \u2b50 would be appreciated.\n"
)

with open("README.md", "w") as f:
    f.write(readme)

print(f"Generated README with {len(projects)} projects")
