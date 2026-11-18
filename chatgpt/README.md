# Utiliser le skill dans ChatGPT

[English](README.en.md) | **Français**

Deux voies. La première est la plus simple si les skills sont activés dans votre espace de travail ; la seconde fonctionne avec un GPT personnalisé.

## Voie 1 : skill ChatGPT (bêta)

Les skills ChatGPT suivent le format ouvert Agent Skills, le même que celui de ce dépôt. Ils sont désactivés par défaut pendant la bêta : le propriétaire de l'espace de travail doit les activer dans les paramètres de l'espace de travail.

1. Construire l'archive : `python3 scripts/build_zips.py` (produit `dist/syscohada-skill.zip`).
2. Dans ChatGPT, importer le skill depuis l'interface de gestion des skills, en fournissant le dossier `skills/syscohada/` (ou l'archive). Si l'import direct n'est pas proposé sur votre offre, demander à ChatGPT « Build me a skill » puis coller le contenu de `skills/syscohada/SKILL.md`, et joindre les fichiers du dossier `references/` et `scripts/`.
3. Mentionner le skill avec @ dans une conversation, ou laisser ChatGPT le choisir selon la description.

Les capacités et les offres concernées évoluent : se référer à la documentation OpenAI en vigueur pour les détails d'import.

## Voie 2 : GPT personnalisé

1. Construire le pack : `python3 scripts/build_zips.py` (produit `dist/syscohada-gpt-pack.zip`) et le décompresser.
2. Dans ChatGPT : Explorer les GPT, puis Créer.
3. Onglet Configurer :
   - Nom : « Assistant SYSCOHADA ».
   - Instructions : coller le contenu de `instructions.md`. Il fait moins de 8 000 caractères.
   - Fichiers de connaissance : téléverser `plan-comptable.csv`, `cloture.md` et `syscohada.py`.
   - Capacités : activer l'interpréteur de code (Code Interpreter), nécessaire pour lancer `syscohada.py` et générer des fichiers XLSX.
4. Enregistrer, puis tester avec :
   - « Quel compte pour une facture d'électricité ? »
   - « Valide ces codes : 6011 4111 9999 »
   - le téléversement de `examples/balance-exemple.csv` avec « Contrôle cette balance et donne le résultat ».

Si le téléversement du fichier `.py` est refusé, renommer `syscohada.py` en `syscohada.txt`, le téléverser, et ajouter dans les instructions : « copier syscohada.txt en syscohada.py avant de l'exécuter ».
