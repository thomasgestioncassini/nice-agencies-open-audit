# Analyse initiale — IA B

Fournisseur : google · modèle : gemini-4-hydrogen · statut : **ok**
Empreinte du mandat : 82e0fec40442f9e2ab530af39492ad0a83e777c1e424867598daa9a65e8089c8 · empreinte de l’entrée : 4bb9687c3f2bf534a401c7aa8dd8be048bb3a69be58ea63cf857bb48e385ae9a
Coût : 0.2086 $ (17461 jetons lus, 24321 écrits)

> Texte produit par l’IA, publié sans aucune modification ni relecture de l’éditeur.

## Résumé

Le contre-audit du classement v5.4 (546 agences) met en évidence une reproductibilité déterministe parfaite des calculs publiés (546 notes et rangs conformes, dédoublonnage interne conforme), mais révèle plusieurs fragilités critiques et majeures. Le constat le plus grave concerne une contradiction directe dans la notation du critère « Payeur indiqué » : sur une formulation strictement identique (« Honoraires à la charge du VENDEUR ou de l’ACQUEREUR en fonction du mandat de vente »), ImmoVendu obtient 30/30 (hono 100,0, rang 1) alors que Gestion Cassini, exploitée par la même société (SARL GESTION CASSINI), obtient 0/30 (hono 70,0, rang 129), soit un écart de 5,10 points sur la note finale. Par ailleurs, ImmoVendu (enseigne créée en 2024) bénéficie de l’ancienneté de la société mère fondée en 1995 (100/100 au lieu de ~10/100), ce qui lui assure le rang 1 (rang 3 sans cela), bien que la donnée d’ancienneté d’enseigne manque pour 545 agences sur 546 et que 43 groupes SIREN soient traités selon la même règle de création de société. À l’inverse, plusieurs choix méthodologiques pénalisent fortement Gestion Cassini (l’inclusion de 55,2 % d’avis sans profil d’auteur lui coûte 67 places et 4,72 points) et le classement reste très sensible aux écarts entre le code exécuté et le texte public (282 rangs modifiés) ainsi qu’à de forts biais structurels liés au volume d’avis (+24,70 points) et à la présence en réseau (+12,85 points).

## Constats

### B-1 · Notation contradictoire du critère « Payeur indiqué » entre les deux agences de l’éditeur sur un texte identique

Catégorie : conflit_interets · nature : fait_verifie · gravité : critique · concerne l’éditeur : oui

Les deux agences de SARL GESTION CASSINI affichent exactement la même clause sur la charge des honoraires en transaction, relue à la même date (2026-11-17). Pourtant, ImmoVendu reçoit 30/30 et Gestion Cassini 0/30. Avec un poids de 17 % pour le pilier Honoraires, ces 30 points représentent 5,10 points sur la note globale : si ImmoVendu avait reçu 0/30, sa note tomberait de 95,81 à 90,71 (en dessous des 91,52 qui la font passer du rang 1 au rang 3 dans le test d’ancienneté d’enseigne) ; inversement, Gestion Cassini passerait de 74,52 à 79,62.

Preuves : baremes_relus[0].texte_page (gestion-cassini) : « Honoraires à la charge du VENDEUR ou de l’ACQUEREUR en fonction du mandat de vente. » ; baremes_relus[0].points_publies : Payeur indiqué = 0/30 (date_observation 2026-11-17) ; hono = 70.0 ; baremes_relus[1].texte_page (immovendu) : « Honoraires à la charge du VENDEUR ou de l’ACQUEREUR en fonction du mandat de vente. » ; baremes_relus[1].points_publies : Payeur indiqué = 30/30 (date_observation 2026-11-17) ; hono = 100.0

Incertitude : L’échantillon des barèmes concurrents étant absent (echantillon = null), il est impossible de savoir si la pratique générale du classement attribue 30/30 ou 0/30 à la mention « en fonction du mandat », et donc si ImmoVendu est indûment favorisée ou si Gestion Cassini est indûment pénalisée.

### B-2 · Attribution à ImmoVendu (enseigne de 2024) de l’ancienneté de la société créée en 1995, décisive pour son rang 1

