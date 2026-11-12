# Contributing

Thanks for helping keep this board accurate.

## Suggesting a change

The easiest way is to [open an issue](../../issues/new/choose) with the "Add a firm" or "Update or remove a firm" form.
A maintainer will update the data for you.

## Editing the data directly

The board is generated from [`firms.csv`](./firms.csv).
Do not edit `README.md` by hand. It is regenerated from `firms.csv`.

1. Fork the repo and edit `firms.csv`.
2. Regenerate the board with `python3 .github/scripts/build_board.py` (Python 3.10+, no dependencies).
3. Commit both `firms.csv` and `README.md`, and open a pull request.
   A GitHub Action fails the pull request if `README.md` does not match `firms.csv`.
   A maintainer reviews and merges it.

### Columns

| Column | Meaning |
|---|---|
| `#` | Stable row ID. Use the next unused number for a new firm. |
| `Section` | Board category. One of `Private Credit & Asset-Based Finance`, `BDCs & Venture Debt`, `Hedge Funds`, `Litigation Finance & Insurance-Linked Securities` or `Emerging Managers`. |
| `Firm` | Firm name. |
| `Strategy` | Short description of what the firm invests in. |
| `HQ` | Headquarters city. |
| `AUM` | Assets under management as reported. |
| `Posting` | `Y` if the firm has a specific role open, otherwise `N`. `Y` shows the 🟢 marker and an Apply button. |
| `Careers / contact` | The open role's title when `Posting` is `Y` (e.g. "Credit Analyst (Lever)"), otherwise a careers page or job board, a public contact, or "No public careers page found". |
| `Careers / contact link` | URL of the posting, careers page or website, or a `mailto:` address. It becomes the Apply, Careers, Website or Email button. |

## Guidelines

- Only add public contact information that the firm publishes itself, such as general inboxes, recruiting addresses and main office numbers.
  Do not add personal emails or phone numbers of individual employees.
- Cite a source for AUM figures in your issue or pull request.
- When a role closes, set `Posting` to `N` and replace the role title in `Careers / contact` with the firm's careers page or contact, if it has one.
