# Clôture d'exercice SYSCOHADA : référence détaillée

Tous les codes cités ont été vérifiés dans `plan-comptable.csv`. Un code absent du plan (par exemple 799, 4486) ne doit pas être utilisé sans l'avoir confirmé dans le plan officiel de l'entité.

## 1. Contrôles préalables sur la balance

1. Total des soldes débiteurs égal au total des soldes créditeurs (et totaux de mouvements égaux).
2. Tous les codes existent dans le plan. Un code de plus de 4 chiffres se rattache à son préfixe (compte auxiliaire de l'entreprise).
3. Soldes à contre-sens à examiner, avec reclassement bilan si l'anomalie est réelle :
   - client créditeur : à présenter en 419 (avances et acomptes reçus) au passif ;
   - fournisseur débiteur : à présenter en 409 (fournisseurs débiteurs) à l'actif ;
   - caisse (57) créditrice : erreur de saisie ou opération non enregistrée ;
   - charge créditrice ou produit débiteur : régularisation ou erreur d'imputation.
4. TVA : solder 443 (facturée) et 445 (récupérable) contre 444 (TVA due ou crédit de TVA).
5. Comptes d'attente (471) et virements internes (58) : doivent être soldés.

## 2. Soldes intermédiaires de gestion (SIG)

Le plan réserve 132 à 138 aux SIG, 131 au résultat net bénéficiaire et 139 au résultat net déficitaire.

| SIG | Compte | Principe de calcul (trame à aligner sur le tableau officiel) |
|---|---|---|
| Marge brute | 132 | Ventes de marchandises (701) moins achats de marchandises (601) corrigés de la variation de stock (6031) ; en industrie, production vendue moins coût d'achat des matières |
| Valeur ajoutée | 133 | Marge brute plus production de l'exercice, moins consommations de tiers (61, 62, 63, autres achats) |
| Excédent brut d'exploitation | 134 | Valeur ajoutée plus subventions d'exploitation (71), moins impôts et taxes (64), moins charges de personnel (66) |
| Résultat d'exploitation | 135 | EBE plus reprises et transferts de charges d'exploitation (78, 791, 798), moins dotations d'exploitation (681, 691, 659), plus autres produits (75), moins autres charges (65) |
| Résultat financier | 136 | Revenus financiers (77) et reprises financières, moins frais financiers (67) et dotations financières (697) |
| Résultat des activités ordinaires | 137 | Résultat d'exploitation plus résultat financier |
| Résultat hors activités ordinaires | 138 | Produits H.A.O. (82, 84, 86, 88) moins charges H.A.O. (81, 83, 85) |
| Résultat net | 131 ou 139 | R.A.O. plus R.H.A.O., moins participation des travailleurs (87), moins impôts sur le résultat (89) |

Contrôle obligatoire : le résultat net obtenu par la cascade doit égaler la somme (crédit moins débit) des comptes de classes 6, 7 et 8. La commande `balance` du script donne cette valeur. S'il y a un écart, chercher le compte mal classé avant de rendre le résultat.

## 3. Écritures d'inventaire

Chaque écriture est présentée en tableau Date, Compte, Libellé, Débit, Crédit, avec l'égalité des totaux vérifiée par calcul.

### Amortissements
Débit 6812 (incorporelles) ou 6813 (corporelles) ; crédit 281 (incorporelles), 282 (terrains), 283 (bâtiments, installations) ou 284 (matériel). Données à demander : valeur d'origine, mode (linéaire ou dégressif), durée, date de mise en service. Prorata temporis pour les entrées et sorties en cours d'année.

### Provisions pour risques et charges
- Exploitation : débit 6911 (risques et charges) ou 6912 (grosses réparations) ; crédit au compte 19x concerné (191 litiges, 192 garanties clients, 195 impôts, 196 pensions, 1971 grosses réparations, 198 autres).
- Financières : débit 6971 ; crédit 19x (par exemple 194 pour pertes de change).
- Dépréciation d'immobilisations : débit 6913 ou 6914 (exploitation), 6972 (financières) ; crédit 291 à 297 selon la nature.

### Dépréciation des stocks
Débit 659 (charges provisionnées d'exploitation, selon le plan fourni, à confirmer dans le plan officiel) ; crédit 391 à 398 selon la catégorie de stock.

### Créances clients douteuses
1. Reclassement : débit 416 (4161 litigieuses) ; crédit 411.
2. Dépréciation : débit 659 ; crédit 491 (4911 litigieuses, 4912 douteuses).
3. Perte définitive : débit 651 ; crédit 416 ou 411 (avec reprise de la dépréciation correspondante).

### Reprises
- Provisions d'exploitation : crédit 791 ; débit du compte de provision.
- Amortissements repris : crédit 798.
- Provisions financières : crédit 797 ; charges provisionnées financières reprises : crédit 779.
- Le plan fourni ne contient pas de compte 799 : pour les reprises de dépréciations d'exploitation (stocks, créances), vérifier le compte exact dans le plan officiel.

### Stocks (variation)
- Annulation du stock initial : débit 603x (6031 marchandises, 6032 matières premières, 6033 autres approvisionnements) ; crédit 31 à 38 concerné.
- Constatation du stock final : débit 31 à 38 ; crédit 603x.
- Production stockée : même mécanisme avec 73x (734 en-cours de produits, 735 services en cours, 736 produits finis, 737 produits intermédiaires).

### Charges à payer
Débit du compte de charge ; crédit :
- 408 (4081) fournisseurs, factures non parvenues ;
- 4281 congés payés à provisionner, 4286 autres charges de personnel à payer ;
- 438 organismes sociaux, charges à payer ;
- 448 État, charges à payer.

### Produits à recevoir
Crédit du compte de produit ; débit :
- 418 (4181 clients, factures à établir) ;
- 4287 personnel, produits à recevoir ;
- 438 ou 448 pour les organismes sociaux et l'État ;
- 475 pour les travaux non encore facturables.

### Régularisations
- Charges constatées d'avance : débit 476 ; crédit du compte de charge.
- Produits constatés d'avance : débit du compte de produit ; crédit 477.
- Écarts de conversion : 478 (actif, perte latente) et 479 (passif, gain latent). Provision pour perte de change : débit 6971 ; crédit 194.

### Participation et impôt sur le résultat
- Participation des travailleurs : débit 871 (légale), 874 (contractuelle) ou 878 ; crédit au compte de dette concerné.
- Impôt : débit 891 (8911 activités exercées dans l'État) ou 895 (impôt minimum forfaitaire) ; crédit 441 (État, impôt sur les bénéfices), net des acomptes déjà versés. Taux et minimum forfaitaire dépendent du pays membre : demander le pays, ne pas trancher, renvoyer vers un fiscaliste.

### Détermination du résultat
Solder les comptes de charges et de produits (classes 6, 7, 8) : le bénéfice est porté au crédit de 131, la perte au débit de 139.

## 4. États financiers

- Compte de résultat : charges (classe 6 puis comptes de gestion de la classe 8) et produits (classe 7 puis classe 8), par nature, selon la cascade des SIG.
- Bilan, actif : immobilisations de la classe 2 nettes de 28 et 29 ; stocks de la classe 3 nets de 39 ; créances de la classe 4 nettes de 49 ; trésorerie-actif de la classe 5.
- Bilan, passif : capitaux propres de la classe 1 (résultat inclus) ; dettes financières ; dettes de la classe 4 ; trésorerie-passif (56).
- Comptes mixtes (42, 44, 45, 46, 47, 48, 52, 53) : actif si le solde est débiteur, passif s'il est créditeur, compte par compte, sans compensation entre comptes différents.
- Contrôle final : total actif égal au total passif.
- Tableau des flux de trésorerie et notes annexes : proposer la structure et la liste des informations à collecter, sans inventer les montants.

## 5. Affectation du résultat

Après approbation des comptes par l'organe compétent :

1. Transfert du résultat vers l'instance d'affectation : 131 vers 1301 (bénéfice), 139 vers 1309 (perte).
2. Ventilation : réserve légale 111, réserves facultatives 1181, report à nouveau créditeur 121 ou débiteur 129 (1291 perte nette à reporter), dividendes à payer 465.

Taux de réserve légale, conditions de distribution et fiscalité des dividendes dépendent de la forme sociale et du pays : demander et signaler comme hypothèse.