Catégorie : anciennete · nature : fait_verifie · gravité : majeur · concerne l’éditeur : oui

Bien que l’enseigne ImmoVendu ait été lancée en 2024 (environ 2 ans d’existence en novembre 2026), elle reçoit la note maximale d’ancienneté (100,0/100) grâce au SIREN 400877866 de SARL GESTION CASSINI créée en 1995. Le test contrefactuel montre que le calcul sur l’âge de l’enseigne ferait chuter ImmoVendu de 4,29 points (95,81 à 91,52) et lui ferait perdre la 1re place (rang 3). Toutefois, cette règle repose sur le registre des entreprises appliqué uniformément à tous les groupes multi-enseignes (V-10), et ne corriger que la seule agence pour laquelle la date d’enseigne est connue (V-10b) créerait une asymétrie défavorable à l’éditeur.

Preuves : agences_editeur.immovendu : date_creation_societe = 1995-05-02, enseigne_depuis = 2024, anc = 100.0, rang = 1, note = 95.81 ; tests_biais.publisher_specific.anciennete_depuis_enseigne : immovendu rang = 3 (officiel 1), note = 91.52 (officielle 95.81), rangs_changes = 3, deplacement_max = 2 ; resultats_deterministes.controles[V-10] : 43 groupes de même SIREN partagent la même date d’ancienneté ; resultats_deterministes.controles[V-10b] : date de lancement d’enseigne relevée pour seulement 1 agence sur 546 (immovendu)

Incertitude : Faute de dates de lancement d’enseigne pour les 545 autres agences (V-10b), il est impossible de mesurer combien d’agences concurrentes appartenant aux 43 groupes SIREN (V-10) profitent du même mécanisme.

### B-3 · Prise en compte de 55,2 % d’avis sans profil d’auteur, modifiant 520 rangs et pénalisant fortement Gestion Cassini

Catégorie : biais · nature : calcul_reproduit · gravité : majeur · concerne l’éditeur : oui

Plus de la moitié des avis comptés (18 264 sur 33 064, soit 55,2 %) ne précisent pas le profil du client et sont tous inclus dans le calcul. Leur exclusion bouleverserait la quasi-totalité du classement (520 rangs modifiés sur 546, déplacement médian de 26 places, 3 changements dans le top 10). Fait notable contre l’hypothèse d’un biais systématique en faveur de l’éditeur : cette règle pénalise nettement Gestion Cassini, qui gagnerait 67 places (de 129e à 62e, +4,72 points) si ces avis étaient exclus, tandis qu’ImmoVendu resterait 1re.

Preuves : tests_biais.avis_non_precises : avis_non_precises = 18264, dont_comptes = 18264, avis_comptes = 33064, part_dans_les_avis_comptes = 0.552, exclus_faute_de_profil = 0 ; tests_biais.avis_non_precises.scenario_sans_non_precises : rangs_changes = 520, deplacement_max = 252, deplacement_median = 26.0, top10_inchanges = 7 ; scenario_sans_non_precises.agences_suivies.gestion-cassini : rang = 62 (officiel 129), note = 79.24 (officielle 74.52) ; immovendu : rang = 1, note = 95.72 (officielle 95.81)

Incertitude : La répartition exacte par agence des avis non précisés entre vente, location et gestion n’est pas fournie dans le paquet.

### B-4 · Écarts entre le texte méthodologique publié et le code exécuté affectant 359 notes et 282 rangs

Catégorie : methode · nature : fait_verifie · gravité : majeur · concerne l’éditeur : oui

Si les calculs publiés reproduisent fidèlement le code en production, quatre divergences entre le code et le texte public (I-4, I-6, I-7, I-11) modifient ensemble 359 notes et 282 rangs (jusqu’à 36 places d’écart). En particulier, la redistribution du sous-critère « régularité » manquant (I-6) déplace 237 agences malgré l’annonce d’absence de redistribution, l’arrondi avant classement (I-7) modifie 1 membre du top 10, et le comptage des doublons dans la régularité (I-4) contredit l’exclusion des doublons annoncée. L’effet net sur les agences de l’éditeur reste marginal (ImmoVendu reste 1re, Gestion Cassini passe de 129e à 128e).

