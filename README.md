# syscohada-skill

Skill pour agents IA dédié à la comptabilité **SYSCOHADA / OHADA** : plan comptable complet, imputation, contrôle de balance, résultat, soldes intermédiaires de gestion et écritures de clôture.

Un seul skill, installable sur **Claude** (Claude Code, claude.ai, Desktop), **Codex** et **ChatGPT**, car il suit le format ouvert Agent Skills (un dossier avec un fichier `SKILL.md`).

## Ce que fait le skill

- **Plan comptable** : retrouver, expliquer et valider un compte parmi 878 (classes 1 à 9), avec libellé, niveau, parent, nature, sens et chemin hiérarchique.
- **Imputation** : proposer l'écriture d'une opération avec débit et crédit équilibrés et une justification par compte.
- **Validation de lots de codes** : valides, invalides, format incorrect, comptes voisins suggérés, rattachement des auxiliaires de plus de 4 chiffres.
- **Contrôle de balance** : équilibre, codes inconnus, soldes à contre-sens, comptes d'attente non soldés, résultat provisoire.
- **Clôture** : soldes intermédiaires de gestion, écritures d'inventaire (amortissements, provisions, stocks, charges à payer, produits à recevoir, régularisations, impôt), bilan, compte de résultat, affectation du résultat.
- **Exports** du plan en CSV, JSON ou Markdown.

## Installation

| Plateforme | Méthode |
|---|---|
| Claude Code | Plugin ou script (voir ci-dessous) |
| Claude (claude.ai, Desktop) | Importer `dist/syscohada-skill.zip` dans les réglages des skills |
| Codex | Script d'installation ou copie dans `~/.agents/skills/syscohada` |
| ChatGPT | Skill (bêta) ou GPT personnalisé : voir [chatgpt/README.md](chatgpt/README.md) |
| Autre agent compatible Agent Skills | Copier `skills/syscohada/` dans le dossier de skills de l'agent |

### Cloner le dépôt

```bash
git clone https://github.com/arnoldkouya/syscohada-skill.git
cd syscohada-skill
```

### Claude Code

Par le plugin :

```text
/plugin marketplace add arnoldkouya/syscohada-skill
/plugin install syscohada@syscohada-skill
```

Ou par le script, qui copie le skill dans `~/.claude/skills/syscohada` :

```bash
scripts/install.sh claude            # pour tous vos projets
scripts/install.sh claude --project  # pour le projet courant (.claude/skills)
```

### Claude (claude.ai, Desktop)

```bash
python3 scripts/build_zips.py
```

Puis, dans les réglages de Claude, section des capacités ou des skills, importer `dist/syscohada-skill.zip` (le dossier `syscohada/` est à la racine de l'archive). L'intitulé exact du menu varie selon la version de l'application.

### Codex

```bash
scripts/install.sh codex            # ~/.agents/skills/syscohada
scripts/install.sh codex --project  # .agents/skills du projet courant
```

Sous Windows, utiliser `scripts\install.ps1 -Target codex` (ou `claude`, `all`, avec `-Project` pour le projet courant). Dans Codex, le skill s'active seul selon la description, ou en le nommant : `$syscohada`.

### ChatGPT

Voir [chatgpt/README.md](chatgpt/README.md) : import comme skill (bêta, à activer dans l'espace de travail) ou GPT personnalisé avec `dist/syscohada-gpt-pack.zip`.

## Exemples de demandes

- « Quel compte utiliser pour une facture d'électricité ? »
- « Valide ces codes : 6011 4111 9999 ABCD »
- « Donne-moi l'arbre du compte 60 sur deux niveaux. »
- « Voici ma balance, contrôle-la et donne le résultat. »
- « Prépare les écritures de clôture : amortissements, charges à payer, impôt. »
- « Exporte la classe 6 en CSV. »

## Utiliser le script seul

`skills/syscohada/scripts/syscohada.py` fonctionne sans l'agent (Python 3.8 ou plus, aucune dépendance) :

```bash
python3 skills/syscohada/scripts/syscohada.py find 6011
python3 skills/syscohada/scripts/syscohada.py search "matières premières"
python3 skills/syscohada/scripts/syscohada.py validate 6011 4111 9999
python3 skills/syscohada/scripts/syscohada.py tree 60 --depth 2
python3 skills/syscohada/scripts/syscohada.py export --format csv --classe 6
python3 skills/syscohada/scripts/syscohada.py balance examples/balance-exemple.csv
```

La balance est un CSV avec les colonnes `compte`, `debit`, `credit` (ou `solde`, positif au débit). Les séparateurs `,`, `;` et tabulation et les nombres au format `1 234,56` ou `1,234.56` sont acceptés. Les lignes de total sont ignorées. Le code de sortie est 1 si la balance est déséquilibrée.

## Structure du dépôt

```text
skills/syscohada/
├── SKILL.md                    # le skill
├── references/
│   ├── plan-comptable.csv      # 878 comptes
│   └── cloture.md              # SIG, écritures d'inventaire, états financiers
└── scripts/syscohada.py        # recherche, validation, contrôle de balance
.claude-plugin/                 # manifestes du plugin Claude Code
chatgpt/                        # instructions et guide pour ChatGPT
scripts/                        # install.sh, install.ps1, build_zips.py
examples/balance-exemple.csv
tests/test_syscohada.py
AGENTS.md                       # consignes pour les agents qui modifient ce dépôt
```

## Développement

```bash
python3 -m unittest discover -s tests -v   # tests
python3 scripts/build_zips.py              # archives dans dist/
```

## Limites

- Le plan s'arrête au niveau 4 (4 chiffres). Les comptes plus fins sont propres à chaque entreprise. Quelques comptes du plan officiel peuvent manquer (par exemple 799).
- Les données viennent de [arnoldkouya/plan-comptable-syscohada](https://github.com/arnoldkouya/plan-comptable-syscohada), une source tierce et non le texte officiel OHADA. Pour une liasse destinée à l'administration ou à un commissaire aux comptes, recouper avec l'Acte uniforme relatif au droit comptable et à l'information financière en vigueur.
- Les formules de SIG et les modèles d'états financiers sont une trame de travail.
- Aucun conseil fiscal : les taux et règles varient selon le pays membre.
- Le résultat est un travail préparatoire qui doit être validé par un expert-comptable.

## Licence

MIT, voir [LICENSE](LICENSE).
