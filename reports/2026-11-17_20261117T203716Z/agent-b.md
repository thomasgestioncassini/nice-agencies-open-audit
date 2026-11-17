# Analyse initiale — IA B

Fournisseur : google · modèle : gemini-4-hydrogen · statut : **ok**
Empreinte du mandat : 82e0fec40442f9e2ab530af39492ad0a83e777c1e424867598daa9a65e8089c8 · empreinte de l’entrée : 7c830bd19e4f1fcb541c77d3e9fea6c5af43ed7cf02246bda620fdf895b75901
Coût : 0.1888 $ (17779 jetons lus, 21617 écrits)

> Texte produit par l’IA, publié sans aucune modification ni relecture de l’éditeur.

## Résumé

Le contre-audit du classement des 546 agences immobilières de Nice publié sur meilleure-agence-nice.fr (version v5.4 du 17/11/2026, édité par SARL GESTION CASSINI) confirme une reproduction arithmétique exacte des notes et des rangs à partir du code et des agrégats fournis, ainsi que l'absence d'anomalies temporelles sur les avis depuis le relevé précédent. Toutefois, il met en évidence une anomalie critique sur la notation des honoraires entre les deux agences de l'éditeur (ImmoVendu reçoit 30/30 et Gestion Cassini 0/30 sur le critère Payeur indiqué pour une phrase strictement identique relue le 17/11/2026, générant un écart de 5,10 points sur la note finale), une modification de points sans mise à jour de la date de lecture du site sur 16 observations (V-13c), une asymétrie majeure sur le contrôle de l'ancienneté d'enseigne (appliquée défavorablement à ImmoVendu seule, invérifiable pour les 42 autres groupes multi-agences), l'inclusion de 55,2 % d'avis sans profil précisé bouleversant 528 rangs sur 546 (et pénalisant fortement Gestion Cassini), ainsi que plusieurs divergences entre les règles codées et la méthode publiée.

## Constats

### B-1 · Notation contradictoire du critère Payeur indiqué entre ImmoVendu (30/30) et Gestion Cassini (0/30) pour une mention identique

Catégorie : conflit_interets · nature : fait_verifie · gravité : critique · concerne l’éditeur : oui

Le critère Payeur indiqué compte pour 30 points sur 100 du pilier Honoraires (poids 17 %), soit 5,10 points de note finale. Alors que les deux sites utilisent exactement la même clause sur la charge des honoraires de transaction, ImmoVendu obtient 30/30 lors de la relecture du 17/11/2026 (conservant un score hono de 100,0 et le rang 3) tandis que Gestion Cassini reçoit 0/30 (abaissant son score hono à 70,0). Les autres critères du barème (Barème publié 30/30, Montants TTC 20/20) sont confirmés par les textes pour les deux agences.

Preuves : baremes_relus[immovendu].texte_page : Honoraires à la charge du VENDEUR ou de l'ACQUEREUR en fonction du mandat de vente -> 30/30 le 2026-11-17 ; baremes_relus[gestion-cassini].texte_page : Honoraires à la charge du VENDEUR ou de l'ACQUEREUR en fonction du mandat de vente -> 0/30 le 2026-11-17 ; agences_editeur[immovendu].piliers.hono = 100.0 (rang 3, note 91.43) vs agences_editeur[gestion-cassini].piliers.hono = 70.0 (rang 94, note 77.27)

Incertitude : La grille d'évaluation interne précisant si la mention VENDEUR ou ACQUEREUR en fonction du mandat mérite 30 ou 0 n'est pas fournie ; il est donc impossible de dire laquelle des deux notes est conforme à la règle voulue, mais l'incohérence entre les deux agences du même éditeur à la même date est certaine.

### B-2 · Inclusion de 55,2 % d'avis sans profil précisé modifiant 528 rangs sur 546 et pénalisant Gestion Cassini de 58 places

Catégorie : biais · nature : calcul_reproduit · gravité : majeur · concerne l’éditeur : oui

Plus de la moitié des avis comptés dans le pilier Avis n'ont pas de profil vendeur ou acheteur déterminé mais entrent tout de même dans le calcul. Leur retrait entraîne un reclassement quasi général (96,7 % des agences changent de rang, avec un déplacement médian de 26 rangs). Ce choix méthodologique constitue un désavantage marqué pour Gestion Cassini (-4,72 points et -58 rangs) et abaisse légèrement ImmoVendu d'une place (rang 3 au lieu de 2).

