# Analyse initiale — IA A

Fournisseur : openai · modèle : gpt-6.1-sol · statut : **ok**
Empreinte du mandat : 82e0fec40442f9e2ab530af39492ad0a83e777c1e424867598daa9a65e8089c8 · empreinte de l’entrée : d99c86ca476477c4f56feb2e78d467e1db07a26e4f0d4ba9bb23633ccb919477
Coût : 0.1139 $ (15277 jetons lus, 8339 écrits)

> Texte produit par l’IA, publié sans aucune modification ni relecture de l’éditeur.

## Résumé

L’audit met en évidence une incohérence de notation des honoraires entre les deux agences de l’éditeur, ainsi qu’une forte dépendance du classement aux avis dont le profil n’est pas précisé. Les calculs pondérés des deux agences sont reproductibles, mais la conformité annoncée pour 546 agences n’est pas vérifiable indépendamment avec ce seul paquet. L’exception d’ancienneté appliquée à ImmoVendu lui est nettement défavorable ; plusieurs autres tests désavantagent également les agences de l’éditeur, ce qui interdit de conclure à une manipulation générale. Les principales réserves portent sur la qualité des données primaires, l’égalité de traitement, les valeurs manquantes et la portée des validations annoncées.

## Constats

### A-1 · Une même mention du payeur reçoit deux notes opposées

Catégorie : honoraires · nature : fait_verifie · gravité : majeur · concerne l’éditeur : oui

L’égalité de traitement est contredite par les données fournies. Selon une lecture exigeant seulement la mention des payeurs possibles, les 30 points d’ImmoVendu sont confirmés et les 0 point de Gestion Cassini sont contredits. Selon une lecture exigeant un payeur déterminé sans renvoi au mandat, il faut appliquer la même restriction aux deux agences. Porter Gestion Cassini à 100/100 en honoraires donnerait 79,62 au lieu de 74,52 ; ramener ImmoVendu à 70/100 donnerait 82,48 au lieu de 87,58. Aucun rang corrigé ne peut être établi avec le paquet.

Preuves : baremes_relus : les deux textes comportent « Honoraires à la charge du VENDEUR ou de l’ACQUEREUR en fonction du mandat de vente. » ; Gestion Cassini : Payeur indiqué = 0/30 ; ImmoVendu : Payeur indiqué = 30/30. ; Les deux observations du critère sont datées du 17/11/2026 ; poids du pilier honoraires = 17 %.

Incertitude : La définition opérationnelle complète du critère n’est pas fournie. Le texte identifie les deux payeurs possibles, sans désigner un payeur unique pour toutes les ventes.

### A-2 · Plus de la moitié des avis comptés ont un profil non précisé

Catégorie : donnees · nature : fait_verifie · gravité : majeur · concerne l’éditeur : oui

L’adéquation d’une majorité des avis au périmètre vente/achat n’est pas établie. Ce choix de classification est beaucoup plus influent que plusieurs variantes techniques. Il pénalise notamment Gestion Cassini dans le test fourni, et non l’inverse. L’amélioration du rang d’ImmoVendu malgré une légère baisse de note rappelle que les rangs sont relatifs.

Preuves : tests_biais.avis_non_precises : 18 264 avis non précisés, tous comptés, sur 33 064 avis comptés ; part annoncée = 55,2 %. ; scenario_sans_non_precises : 527 rangs changés, déplacement médian de 26, maximum de 251 ; 6 membres du top 10 conservés. ; Gestion Cassini : rang 131 vers 63, note 74,52 vers 79,24 ; ImmoVendu : rang 12 vers 9, note 87,58 vers 87,50.

Incertitude : Un profil non précisé ne prouve pas qu’un avis relève de la location ou du syndic. Leur exclusion intégrale est un test de sensibilité, pas une correction validée.

### A-3 · L’éditeur classe ses propres agences : conflit d’intérêts structurel

Catégorie : conflit_interets · nature : fait_verifie · gravité : majeur · concerne l’éditeur : oui