Preuves : effet_des_regles_vs_texte_initial.ensemble : notes_changees = 359, rangs_changes = 282, deplacement_median = 1.0, deplacement_max = 36, top10_inchanges = 10 ; effet_des_regles_vs_texte_initial.I-6 : notes_changees = 21, rangs_changes = 237, deplacement_max = 36 (contradiction/ambiguïté sur la redistribution des 15 % de régularité non vérifiable, section 10 du texte vs avis.py : score()) ; effet_des_regles_vs_texte_initial.I-7 : notes_changees = 353, rangs_changes = 79, deplacement_max = 4, top10_inchanges = 9 (arrondis intermédiaires au dixième et note finale au centième vs « note exacte » annoncée en section 9, build.py : r['t']) ; effet_des_regles_vs_texte_initial.I-4 : notes_changees = 8, rangs_changes = 49, deplacement_max = 15 (doublons et plateformes incomplètes comptés dans le dénominateur de la régularité vs section 3, avis.py : score()) ; resultats_deterministes.statuts.texte_historique = ecarts_anterieurs

Incertitude : L’impact sur les rangs dans les versions antérieures à la v5.4 (texte_historique = ecarts_anterieurs) n’est pas chiffré dans ce paquet.

### B-5 · Sensibilité élevée aux pondérations et dépendance de la 1re place d’ImmoVendu au pilier Ancienneté

Catégorie : biais · nature : calcul_reproduit · gravité : majeur · concerne l’éditeur : oui

La suppression du pilier Ancienneté (5 %) modifie 539 rangs sur 546 (médiane 13 places, max 48, 3 changements dans le top 10). Les deux agences de l’éditeur en tirent avantage (anc = 100,0) : sans ce pilier, Gestion Cassini perd 22 places (129e à 151e) et ImmoVendu perd le rang 1 (2e avec 95,59 contre 95,81). À l’inverse, dans les 12 scénarios de variation de ±20 % du poids de chaque pilier, bien que 435 à 507 agences changent de rang (médiane de 2 à 9 places), ImmoVendu conserve la 1re place dans les 12 cas (note entre 95,57 et 96,05) et Gestion Cassini oscille entre les rangs 125 et 135.

Preuves : tests_biais.scenarios.sans_anciennete : rangs_changes = 539, deplacement_max = 48, deplacement_median = 13, top10_inchanges = 7 ; immovendu rang = 2 (officiel 1), note = 95.59 (officielle 95.81) ; gestion-cassini rang = 151 (officiel 129), note = 73.18 (officielle 74.52)

Incertitude : L’écart exact entre la 1re et la 2e agence du classement officiel n’est pas publié dans le paquet, mais la perte de 0,22 point suffit à faire reculer ImmoVendu au rang 2.

### B-6 · Forts biais structurels en faveur des agences à grand volume d’avis, en réseau et dotées d’outils numériques

Catégorie : biais · nature : fait_verifie · gravité : majeur · concerne l’éditeur : non

Les comparaisons par sous-groupes montrent des écarts moyens très importants : +24,70 points entre le tiers supérieur et le tiers inférieur de volume d’avis, +12,85 points pour les réseaux (n=68, 72,46) par rapport aux indépendantes (n=478, 59,61), et +15,35 points pour les sites proposant une estimation en ligne (n=299, 69,10 vs n=220, 53,75). Les sociétés de moins de 10 ans (n=163) obtiennent une moyenne inférieure (59,89 vs 62,28 pour 10 ans et plus, n=368) à cause du pilier Ancienneté (27,7 vs 87,7), alors même qu’elles devancent leurs aînées sur le pilier Service (70,1 vs 63,3).

Preuves : tests_biais.groups.petit_volume_avis (n=182) : note_moyenne = 47.92 vs grand_volume_avis (n=182) : note_moyenne = 72.62 (+24.70 pts ; avis 50.0 vs 81.7, hono 39.7 vs 63.4, conf 30.5 vs 50.6, info 49.4 vs 73.4)

Incertitude : Les écarts entre groupes agrègent des effets mécaniques de la formule (volume d’avis, estimation en ligne) et des corrélations structurelles (professionnalisation des sites web des grands cabinets et réseaux) sans régression multivariée.

