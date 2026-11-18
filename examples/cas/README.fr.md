# Cas de test avec soldes de clôture connus

**Français** | [English](README.md)

Chaque dossier est une petite entreprise fictive dont les chiffres ont été calculés à la main :

- `avant.csv` : balance **avant** clôture.
- `ecritures.csv` : les écritures de clôture (mêmes colonnes, ajoutées compte par compte).
- `attendu.json` : le résultat attendu : totaux, résultat, actif net et solde de chaque compte après clôture.

| Cas | Contenu | Total débit après clôture (FCFA) | Résultat | Actif net |
|---|---|---|---|---|
| `01-societe-de-services` | Société de services : amortissement, charge à payer, charge constatée d'avance, impôt | 26 310 000 | 3 520 000 | 14 170 000 |
| `02-commerce-cession-hao` | Commerce : variation de stock, cession d'un véhicule (comptes H.A.O. 81/82), amortissement, impôt | 63 500 000 | 4 900 000 | 22 500 000 |

## Vérifier soi-même

```bash
python3 skills/syscohada/scripts/syscohada.py balance examples/cas/01-societe-de-services/avant.csv --ecritures examples/cas/01-societe-de-services/ecritures.csv
python3 -m unittest tests.test_cas -v
```

Le test recalcule les chiffres avec son propre code, indépendant du script, puis vérifie que le script retrouve les mêmes totaux et le même résultat. Règle de bilan utilisée : les comptes de classes 1 à 5 à solde débiteur vont à l'actif, à solde créditeur au passif ; les comptes de provisions et amortissements (28, 29, 39, 49, 59) viennent en déduction de l'actif ; le résultat s'ajoute au passif.

## Limites, et une demande

- Les entreprises et les chiffres sont **inventés**. Ils montrent comment le skill calcule ; ce n'est pas un modèle pour une liasse réelle.
- Les chiffres ont été calculés à la main et vérifiés par du code, **sans relecture d'un comptable**. Le choix des comptes et les écritures de clôture sont simplifiés (par exemple, pas de liquidation de TVA ni d'affectation du résultat).
- **Si vous êtes comptable, je serais ravi que vous testiez ces cas et que vous me fassiez un retour** (mauvais compte, écriture manquante, pratique de clôture différente) : [ouvrez une issue](https://github.com/arnoldkouya/syscohada-skill/issues) ou proposez une pull request. Les corrections sont les bienvenues et seront créditées.