La même société bénéficie du classement et intervient dans la collecte, les classifications et les règles qui le produisent. Cela justifie une validation externe, particulièrement pour les critères interprétatifs. Ce conflit n’est pas une preuve de manipulation : la pénalisation d’ancienneté d’ImmoVendu et plusieurs tests défavorables aux agences de l’éditeur constituent des éléments contraires à une telle conclusion.

Preuves : classement.editeur = SARL GESTION CASSINI ; agences_editeur = gestion-cassini et immovendu. ; Les deux agences ont le SIREN 400877866. ; Rangs publiés : Gestion Cassini 131 ; ImmoVendu 12.

Incertitude : Le paquet ne décrit pas de dispositif de validation indépendant. Son absence dans le paquet ne démontre pas son inexistence.

### A-4 · La conformité des calculs ne valide pas les données primaires

Catégorie : donnees · nature : non_verifiable · gravité : majeur · concerne l’éditeur : oui

Il n’est pas possible de vérifier la fidélité des avis, leur classement par profil, la détection des problèmes ou l’ensemble des observations de sites. Une note correctement calculée peut reposer sur une mauvaise classification. Les 546 conformités doivent être présentées comme un résultat du contrôle fourni, et non comme une validation indépendante des données par ce présent audit.

Preuves : resultats_deterministes.statuts.donnees_primaires = non_verifiees. ; recalcul : 546 notes conformes et 0 rang divergent annoncés. ; echantillon = null ; les fichiers complets d’avis, de critères et le code exécutable ne sont pas joints. ; I-9 : les problèmes signalés reposent sur les avis dont le texte a été lu par l’IA.

Incertitude : Les résultats des contrôles sont disponibles, mais pas les éléments permettant de les reproduire intégralement.

### A-5 · L’exception d’ancienneté d’ImmoVendu est défavorable, mais non généralisable aux concurrentes

Catégorie : anciennete · nature : calcul_reproduit · gravité : majeur · concerne l’éditeur : oui

Avec l’ancienneté de sa société, ImmoVendu aurait 100 au lieu de 12,5 sur ce pilier, soit 4,375 points supplémentaires avant arrondi et une note de 91,96 au lieu de 87,58. L’exception est donc nettement défavorable à cette agence de l’éditeur. En revanche, l’absence de dates d’enseigne concurrentes empêche de savoir combien de concurrentes bénéficient d’une société ancienne pour une enseigne récente. Le test intitulé anciennete_depuis_enseigne, qui donne 87,67 et le rang 11, n’est pas le contrefactuel « date de société » ; son léger écart avec la production n’est pas expliqué précisément.

Preuves : V-10f : Gestion Cassini utilise le 02/05/1995 ; ImmoVendu utilise le 01/05/2024, malgré le même SIREN. ; ImmoVendu : source_anciennete = exception_editeur_depot_de_marque ; pilier ancienneté = 12,5. ; V-10b : date de lancement d’enseigne disponible pour 1 agence sur 546 seulement. ; Poids de l’ancienneté = 5 %.

Incertitude : La date de dépôt de marque n’est pas vérifiée par une pièce de registre de marques jointe. Les dates d’enseigne des concurrentes manquent.

### A-6 · Les valeurs manquantes entraînent des traitements hétérogènes et influents

Catégorie : methode · nature : fait_verifie · gravité : majeur · concerne l’éditeur : oui

Une information absente est tantôt remplacée par 50, tantôt exclue avec redistribution de poids, tantôt omise du dénominateur observé. Pour l’ancienneté, 50 équivaut à dix ans : cela peut avantager une société plus récente ou désavantager une plus ancienne. La variante I-6 améliore Gestion Cassini de 131 à 129 et laisse ImmoVendu au rang 12 ; le traitement de production n’avantage donc pas systématiquement l’éditeur.

