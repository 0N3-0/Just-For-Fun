import random
import base64
import requests
from datetime import datetime, timedelta, timezone

days = 30
date_limit = datetime.now(timezone.utc) - timedelta(days=days)
date_str = date_limit.strftime("%Y-%m-%d")  
SEARCH_URL = "https://api.github.com/search/repositories"
README_URL_TMPL = "https://api.github.com/repos/{full_name}/readme"

headers = {
    "Accept": "application/vnd.github+json"
}

def fetch_readme(full_name: str) -> str:
    url = README_URL_TMPL.format(full_name=full_name)
    r = requests.get(url, headers=headers, timeout=10)
    if r.status_code != 200:
        return ""
    data = r.json()
    if "content" not in data:
        return ""
    try:
        text = base64.b64decode(data["content"]).decode("utf-8", errors="ignore")
        return text
    except Exception:
        return ""

def main():
    page = random.randint(1, 200)

    params = {
        "q": f"pushed:>{date_str}",
        "sort": "stars",
        "order": "desc",
        "per_page": 5,
        "page": page
    }

    resp = requests.get(SEARCH_URL, params=params, headers=headers, timeout=10)
    resp.raise_for_status()
    data = resp.json()

    for repo in data["items"]:
        full_name = repo["full_name"]

        readme = fetch_readme(full_name)
        readme_preview = readme

        print("=" * 66)
        print(f"Project: {full_name}")
        print(f"Updated at: {repo['updated_at']}")
        print(f"Stars: {repo['stargazers_count']}")
        print(f"Forks: {repo['forks_count']}")
        print(f"Watchers: {repo['watchers_count']}")
        print(f"Language: {repo.get('language')}")
        print(f"Topics: {', '.join(repo.get('topics', []))}")
        print(f"License: {(repo['license'] or {}).get('name')}")
        print(f"URL: {repo['html_url']}")
        print(f"Created: {repo['created_at']} | Updated: {repo['updated_at']}")
        print(f"Description: {repo.get('description')}")
        print("\nREADME Preview:")
        print(readme_preview or "(No README or not accessible)")
        print()

if __name__ == "__main__":
    main()
