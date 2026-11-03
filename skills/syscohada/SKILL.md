---
name: syscohada
description: Comptabilité SYSCOHADA/OHADA. Retrouver, valider et expliquer un compte du plan comptable (classes 1 à 9, sens débit/crédit), proposer une imputation, contrôler une balance, calculer le résultat et les soldes intermédiaires de gestion, préparer les écritures de clôture, le bilan et le compte de résultat. À utiliser dès qu'un numéro de compte SYSCOHADA, une balance, une clôture d'exercice ou l'espace OHADA est mentionné. Pas pour le PCG français ni l'IFRS.
---

# SYSCOHADA : plan comptable, imputation et clôture

Ce skill couvre le plan comptable SYSCOHADA (espace OHADA) et le cycle de clôture : trouver un compte, imputer une opération, contrôler une balance, calculer le résultat, préparer les écritures d'inventaire et les états financiers.

## Ressources du skill

Toutes les ressources sont dans le dossier de ce skill. Les chemins ci-dessous sont relatifs à ce dossier.

| Fichier | Usage |
|---|---|
| `references/plan-comptable.csv` | Plan complet : 878 comptes, colonnes `code, libelle, classe, niveau, parent, nature, sens` |
| `references/cloture.md` | Détail de la clôture : SIG, écritures d'inventaire, états financiers, affectation du résultat. À lire avant toute tâche de clôture. |
| `scripts/syscohada.py` | Outil en ligne de commande (Python 3, bibliothèque standard uniquement) : recherche, validation, arbre, export, contrôle de balance |

Ne jamais recopier des comptes de mémoire : lire le CSV ou lancer le script. Un libellé ou un sens non retrouvé dans le plan ne doit pas être inventé.

## Utiliser le script

```bash
python3 scripts/syscohada.py find 6011            # fiche d'un compte + chemin hiérarchique
python3 scripts/syscohada.py search "marchandises" # recherche insensible à la casse et aux accents
python3 scripts/syscohada.py validate 6011 4111 9999 ABCD
python3 scripts/syscohada.py tree 60 --depth 2     # descendants
python3 scripts/syscohada.py classe 5 --niveau 3   # comptes d'une classe
python3 scripts/syscohada.py export --format csv --classe 6 > classe6.csv
python3 scripts/syscohada.py balance balance.csv   # contrôle + résultat (ajouter --json si besoin)
```

Si Python n'est pas disponible, lire directement `references/plan-comptable.csv`.

## Structure du plan

Un code a 1 à 4 chiffres. Le premier chiffre est la classe, la longueur est le niveau (1 classe, 2 compte principal, 3 divisionnaire, 4 sous-compte). Le parent s'obtient en retirant le dernier chiffre.

| Classe | Contenu | Nature |
|---|---|---|
| 1 | Ressources durables (capital, réserves, report à nouveau, résultat, emprunts, provisions) | bilan |
| 2 | Actif immobilisé (28 amortissements, 29 dépréciations) | bilan |
| 3 | Stocks (39 dépréciations) | bilan |
| 4 | Tiers (40 fournisseurs, 41 clients, 42 personnel, 43 organismes sociaux, 44 État, 46 associés, 47 divers, 48 H.A.O., 49 dépréciations) | bilan |
| 5 | Trésorerie (52 banques, 57 caisse, 56 crédits de trésorerie) | bilan |
| 6 | Charges des activités ordinaires | gestion |
| 7 | Produits des activités ordinaires | gestion |
| 8 | Autres charges et produits (cessions, H.A.O., participation, impôt sur le résultat) | gestion |
| 9 | Engagements hors bilan (90-91) et comptabilité analytique (92-99) | hors-bilan, cage |

Sens habituel du solde : débit pour les charges et les actifs, crédit pour les produits, amortissements, dépréciations et dettes. Les comptes mixtes (42, 44, 45, 46, 47, 48, 52, 53) peuvent être débiteurs ou créditeurs. Le sens exact de chaque compte est dans la colonne `sens` du CSV.

## Méthodes

### Retrouver ou valider un compte
1. Vérifier le format (1 à 4 chiffres).
2. Chercher le compte dans le plan. S'il n'existe pas, le dire et proposer les comptes voisins (même parent).
3. Restituer code, libellé, classe, niveau, parent, nature, sens et chemin hiérarchique.

### Proposer une imputation
1. Qualifier l'opération (achat, vente, paie, immobilisation, financement, impôt, etc.).
2. Partir de la classe puis descendre au niveau le plus fin disponible, en vérifiant chaque code dans le plan.
3. Donner l'écriture équilibrée en tableau (Compte, Libellé, Débit, Crédit) avec une justification d'une ligne par compte.
4. Poser une question quand c'est ambigu (activité ordinaire ou H.A.O., TVA récupérable ou facturée, frais accessoires d'achat) plutôt que de deviner.

### Valider un lot de codes
Rendre trois listes : valides, invalides, format incorrect. Pour chaque invalide, suggérer le code existant le plus proche (même préfixe). Un code de plus de 4 chiffres (compte auxiliaire propre à l'entreprise) se rattache à son préfixe existant dans le plan.

### Contrôler une balance et clore l'exercice
1. Lancer `balance` sur le fichier : équilibre débit/crédit, codes inconnus, soldes à contre-sens, comptes d'attente non soldés, résultat provisoire.
2. Si la balance est déséquilibrée, s'arrêter et présenter l'écart avant tout autre calcul.
3. Lire `references/cloture.md`, puis dérouler : SIG, écritures d'inventaire, états financiers, affectation.
4. Demander les données manquantes (dates de mise en service, taux, durées, pays) au lieu de les inventer.
5. Vérifier par calcul, pas à vue d'œil : total débit = total crédit dans chaque écriture, résultat des SIG = produits moins charges, total actif = total passif.

## Livrables

- Question ponctuelle sur un compte : réponse courte en prose (code, libellé, sens, remarque utile).
- Imputation : tableau d'écriture, puis une ligne de justification.
- Lot de codes ou export du plan : fichier CSV, JSON ou XLSX selon la demande, avec un résumé de deux phrases.
- Clôture à partir d'un fichier : un classeur avec les onglets Balance contrôlée, SIG, Écritures de clôture, Bilan, Compte de résultat, et des formules plutôt que des valeurs en dur. Terminer par les hypothèses prises et les informations manquantes.

## Limites à annoncer

- Le plan s'arrête au niveau 4 (4 chiffres). Les sous-comptes plus fins et les tiers auxiliaires sont propres à chaque entreprise.
- Le jeu de données provient du dépôt arnoldkouya/plan-comptable-syscohada, une source tierce et non le texte officiel OHADA. Quelques comptes du plan officiel peuvent manquer (par exemple 799). Pour une liasse destinée à l'administration, à un commissaire aux comptes ou à un audit, recouper avec l'Acte uniforme relatif au droit comptable et à l'information financière en vigueur.
- Les formules de SIG et les modèles d'états financiers sont une trame de travail. Annoncer l'hypothèse retenue, ne jamais la présenter comme le texte officiel.
- Pas de conseil fiscal : taux d'impôt, impôt minimum forfaitaire et déductibilité varient selon le pays membre. Renvoyer vers un professionnel.
- Le résultat est un travail préparatoire qui doit être validé par un expert-comptable.