Preuves : V-10d : 15 agences sans date de création reçoivent une ancienneté neutre de 50. ; I-6 : sans avis relevé individuellement, les 15 % de régularité sont redistribués entre qualité et volume. ; Variante I-6 : 21 notes et 211 rangs changés ; déplacement maximal de 34. ; I-8 : seules les réponses négatives dont la présence ou l’absence a été relevée entrent dans le périmètre.

Incertitude : Le paquet ne fournit pas une matrice exhaustive des valeurs manquantes et de leur distribution entre agences.

### A-7 · Le paquet ne permet pas de certifier l’absence actuelle de contradiction documentaire

Catégorie : methode · nature : fait_verifie · gravité : majeur · concerne l’éditeur : oui

Il faut distinguer la méthode initiale, les précisions de v5.4 et la pratique de calcul. Les champs documented_by suggèrent plusieurs corrections documentaires, mais les extraits ne permettent pas de contrôler leur articulation avec les affirmations générales. La conformité annoncée est donc plus forte que ce que ce paquet permet de vérifier indépendamment.

Preuves : statuts : texte_documentation = complete ; texte_coherence = aucune_contradiction_repertoriee ; texte_historique = ecarts_anterieurs. ; La liste regles_appliquees_absentes_ou_contraires_au_texte contient encore des text_gap, kind, documented_by et contradicted_by. ; I-4 oppose « ne compte qu’une fois » à « La régularité [...] les compte tous ». ; Le texte public intégral de la version v5.4 n’est pas joint.

Incertitude : Les entrées peuvent conserver des écarts historiques corrigés par des précisions plus récentes. Leur coexistence ne prouve pas que toutes les contradictions subsistent sur le site.

### A-8 · Le volume d’avis et l’ancienneté structurent fortement le classement

Catégorie : biais · nature : fait_verifie · gravité : majeur · concerne l’éditeur : oui

Le classement valorise des caractéristiques de visibilité et d’historique qui ne sont pas identiques à la qualité du service rendu. L’ancienneté avantage Gestion Cassini mais pénalise ImmoVendu. Les sociétés jeunes ont de meilleurs scores moyens de services dans le paquet, tout en recevant mécaniquement moins de points d’ancienneté.

Preuves : Grand volume d’avis : note moyenne 72,68 ; petit volume : 48,03 ; 182 agences dans chaque groupe. ; Scénario sans ancienneté : 536 rangs changés, déplacement médian 13, maximum 49 ; 7 membres du top 10 conservés. ; Sans ancienneté : Gestion Cassini passe de 131 à 151 ; ImmoVendu de 12 à 6. ; Sociétés de moins de dix ans : services 70,1 ; sociétés plus anciennes : services 63,3.

Incertitude : Les groupes ne sont pas appariés. L’écart de 24,65 points entre petits et grands volumes ne mesure pas à lui seul un effet causal du barème.

### A-9 · Des avantages de visibilité numérique et de réseau sont observés sans preuve causale

Catégorie : biais · nature : fait_verifie · gravité : mineur · concerne l’éditeur : oui

Les écarts descriptifs sont de 12,64 points en faveur des réseaux et de 15,17 points en présence d’une estimation en ligne. Les deux agences de l’éditeur bénéficient de leur score maximal d’information. En revanche, les groupes d’activités ne soutiennent pas l’hypothèse d’un avantage général aux agences de vente seule comme ImmoVendu : leur moyenne est inférieure de 1,53 point.

Preuves : Réseaux : moyenne 72,38 sur 68 agences ; indépendantes : 59,74 sur 478 agences. ; Avec estimation en ligne : 69,13 sur 299 agences ; sans : 53,96 sur 220 agences. ; Pilier information : 100 pour chacune des deux agences de l’éditeur ; moyenne générale 62. ; Vente seule : moyenne 63,81 ; vente avec location ou gestion : 65,34.

Incertitude : La détection des réseaux repose sur des motifs de site ou d’identifiant. Aucun contrôle multivarié ou appariement n’est fourni.