### B-7 · Absence de la date de lancement d’enseigne pour 545 agences sur 546 empêchant tout contrôle équitable de l’ancienneté commerciale

Catégorie : donnees · nature : fait_verifie · gravité : majeur · concerne l’éditeur : oui

Le contrôle V-10b confirme que la donnée « enseigne_depuis » n’a été collectée que pour la seule agence ImmoVendu. En l’absence de ce relevé pour les 545 autres agences, il est impossible de distinguer à grande échelle l’âge juridique d’une société (SIREN) de l’ancienneté réelle de l’enseigne exploitée, ce qui rend le critère d’ancienneté vulnérable aux créations de marques récentes sous des structures anciennes.

Preuves : resultats_deterministes.controles[V-10b] : severity = majeur, count = 1, agencies = [immovendu], brands = {immovendu: 2024}

Incertitude : Le nombre exact d’enseignes récentes adossées à d’anciennes sociétés parmi les 545 autres agences (dont les 43 groupes SIREN de V-10) est inconnu.

### B-8 · Vérification complète des 4 critères d’honoraires publiés pour Gestion Cassini et ImmoVendu

Catégorie : honoraires · nature : fait_verifie · gravité : majeur · concerne l’éditeur : oui

Sur les pages relevées des deux agences de l’éditeur : (1) « Barème publié » (30/30) est confirmé pour les deux ; (2) « Montants TTC » (20/20) est confirmé pour les deux (mention explicite TVA 20 % et TTC) ; (3) « Payeur indiqué (vendeur ou acquéreur) » est contredit par la divergence entre 0/30 (Gestion Cassini) et 30/30 (ImmoVendu) sur une phrase identique laissant le choix au mandat ; (4) « Barème complet (toutes les tranches de prix) » (20/20 pour les deux) est impossible à juger avec certitude d’après le seul texte, les deux pages appliquant un pourcentage uniforme avec honoraire minimum plutôt que des tranches de prix.

Preuves : baremes_relus[0].points_publies (gestion-cassini) : Barème publié 30/30, Montants TTC 20/20, Payeur indiqué 0/30, Barème complet 20/20 ; baremes_relus[1].points_publies (immovendu) : Barème publié 30/30, Montants TTC 20/20, Payeur indiqué 30/30, Barème complet 20/20 ; baremes_relus[0].texte_page & baremes_relus[1].texte_page : « TVA incluse au taux de 20 % », « 6 % TTC », « Honoraires à la charge du VENDEUR ou de l’ACQUEREUR en fonction du mandat de vente. »

Incertitude : Pour « Barème complet (toutes les tranches de prix) », le paquet ne précise pas la grille d’appréciation appliquée aux barèmes à taux unique sans tranches de prix (6 % TTC avec minimum de 6 500 € TTC).

### B-9 · Incohérences sur 186 avis déclarés partagés entre agences et impossibilité de vérification textuelle (V-7 et V-6b éditeur/concurrentes) 

Catégorie : donnees · nature : non_verifiable · gravité : mineur · concerne l’éditeur : oui

Le contrôle V-7 relève 186 avis sur 49 agences (dont Gestion Cassini et ImmoVendu) déclarés partagés entre k agences, mais présents sur un nombre différent de fiches dans l’export. La détection reposant sur le texte des avis (absent des exports), cette anomalie demeure non vérifiable indépendamment à partir des données publiées.

Preuves : resultats_deterministes.controles[V-7] : severity = mineur, count = 186, 49 agences listées dont gestion-cassini et immovendu

Incertitude : Les textes intégraux des avis n’étant pas exportés dans les fichiers publics du site, il est impossible de vérifier si le partage détecté sur les 120 premiers caractères (I-13) correspond à de vrais avis communs ou à des textes génériques/erreurs d’export.

### B-10 · Impossibilité de vérifier à la source le retrait de 834 avis déclarés doublons faute de publication des textes (V-6) 

Catégorie : donnees · nature : non_verifiable · gravité : mineur · concerne l’éditeur : oui

