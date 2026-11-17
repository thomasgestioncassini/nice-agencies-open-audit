# Analyse initiale — IA B

Fournisseur : google · modèle : gemini-4-hydrogen · statut : **ok**
Empreinte du mandat : 82e0fec40442f9e2ab530af39492ad0a83e777c1e424867598daa9a65e8089c8 · empreinte de l’entrée : c6839fa63f47ff91b745dbdf66218d568b14b795769db4bb534886fb2f3d8dbc
Coût : 0.1863 $ (17737 jetons lus, 21286 écrits)

> Texte produit par l’IA, publié sans aucune modification ni relecture de l’éditeur.

## Résumé

Le contre-audit du classement v5.6 de meilleure-agence-nice.fr (546 agences, relevé du 17/11/2026) confirme une reproduction arithmétique exacte des notes et des rangs (546/546 conformes, 0 divergence). En revanche, l'examen approfondi révèle une contradiction critique et un double standard dans la notation des honoraires des deux agences de l'éditeur (SARL GESTION CASSINI) : sur une phrase strictement identique concernant le payeur, Gestion Cassini obtient 0/30 tandis qu'ImmoVendu obtient 30/30 (+5,10 points sur sa note finale). Par ailleurs, des écarts entre le code appliqué et la méthode publiée déplacent 254 rangs sur 546, et l'inclusion de 18 264 avis sans profil précisé (55,2 % des avis comptés) bouleverse 526 rangs sur 546, pénalisant lourdement Gestion Cassini (-69 rangs). L'hypothèse d'une manipulation unilatérale en faveur de l'éditeur est toutefois contredite par l'exception d'ancienneté qu'il s'est imposée sur ImmoVendu (-4,38 points, la faisant sortir du Top 10 au rang 12) et par le score de 0/30 infligé à Gestion Cassini.

## Constats

### B-1 · Contradiction critique et double standard sur le critère Payeur indiqué des barèmes d'honoraires

Catégorie : honoraires · nature : fait_verifie · gravité : critique · concerne l’éditeur : oui

Le 17/11/2026 (date_relecture_payeur), les deux sites de l'éditeur affichaient exactement la même formule conditionnelle renvoyant au mandat de vente sans désigner un payeur unique. Gestion Cassini a reçu 0/30 (confirmé par l'ambiguïté du texte, hono=70,0) tandis qu'ImmoVendu a reçu 30/30 (contredit par son propre texte, hono=100,0). Ce seul écart apporte +5,10 points à ImmoVendu (qui tomberait de 87,58 à 82,48 avec 0/30) et prive Gestion Cassini d'un gain potentiel de +5,10 points (79,62 au lieu de 74,52).

Preuves : baremes_relus[0] (gestion-cassini, 2026-11-17) : Payeur indiqué = 0/30 ; texte_page : « Honoraires à la charge du VENDEUR ou de l’ACQUEREUR en fonction du mandat de vente. » ; baremes_relus[1] (immovendu, 2026-11-17) : Payeur indiqué = 30/30 ; texte_page : « Honoraires à la charge du VENDEUR ou de l’ACQUEREUR en fonction du mandat de vente. » ; agences_editeur : gestion-cassini hono=70.0, immovendu hono=100.0 (poids hono=17 %, soit 5,10 points de note finale)

Incertitude : Impossible de déterminer d'après le paquet seul si l'erreur vient d'un excès de sévérité envers Gestion Cassini ou d'une indulgence injustifiée envers ImmoVendu ; les barèmes des 544 agences concurrentes ne sont pas fournis.

### B-2 · Impact massif de l'inclusion des 18 264 avis sans profil d'auteur précisé (55,2 % des avis comptés), pénalisant Gestion Cassini

Catégorie : biais · nature : calcul_reproduit · gravité : critique · concerne l’éditeur : oui

Bien que la méthode privilégie les avis de vente et d'achat, 55,2 % des avis retenus ne comportent aucune indication de profil et sont intégralement comptés. Leur exclusion dans le test contrefactuel déplace 526 agences sur 546 (médiane de 26 places, jusqu'à 252 places) et modifie 4 places du Top 10. Contrairement à l'hypothèse d'un biais pro-éditeur, cette règle pénalise fortement Gestion Cassini (qui perd 69 rangs et 4,72 points) ainsi qu'ImmoVendu (rang 12 au lieu de 9).