Preuves : tests_biais.avis_non_precises : 18264 avis non précisés sur 33064 avis comptés (part = 0.552), exclus_faute_de_profil = 0 ; scenario_sans_non_precises : rangs_changes = 528, deplacement_median = 26.0, deplacement_max = 252, top10_inchanges = 7 ; gestion-cassini : rang officiel 94 (note 77.27) vs rang 36 (note 81.99) sans avis non précisés ; immovendu : rang officiel 3 (note 91.43) vs rang 2 (note 91.34) sans avis non précisés

Incertitude : Aucune incertitude sur le calcul contrefactuel reproduit dans le paquet ; l'effet réel si ces 18264 avis étaient reclassés selon le vrai profil de chaque auteur reste inconnu faute d'accès aux textes.

### B-3 · Contrôle de l'ancienneté d'enseigne appliqué uniquement à ImmoVendu et impossible à vérifier sur les 42 autres groupes multi-agences

Catégorie : conflit_interets · nature : fait_verifie · gravité : majeur · concerne l’éditeur : oui

Par exception déclarée de l'éditeur, ImmoVendu se voit attribuer la date de dépôt de marque de 2024 (12,5/100 en ancienneté) au lieu de la date de création de SARL GESTION CASSINI de 1995 (100/100), ce qui la pénalise d'environ 4,38 points sur sa note finale (poids 5 %). Toutefois, cette règle n'étant appliquée à aucune des 42 autres sociétés exploitant plusieurs agences sous un même SIREN (qui conservent toutes la date légale du SIREN), le traitement de l'ancienneté présente une asymétrie méthodologique majeure.

Preuves : contrôle V-10b (majeur) : date de lancement d'enseigne relevée pour 1 agence sur 546 (immovendu = 2024) ; contrôle V-10e et V-10f : SIREN 400877866 seul groupe parmi 43 avec des dates différentes (gestion-cassini = 1995-05-02, immovendu = 2024-05-01, exception_editeur_depot_de_marque) ; agences_editeur[immovendu].piliers.anc = 12.5 contre 100.0 pour gestion-cassini

Incertitude : L'impact exact sur les 42 autres groupes SIREN est non vérifiable faute de collecte de la date d'enseigne pour les 545 agences concurrentes.

### B-4 · Modification de points de critères sans mise à jour de la date de lecture du site (contrôle V-13c), incluant les agences de l'éditeur

Catégorie : donnees · nature : fait_verifie · gravité : majeur · concerne l’éditeur : oui

Seize modifications de points de critères ont eu lieu sans actualisation de la date de lecture du site. Pour Gestion Cassini et ImmoVendu, cela correspond à la relecture du critère Payeur indiqué le 17/11/2026 (date du relevé final) alors que la lecture générale du site reste datée du 12/11/2026.

Preuves : contrôle V-13c (majeur) : count = 16, 11 agences listées dont gestion-cassini et immovendu ; agences_editeur : date_lecture_site = 2026-11-12 et date_relecture_payeur = 2026-11-17 pour gestion-cassini et immovendu ; baremes_relus : Payeur indiqué daté du 2026-11-17 contre 2026-11-12 pour les 3 autres critères

Incertitude : La liste agencies de V-13c comporte 11 identifiants pour count = 16 (probablement 16 critères modifiés ou une liste tronquée) ; la nature des modifications pour les 9 agences concurrentes listées n'est pas détaillée.

### B-5 · Contradictions et ambiguïtés entre le code exécuté et le texte public modifiant 359 notes et 261 rangs

Catégorie : methode · nature : calcul_reproduit · gravité : majeur · concerne l’éditeur : oui

Quatre écarts notables affectent le classement par rapport à une lecture stricte du texte publié : l'inclusion des doublons et plateformes incomplètes au dénominateur de la régularité (I-4, contraire à la section 3), l'arrondi intermédiaire des sous-critères/piliers et du rangement au centième au lieu de la note exacte (I-7, contraire à la section 9), la redistribution des 15 % de régularité lorsque aucun avis n'est relevé un par un (I-6, ambiguïté sur la section 10), et le départage des égalités sur tous profils d'avis confondus puis l'ordre interne (I-11). Globalement, ces écarts modifient près de la moitié des rangs (47,8 %) mais laissent le top 10 inchangé et ont un impact minime sur l'éditeur.

