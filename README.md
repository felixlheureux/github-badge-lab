# GitHub Badge Lab

[![Test tracker](https://github.com/felixlheureux/github-badge-lab/actions/workflows/test.yml/badge.svg)](https://github.com/felixlheureux/github-badge-lab/actions/workflows/test.yml)

A small achievement tracker and a place to practice GitHub's issue and pull
request workflows. Work stays in this repository.

## Track progress

Requires Python 3.10 or newer; no dependencies or network access are needed.

```sh
python3 tracker.py --merged 12
python3 -m unittest -v
```

The tracker prints the last reached Pull Shark milestone, the next target,
and the number of merges remaining. Negative counts are rejected.

GitHub Actions runs the offline tests and CLI smoke checks on Python 3.10 and
3.13 for pull requests and changes to `main`. Live profile requests stay manual
so CI does not depend on external profile availability or account credentials.

To read current activity and publicly displayed achievements:

```sh
gh auth login
python3 tracker.py --user YOUR_USERNAME
```

Live mode requires the [GitHub CLI](https://cli.github.com/) and network access.
It only reads data. Search results can lag behind merges, and hidden achievements
cannot be detected. Private PRs may be included when the authenticated account
can access them. Image URLs preserve GitHub's displayed tier artwork.

You can also inspect a saved public profile without network access:

```sh
python3 tracker.py --merged 16 --profile-html profile.html
```

## Achievement checklist

| Achievement | Next action |
| --- | --- |
| Quickdraw | Close an issue or pull request within five minutes of opening it. |
| YOLO | Merge your own pull request without a review, where repository rules allow it. |
| Pull Shark | Open pull requests that get merged. Reported milestones: 2, 16, 128, 1,024. |
| Pair Extraordinaire | Collaborate with another person and credit their coauthored work in a merged PR. |
| Galaxy Brain | Write useful Discussion answers that maintainers accept. |
| Starstruck | Build a repository that attracts stars from other people. |
| Public Sponsor | Sponsor an open source maintainer through GitHub Sponsors. This costs money. |

GitHub awards achievements asynchronously. Completing an action does not prove
that a badge has appeared; check the live profile afterward. Tier thresholds are
community reported and can change. Historical awards such as Arctic Code Vault
Contributor cannot be newly earned.

See [GitHub's profile reference](https://docs.github.com/en/account-and-profile/reference/profile-reference#earning-achievements)
and the [community achievement catalog](https://github.com/Schweinepriester/github-profile-achievements).

## Boundaries

Use real contributions and accurate attribution. Do not manufacture identities,
stars, accepted answers, or contributions to other people's repositories.
Sponsorship needs a separate choice of recipient and budget.
A small GitHub achievement tracker and workflow playground.
