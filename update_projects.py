from pathlib import Path

import requests

USERNAME = "ldgk2712"
URL = f"https://api.github.com/users/{USERNAME}/repos?sort=created&direction=desc"
README_PATH = Path(__file__).resolve().parent / "README.md"
START_TAG = "<!-- featured-projects:start -->"
END_TAG = "<!-- featured-projects:end -->"
MAX_PROJECTS = 5


def fetch_repos():
    response = requests.get(URL, timeout=15)
    response.raise_for_status()

    repos = response.json()
    public_repos = [
        repo
        for repo in repos
        if repo.get("name") != USERNAME and not repo.get("fork", False)
    ]
    return public_repos[:MAX_PROJECTS]


def build_project_html(repos):
    if not repos:
        return '<p align="center"><i>No public projects to feature right now.</i></p>'

    cards = []
    for repo in repos:
        name = repo["name"]
        url = repo["html_url"]
        cards.append(
            f"""<p align="center">
  <a href="{url}">
    <img src="https://github-readme-stats.vercel.app/api/pin/?username={USERNAME}&repo={name}&bg_color=ffe4e1&title_color=ff1493&text_color=c71585&icon_color=ff69b4&border_color=ffb6c1" />
  </a>
</p>"""
        )
    return "\n".join(cards)


def replace_section(content, replacement):
    start_idx = content.find(START_TAG)
    end_idx = content.find(END_TAG)

    if start_idx == -1 or end_idx == -1 or start_idx >= end_idx:
        raise ValueError("Featured projects markers are missing or invalid in README.md")

    section_start = start_idx + len(START_TAG)
    return content[:section_start] + "\n" + replacement + "\n" + content[end_idx:]


def update_readme():
    repos = fetch_repos()
    project_html = build_project_html(repos)
    content = README_PATH.read_text(encoding="utf-8")
    new_content = replace_section(content, project_html)
    README_PATH.write_text(new_content, encoding="utf-8")


if __name__ == "__main__":
    update_readme()