### A-10 · Le rang d’ImmoVendu près du top 10 dépend des pondérations

Catégorie : biais · nature : fait_verifie · gravité : mineur · concerne l’éditeur : oui

La position exacte d’ImmoVendu autour de la dixième place n’est pas robuste à plusieurs pondérations plausibles. Les piliers information et avis lui sont favorables, tandis qu’une hausse du poids confiance le pénalise. Le maintien du top 10 dans les variantes honoraires constitue toutefois un élément de stabilité.

Preuves : Variation de ±20 % du poids avis : ImmoVendu aux rangs 10 et 16 ; Gestion Cassini aux rangs 134 et 126. ; Variation de ±20 % du poids confiance : ImmoVendu aux rangs 16 et 9. ; Variation de ±20 % du poids honoraires : 10 membres du top 10 conservés dans les deux variantes. ; Variation du poids information : Gestion Cassini aux rangs 128 et 137 ; ImmoVendu aux rangs 10 et 13.

Incertitude : Ces variantes sont des choix méthodologiques alternatifs, pas des intervalles statistiques de confiance.

### A-11 · Les trois autres critères d’honoraires sont étayés pour les deux agences

Catégorie : honoraires · nature : fait_verifie · gravité : mineur · concerne l’éditeur : oui

Pour Gestion Cassini comme pour ImmoVendu, « Barème publié » 30/30 est confirmé et « Montants TTC » 20/20 est confirmé au moment de la capture. « Barème complet, toutes les tranches de prix » 20/20 est également confirmé dans le périmètre tarifaire visible : taux proportionnels et minima couvrent les prix sans trou apparent ; des tranches explicites ne sont pas nécessaires à un taux constant. Cette appréciation ne certifie pas l’exhaustivité juridique de toutes les prestations. Le critère payeur demeure celui traité en A-1.

Preuves : Les deux pages : HTTP 200, status = lu et présence d’un tableau ou texte tarifaire. ; Les deux textes : TVA incluse au taux de 20 %, taux de transaction et montants expressément TTC. ; Habitation/professionnel : 6 % avec minimum de 6 500 € ; garages/parkings : minimum de 3 000 € et taux précisé. ; Gestion Cassini : text_truncated = false ; ImmoVendu : text_truncated = true.

Incertitude : Les captures du 17/11 ne prouvent pas l’état exact des pages au 12/11, date d’observation de ces trois critères. Le texte ImmoVendu est tronqué après la section tarifaire visible.

### A-12 · Les doublons sont traités différemment selon les sous-critères

Catégorie : methode · nature : fait_verifie · gravité : mineur · concerne l’éditeur : oui

La formule générale « un même avis [...] ne compte qu’une fois » ne décrit pas tous les usages effectifs des avis. Il faut préciser le traitement critère par critère. Dans le test fourni, la règle de régularité de production procure une place à ImmoVendu, sans effet sur Gestion Cassini ; cela établit un avantage ponctuel, pas son intention.

Preuves : I-4 : les doublons restent dans le dénominateur de régularité. ; I-8 : réponses aux avis négatifs calculées doublons compris ; I-9 : problèmes signalés calculés sur avis uniques. ; Variante I-4 : 8 notes et 56 rangs changés ; déplacement maximal de 17. ; ImmoVendu : rang 12 en production contre 13 dans la variante ; Gestion Cassini : 131 dans les deux cas.

Incertitude : La variante porte sur le texte initial. La précision de v5.4 peut désormais expliciter l’exception de régularité.

### A-13 · La validation des doublons et des avis partagés reste partiellement invérifiable

Catégorie : donnees · nature : non_verifiable · gravité : mineur · concerne l’éditeur : oui

V-14 ne suffit pas à lever la limite explicitement reconnue par V-6 et V-7. Les seuils de similarité et de début de texte peuvent produire des faux positifs ou faux négatifs, sans que leur fréquence soit mesurable ici. Les 21 exclusions d’ImmoVendu ne prouvent ni un avantage ni un désavantage net sans connaître les notes et poids des copies écartées.

