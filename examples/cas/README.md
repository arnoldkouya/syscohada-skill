# Test cases with known closing balances

[Français](README.fr.md) | **English**

Each folder is a small fictional company with figures worked out by hand:

- `avant.csv`: trial balance **before** closing.
- `ecritures.csv`: the closing entries (same columns, added account by account).
- `attendu.json`: the expected result: totals, profit, net assets, and the balance of every account after closing.

| Case | Content | Total debit after closing (FCFA) | Profit | Net assets |
|---|---|---|---|---|
| `01-societe-de-services` | Services company: depreciation, accrued expense, prepaid expense, income tax | 26 310 000 | 3 520 000 | 14 170 000 |
| `02-commerce-cession-hao` | Trading company: stock variation, vehicle disposal (H.A.O. accounts 81/82), depreciation, income tax | 63 500 000 | 4 900 000 | 22 500 000 |

## Check it yourself

```bash
python3 skills/syscohada/scripts/syscohada.py balance examples/cas/01-societe-de-services/avant.csv --ecritures examples/cas/01-societe-de-services/ecritures.csv
python3 -m unittest tests.test_cas -v
```

The test recomputes the figures with its own code, independently of the script, then checks that the script returns the same totals and profit. The balance sheet rule used: classes 1 to 5 with a debit balance go to assets, with a credit balance to liabilities; contra accounts (28, 29, 39, 49, 59) are netted against assets; the profit is added to liabilities.

## Limits, and a request

- The companies and figures are **invented**. They show how the skill computes; they are not a model for a real filing.
- The figures were worked out by hand and checked by code, **not reviewed by an accountant**. The choice of accounts and the closing entries are simplified (for example, no VAT settlement and no appropriation of the result).
- **If you are an accountant, I would be glad if you tested these cases and told me what you find** (wrong account, missing entry, a closing practice that differs): [open an issue](https://github.com/arnoldkouya/syscohada-skill/issues) or send a pull request. Corrections are welcome and will be credited.
