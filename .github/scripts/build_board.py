#!/usr/bin/env python3
"""Render README.md, a GitHub job board of buy-side firms, from firms.csv.

The layout follows community boards such as SimplifyJobs/Summer2027-Internships:
a category index with counts, a legend, then one table per category.

Usage:
    python3 .github/scripts/build_board.py [--input firms.csv] [--output README.md]

The update-readme workflow runs this on every push that changes firms.csv.
"""

from __future__ import annotations

import argparse
import csv
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]  # repo root, two levels above .github/scripts

# Allowed values of the CSV "Section" column, in board order.
CATEGORIES = {
    "Private Credit & Asset-Based Finance": "💳",
    "BDCs & Venture Debt": "🏦",
    "Hedge Funds": "📈",
    "Litigation Finance & Insurance-Linked Securities": "⚖️",
    "Emerging Managers": "🌱",
}

POSTING = re.compile(r"\bposting\b|handshake", re.I)
JOB_BOARD = re.compile(r"job board|\bjobs\b|careers (page|link|via)|job listings|built in|apply", re.I)
NO_CAREERS = re.compile(r"no public careers page", re.I)
# A bare website such as "engagedcapital.com" or "numer.ai".
BARE_DOMAIN = re.compile(r"(?:[a-z0-9-]+\.)+[a-z]{2,}", re.I)

BADGE = "https://img.shields.io/badge/{label}-{color}?style=flat"
BADGE_COLORS = {"Apply": "2ea44f", "Careers": "0969da", "Website": "6e7781", "Email": "6e7781"}


@dataclass
class Firm:
    name: str
    section: str
    strategy: str
    hq: str
    aum: str
    careers: str
    link: str

    @property
    def status(self) -> str:
        """posting: a specific role was seen; board: a jobs page exists; contact: neither."""
        if POSTING.search(self.careers):
            return "posting"
        if NO_CAREERS.search(self.careers):
            return "contact"
        if JOB_BOARD.search(self.careers):
            return "board"
        return "contact"

    @property
    def opportunity(self) -> str:
        """The posted role, the jobs page, or the public contact, as shown on the board."""
        if self.status == "posting":
            # "Credit Analyst posting" -> "Credit Analyst"; "Job posting (Paylocity)" -> "Open role (Paylocity)"
            role = " ".join(re.sub(r"\b(job\s+)?posting\b", "", self.careers, flags=re.I).split())
            if not role or role.startswith("(") or role.lower().startswith("on "):
                role = f"Open role {role}".strip()
            return role
        if NO_CAREERS.search(self.careers):
            return ""
        if self.link and BARE_DOMAIN.fullmatch(self.careers):
            return ""  # the link button already points at this website
        return self.careers

    @property
    def link_label(self) -> str | None:
        if not self.link:
            return None
        if self.link.startswith("mailto:"):
            return "Email"
        return {"posting": "Apply", "board": "Careers", "contact": "Website"}[self.status]


