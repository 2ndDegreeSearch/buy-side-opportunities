# Contributing

Thanks for helping keep this board accurate.

## Suggesting a change

The easiest way is to [open an issue](../../issues/new/choose) with the "Add a firm" or "Update or remove a firm" form.
A maintainer will update the data for you.

## Editing the data directly

The board is generated from [`firms.csv`](./firms.csv).
Do not edit `README.md` by hand, because it is overwritten on every update.

1. Fork the repo and edit `firms.csv`.
2. Optionally preview the result with `python3 .github/scripts/build_board.py` (Python 3.10+, no dependencies).
3. Open a pull request.
   A GitHub Action checks that the CSV renders, and regenerates `README.md` once the pull request is merged.

### Columns

| Column | Meaning |
|---|---|
| `#` | Stable row ID. Use the next unused number for a new firm. |
| `Section` | Board category. One of `Private Credit & Asset-Based Finance`, `BDCs & Venture Debt`, `Hedge Funds`, `Litigation Finance & Insurance-Linked Securities` or `Emerging Managers`. |
| `Firm` | Firm name. |
| `Strategy` | Short description of what the firm invests in. |
| `HQ` | Headquarters city. |
| `AUM` | Assets under management as reported. |
| `Careers / contact` | A posted role (write "<Title> posting", e.g. "Credit Analyst posting"), a careers page or job board, a public contact, or "No public careers page found". |
| `Careers / contact link` | URL of the posting, careers page or website, or a `mailto:` address. It becomes the Apply, Careers, Website or Email button. |

## Guidelines

- Only add public contact information that the firm publishes itself, such as general inboxes, recruiting addresses and main office numbers.
  Do not add personal emails or phone numbers of individual employees.
- Cite a source for AUM figures in your issue or pull request.
- When a role closes, remove the word "posting" from `Careers / contact` so the firm drops the 🟢 marker.
