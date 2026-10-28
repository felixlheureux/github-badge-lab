#!/usr/bin/env python3
"""Plan GitHub achievement progress using only the Python standard library."""

import argparse
import json
from pathlib import Path


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
    parser.add_argument("--merged", type=int, required=True,
                        help="number of merged pull requests you authored")
    args = parser.parse_args()
    catalog = json.loads(Path(__file__).with_name("achievements.json").read_text())
    try:
        progress = pull_shark_progress(args.merged, catalog["pull_shark"]["milestones"])
    except ValueError as error:
        parser.error(str(error))
    print(json.dumps({"pull_shark": progress,
                      "note": "Reported milestones; confirm awards on your live profile."},
                     indent=2))


if __name__ == "__main__":
    main()