Preuves : tests_biais.avis_non_precises : avis_non_precises=18264, avis_comptes=33064, part_dans_les_avis_comptes=0.552, exclus_faute_de_profil=0 ; scenario_sans_non_precises : rangs_changes=526, deplacement_max=252, deplacement_median=26.0, top10_inchanges=6 ; agences_suivies : gestion-cassini passe du rang 131 (74.52) au rang 62 (79.24) ; immovendu passe du rang 12 (87.58) au rang 9 (87.50)

Incertitude : La proportion d'avis réellement liés à la vente ou à l'achat parmi ces 18 264 avis sans profil (notamment issus de Google) n'est pas mesurable sans les textes et profils primaires.

### B-3 · Écarts entre les règles programmées et le texte méthodologique publié, modifiant 254 rangs sur 546

Catégorie : methode · nature : calcul_reproduit · gravité : majeur · concerne l’éditeur : oui

Quatre règles appliquées contredisent le texte public ou comportent une ambiguïté majeure : l'inclusion des doublons dans le dénominateur de la régularité (I-4), la redistribution des 15 % de régularité quand aucun avis unitaire n'est relevé malgré l'interdiction annoncée de redistribuer un poids manquant (I-6), le classement sur note arrondie au centième plutôt que sur note exacte (I-7) et le départage par tous les avis quel que soit le profil (I-11). L'effet combiné modifie 359 notes et 254 rangs (jusqu'à 34 places). L'écart I-4 favorise ImmoVendu d'une place (12e au lieu de 13e), tandis que I-6 défavorise Gestion Cassini de deux places (131e au lieu de 129e).

Preuves : regles_appliquees_absentes_ou_contraires_au_texte : I-4 (contradiction sur doublons de régularité), I-6 (redistribution de 15 % si régularité absente), I-7 (arrondis intermédiaires au dixième/centième), I-11 (départage tous profils + id interne). ; effet_des_regles_vs_texte_initial.ensemble : notes_changees=359, rangs_changes=254, deplacement_median=1.0, deplacement_max=34 ; I-6 : rangs_changes=210, deplacement_max=34, gestion-cassini 131->129 ; I-4 : rangs_changes=58, deplacement_max=19, immovendu 12->13 ; I-7 : notes_changees=353, rangs_changes=78, top10_inchanges=9

Incertitude : Les écarts portent sur la cohérence interne entre le code Python (avis.py, service.py, build.py) et le texte publié, telle que mesurée par les variantes contrefactuelles.

### B-4 · Asymétrie de l'exception d'ancienneté d'ImmoVendu (v5.5) : défavorable à l'éditeur mais inapplicable aux concurrentes faute de données

Catégorie : anciennete · nature : fait_verifie · gravité : majeur · concerne l’éditeur : oui

L'éditeur a appliqué à sa propre enseigne ImmoVendu (lancée en 2024 sous le SIREN de 1995 de SARL GESTION CASSINI) une exception qui ramène son score d'ancienneté de 100,0 à 12,5, soit une pénalité de 4,375 points sur la note globale (sans cela, elle atteindrait environ 91,96 et le 6e rang). Ce traitement est manifestement défavorable à l'éditeur, mais la méthode manque d'uniformité car la date de lancement d'enseigne n'a été relevée pour aucune des 545 agences concurrentes.

Preuves : V-10b : date de lancement d’enseigne relevée pour seulement 1 agence(s) sur 546 (immovendu: 2024). ; V-10e : exception_editeur_depot_de_marque pour immovendu ; V-10f : SIREN 400877866 avec gestion-cassini (1995-05-02, anc=100.0) et immovendu (2024-05-01, anc=12.5). ; tests_biais.publisher_specific.anciennete_depuis_enseigne : immovendu passe au rang 11 (87.67) avec l'année seule (juin 2024) contre rang 12 (87.58) en production.

Incertitude : Il est impossible de savoir combien d'agences parmi les 43 groupes de SIREN partagés (V-10) exploitent une enseigne récente sous une société ancienne.

### B-5 · Forte sensibilité du classement aux pondérations et au pilier Ancienneté

Catégorie : biais · nature : calcul_reproduit · gravité : majeur · concerne l’éditeur : oui

Malgré un poids limité à 5 %, la suppression du pilier Ancienneté modifie 537 rangs sur 546 (médiane de 13 places) et 3 places dans le Top 10. Elle révèle une opposition nette entre les deux agences de l'éditeur : Gestion Cassini (anc=100,0) perd 19 places sans ancienneté, tandis qu'ImmoVendu (anc=12,5) gagne 6 places et atteint le 6e rang. De même, une variation de +/-20 % de n'importe quel pilier déplace entre 77 % et 95 % des agences.

Preuves : tests_biais.scenarios.sans_anciennete : rangs_changes=537, deplacement_max=49, deplacement_median=13, top10_inchanges=7 ; gestion-cassini 131->150 (74.52->73.18), immovendu 12->6 (87.58->91.53). ; scenarios +/-20 % : entre 421 (info_plus20) et 517 (avis_moins20) rangs changés ; medianes de déplacement jusqu'à 9.0 (hono_moins20) et max 37 (avis_moins20). ; immovendu entre dans le Top 10 dans avis_plus20 (10e), conf_moins20 (9e), anc_moins20 (10e) et sans_anciennete (6e).

Incertitude : La sensibilité mesure l'instabilité mécanique des rangs face à des choix de pondération conventionnels, sans définir une pondération idéale.

### B-6 · Biais structurels prononcés en faveur des gros volumes d'avis, des réseaux et des sites dotés d'estimation en ligne

Catégorie : biais · nature : fait_verifie · gravité : majeur · concerne l’éditeur : non

Les tests par groupes montrent des écarts moyens massifs par rapport à la moyenne générale (61,32) : +24,61 points entre le tiers à grand volume d'avis et le tiers à petit volume, +15,20 points pour les agences proposant une estimation en ligne et +12,63 points pour les agences en réseau. L'avantage se retrouve systématiquement sur les piliers déclaratifs/web (honoraires, information, conformité), pénalisant structurellement les petites agences indépendantes peu numérisées. À l'inverse, l'écart selon l'ancienneté de la société (+2,45 pts) ou le type d'activité (+1,53 pt) reste modéré.

Preuves : tests_biais.groups : grand_volume_avis (n=182, 72.66) vs petit_volume_avis (n=182, 48.05) soit +24.61 pts (hono 63.4 vs 39.7, info 73.4 vs 49.4, conf 51.1 vs 31.7). ; estimation_en_ligne (n=299, 69.15) vs sans_estimation_en_ligne (n=220, 53.95) soit +15.20 pts (hono 67.4 vs 38.2, info 77.5 vs 48.6). ; reseau (n=68, 72.38) vs independante (n=478, 59.75) soit +12.63 pts.

Incertitude : Ces écarts peuvent refléter en partie une corrélation réelle entre professionnalisation numérique et qualité de gestion, autant qu'un biais de construction des critères.

### B-7 · Règles non documentées (I-1, I-2, I-13) et absence des textes d'avis empêchant de vérifier le dédoublonnage (834 avis) et les données primaires

Catégorie : donnees · nature : non_verifiable · gravité : majeur · concerne l’éditeur : oui

Trois briques structurantes du calcul (I-1, I-2, I-13) ne sont pas décrites dans le texte méthodologique publié. De plus, l'absence des textes d'avis dans les exports publics rend impossible la vérification indépendante des 834 doublons retirés (dont 21 pour ImmoVendu) ainsi que la vérification à la source des notes et profils relevés sur les plateformes tierces.

Preuves : resultats_deterministes.statuts : donnees_primaires=non_verifiees ; I-1 (poids fixe 0,5 sur plateformes non relevées avis par avis), I-2 (moyenne simple m_ref=4,453 incluant agences non classées), I-13 (seuils 70 %/90 % et 120 caractères pour doublons/partages) : non documentés dans le texte public. ; V-6 : 834 avis déclarés doublons non vérifiables faute de textes dans les exports (immovendu: 21, gestion-cassini: 0).

Incertitude : Bien que le contrôle V-14 indique que l'algorithme de dédoublonnage est reproductible à partir des drapeaux de l'export, l'exactitude sémantique des 834 fusions et la fiabilité des avis sources restent invérifiables.

### B-8 · Évaluation globale du conflit d'intérêts : des avantages et des désavantages significatifs pour les agences de l'éditeur

Catégorie : conflit_interets · nature : fait_verifie · gravité : majeur · concerne l’éditeur : oui

Les agences de SARL GESTION CASSINI obtiennent en moyenne 81,05 contre 61,32 pour l'ensemble (ImmoVendu 12e à 87,58 ; Gestion Cassini 131e à 74,52). Toutefois, les données contredisent l'hypothèse d'un classement taillé sur mesure pour maximiser leurs rangs : les choix de l'éditeur et la règle sur les avis sans profil amputent lourdement les notes des deux agences, même si l'incohérence manifeste sur le critère Payeur indiqué avantage indûment ImmoVendu par rapport à Gestion Cassini.

Preuves : Avantages : groupe editeur moyenne 81.05 vs 61.32 ; immovendu 30/30 sur Payeur indiqué malgré texte identique à gestion-cassini (+5.10 pts) ; I-4 place immovendu 12e au lieu de 13e ; gestion-cassini profite de anc=100.0 (+19 rangs vs sans_anciennete). ; Désavantages : exception d'ancienneté sur immovendu (-4.38 pts, rang 12 au lieu de ~6) ; gestion-cassini à 0/30 sur Payeur indiqué (-5.10 pts) ; inclusion des avis sans profil fait chuter gestion-cassini de 62e à 131e (-69 rangs) ; I-6 coûte 2 places à gestion-cassini ; v5.6 gel de l'éditeur.

Incertitude : L'absence de liste d'agences voisines (voisines_editeur n=0) et de barèmes de concurrentes limite la comparaison fine des écarts de notation avec les agences proches dans le classement.

### B-9 · Discordances sur 186 avis déclarés partagés entre fiches d'agences (V-7), incluant les agences de l'éditeur

Catégorie : donnees · nature : fait_verifie · gravité : mineur · concerne l’éditeur : oui

Le contrôle V-7 relève 186 avis déclarés partagés entre k agences mais présents sur un nombre différent de fiches dans l'export, parmi lesquelles Gestion Cassini et ImmoVendu. Le mécanisme de détection reposant sur les 120 premiers caractères d'un texte non publié dans l'export, l'écart entre le nombre déclaré et l'export ne peut être résolu à partir du paquet.

Preuves : controles V-7 (mineur) : count=186, 49 agences listées dont gestion-cassini et immovendu. ; I-13 : partage détecté sur les 120 premiers caractères (si >=60 caractères), texte absent de l'export.

Incertitude : L'impact chiffré exact de ces 186 avis sur les notes des agences concernées n'est pas isolé dans les données fournies.

### B-10 · Prise en compte de 19 avis notés sous 1/5 sur Opinion System (V-4b), dont 9 comptés

Catégorie : donnees · nature : fait_verifie · gravité : mineur · concerne l’éditeur : non

Dix agences présentent au total 19 avis inférieurs à 1/5 (seuil usuel d'une échelle à 5 étoiles), dont 9 entrent tels quels dans le calcul de la moyenne. Cela tire mécaniquement vers le bas la composante qualité des agences concernées.

Preuves : controles V-4b (mineur) : count=19, counted=9, 10 agences concernées.

Incertitude : Sans vérification à la source sur Opinion System, il est impossible de savoir s'il s'agit d'une échelle incluant le zéro ou d'une erreur d'extraction.

### B-11 · Écarts entre avis Google relevés un par un et totaux déclarés sur 11 agences (V-12a), jusqu'à 11 avis d'écart

Catégorie : donnees · nature : fait_verifie · gravité : mineur · concerne l’éditeur : non

Dix agences présentent un écart d'un seul avis sur Google entre le nombre relevé et le nombre affiché, ce qui est marginal (décalage de collecte). En revanche, Orpi Agerim Properties présente 115 avis relevés contre 126 déclarés (11 avis manquants).

Preuves : controles V-12a (info) : count=11 ; orpi-agerim-properties-nice|google (115 relevés vs 126.0 déclarés) ; les 10 autres ont un écart de +/- 1 avis. ; controles V-12 : count=0 sur les 525 plateformes relevées en entier (seuil 10 % ou 2 avis).

Incertitude : L'écart de 11 avis sur Orpi Agerim Properties (8,7 %) reste sous la tolérance de 10 % du contrôle V-12, sans explication fournie (avis filtrés ou décalage temporel).

### B-12 · Traitement non documenté des dates partielles d'ancienneté (I-10) et valeur neutre 50 pour 15 agences sans date (V-10d) et 11 agences sur le critère I-12

Catégorie : methode · nature : fait_verifie · gravité : mineur · concerne l’éditeur : non

L'attribution d'une note neutre de 50 en cas de date non relevée pénalise les agences de plus de 10 ans non identifiées (moyenne des plus de 10 ans : 87,5) et avantage les agences de moins de 10 ans non identifiées (moyenne : 27,7). Par ailleurs, l'arrondi au mois (jour ignoré) et la valeur par défaut de juin (I-10) ne figurent pas dans la méthode publique.

Preuves : V-10d : 15 agences sans date de création reçoivent la valeur neutre 50 (contre 68.6 de moyenne globale en anc). ; I-10 : le jour est ignoré et juin est attribué si le mois est inconnu (non documenté dans le texte). ; I-12 : ordre des opérations modifiant 0,1 point d'ancienneté pour 2 agences.

Incertitude : On ignore si les 15 agences de V-10d sont réellement récentes ou anciennes faute d'identification SIREN.

### B-13 · Limites du registre des entreprises pour dater les enseignes commerciales et incohérences d'affichage sur le site ImmoVendu

Catégorie : anciennete · nature : fait_verifie · gravité : mineur · concerne l’éditeur : oui

Le registre officiel des entreprises atteste correctement la création de SARL GESTION CASSINI le 02/05/1995. Toutefois, 43 sociétés exploitent plusieurs agences ou enseignes sous un même SIREN, rendant impossible la détection automatique d'enseignes récentes adossées à d'anciennes structures. On relève par ailleurs que la page publique d'ImmoVendu laisse affichés des compteurs factices à zéro pour son expérience et son année de création.

Preuves : registre_entreprises : SIREN 400877866 conforme au 1995-05-02 pour gestion-cassini et immovendu ; limite explicite : le registre ne donne que la date de création de la personne morale. ; V-10 : 43 groupes de SIREN partagés (jusqu'à 7 agences sous un même SIREN, ex. 478261233 et 823781760). ; baremes_relus[1] (immovendu) : le texte de la page affiche « 0 D’expérience immobilière 0 ans Année de création 0 ».

Incertitude : La date de création commerciale des autres enseignes adossées à un SIREN partagé n'est pas connue.

### B-14 · Confirmation des trois autres critères d'honoraires (barème publié, montants TTC, barème complet) pour Gestion Cassini et ImmoVendu

Catégorie : honoraires · nature : fait_verifie · gravité : info · concerne l’éditeur : oui

Pour les deux agences dont le texte du barème a été relu, les points publiés pour les critères « Barème publié » (30/30), « Montants TTC » (20/20) et « Barème complet » (20/20) sont pleinement confirmés par les pages extraites le 17/11/2026.

Preuves : baremes_relus[0] (gestion-cassini) : Barème publié 30/30, Montants TTC 20/20, Barème complet 20/20 ; taux 6 % TTC et 10 % TTC avec minimums 6 500 € et 3 000 € TTC, plus gestion et location TTC. ; baremes_relus[1] (immovendu) : Barème publié 30/30, Montants TTC 20/20, Barème complet 20/20 ; taux 6 % TTC et 10 % TTC avec minimums 6.500 € et 3.000 € TTC.

Incertitude : La page d'ImmoVendu est marquée text_truncated=true (122 171 octets), mais la troncature n'affecte que les derniers caractères du bandeau cookies en pied de page, tout le barème étant lisible.

### B-15 · Conformité totale du recalcul déterministe des notes et des rangs sur les 546 agences

Catégorie : calcul · nature : calcul_reproduit · gravité : info · concerne l’éditeur : oui

Les notes finales et le classement des 546 agences sont intégralement reproductibles sans aucune erreur arithmétique ni anomalie d'arrondi de frontière.

Preuves : resultats_deterministes.recalcul : examined=546, conforme=546, divergente=0, frontiere_arrondi=0, ranks_divergent=0, m_ref=4.453. ; Recalcul vérifié sur agences_editeur : gestion-cassini (0.43*76.7+0.16*69.6+0.17*70+0.11*50+0.08*100+0.05*100 = 74.517 -> 74.52) ; immovendu (0.43*94.6+0.16*88.3+0.17*100+0.11*65+0.08*100+0.05*12.5 = 87.581 -> 87.58).

Incertitude : La conformité porte sur la reproduction de l'algorithme en production à partir des scores de piliers et d'exports, non sur la véracité des collectes primaires.

### B-16 · Stabilité temporelle des avis entre relevés (V-13, V-14 à zéro) et absence d'instructions suspectes

Catégorie : donnees · nature : fait_verifie · gravité : info · concerne l’éditeur : oui

Aucune manipulation rétroactive d'avis (disparitions, apparitions antidatées ou modifications de notes/drapeaux) n'est détectée entre les deux derniers relevés, et aucun texte injecté ne tente d'influencer l'audit.

Preuves : controles V-13a, V-13b, V-13d, V-13e, V-14 : count=0 pour tous. ; Inspection intégrale des champs texte fournis (baremes_relus, messages, regles) : aucune consigne dissimulée.

Incertitude : Les contrôles V-13 comparent au relevé précédent disponible dans le système de suivi de l'auditeur technique.

## Points favorables au classement

- Reproduction déterministe irréprochable sur l'ensemble des 546 agences classées (0 divergence de note ou de rang) et stabilité des avis entre les deux relevés (V-13 et V-14 à 0).
- Transparence de l'éditeur qui déclare son lien capitalistique (SIREN 400877866), gèle sa méthode (v5.6) et s'applique volontairement une exception d'ancienneté défavorable sur ImmoVendu (-4,38 points, la privant du Top 10).
- Cohérence satisfaisante du décompte global des avis sur 525 plateformes relevées en entier (0 écart supérieur au seuil V-12 de 10 % ou 2 avis) et confirmation de 3 des 4 critères d'honoraires sur les deux barèmes relus.

## Points défavorables au classement

- Contradiction manifeste dans l'évaluation du critère « Payeur indiqué » le 17/11/2026 : Gestion Cassini reçoit 0/30 et ImmoVendu 30/30 pour une phrase rigoureusement identique, créant un écart injustifié de 5,10 points.
- Exclusion de fait non appliquée aux 18 264 avis sans profil précisé (55,2 % des avis comptés), dont le retrait bouleverserait 526 rangs sur 546 et ferait bondir Gestion Cassini de 69 places.
- Écarts importants entre le code appliqué et la méthode publiée (I-4, I-6, I-7, I-11), modifiant 359 notes et 254 rangs, ainsi que règles importantes non documentées (I-1, I-2, I-13).
- Biais structurels massifs en faveur des gros volumes d'avis (+24,61 pts), des sites avec estimation en ligne (+15,20 pts) et des réseaux (+12,63 pts), et asymétrie de l'exception d'enseigne récente (vérifiée sur 1 seule agence sur 546).

## Instructions suspectes repérées dans les données


## Limites

- Les données primaires (textes et profils individuels des avis sur Google, Opinion System, Immodvisor) ne sont pas fournies dans les exports, rendant invérifiables à la source les 834 doublons (V-6), les 186 avis partagés (V-7) et les 19 notes inférieures à 1/5 (V-4b).
- Seuls les barèmes d'honoraires des deux agences de l'éditeur figurent dans le paquet (echantillon est nul) : il est impossible de vérifier si l'erreur sur le critère Payeur indiqué touche aussi des agences concurrentes.
- Le groupe voisines_editeur est vide (n=0), empêchant de comparer directement les scores d'honoraires ou de conformité de Gestion Cassini et d'ImmoVendu avec leurs voisines immédiates.
- La date de création commerciale de l'enseigne n'est relevée que pour ImmoVendu (V-10b), interdisant de quantifier le biais lié aux enseignes récentes adossées à d'anciens SIREN chez les concurrentes.