Preuves : V-6 : 834 avis déclarés doublons ; textes non publiés ; ImmoVendu 21, Gestion Cassini 0. ; V-7 : 186 cas d’écart entre partage déclaré et nombre de fiches observées, dont les deux agences de l’éditeur. ; V-14 : aucune divergence de dédoublonnage annoncée. ; I-13 : priorité de conservation Opinion System, puis Immodvisor, puis Google ; seuils textuels et partage par début de texte.

Incertitude : Le décompte exact des 834 cas et l’effet net des exclusions sur chaque note ne sont pas fournis. Les textes nécessaires à une vérification sémantique manquent.

### A-14 · Des notes inférieures à 1/5 nécessitent un contrôle d’échelle

Catégorie : donnees · nature : fait_verifie · gravité : mineur · concerne l’éditeur : non

Si le minimum de l’échelle source est bien 1/5, l’intégration brute de ces valeurs minore les notes d’agences concurrentes. Aucune correction automatique n’est justifiée avant vérification de l’échelle et de la conversion. L’effet sur les notes finales n’est pas quantifiable avec les seuls comptes fournis.

Preuves : V-4b : 19 avis signalés sous 1/5, dont 9 comptés selon le champ counted. ; V-4b : l’échelle Opinion System doit être vérifiée à la source.

Incertitude : Une note sous 1 peut être valide sur l’échelle source ou résulter d’une conversion ; le paquet ne permet pas de trancher.

### A-15 · Les agrégats incomplets et la moyenne de référence introduisent des conventions importantes

Catégorie : methode · nature : fait_verifie · gravité : mineur · concerne l’éditeur : non

Le poids fixe assimile des avis d’âges inconnus à des avis de trois ans, et ne permet pas de contrôler leur profil. La « moyenne de Nice » n’est ni une moyenne pondérée par les avis ni nécessairement limitée aux agences classées. Ces choix peuvent être défendables, mais leur périmètre, leur date et leurs effets doivent être explicités.

Preuves : I-1 : plateformes non relevées intégralement représentées par leur note globale, chaque avis recevant un poids fixe de 0,5, sans profil ni date. ; I-2 : moyenne simple des notes moyennes des agences présentes dans agregats-plateformes.csv, classées ou non. ; m_ref = 4,453 ; description I-2 datée du 15/11/2026, relevé du classement au 17/11/2026.

Incertitude : Le nombre et la répartition des plateformes traitées par agrégat ne sont pas fournis. Aucun test isolant ces conventions n’est joint.

### A-16 · Les arrondis et le départage peuvent intégrer des avis hors vente/achat

Catégorie : methode · nature : fait_verifie · gravité : mineur · concerne l’éditeur : oui

Le rang n’utilise pas une note sans arrondi. Le volume d’avis hors vente/achat peut décider d’une égalité dans un classement orienté transaction, et l’ordre interne n’est pas un dernier recours pleinement transparent. Les effets observés sont limités : aucun des deux rangs de l’éditeur ne change dans ces deux variantes.

Preuves : I-7 : sous-critères et piliers arrondis au dixième, note finale au centième. ; Variante sans arrondis intermédiaires : 353 notes et 80 rangs changés, déplacement maximal de 2 ; 9 membres du top 10 conservés. ; I-11 : égalités départagées par tous les avis, y compris locataires, bailleurs et syndic, puis ordre interne. ; Variante de départage par avis vente/achat : 4 rangs changés, aucun changement de note.

Incertitude : Le texte v5.4 complet manque ; les extraits documented_by indiquent que certaines précisions ont pu être ajoutées.

### A-17 · La comparaison avec les voisines de rang annoncée n’a pas été produite

Catégorie : donnees · nature : fait_verifie · gravité : mineur · concerne l’éditeur : oui