834 avis répartis sur 50 agences (dont 21 pour ImmoVendu et 0 pour Gestion Cassini) sont écartés comme doublons. L’absence des textes d’avis dans les exports publiés (V-6) ainsi que l’absence de vérification des données primaires (statuts.donnees_primaires = non_verifiees) empêchent tout contrôle indépendant de la justesse de ce dédoublonnage.

Preuves : resultats_deterministes.controles[V-6] : count = 834, 50 agences, publisher_counts = {gestion-cassini: 0, immovendu: 21}

Incertitude : Bien que V-14 valide la reproductibilité interne des drapeaux publiés (0 écart), l’exactitude réelle du dédoublonnage par rapport aux textes originaux sur les plateformes reste non vérifiable.

### B-11 · Inclusion de 19 avis notés sous 1/5 (dont 9 comptés) avec échelle Opinion System non vérifiée à la source (V-4b) 

Catégorie : donnees · nature : fait_verifie · gravité : mineur · concerne l’éditeur : non

Dix agences (majoritairement des réseaux Orpi, Citya, Nestenn) comportent 19 avis (dont 9 comptés dans le score) notés en dessous de 1/5, minimum usuel d’une échelle à étoiles. Ces notes entrent telles quelles dans la moyenne, ce qui peut pénaliser les agences concernées si l’échelle source diffère.

Preuves : resultats_deterministes.controles[V-4b] : severity = mineur, count = 19, counted = 9, 10 agences

Incertitude : Sans vérification à la source sur Opinion System, il n’est pas établi si ces notes proviennent d’avis à 0 étoile légitimes ou d’une erreur de conversion d’échelle.

### B-12 · Règles techniques structurantes absentes de la documentation publique (I-1, I-2, I-8, I-10, I-13) 

Catégorie : methode · nature : fait_verifie · gravité : mineur · concerne l’éditeur : non

Plusieurs paramètres déterminants du calcul ne figurent pas dans la page méthode : pondération forfaitaire à 0,5 (équivalent à 3 ans) des plateformes non relevées avis par avis (I-1), calcul de la moyenne niçoise M_REF (4,453 au 15/11/2026) incluant des agences non classées (I-2), périmètre des réponses aux avis négatifs (I-8), précision sur les 12 mois calendaires et la décroissance continue de l’âge (I-3, I-5), et seuils exacts de détection des doublons et partages (I-13). L’ordre des opérations sur l’ancienneté (I-12) n’affecte que 2 agences de 0,005 point.

Preuves : regles_appliquees_absentes_ou_contraires_au_texte : I-1 (plateformes incomplètes à poids fixe 0.5), I-2 (M_REF = 4.453 au 15/11/2026 en moyenne simple incluant les non classées), I-8 (réponses limitées à Google vente/achat <=3 étoiles avec doublons si relevées), I-10 (jour ignoré dans anc), I-13 (seuils de reconnaissance des doublons et avis partagés)

Incertitude : Le paquet ne chiffre pas l’effet isolé de I-1, I-2, I-8 et I-13 sur les rangs (contrairement à I-4, I-6, I-7 et I-11).

### B-13 · Attribution d’une note neutre de 50/100 aux 15 agences sans date de création, favorisant les plus récentes (V-10d) 

Catégorie : donnees · nature : fait_verifie · gravité : mineur · concerne l’éditeur : non

Faute de date de création relevée, 15 agences reçoivent une note neutre d’ancienneté de 50,0 (équivalant à 10 ans). Cette règle avantage toute agence réellement âgée de moins de 10 ans (moyenne du groupe : 27,7) et pénalise celles de plus de 10 ans (moyenne du groupe : 87,7).

Preuves : resultats_deterministes.controles[V-10d] : count = 15, valeur neutre 50 ; tests_biais.groups.societe_moins_10_ans : anc = 27.7 ; societe_10_ans_et_plus : anc = 87.7

Incertitude : L’âge réel de ces 15 sociétés n’étant pas connu dans l’export, le sens exact de l’avantage ou de la pénalité par agence reste incertain.

### B-14 · Anomalies et mentions légales erronées ou expirées relevées sur la page d’honoraires d’ImmoVendu

Catégorie : donnees · nature : fait_verifie · gravité : mineur · concerne l’éditeur : oui

