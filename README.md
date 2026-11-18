# syscohada-skill

**English** | [Français](README.fr.md)

AI agent skill for **SYSCOHADA / OHADA** accounting, the accounting system of the OHADA member states (mainly in West and Central Africa): full chart of accounts, entry posting suggestions, trial balance checks, result calculation, intermediate management balances (SIG) and year-end closing entries.

One skill, installable on **Claude** (Claude Code, claude.ai, Desktop), **Codex** and **ChatGPT**, because it follows the open Agent Skills format (a folder with a `SKILL.md` file).

> **Language note:** the skill's instructions (`SKILL.md`), reference documents and the ChatGPT instructions are written in French, as is the accounting vocabulary of the chart of accounts. This README and the ChatGPT guide are available in English; translating the skill itself is a welcome contribution.

## What the skill does

- **Chart of accounts**: look up, explain and validate any of 878 accounts (classes 1 to 9), with label, level, parent, nature, normal balance side and hierarchical path.
- **Posting**: suggest the journal entry for a transaction, with balanced debit and credit and a one-line justification per account.
- **Batch validation of account codes**: valid, invalid, wrong format, nearest accounts suggested, and codes longer than 4 digits attached to their parent in the plan.
- **Trial balance check**: debit/credit balance, unknown codes, balances on the unusual side, suspense accounts not cleared, provisional result.
- **Year-end closing**: intermediate management balances (SIG), adjusting entries (depreciation, provisions, inventory, accruals, deferrals, income tax), balance sheet, income statement, appropriation of the result.
- **Exports** of the chart as CSV, JSON or Markdown.

## Installation

| Platform | Method |
|---|---|
| Claude Code | Plugin or script (see below) |
| Claude (claude.ai, Desktop) | Import `dist/syscohada-skill.zip` in the skills settings |
| Codex | Install script, or copy into `~/.agents/skills/syscohada` |
| ChatGPT | Skill (beta) or custom GPT: see [chatgpt/README.en.md](chatgpt/README.en.md) |
| Any other Agent Skills compatible agent | Copy `skills/syscohada/` into the agent's skills folder |

### Clone the repository

```bash
git clone https://github.com/arnoldkouya/syscohada-skill.git
cd syscohada-skill
```

### Claude Code

With the plugin:

```text
/plugin marketplace add arnoldkouya/syscohada-skill
/plugin install syscohada@syscohada-skill
```

Or with the script, which copies the skill into `~/.claude/skills/syscohada`:

```bash
scripts/install.sh claude            # for all your projects
scripts/install.sh claude --project  # for the current project (.claude/skills)
```

### Claude (claude.ai, Desktop)

```bash
python3 scripts/build_zips.py
```

Then, in Claude's settings (capabilities or skills section), import `dist/syscohada-skill.zip` (the `syscohada/` folder sits at the root of the archive). The exact menu name varies with the app version.

### Codex

```bash
scripts/install.sh codex            # ~/.agents/skills/syscohada
scripts/install.sh codex --project  # .agents/skills of the current project
```

On Windows, use `scripts\install.ps1 -Target codex` (or `claude`, `all`, with `-Project` for the current project). In Codex the skill activates on its own based on its description, or by name: `$syscohada`.

### ChatGPT

See [chatgpt/README.en.md](chatgpt/README.en.md): import as a skill (beta, to be enabled in the workspace) or a custom GPT with `dist/syscohada-gpt-pack.zip`.

## Example requests

The skill is written in French; these are English renderings of the kind of request it handles.

- "Which account should I use for an electricity bill?"
- "Validate these codes: 6011 4111 9999 ABCD"
- "Show me the tree of account 60, two levels deep."
- "Here is my trial balance, check it and give me the result."
- "Prepare the closing entries: depreciation, accruals, income tax."
- "Export class 6 as CSV."

## Using the script on its own

`skills/syscohada/scripts/syscohada.py` works without any agent (Python 3.8 or later, no dependencies):

```bash
python3 skills/syscohada/scripts/syscohada.py find 6011
python3 skills/syscohada/scripts/syscohada.py search "matières premières"
python3 skills/syscohada/scripts/syscohada.py validate 6011 4111 9999
python3 skills/syscohada/scripts/syscohada.py tree 60 --depth 2
python3 skills/syscohada/scripts/syscohada.py export --format csv --classe 6
python3 skills/syscohada/scripts/syscohada.py balance examples/balance-exemple.csv
```

Account labels are in French, so searches use French terms. A trial balance is a CSV with the columns `compte` (account), `debit`, `credit` (or `solde`, positive on the debit side). The separators `,`, `;` and tab, and numbers written `1 234,56` or `1,234.56`, are accepted. Total rows are ignored. The exit code is 1 when the trial balance does not balance.

## Repository layout

```text
skills/syscohada/
├── SKILL.md                    # the skill
├── references/
│   ├── plan-comptable.csv      # 878 accounts
│   └── cloture.md              # SIG, adjusting entries, financial statements
└── scripts/syscohada.py        # search, validation, trial balance check
.claude-plugin/                 # Claude Code plugin manifests
chatgpt/                        # instructions and guide for ChatGPT
scripts/                        # install.sh, install.ps1, build_zips.py
examples/balance-exemple.csv
tests/test_syscohada.py
AGENTS.md                       # guidelines for agents that modify this repository
```

## Development

```bash
python3 -m unittest discover -s tests -v   # tests
python3 scripts/build_zips.py              # archives in dist/
```

## Limitations

- The chart stops at level 4 (4 digits). Finer accounts are specific to each company. A few accounts of the official chart may be missing (for example 799).
- The data comes from [arnoldkouya/plan-comptable-syscohada](https://github.com/arnoldkouya/plan-comptable-syscohada), a third-party source and not the official OHADA text. For financial statements filed with the tax authorities or reviewed by an auditor, cross-check against the Uniform Act on Accounting Law and Financial Reporting in force.
- The SIG formulas and the financial statement layouts are a working framework.
- No tax advice: rates and rules vary by member state.
- The output is preparatory work and must be validated by a qualified accountant.

## License

MIT, see [LICENSE](LICENSE).