Le groupe vide ne peut pas signifier qu’il n’existe aucune voisine de rang. La comparaison locale promise est manquante, et le tableau vide not_testable ne reflète pas cette limite ni l’impossibilité de comparer systématiquement les dates d’enseigne. La moyenne des deux agences de l’éditeur, 81,05 contre 61,32 globalement, n’est pas un substitut à une comparaison appariée.

Preuves : groups_definition.voisines_editeur : cinq agences juste au-dessus et cinq juste au-dessous de chaque agence de l’éditeur. ; groups.voisines_editeur.n = 0, alors que les agences de l’éditeur sont aux rangs 12 et 131 sur 546. ; tests_biais.not_testable = [].

Incertitude : Le paquet ne donne ni les identités ni les données des voisines, ni la cause de leur absence.

### A-18 · Les dates du registre sont cohérentes avec la société, pas avec l’âge de chaque enseigne

Catégorie : anciennete · nature : fait_verifie · gravité : info · concerne l’éditeur : oui

Il n’y a pas d’écart de création de société dans les deux lignes contrôlées. Le statut conforme d’ImmoVendu ne valide toutefois ni un lancement d’enseigne en 1995 ni la date exceptionnelle de 2024 utilisée au calcul : il compare seulement deux dates de société. La distinction entre date juridique publiée et date de notation explique l’écart apparent.

Preuves : registre_entreprises.rows : date_publiee = date_registre = 1995-05-02 pour les deux agences. ; SIREN commun 400877866 et même référence d’API et empreinte de réponse. ; ImmoVendu : enseigne_depuis = 2024 ; V-10f : date de calcul d’ancienneté = 2024-05-01.

Incertitude : Les réponses d’API ne sont pas directement consultées dans cet audit ; leur résultat est fourni dans le paquet.

### A-19 · Les pondérations et les deux notes de l’éditeur sont arithmétiquement cohérentes

Catégorie : calcul · nature : calcul_reproduit · gravité : info · concerne l’éditeur : oui

Les arrondis au centième donnent bien 74,52 et 87,58. Aucune erreur d’addition ou de pondération n’est constatée pour les deux agences de l’éditeur. Le paquet annonce également 546 notes conformes, aucun rang divergent et aucun cas frontière d’arrondi, sans fournir ici les données nécessaires à leur reproduction complète.

Preuves : Somme des poids : 43 + 16 + 17 + 11 + 8 + 5 = 100. ; Nombre de critères : 3 + 2 + 4 + 7 + 5 + 1 = 22. ; Gestion Cassini : 0,43×76,7 + 0,16×69,6 + 0,17×70 + 0,11×50 + 0,08×100 + 0,05×100 = 74,517. ; ImmoVendu : 0,43×94,6 + 0,16×88,3 + 0,17×100 + 0,11×65 + 0,08×100 + 0,05×12,5 = 87,581.

Incertitude : Ce recalcul porte sur les piliers fournis, pas sur la formation de chaque pilier ni sur les 544 autres agences.

### A-20 · Les écarts de compte d’avis sont faibles et compatibles avec le contrôle tolérant

Catégorie : donnees · nature : fait_verifie · gravité : info · concerne l’éditeur : non

V-12 et V-12a ne se contredisent pas : l’un recherche les écarts dépassant une tolérance, l’autre tous les écarts, même d’un avis. Dix différences sont d’un avis ; celle d’Orpi Agerim reste sous 10 %. Ces résultats sont plutôt favorables à la cohérence des comptes exportés, sans certifier leur exactitude à la source.

Preuves : V-12a : 11 plateformes avec différence exacte entre nombre relevé et affiché. ; Orpi Agerim : 115 avis relevés contre 126 déclarés, soit 11 d’écart et environ 8,7 % du nombre déclaré. ; Winter : 438 relevés contre 437 déclarés. ; V-12 : aucune anomalie parmi 525 plateformes avec tolérance de 10 % ou 2 avis.

Incertitude : Les deux nombres proviennent des exports du site et ne constituent pas une confrontation directe à la plateforme source.