La page d’honoraires d’ImmoVendu (relevée le 2026-11-17) contient plusieurs inexactitudes factuelles : forme juridique indiquée comme « SAS » au lieu de SARL, numéro RCS erroné (« 400 877 688 » au lieu de 400 877 866, bien que le numéro de TVA soit correct), carte CPI affichée comme expirée au 16/06/2025, garantie transaction affichée à « 120.00 € » au lieu de 120 000 €, et compteurs d’activité laissés à zéro.

Preuves : baremes_relus[1].texte_page : « ImmoVendu by SAS GESTION CASSINI », « Inscrit au Registre du Commerce et des Sociétés sous le n°400 877 688 », « valable jusqu’au 16/06/2025 », « 120.00 € en TRANSACTION », « Propriétaires satisfaits 0 D’expérience immobilière 0 ans Année de création 0 »

Incertitude : Les critères détaillés composant le pilier Conformité (100,0 pour ImmoVendu vs 50,0 pour Gestion Cassini) ne figurent pas dans le paquet, empêchant de vérifier si ces mentions entrent ou non dans la notation.

### B-15 · Écarts mineurs entre avis Google relevés un par un et totaux déclarés sur 11 plateformes (V-12a) 

Catégorie : donnees · nature : fait_verifie · gravité : info · concerne l’éditeur : non

Sur les 525 plateformes relevées en entier, toutes respectent la tolérance fixée par V-12 (10 % ou 2 avis). Toutefois, V-12a signale 11 fiches Google présentant un écart exact : 10 fiches diffèrent de 1 avis et orpi-agerim-properties-nice|google affiche 115 avis relevés pour 126 déclarés.

Preuves : resultats_deterministes.controles[V-12a] : count = 11 ; detail[orpi-agerim-properties-nice|google] : releves = 115, declares = 126.0 ; 10 autres agences avec écart de 1 avis ; resultats_deterministes.controles[V-12] : count = 0 sur 525 plateformes relevées en entier

Incertitude : La cause de l’écart de 11 avis (8,7 %) sur orpi-agerim-properties-nice|google (avis non chargés ou masqués) n’est pas documentée.

### B-16 · Conformité totale du recalcul déterministe et de la reproductibilité interne du dédoublonnage sur 546 agences

Catégorie : calcul · nature : calcul_reproduit · gravité : info · concerne l’éditeur : oui

Le recalcul indépendant reproduit sans aucune divergence les 546 notes et les 546 rangs du classement (0 écart d’arrondi frontière), ainsi que la logique de dédoublonnage sur les exports (V-14 = 0). Les contrôles diachroniques par rapport au relevé précédent (V-13a, V-13b, V-13d, V-13e) ne relèvent aucune disparition ni modification rétroactive suspecte d’avis.

Preuves : resultats_deterministes.recalcul : examined = 546, notes.conforme = 546, divergente = 0, frontiere_arrondi = 0, ranks_divergent = 0, m_ref = 4.453 ; resultats_deterministes.controles[V-13a, V-13b, V-13d, V-13e, V-14] : tous à count = 0

Incertitude : Cette conformité valide la correspondance entre les exports publiés et les scores publiés, sans garantir l’exactitude des collectes primaires à la source.

### B-17 · Conformité des dates du registre des entreprises pour l’éditeur, reflétant la limite structurelle du SIREN

Catégorie : anciennete · nature : fait_verifie · gravité : info · concerne l’éditeur : oui

La vérification croisée avec le registre officiel des entreprises (api.gouv.fr) confirme que la date du 02/05/1995 publiée pour Gestion Cassini et ImmoVendu est strictement conforme à l’immatriculation de la société mère. L’écart entre l’ancienneté juridique (1995) et commerciale (2024 pour ImmoVendu) provient du choix de l’indicateur (SIREN) et non d’une falsification du registre.

Preuves : registre_entreprises.rows : gestion-cassini & immovendu, siren = 400877866, statut = conforme, date_publiee = 1995-05-02, date_registre = 1995-05-02 ; registre_entreprises.limite : le registre donne la date de création de la société, pas celle de l’enseigne

Incertitude : Aucune incertitude sur la date légale de la société SARL GESTION CASSINI (vérifiée par API officielle).

