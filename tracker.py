#!/usr/bin/env python3
"""Plan GitHub achievement progress using only the Python standard library."""

import argparse
import json
import re
import subprocess
from html.parser import HTMLParser
from pathlib import Path
from urllib.request import Request, urlopen


def parse_achievements(html):
    """Read visible achievement images, deduplicating repeated profile sections."""
    class AchievementParser(HTMLParser):
        def __init__(self):
            super().__init__()
            self.badges = {}

        def handle_starttag(self, tag, attrs):
            attrs = dict(attrs)
            alt = attrs.get("alt", "")
            if tag == "img" and alt.startswith("Achievement: "):
                name = alt.removeprefix("Achievement: ").strip()
                if name:
                    self.badges[name] = attrs.get("src", "")

    parser = AchievementParser()
    parser.feed(html)
    return [{"name": name, "image_url": url} for name, url in sorted(parser.badges.items())]


def live_snapshot(user):
    """Read merge counts through gh and visible badges from the public profile."""
    if not re.fullmatch(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?", user):
        raise ValueError("invalid GitHub username")
    result = subprocess.run(
        ["gh", "api", "--method", "GET", "search/issues", "-f",
         f"q=is:pr is:merged author:{user}", "-f", "per_page=1"],
        check=True, capture_output=True, text=True, timeout=30)
    data = json.loads(result.stdout)
    if data.get("incomplete_results"):
        raise ValueError("GitHub returned incomplete search results; retry later")
    request = Request(f"https://github.com/{user}",
                      headers={"User-Agent": "github-badge-lab/1.0"})
    with urlopen(request, timeout=20) as response:
        badges = parse_achievements(response.read().decode("utf-8"))
    return data["total_count"], badges


def pull_shark_progress(merged, milestones):
    """Return the highest reached milestone and the next target."""
    if merged < 0:
        raise ValueError("merged pull request count cannot be negative")
    reached = 0
    for target in milestones:
        if merged < target:
            return {"merged": merged, "reached": reached, "next": target,
                    "remaining": target - merged}
        reached = target
    return {"merged": merged, "reached": reached, "next": None, "remaining": 0}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--merged", type=int,
                        help="number of merged pull requests you authored (offline)")
    source.add_argument("--user", help="read a user's merge count and public badges")
    parser.add_argument("--profile-html", type=Path,
                        help="read badges from a saved profile instead (with --merged)")
    args = parser.parse_args()
    catalog = json.loads(Path(__file__).with_name("achievements.json").read_text())
    if args.user and args.profile_html:
        parser.error("--profile-html requires --merged")
    try:
        merged, badges = live_snapshot(args.user) if args.user else (args.merged, None)
        if args.profile_html:
            badges = parse_achievements(args.profile_html.read_text())
        progress = pull_shark_progress(merged, catalog["pull_shark"]["milestones"])
    except subprocess.CalledProcessError as error:
        parser.error(f"GitHub CLI failed: {error.stderr.strip()}")
    except (OSError, ValueError, subprocess.TimeoutExpired) as error:
        parser.error(str(error))
    report = {"pull_shark": progress,
              "note": "Search counts can lag. Reported milestones are not proof of an award."}
    if badges is not None:
        report["visible_achievements"] = badges
        report["visibility_note"] = "Only publicly displayed badges are included; hidden badges are unknown."
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