Preuves : regles_appliquees_absentes_ou_contraires_au_texte : I-4 (contradiction), I-7 (contradiction), I-6 (ambiguite), I-11 (ambiguite) ; effet_des_regles_vs_texte_initial.ensemble : notes_changees = 359, rangs_changes = 261, deplacement_max = 35, top10_inchanges = 10 ; I-6 seul : 21 notes et 218 rangs changés (max 35) ; I-7 seul : 353 notes et 79 rangs changés ; I-4 seul : 8 notes et 58 rangs changés ; agences_suivies : gestion-cassini passe de 94 à 93 sous variante texte, immovendu reste 3

Incertitude : Le contrôle porte sur la comparaison entre le code source analysé et le texte méthodologique de la v5.4 ; d'éventuels autres écarts sur des modules non fournis ne sont pas mesurables.

### B-6 · Biais structurels prononcés selon le volume d'avis (+24,64 points), l'outil d'estimation en ligne (+15,26 points) et l'appartenance à un réseau (+12,61 points) - constat favorable/neutre ou critique selon usage

Catégorie : biais · nature : calcul_reproduit · gravité : majeur · concerne l’éditeur : oui

La note globale moyenne (61,33 sur 546 agences) présente de très forts gradients structurels : +24,64 points entre le tiers inférieur et supérieur de volume d'avis, +15,26 points pour les sites disposant d'une estimation en ligne et +12,61 points pour les agences en réseau. Ces écarts ne se limitent pas au pilier Avis mais s'observent aussi sur les piliers Honoraires, Conformité et Informations, favorisant les agences équipées numériquement comme celles de l'éditeur.

Preuves : tests_biais.groups : petit_volume_avis (n=182, moyenne 48.05) vs grand_volume_avis (n=182, moyenne 72.69) ; estimation_en_ligne (n=299, moyenne 69.18) vs sans_estimation_en_ligne (n=220, moyenne 53.92) ; reseau (n=68, moyenne 72.37) vs independante (n=478, moyenne 59.76) ; agences_editeur : url_estimation présente pour gestion-cassini et immovendu

Incertitude : Ces écarts peuvent refléter en partie une corrélation réelle de qualité digitale entre les critères plutôt qu'une causalité directe, mais l'amplitude de la corrélation sur des piliers indépendants comme les honoraires (39.7 vs 63.4 selon le volume) montre un fort biais de structuration digitale.

### B-7 · Forte instabilité du classement aux choix de pondération, notamment à la suppression du pilier Ancienneté (536 rangs modifiés sur 546) - sensible

Catégorie : biais · nature : calcul_reproduit · gravité : majeur · concerne l’éditeur : oui

