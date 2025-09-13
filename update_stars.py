"""GitHub Stars Updater"""

import os
from pathlib import Path

import requests

GITHUB_API_URL = "https://api.github.com/repos"
GITHUB_USER_REPOS_URL = "https://api.github.com/user/repos?visibility=public&affiliation=owner&sort=stars&direction=desc"
README_TEMPLATE = """
## Socials

- Twitter: [@rushter](https://x.com/rushter)
- Blog: [https://rushter.com/blog/](https://rushter.com/blog/)


## 📦 Public Projects

{projects}
"""
repos_to_ignore = [
    "Facebook-Recruiting",
    "strolax",
    "rushter",
    "find_domains",
]


def get_user_repos(token):
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {token}",
    }
    try:
        r = requests.get(GITHUB_USER_REPOS_URL, headers=headers)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"Exception when fetching user repos: {str(e)}")
        return None


def update_readme():
    readme_path = Path("README.md")

    token = os.environ.get("GH_TOKEN")
    repos = get_user_repos(token)
    if not repos:
        return False

    projects = []
    for repo in sorted(repos, key=lambda x: x["stargazers_count"], reverse=True):
        if repo["fork"]:
            continue
        name = repo["name"]
        if name in repos_to_ignore:
            continue
        url = repo["html_url"]
        description = repo["description"] or ""
        stars = repo["stargazers_count"]
        projects.append(f"- [{name}]({url}) — {description} **(★ {stars:,})**")

    content = README_TEMPLATE.format(projects="\n".join(projects))
    readme_path.write_text(content)
    return True


if __name__ == "__main__":
    assert update_readme()