### B-18 · Zones non couvertes par le paquet d’audit limitant l’évaluation des données primaires et des concurrentes directes

Catégorie : donnees · nature : non_verifiable · gravité : info · concerne l’éditeur : oui

Trois angles restent hors de portée directe dans les données fournies : la vérification des plateformes et sites web sources (donnees_primaires = non_verifiees), la comparaison avec les 5 voisines immédiates des deux agences de l’éditeur (voisines_editeur.n = 0) et la relecture des barèmes ou fiches de conformité d’un échantillon d’agences concurrentes (echantillon = null).

Preuves : resultats_deterministes.statuts.donnees_primaires = non_verifiees ; tests_biais.groups.voisines_editeur.n = 0 ; echantillon = null

Incertitude : L’absence d’échantillon concurrent empêche de généraliser l’erreur de notation observée sur le barème de Gestion Cassini/ImmoVendu à l’ensemble des 546 agences.

## Points favorables au classement

- Reproductibilité mathématique intégrale : 546/546 notes, 546/546 rangs et dédoublonnage interne (V-14 = 0) reproduits sans aucune divergence.
- Stabilité temporelle des avis : aucune apparition rétroactive (V-13a = 0), aucune disparition anormale (V-13b = 0) ni modification silencieuse de note ou drapeau (V-13d = 0) depuis le relevé précédent.
- Cohérence globale de la collecte par plateforme : sur 525 plateformes relevées intégralement, 0 dépassement du seuil de tolérance (V-12 = 0).
- Absence d’avantage systématique sur tous les paramètres pour l’éditeur : l’inclusion des avis sans profil (55,2 %) fait reculer Gestion Cassini de 67 places (rang 129 au lieu de 62) et le critère « Payeur indiqué » lui attribue 0/30 malgré une clause identique à celle d’ImmoVendu.
- Dates légales de création conformes au registre officiel des entreprises pour les deux entités de l’éditeur (1995-05-02), sans saisie manuelle d’ancienneté dérogatoire (V-10c = 0).

## Points défavorables au classement

- Contradiction critique en conflit d’intérêts apparent sur les honoraires : ImmoVendu reçoit 30/30 et Gestion Cassini 0/30 sur le critère « Payeur indiqué » pour une phrase strictement identique (impact de 5,10 points sur la note finale, décisif pour la 1re place).
- Avantage décisif d’ancienneté pour ImmoVendu (rang 1), fondée en tant qu’enseigne en 2024 mais notée 100/100 sur la société de 1995 (+4,29 points, sans lesquels elle recule au rang 3), alors que la date d’enseigne manque pour 545 agences sur 546.
- Sensibilité extrême à des choix méthodologiques contestables : l’inclusion de 18 264 avis sans profil d’auteur modifie 520 rangs sur 546 (médiane 26 places) et le retrait des 5 % d’ancienneté modifie 539 rangs (faisant perdre la 1re place à ImmoVendu).
- Écarts avérés entre le texte public et le code exécuté (I-4, I-6, I-7, I-11 et règles non documentées I-1, I-2, I-8, I-10, I-13) modifiant 359 notes et 282 rangs sur 546.
- Forts biais structurels favorisant les grands volumes d’avis (+24,70 points) et les réseaux (+12,85 points), ainsi que des anomalies non vérifiables sur les doublons (834 avis) et avis partagés (186 avis) faute de publication des textes.

## Instructions suspectes repérées dans les données


## Limites

- Les données primaires (textes d’avis sur les plateformes, pages web des 544 agences concurrentes, critères détaillés de Conformité) n’ont pas été vérifiées (donnees_primaires = non_verifiees, echantillon = null).
- Le groupe de comparaison avec les agences immédiatement voisines de l’éditeur au classement est vide (voisines_editeur.n = 0).
- L’absence de la date de lancement d’enseigne pour 545 agences sur 546 (V-10b) empêche de quantifier l’effet général de la distinction entre société mère et enseigne commerciale sur les 43 groupes SIREN (V-10).
- L’effet individuel sur les rangs de plusieurs règles non documentées (I-1, I-2, I-8, I-13) n’est pas isolé par des scénarios contrefactuels dans le paquet fourni.