### A-21 · Aucun changement suspect d’avis n’est signalé sur la période comparée

Catégorie : donnees · nature : declaration_site · gravité : info · concerne l’éditeur : oui

Les contrôles fournis n’apportent pas d’indice d’une suppression sélective ou d’un reclassement récent d’avis favorable à l’éditeur. C’est un élément favorable au classement et contraire à une hypothèse de manipulation récente par ces procédés. Sa portée reste limitée à la période et aux champs effectivement comparés.

Preuves : V-13a : aucun avis apparu avec une date ancienne sur une plateforme déjà relevée intégralement. ; V-13b et V-13e : aucun avis disparu et aucune agence retirée. ; V-13d : aucun changement de note, profil, problème signalé ou drapeau de comptage. ; Comptes de Gestion Cassini et d’ImmoVendu à zéro sur ces contrôles.

Incertitude : Les instantanés antérieurs et la durée exacte de comparaison ne sont pas joints.

## Points favorables au classement

- Les poids totalisent 100 %, les critères totalisent 22 et les deux notes de l’éditeur sont reproduites au centième.
- Le contrôle fourni annonce 546 notes conformes et aucun rang divergent.
- L’exception d’ancienneté réduit la note d’ImmoVendu d’environ 4,38 points par rapport à l’utilisation de la date de sa société.
- L’inclusion des profils non précisés et le traitement de la régularité manquante ne favorisent pas systématiquement les agences de l’éditeur.
- Les contrôles temporels ne signalent aucune disparition, modification ou arrivée ancienne d’avis.
- Les faibles écarts de compte sont compatibles avec les seuils annoncés.
- Plusieurs écarts documentaires semblent avoir été explicités en v5.4 ; il serait excessif de les présenter tous comme encore non documentés.

## Points défavorables au classement

- La même phrase relative au payeur vaut 0/30 chez Gestion Cassini et 30/30 chez ImmoVendu, soit un enjeu de 5,10 points de note par agence selon la correction retenue.
- Les profils non précisés représentent 55,2 % des avis comptés ; leur retrait déplace les rangs de 26 places en médiane.
- L’éditeur évalue ses propres agences sans validation externe démontrée dans le paquet.
- La reproductibilité annoncée ne garantit pas la qualité des classifications et des données primaires.
- Les informations manquantes reçoivent des traitements différents, dont certains modifient fortement les rangs.
- Les dates d’enseigne ne sont connues que pour une agence ; une application comparable de cette notion est impossible.
- La comparaison locale avec les voisines de rang est absente.
- La visibilité, le volume et l’historique pèsent fortement ; leur association à la qualité réelle du service n’est pas établie par les tests.

## Instructions suspectes repérées dans les données


## Limites

- Audit limité au paquet fourni, sans navigation ni consultation directe des URL mentionnées.
- Les empreintes SHA-256 identifient les captures déclarées mais ne valident pas à elles seules leur authenticité ou leur exhaustivité.
- Absence des fichiers complets d’avis, de critères et du code exécutable : impossibilité de reproduire indépendamment les 546 notes, les rangs et les scénarios.
- Absence du texte intégral actuel de la méthode : certaines contradictions peuvent être historiques ou déjà levées par les précisions de v5.4.
- Les barèmes de concurrentes ne sont pas fournis ; l’audit des quatre critères d’honoraires ne peut porter que sur les deux agences de l’éditeur.
- Le texte ImmoVendu est signalé tronqué, même si les éléments tarifaires nécessaires aux appréciations figurent dans l’extrait.
- Les captures tarifaires du 17/11 ne permettent pas de valider rétrospectivement leur contenu au 12/11.
- Les tests de sensibilité sont des contrefactuels, pas des corrections établies ni des preuves d’intention.
- Les comparaisons de groupes sont descriptives, non causales ; leurs règles de classification ne sont pas vérifiables agence par agence.
- Aucune preuve suffisante ne permet de conclure à une manipulation générale du classement.