Retirer le pilier Ancienneté (poids 5 %) modifie 98,2 % des rangs (déplacement médian de 13 places) et change 2 agences du top 10. Ce pilier aide nettement Gestion Cassini (+23 rangs grâce à ses 31 ans d'ancienneté) mais pénalise ImmoVendu (-1 rang dans le top 3 du fait de son exception à 2024). Par ailleurs, des variations de +/-20 % du poids de n'importe quel pilier déplacent entre 77,7 % et 94,5 % des agences, tout en préservant généralement au moins 9 membres du top 10.

Preuves : tests_biais.scenarios.sans_anciennete : rangs_changes = 536, deplacement_median = 13.0, deplacement_max = 49, top10_inchanges = 8 ; gestion-cassini : rang 94 (77.27) -> rang 117 (76.07) sans ancienneté ; immovendu : rang 3 (91.43) -> rang 2 (95.59) ; variations +/-20 % par pilier : entre 424 (info_plus20) et 516 (avis_moins20) rangs changés sur 546

Incertitude : La sensibilité aux pondérations mesure la robustesse statistique du rang ; elle ne prouve pas à elle seule un choix délibéré de pondération pour favoriser un acteur.

### B-8 · Intégration brute d'avis notés sous 1/5 provenant d'Opinion System (contrôle V-4b) sans vérification d'échelle à la source

Catégorie : donnees · nature : fait_verifie · gravité : mineur · concerne l’éditeur : non

Dix-neuf avis (dont 9 effectivement comptés) affichent une note inférieure au minimum usuel de 1/5 et sont intégrés tels quels dans les moyennes de 10 agences concurrentes, ce qui peut abaisser artificiellement leur note si la source utilise une échelle différente de 1 à 5.

Preuves : contrôle V-4b (mineur) : count = 19, counted = 9, 10 agences concernées

Incertitude : L'échelle exacte utilisée à la source par Opinion System pour ces 19 avis n'a pas été vérifiée sur les données primaires.

### B-9 · Non-vérifiabilité des 834 avis doublons (V-6) et 186 avis partagés (V-7) faute de publication des textes d'avis

Catégorie : donnees · nature : non_verifiable · gravité : mineur · concerne l’éditeur : oui

Bien que le dédoublonnage soit reproductible à partir des marqueurs exportés (V-14 = 0), la détection même des doublons et des avis partagés entre agences repose sur les textes bruts non publiés. L'écart de cardinalité signalé en V-7 touche 186 avis sur plusieurs dizaines d'agences, dont les deux entités de l'éditeur.

Preuves : resultats_deterministes.statuts.donnees_primaires = non_verifiees ; contrôle V-6 : 834 avis déclarés doublons, immovendu = 21, gestion-cassini = 0 ; contrôle V-7 (mineur) : 186 avis déclarés partagés entre k agences mais présents sur un autre nombre de fiches dans l'export, incluant gestion-cassini et immovendu

Incertitude : Les exports publiés ne contiennent pas le texte des avis, rendant impossible le contrôle indépendant de l'appariement textuel décrit en I-13.

### B-10 · Règles de calcul essentielles non documentées dans le texte public (I-1, I-2, I-8, I-10, I-13) - opacité

Catégorie : methode · nature : fait_verifie · gravité : mineur · concerne l’éditeur : non

Plusieurs paramètres structurants du score ne figurent pas dans la documentation publique, notamment la pondération fixe de 0,5 pour les plateformes non relevées avis par avis, la définition exacte de la moyenne de Nice (incluant des agences non classées dans agregats-plateformes.csv), le périmètre exact des réponses aux avis négatifs et les seuils algorithmiques de détection des doublons.

Preuves : regles_appliquees_absentes_ou_contraires_au_texte : I-1 (plateformes incomplètes à poids fixe 0,5), I-2 (M_REF = 4,453 moyenne simple des agences listées), I-8 (réponses aux avis négatifs Google <= 3 étoiles doublons compris), I-10 (calcul ancienneté jour ignoré, juin si mois inconnu), I-13 (seuils de 70 % / 90 % de mots et préfixe 120 caractères)

Incertitude : L'impact chiffré isolé de I-1, I-2, I-8, I-10 et I-13 n'est pas simulé dans effet_des_regles_vs_texte_initial.

### B-11 · Critère Barème complet (toutes les tranches de prix) noté 20/20 pour l'éditeur sans tranches de prix explicites, impossible à trancher sans grille

Catégorie : honoraires · nature : non_verifiable · gravité : mineur · concerne l’éditeur : oui

Sur les quatre critères d'honoraires de Gestion Cassini et ImmoVendu, Barème publié (30/30) et Montants TTC (20/20) sont pleinement confirmés par les pages relues, Payeur indiqué est contredit par l'écart 0 vs 30 (constat B-1), et Barème complet (20/20) reste impossible à juger définitivement car les barèmes appliquent un taux unique par nature de bien plutôt que des tranches de prix.

Preuves : baremes_relus[gestion-cassini] et baremes_relus[immovendu] : Barème complet (toutes les tranches de prix) = 20/20 le 2026-11-12 ; texte_page : taux proportionnels fixes de 6 % ou 10 % TTC selon le type de bien avec minimums de 6 500 € ou 3 000 € TTC ; baremes_relus[immovendu].text_truncated = true (122171 octets, troncature dans le bandeau cookies final)

Incertitude : Sans la grille d'interprétation de l'éditeur ni d'échantillon de concurrents (echantillon = null), il est impossible de confirmer si un taux unique sans tranches de prix satisfait ce critère chez toutes les agences.

### B-12 · Attribution d'une valeur neutre de 50 en ancienneté aux 15 agences sans date de création relevée (V-10d) - impact

Catégorie : donnees · nature : fait_verifie · gravité : mineur · concerne l’éditeur : non

Faute de date de création identifiée au registre, 15 agences reçoivent automatiquement 50/100 sur le pilier Ancienneté, soit l'équivalent exact de 10 ans d'existence.

Preuves : contrôle V-10d : count = 15, valeur neutre 50

Incertitude : L'âge réel de ces 15 agences n'est pas fourni ; la règle peut donc autant les avantager (si moins de 10 ans) que les pénaliser (si plus de 10 ans).

### B-13 · Conformité totale du recalcul déterministe des 546 notes et rangs et stabilité temporelle des avis (V-12, V-13a/b/d/e, V-14 = 0) - favorable

Catégorie : calcul · nature : calcul_reproduit · gravité : info · concerne l’éditeur : oui

À partir des données fournies, aucune divergence de note ou de rang n'a été trouvée sur les 546 agences. De plus, aucun ajout rétroactif suspect, disparition d'avis ou modification silencieuse d'avis déjà relevés n'a été constaté depuis le relevé précédent.

Preuves : resultats_deterministes.recalcul : examined = 546, notes.conforme = 546, divergente = 0, frontiere_arrondi = 0, ranks_divergent = 0 ; contrôles V-13a, V-13b, V-13d, V-13e, V-14 : count = 0 sur l'ensemble et 0 pour les agences de l'éditeur ; contrôle V-12 : 0 plateforme hors tolérance sur 525 relevées en entier

Incertitude : La conformité porte sur la reproductibilité des calculs à partir des données et scripts fournis ; elle ne garantit pas l'exactitude des relevés initiaux ni des grilles manuelles de critères de sites.

### B-14 · Conformité au registre des entreprises pour SARL GESTION CASSINI et interprétation de l'écart 1995 vs 2024 - ancienneté

Catégorie : anciennete · nature : fait_verifie · gravité : info · concerne l’éditeur : oui

La vérification sur l'API officielle confirme l'immatriculation de SARL GESTION CASSINI le 02/05/1995. L'écart entre la date publiée pour Gestion Cassini (1995) et l'ancienneté retenue pour ImmoVendu (2024) s'explique par l'exploitation de deux marques distinctes par une même société ancienne (même phénomène que dans 42 autres groupes SIREN), l'éditeur ayant choisi d'appliquer la date de marque à ImmoVendu uniquement.

Preuves : registre_entreprises : counts.conforme = 2, SIREN 400877866, date_registre = 1995-05-02 ; gestion-cassini : date_publiee = 1995-05-02 (registre_des_entreprises) ; immovendu : enseigne_depuis = 2024 (exception_editeur_depot_de_marque)

Incertitude : Le registre des entreprises ne recense que la date de création juridique de la personne morale et non la date d'ouverture commerciale d'une nouvelle enseigne ou d'un site web.

### B-15 · Écarts mineurs entre avis Google relevés et déclarés sur 11 plateformes (V-12a), restant dans les tolérances

Catégorie : donnees · nature : fait_verifie · gravité : info · concerne l’éditeur : non

Onze fiches Google présentent une différence entre le nombre d'avis affichés et le nombre relevé un par un, mais toutes restent dans la tolérance de V-12 (10 % ou 2 avis) et aucune agence de l'éditeur n'est concernée.

Preuves : contrôle V-12a : count = 11, 10 écarts de +/-1 avis et orpi-agerim-properties-nice|google (115 relevés vs 126 déclarés, soit 8,7 %)

Incertitude : La cause exacte de l'écart de 11 avis pour orpi-agerim-properties-nice (filtrage Google ou délai de collecte) ne peut être déterminée sans les données brutes de la plateforme.

### B-16 · Bilan contrasté des avantages et désavantages des agences de l'éditeur (moyenne 84,35 contre 61,33 pour le marché) - synthèse

Catégorie : conflit_interets · nature : fait_verifie · gravité : info · concerne l’éditeur : oui

L'examen ne révèle pas de manipulation globale unilatérale : Gestion Cassini est classée 94e et subit des règles défavorables (comptage des avis sans profil coûtant 58 places, 0/30 sur Payeur indiqué, perte d'un rang via I-6 et I-7), tandis qu'ImmoVendu est pénalisée de 4,38 points par l'exception sur l'ancienneté de marque. À l'inverse, l'éditeur bénéficie de scores maximaux en info/estimation en ligne, et surtout ImmoVendu accède au rang 3 grâce à un 30/30 sur Payeur indiqué refusé à Gestion Cassini le même jour, malgré un site contenant encore des mentions modèles non renseignées (0 ans d'expérience).