def read_firms(path: Path) -> list[Firm]:
    with open(path, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    firms = []
    for row in rows:
        section = row["Section"].strip()
        if section not in CATEGORIES:
            raise SystemExit(
                f"Unknown section {section!r} for {row['Firm']!r}. Use one of: {', '.join(CATEGORIES)}"
            )
        firms.append(
            Firm(
                name=row["Firm"].strip(),
                section=section,
                strategy=row["Strategy"].strip(),
                hq=row["HQ"].strip(),
                aum=row["AUM"].strip().strip('"'),
                careers=row["Careers / contact"].strip(),
                link=row["Careers / contact link"].strip(),
            )
        )
    return firms


def cell(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ")


def anchor(heading: str) -> str:
    """GitHub heading anchor: lowercase, drop punctuation and emoji, spaces to dashes.

    GitHub keeps the invisible emoji variation selector U+FE0F (as in "⚖️"), so it is kept here too.
    """
    return re.sub(r"[^\w\- ️]", "", heading.lower()).replace(" ", "-")


def render_row(firm: Firm) -> str:
    name = f"**{cell(firm.name)}**"
    if firm.status == "posting":
        name = f"🟢 {name}"
    button = "-"
    if firm.link_label:
        badge = BADGE.format(label=firm.link_label, color=BADGE_COLORS[firm.link_label])
        button = f'<a href="{firm.link}"><img src="{badge}" alt="{firm.link_label}"></a>'
    return (
        f"| {name} | {cell(firm.strategy)} | {cell(firm.hq)} | {cell(firm.aum)} "
        f"| {cell(firm.opportunity) or '-'} | {button} |"
    )


def sort_key(firm: Firm) -> tuple:
    rank = {"posting": 0, "board": 1, "contact": 2}[firm.status]
    return (rank, firm.name.lower())


def render(firms: list[Firm], today: date) -> str:
    by_section = {s: sorted((f for f in firms if f.section == s), key=sort_key) for s in CATEGORIES}
    n_posting = sum(f.status == "posting" for f in firms)

    out = [
        "# Buy-Side Opportunities",
        "",
        f"A curated list of **{len(firms)} small and mid-sized buy-side firms** across private credit, "
        "BDCs, hedge funds, litigation finance and insurance-linked securities, "
        "with what is known about how each one hires.",
        f"**{n_posting}** firms had a specific role posted when the list was compiled.",
        "",
        "Most of these firms are too small for campus recruiting, so a direct note to the contact listed often goes further than a portal.",
        "",
        "🙏 **Know a firm that belongs here, or a role that opened or closed? "
        "[Open an issue](../../issues/new/choose) or see the [contribution guidelines](./CONTRIBUTING.md).** 🙏",
        "",
        "---",
        "",
        f"### Browse {len(firms)} Firms by Category",
        "",
    ]
    for section, emoji in CATEGORIES.items():
        open_roles = sum(f.status == "posting" for f in by_section[section])
        out.append(
            f"{emoji} **[{section}](#{anchor(emoji + ' ' + section)})** "
            f"({len(by_section[section])} firms, {open_roles} with open roles)"
        )
        out.append("")
    out += [
        "---",
        "",
        "## Legend",
        "",
        "- 🟢 A specific role was posted when the list was compiled (it may have closed since)",
        "- **Opportunity / contact**: the posted role, the firm's jobs page, or a public contact when neither exists",
        "- **Link**: Apply goes to the posting, Careers to the firm's jobs page, Website and Email to the firm's public contact",
        "",
        "---",
        "",
    ]
    for section, emoji in CATEGORIES.items():
        out += [
            f"## {emoji} {section}",
            "",
            "[Back to top](#buy-side-opportunities)",
            "",
            "| Firm | Strategy | HQ | AUM | Opportunity / contact | Link |",
            "|---|---|---|---|---|---|",
        ]
        out += [render_row(f) for f in by_section[section]]
        out.append("")
    out += [
        "---",
        "",
        "## Updating this board",
        "",
        "This README is generated from [`firms.csv`](./firms.csv) by "
        "[`.github/scripts/build_board.py`](./.github/scripts/build_board.py). "
        "Do not edit it by hand: change `firms.csv` and a GitHub Action regenerates it.",
        "",
        f"<sub>Last generated {today.isoformat()}. AUM figures come from Form ADV, 13F and press sources noted in `firms.csv`.</sub>",
        "",
    ]
    return "\n".join(out)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--input", default=ROOT / "firms.csv", type=Path)
    parser.add_argument("--output", default=ROOT / "README.md", type=Path)
    args = parser.parse_args()
    firms = read_firms(args.input)
    args.output.write_text(render(firms, date.today()), encoding="utf-8")
    print(f"Wrote {args.output} ({len(firms)} firms)")


if __name__ == "__main__":
    main()
