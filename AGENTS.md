# Instructions pour les agents qui modifient ce dépôt

Ce dépôt contient un seul skill, `skills/syscohada/`, au format Agent Skills (dossier avec `SKILL.md`, `references/`, `scripts/`).

## Règles

- Source de vérité du skill : `skills/syscohada/`. Ne pas dupliquer son contenu ailleurs ; les scripts d'installation et de packaging le copient.
- `SKILL.md` doit garder un frontmatter avec `name: syscohada` et une `description` de moins de 1024 caractères.
- Toute modification de `references/plan-comptable.csv` doit conserver les colonnes `code, libelle, classe, niveau, parent, nature, sens` et l'intégrité hiérarchique (le test `test_plan_size_and_integrity` la vérifie).
- Tout code cité dans `references/cloture.md` ou `SKILL.md` doit exister dans `plan-comptable.csv`. Vérifier avec `python3 skills/syscohada/scripts/syscohada.py find CODE`.
- `scripts/syscohada.py` n'utilise que la bibliothèque standard Python (3.8+). Ne pas ajouter de dépendance.
- `chatgpt/instructions.md` doit rester sous 8 000 caractères (limite des GPT personnalisés).
- `README.md` (anglais) et `README.fr.md` (français) disent la même chose : toute modification de l'un se répercute dans l'autre. Même règle pour `chatgpt/README.md` et `chatgpt/README.en.md`.

## Vérifications avant de livrer

```bash
python3 -m unittest discover -s tests -v
python3 scripts/build_zips.py
```