Preuves : tests_biais.groups.editeur : n = 2, note_moyenne = 84.35 (avis 85.7, serv 78.9, hono 85.0, conf 87.5, info 100.0, anc 56.2) vs toutes (n = 546) = 61.33 ; gestion-cassini rang 94 (77.27), immovendu rang 3 (91.43) ; baremes_relus[immovendu].texte_page : mentions 0 D'expérience immobilière 0 ans Année de création 0

Incertitude : En l'absence d'échantillon de concurrentes (echantillon = null) et de vérification des données primaires, il est impossible d'évaluer si les scores élevés de conf (100,0 pour ImmoVendu) et info (100,0 pour les deux) sont attribués avec la même rigueur que chez les concurrentes.

## Points favorables au classement

- Reproductibilité mathématique parfaite : 546 notes et 546 rangs conformes au recalcul déterministe (0 divergence, 0 cas limite d'arrondi, V-14 = 0).
- Intégrité temporelle des relevés d'avis : aucun avis rétroactif, disparu, ni modifié silencieusement depuis le relevé précédent (V-13a, V-13b, V-13d, V-13e tous à 0).
- Couverture quasi complète des avis : toutes les 525 plateformes relevées en entier respectent la tolérance d'écart de V-12.
- L'éditeur s'est appliqué à lui-même une exception défavorable sur ImmoVendu (ancienneté ramenée de 1995 à 2024, -4,38 points) et maintient sa propre agence historique Gestion Cassini au 94e rang avec 0/30 sur le critère Payeur indiqué.
- Les deux agences de l'éditeur sont conformes au registre officiel des entreprises pour le SIREN 400877866 (création le 02/05/1995).

## Points défavorables au classement

- Contradiction directe le 17/11/2026 sur le critère Payeur indiqué : ImmoVendu reçoit 30/30 (maintenant son 3e rang) et Gestion Cassini 0/30 pour la même clause textuelle exacte (impact de 5,10 points sur la note finale).
- Seize modifications de points de critères sans mise à jour de la date de lecture du site (V-13c, gravité majeure), touchant notamment Gestion Cassini et ImmoVendu.
- Asymétrie majeure de l'ancienneté d'enseigne (V-10b) : vérifiée et appliquée uniquement pour ImmoVendu, laissant 42 autres groupes multi-agences bénéficier de la date de leur société mère faute de données.
- Inclusion de 55,2 % d'avis sans profil précisé (18264 sur 33064), qui déplace 528 rangs sur 546 (médiane 26 rangs, maximum 252).
- Écarts avérés entre le code appliqué et la méthode publique (I-4, I-6, I-7, I-11) modifiant 359 notes et 261 rangs, auxquels s'ajoutent cinq règles importantes non documentées (I-1, I-2, I-8, I-10, I-13).
- Forts biais structurels en faveur du volume d'avis (+24,64 points), des outils d'estimation en ligne (+15,26 points) et des réseaux (+12,61 points), et très forte sensibilité à la pondération de l'ancienneté (536 rangs changés en son absence).

## Instructions suspectes repérées dans les données


## Limites

- Les données primaires (pages web des 544 agences concurrentes, textes bruts des avis et grilles détaillées d'évaluation des critères manuels) n'ont pas été vérifiées (donnees_primaires = non_verifiees) ; aucun échantillon d'agences concurrentes n'est fourni (echantillon = null).
- Le groupe de comparaison voisines_editeur est vide (n = 0) dans tests_biais.groups, limitant la comparaison ciblée avec les concurrents immédiats d'ImmoVendu (autour du rang 3) et de Gestion Cassini (autour du rang 94).
- Les textes des avis n'étant pas exportés, le bien-fondé des 834 doublons (V-6), des 186 avis partagés (V-7) et de la classification des profils vendeur/acheteur est invérifiable à la source.
- La page des honoraires d'ImmoVendu dans baremes_relus est tronquée en fin de document (text_truncated = true à 122171 octets), bien que la troncature n'intervienne qu'après le barème et les mentions légales, dans le bandeau de consentement aux cookies.
- L'impact isolé des règles non documentées I-1, I-2, I-8, I-10 et I-13 n'a pas fait l'objet de simulations contrefactuelles dans les données fournies.
