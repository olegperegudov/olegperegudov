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

    # Fetch description from GitHub API
    result = subprocess.run(
        ["gh", "api", f"repos/{repo}", "--jq", ".description // empty"],
        capture_output=True, text=True
    )
    desc = result.stdout.strip() or "No description"

    rows.append(f"""  <tr>
    <td align="center" width="80">
      <a href="https://github.com/{repo}">
        <img src="https://raw.githubusercontent.com/{repo}/main/{icon}" width="48" />
      </a>
    </td>
    <td>
      <b><a href="https://github.com/{repo}">{name}</a></b> — {desc}<br/>
      <sub>{tags}</sub>
    </td>
  </tr>""")

table = "
".join(rows)

readme = f"""## Hey, I'm Oleg 👋

I build small apps that solve real problems — usually for myself first, then share them when they turn out useful.

### My projects

<table>
{table}
</table>

### Tech I work with

<p>
  <img src="https://img.shields.io/badge/Rust-000?logo=rust&logoColor=fff" alt="Rust" />
  <img src="https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff" alt="Python" />
  <img src="https://img.shields.io/badge/Tauri-24C8D8?logo=tauri&logoColor=fff" alt="Tauri" />
  <img src="https://img.shields.io/badge/TypeScript-3178C6?logo=typescript&logoColor=fff" alt="TypeScript" />
  <img src="https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=fff" alt="Docker" />
  <img src="https://img.shields.io/badge/Linux-FCC624?logo=linux&logoColor=000" alt="Linux" />
</p>

---

If any of these save you time, a ⭐ would be appreciated.
"""

with open("README.md", "w") as f:
    f.write(readme)

print(f"Generated README with {len(projects)} projects")
