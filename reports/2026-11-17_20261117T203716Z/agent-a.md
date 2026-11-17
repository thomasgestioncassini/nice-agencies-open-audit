# Analyse initiale — IA A

Fournisseur : openai · modèle : gpt-6.1-sol · statut : **ok**
Empreinte du mandat : 82e0fec40442f9e2ab530af39492ad0a83e777c1e424867598daa9a65e8089c8 · empreinte de l’entrée : 8b2c016bf806f802985afd92ebfd4110bc5ca77c97f0087c3441a8d426e817d4
Coût : 0.1058 $ (15395 jetons lus, 7503 écrits)

> Texte produit par l’IA, publié sans aucune modification ni relecture de l’éditeur.

## Résumé

Audit A du paquet fourni : les notes des deux agences de l’éditeur sont arithmétiquement cohérentes, mais la validité des données primaires et du classement complet n’est pas démontrée indépendamment. Les principales réserves concernent le conflit d’intérêts structurel, le traitement différent d’une même mention du payeur des honoraires, les 55,2 % d’avis au profil non précisé et la traçabilité des modifications. À l’inverse, plusieurs résultats contredisent l’hypothèse d’un avantage systématique à l’éditeur : l’exception d’ancienneté pénalise fortement ImmoVendu et l’inclusion des profils non précisés dégrade les rangs des deux agences de l’éditeur dans le test fourni. Aucune manipulation intentionnelle n’est établie.

## Constats

### A-1 · Conflit d’intérêts structurel entre l’éditeur et deux agences évaluées

Catégorie : conflit_interets · nature : fait_verifie · gravité : majeur · concerne l’éditeur : oui

L’éditeur évalue ses propres agences et leurs concurrentes. Cela constitue un risque objectif pour l’indépendance du classement, mais ne prouve ni une erreur particulière ni une manipulation.

Preuves : classement.editeur : SARL GESTION CASSINI ; classement.agences_editeur : gestion-cassini et immovendu. ; Les deux fiches indiquent le SIREN 400877866 et la raison sociale GESTION CASSINI. ; Rangs publiés : ImmoVendu 3 ; Gestion Cassini 94.

Incertitude : Le paquet ne décrit pas les garanties de séparation éditoriale, de validation indépendante ou de traitement des contestations.

### A-2 · Même mention du payeur, mais attribution opposée de 30 points

Catégorie : honoraires · nature : fait_verifie · gravité : majeur · concerne l’éditeur : oui

L’asymétrie n’est pas justifiée par les textes transmis. Selon la lecture littérale « payeur indiqué », les 30 points d’ImmoVendu sont confirmés et les 0 point de Gestion Cassini sont contredits. Si le critère exige un payeur unique et inconditionnel, aucun des deux textes ne le fournit : les mêmes exigences doivent alors s’appliquer aux deux agences. L’enjeu est de 5,10 points de note par agence : Gestion Cassini passerait à 82,37 avec 30 points supplémentaires ; ImmoVendu à 86,33 avec leur retrait. Les rangs correspondants ne sont pas calculables ici.

Preuves : Les deux textes contiennent : « Honoraires à la charge du VENDEUR ou de l’ACQUEREUR en fonction du mandat de vente. » ; Payeur indiqué : Gestion Cassini 0/30 ; ImmoVendu 30/30, observations datées du 17/11/2026. ; Poids du pilier honoraires : 17 %.

Incertitude : La règle opérationnelle permettant de décider si une mention conditionnelle suffit n’est pas fournie.

### A-3 · La majorité des avis comptés n’a pas de profil précisé

Catégorie : donnees · nature : fait_verifie · gravité : majeur · concerne l’éditeur : oui

Le périmètre effectivement évalué dépend fortement d’avis dont l’appartenance à la population visée n’est pas établie. Ce choix est matériel pour le classement. Le test fourni contredit toutefois l’idée qu’il favoriserait systématiquement l’éditeur : son exclusion améliore les rangs des deux agences de celui-ci.

Preuves : tests_biais.avis_non_precises : 18 264 avis non précisés, tous comptés, sur 33 064 avis comptés ; part annoncée 0,552. ; Scénario sans ces avis : 528 rangs changés, déplacement médian 26, maximum 252 ; 7 membres du top 10 conservés. ; Gestion Cassini : rang 94 vers 36 ; ImmoVendu : rang 3 vers 2.

Incertitude : Un profil non précisé n’est pas nécessairement un profil hors vente ou achat. Le test d’exclusion n’est pas une correction démontrée.

### A-4 · Les données primaires ne permettent pas de valider les classifications

Catégorie : donnees · nature : non_verifiable · gravité : majeur · concerne l’éditeur : oui

Il est impossible de contrôler ici les distinctions vente/achat/location/gestion, les problèmes signalés ou les faux rapprochements entre avis. Une reproduction du calcul à partir des étiquettes publiées ne valide pas ces étiquettes. Cette limite s’applique également aux agences de l’éditeur et aux concurrentes.

Preuves : resultats_deterministes.statuts.donnees_primaires : non_verifiees. ; Le paquet ne contient pas les textes individuels des avis ni les décisions détaillées de profil et de problème signalé. ; La règle I-9 utilise les avis uniques dont le texte a été lu par l’IA.

Incertitude : Le taux d’erreur de classification et son éventuelle asymétrie sont inconnus.

### A-5 · Modifications de critères insuffisamment tracées

Catégorie : donnees · nature : fait_verifie · gravité : majeur · concerne l’éditeur : oui

L’alerte révèle une traçabilité générale incomplète, pas nécessairement une absence de relecture. Pour le payeur des agences de l’éditeur, la date spécifique explique au moins partiellement l’écart avec la date générale. Sans journal des modifications, leur direction et leur effet cumulé restent inconnus.

Preuves : Contrôle V-13c : 16 modifications de points sans nouvelle date de lecture du site ; 11 agences listées. ; Gestion Cassini et ImmoVendu : date_lecture_site 2026-11-12, mais date_relecture_payeur 2026-11-17. ; Les observations du critère payeur des deux agences sont datées du 17/11/2026.

Incertitude : Les anciennes valeurs et le détail des 16 modifications ne sont pas fournis. Une relecture spécifique du payeur est néanmoins documentée pour les deux agences de l’éditeur.

### A-6 · La documentation historique ne doit pas être confondue avec la méthode actuelle

Catégorie : methode · nature : fait_verifie · gravité : majeur · concerne l’éditeur : oui

Les écarts historiques sont matériels, mais leur persistance actuelle ne peut pas être affirmée à partir des seuls intitulés hérités. Les formulations fournies suggèrent plusieurs clarifications récentes, notamment sur les doublons, les arrondis et la redistribution. Il faut rapprocher chaque règle du texte daté applicable. Dans la variante historique d’ensemble, Gestion Cassini passe de 94 à 93 et ImmoVendu reste 3e.

Preuves : Statuts : texte_documentation complete, texte_coherence aucune_contradiction_repertoriee, texte_historique ecarts_anterieurs. ; La liste regles_appliquees_absentes_ou_contraires_au_texte conserve des qualifications non_documente et contradiction, tout en donnant des formulations documented_by. ; Variante historique d’ensemble : 359 notes et 261 rangs changés, maximum 35 places ; top 10 intégralement conservé.

Incertitude : Le texte public intégral de la v5.4 et ses versions antérieures ne sont pas reproduits.

### A-7 · Les poids produisent une forte mobilité hors du sommet du classement

Catégorie : biais · nature : fait_verifie · gravité : majeur · concerne l’éditeur : oui

Le rang précis dépend sensiblement de choix normatifs de pondération. Cela relativise les écarts de quelques places sans invalider les scores. La stabilité d’ImmoVendu dans tous ces scénarios constitue un résultat favorable à la robustesse de sa position.

Preuves : Poids : avis 43 %, services 16 %, honoraires 17 %, confiance 11 %, informations 8 %, ancienneté 5 %. ; avis_moins20 : 516 rangs changés, déplacement médian 6 et maximum 37. ; hono_moins20 : 454 rangs changés, déplacement médian 9 et maximum 30. ; Dans les douze scénarios de variation de poids, ImmoVendu reste 3e ; Gestion Cassini varie de la 83e à la 104e place.

Incertitude : Les modalités exactes de renormalisation des poids ne sont pas détaillées dans le paquet.

### A-8 · L’ancienneté est comparée sur des bases différentes selon les enseignes

Catégorie : anciennete · nature : fait_verifie · gravité : majeur · concerne l’éditeur : oui

La règle générale mesure l’âge de la société, alors que l’exception mesure un événement lié à l’enseigne. La comparaison homogène des enseignes récentes exploitées par des sociétés anciennes est impossible. Cette asymétrie est ici défavorable à ImmoVendu, et non favorable.

Preuves : V-10b : date de lancement d’enseigne connue pour 1 agence sur 546, ImmoVendu. ; V-10f : même SIREN 400877866 ; dates utilisées 1995-05-02 pour Gestion Cassini et 2024-05-01 pour ImmoVendu. ; Source d’ImmoVendu : exception_editeur_depot_de_marque ; ancienneté publiée 12,5/100 contre 100/100 pour Gestion Cassini.

Incertitude : Le justificatif de dépôt de marque et les dates d’enseigne des concurrentes ne sont pas fournis.

### A-9 · Valeurs manquantes et redistribution ont des effets non neutres

Catégorie : methode · nature : fait_verifie · gravité : mineur · concerne l’éditeur : oui

Une valeur dite neutre n’est pas neutre en résultat : 50 points d’ancienneté apportent 2,50 points de note, autant qu’environ dix ans d’activité selon l’échelle. La redistribution de la régularité peut avantager ou désavantager selon les autres sous-scores. Elle ne contredit pas, à elle seule, une interdiction limitée à la redistribution des piliers entiers.

Preuves : V-10d : 15 agences sans date de création reçoivent 50 points d’ancienneté. ; I-6 : sans avis relevés individuellement, les 15 % de régularité sont reportés sur qualité et volume. ; Variante régularité neutre à 50 : 21 notes et 218 rangs changés, maximum 35 places ; Gestion Cassini 94 vers 93, ImmoVendu inchangé.

Incertitude : Les valeurs des autres piliers manquants et toutes les agences soumises à I-6 ne sont pas détaillées.

### A-10 · Les plateformes incomplètes sont traitées comme des avis d’âge et de profil synthétiques

Catégorie : methode · nature : fait_verifie · gravité : mineur · concerne l’éditeur : non

Le poids 0,5 est une convention, pas l’âge observé des avis. Le traitement agrégé n’est donc pas équivalent au traitement individuel avec dates et profils. La référence de Nice est une moyenne par agence, non une moyenne de tous les avis, et sa population dépasse les seules agences classées. Ces choix doivent être explicités sans être assimilés automatiquement à des erreurs.

Preuves : I-1 : note globale de plateforme, chaque avis recevant un poids fixe de 0,5, sans profil ni date. ; I-2 : référence de Nice calculée sur les moyennes par agence de toutes les agences de agregats-plateformes.csv, classées ou non ; m_ref 4,453. ; I-4 : le dénominateur de régularité compte notamment les doublons et les plateformes incomplètes.

Incertitude : Les effectifs concernés et leurs effets séparés sur les agences ne sont pas fournis.

### A-11 · Les associations de scores avec volume, réseau et outils numériques ne prouvent pas un biais causal

Catégorie : biais · nature : calcul_reproduit · gravité : mineur · concerne l’éditeur : oui

Ces écarts sont compatibles avec un avantage structurel aux agences visibles, équipées et dotées de nombreux avis, mais aussi avec des différences réelles de qualité et de documentation. Ils ne démontrent pas un favoritisme. Le volume est en partie directement récompensé par la méthode : l’association n’est donc pas une validation indépendante de qualité.

Preuves : Grand volume contre petit volume : 72,69 − 48,05 = 24,64 points de note moyenne. ; Réseau contre indépendante : 72,37 − 59,76 = 12,61 points. ; Estimation en ligne contre absence : 69,18 − 53,92 = 15,26 points. ; Moyenne éditeur contre ensemble : 84,35 − 61,33 = 23,02 points ; seulement deux agences chez l’éditeur.

Incertitude : Les groupes ne sont pas appariés et aucune analyse multivariée n’est fournie.

### A-12 · La comparaison prévue avec les voisines de l’éditeur est absente

Catégorie : donnees · nature : fait_verifie · gravité : mineur · concerne l’éditeur : oui

Le groupe devrait comporter des observations compte tenu des rangs indiqués, même en tenant compte de la borne supérieure pour la 3e place. Son absence empêche la comparaison locale promise. Le champ not_testable vide ne rend pas compte de cette impossibilité.

Preuves : tests_biais.groups.voisines_editeur.n : 0. ; Définition annoncée : les cinq agences juste au-dessus et juste en dessous de chaque agence de l’éditeur. ; Les deux rangs suivis sont 3 et 94 sur 546.

Incertitude : La cause de ce groupe vide n’est pas documentée.

### A-13 · Des notes inférieures à une étoile nécessitent une vérification de l’échelle source

Catégorie : donnees · nature : fait_verifie · gravité : mineur · concerne l’éditeur : non

Il peut s’agir d’une échelle valide ou d’une erreur de conversion. Si l’échelle attendue commence réellement à 1, l’intégration sans correction pénaliserait les agences concernées. Aucun effet chiffré sur leurs notes ou rangs ne peut être établi ici.

Preuves : V-4b : 19 avis sous 1/5, dont 9 comptés ; échelle d’Opinion System à vérifier. ; Le contrôle indique que ces notes entrent telles quelles dans la moyenne.

Incertitude : Les notes individuelles et l’échelle native d’Opinion System ne sont pas fournies.

### A-14 · Dédoublonnage reproductible ne signifie pas identité des avis vérifiée

Catégorie : donnees · nature : non_verifiable · gravité : mineur · concerne l’éditeur : oui

Le résultat V-14 soutient la cohérence algorithmique annoncée, mais ne mesure ni faux doublons ni doublons manqués. Les 186 écarts de partage ne suffisent pas à établir des erreurs : leur détection utilise des informations absentes de l’export. Les mêmes réserves valent pour l’éditeur et les concurrentes.

Preuves : V-6 : 834 avis déclarés doublons ; Gestion Cassini 0, ImmoVendu 21. ; V-7 : 186 avis avec écart entre partage déclaré et présence observée sur les fiches exportées ; les deux agences de l’éditeur figurent dans la liste. ; V-14 : aucune agence présentant une divergence dans le dédoublonnage refait selon le rapport fourni. ; I-13 : rapprochement textuel ou identité approchée ; partage fondé sur les 120 premiers caractères.

Incertitude : Les textes individuels nécessaires au contrôle sémantique sont absents du paquet.

### A-15 · Arrondis et départage modifient certains rangs sans changer le top 10

Catégorie : methode · nature : fait_verifie · gravité : mineur · concerne l’éditeur : oui

La notion de « note exacte » doit être distinguée d’une note arrondie au centième. Le départage réintroduit des profils hors vente/achat, mais seulement à égalité. Les effets observés sont limités : top 10 inchangé dans les deux variantes ; Gestion Cassini gagne une place dans la variante d’arrondi et ImmoVendu reste 3e.

Preuves : I-7 : sous-critères et piliers arrondis au dixième, note au centième utilisée pour le rang. ; Variante sans arrondis intermédiaires : 353 notes et 79 rangs changés, maximum 2 places. ; I-11 : égalités départagées par tous les avis, y compris locataires, bailleurs et syndic, puis ordre interne. ; Variante départage par avis vente/achat : 4 rangs changés, maximum 1 place.

Incertitude : Le texte courant intégral et les derniers ex æquo ne sont pas fournis.

### A-16 · Les trois autres critères d’honoraires sont confirmés pour les deux agences

Catégorie : honoraires · nature : fait_verifie · gravité : info · concerne l’éditeur : oui

Pour Gestion Cassini comme pour ImmoVendu : « Barème publié » confirmé ; « Montants TTC » confirmé ; « Barème complet, toutes les tranches de prix » confirmé pour les transactions décrites, les taux fixes et minimums couvrant les prix sans trou apparent. Le critère du payeur est traité séparément en A-2. Ces appréciations ne constituent pas une certification juridique du barème.

Preuves : Les deux pages sont relevées avec HTTP 200 et contiennent une grille de transaction. ; Les deux textes indiquent une TVA incluse à 20 %, des taux TTC et des minimums de 6 500 € et 3 000 € TTC. ; Points publiés pour chacune : barème publié 30/30 ; montants TTC 20/20 ; barème complet 20/20.

Incertitude : Le texte d’ImmoVendu est signalé tronqué, mais la grille de transaction et ses minimums figurent dans l’extrait. L’exhaustivité de prestations non mentionnées ne peut pas être certifiée.

### A-17 · Les notes des deux agences de l’éditeur sont correctement pondérées

Catégorie : calcul · nature : calcul_reproduit · gravité : info · concerne l’éditeur : oui

Aucune anomalie arithmétique n’apparaît dans les deux notes directement contrôlables. Cela confirme leur agrégation, non la justesse des données d’entrée ni leurs rangs.

Preuves : Gestion Cassini : 76,7×0,43 + 69,6×0,16 + 70×0,17 + 75×0,11 + 100×0,08 + 100×0,05 = 77,267, arrondi à 77,27. ; ImmoVendu : 94,6×0,43 + 88,3×0,16 + 100×0,17 + 100×0,11 + 100×0,08 + 12,5×0,05 = 91,431, arrondi à 91,43. ; Somme des poids : 100 ; somme des nombres de critères : 3+2+4+7+5+1 = 22.

Incertitude : Les sous-scores de toutes les agences ne sont pas fournis.

### A-18 · La reproduction complète est favorable, mais seulement rapportée dans ce paquet

Catégorie : calcul · nature : declaration_site · gravité : info · concerne l’éditeur : oui

Ces résultats sont favorables à la cohérence technique et à la stabilité récente des avis. Ils sont consignés comme résultats rapportés, et non comme une reproduction indépendante des 546 lignes réalisée dans le présent audit.

Preuves : resultats_deterministes.recalcul : 546 agences examinées, 546 notes conformes, 0 divergente, 0 frontière d’arrondi et 0 rang divergent. ; V-13a, V-13b, V-13d et V-13e : aucun ajout ancien suspect, disparition, changement d’avis déjà relevé ou retrait d’agence signalé.

Incertitude : Les fichiers complets, scripts exécutables et relevés successifs nécessaires pour refaire ces contrôles ne sont pas joints.

### A-19 · Les dates du registre sont cohérentes ; l’exception d’ImmoVendu est pénalisante

Catégorie : anciennete · nature : calcul_reproduit · gravité : info · concerne l’éditeur : oui

La création de la société en 1995 et le lancement d’une enseigne en 2024 ne sont pas contradictoires. Sans l’exception et toutes choses égales par ailleurs, ImmoVendu aurait une note calculée de 95,81 au lieu de 91,43 ; son rang n’est pas fourni. Le scénario fondé sur l’année d’enseigne donne 91,52, soit seulement 0,09 point de plus et le même rang. L’ancienneté avantage Gestion Cassini mais pénalise ImmoVendu.

Preuves : registre_entreprises : date publiée et date du registre identiques, 1995-05-02, pour le SIREN 400877866. ; Date d’ancienneté effective d’ImmoVendu : 2024-05-01 ; de mai 2024 à novembre 2026, 30 mois donnent 2,5/20×100 = 12,5 points. ; Différence avec 100 points d’ancienneté : 87,5×0,05 = 4,375 points de note. ; Scénario sans ancienneté : Gestion Cassini 94 vers 117 ; ImmoVendu 3 vers 2.

Incertitude : Le registre est fourni sous forme de résultats avec URL et empreinte, sans consultation indépendante. La preuve du dépôt de marque n’est pas jointe.

### A-20 · Les écarts de comptage des plateformes restent sous la tolérance annoncée

Catégorie : donnees · nature : calcul_reproduit · gravité : info · concerne l’éditeur : non

Les contrôles V-12a et V-12 ne se contredisent pas : le premier relève tout écart, le second applique une tolérance. Ces différences appellent une réconciliation des dates et des sources, mais n’établissent pas une collecte sélective.

Preuves : V-12a : 11 plateformes présentent un écart non nul ; 10 écarts valent un avis. ; Orpi Agerim : 115 avis relevés contre 126 déclarés, soit 11/126 = environ 8,73 %. ; V-12 : aucune alerte sur 525 plateformes intégralement relevées, avec tolérance de 10 % ou 2 avis.

Incertitude : Les deux nombres comparés proviennent des exports du site, non d’une vérification directe des plateformes.

## Points favorables au classement

- Les deux notes directement recalculables sont conformes aux poids publiés ; les poids totalisent 100 % et les critères annoncés totalisent 22.
- Le rapport déterministe fourni annonce 546 notes et rangs conformes, sans divergence.
- ImmoVendu reste 3e dans les douze variations de poids ; le top 10 est intégralement conservé dans les variantes liées au texte initial.
- L’exception d’ancienneté retire 4,375 points de note à ImmoVendu par rapport à l’âge de sa société : elle est défavorable à cette agence de l’éditeur.
- L’exclusion des avis au profil non précisé améliore le rang des deux agences de l’éditeur : leur inclusion n’apparaît donc pas comme un avantage systématique pour celui-ci.
- Les textes fournis confirment la publication, l’affichage TTC et la couverture des prix des barèmes des deux agences.
- Les contrôles historiques fournis ne signalent ni disparition d’avis, ni modification d’avis déjà relevés, ni retrait d’agence.

## Points défavorables au classement

- L’éditeur classe deux agences qu’il exploite lui-même, sans garanties d’indépendance documentées dans le paquet.
- Une mention identique du payeur reçoit 0/30 chez Gestion Cassini et 30/30 chez ImmoVendu, soit un enjeu de 5,10 points de note.
- Les avis au profil non précisé représentent 55,2 % des avis comptés ; leur exclusion modifie 528 rangs.
- Les textes individuels et les classifications primaires ne sont pas disponibles pour vérifier le périmètre vente/achat et les problèmes signalés.
- La traçabilité des changements de critères et la correspondance entre documentation historique et actuelle doivent être consolidées.
- L’ancienneté mélange âge de société et événement d’enseigne ; les dates d’enseigne sont absentes pour 545 agences.
- Les conventions de traitement des données incomplètes et les pondérations peuvent déplacer substantiellement les rangs.
- La comparaison locale annoncée avec les voisines de l’éditeur est vide.

## Instructions suspectes repérées dans les données


## Limites

- Audit limité au paquet transmis : aucune page externe, API ou empreinte n’a été vérifiée indépendamment.
- Absence des fichiers complets des 546 agences, des avis individuels, du code exécutable et du texte intégral de la méthode v5.4.
- Les tests contrefactuels sont analysés comme résultats fournis ; ils n’ont pas été réexécutés.
- Les scénarios de modification des poids ou d’exclusion d’avis mesurent une sensibilité, pas une correction nécessairement plus juste.
- Le texte d’ImmoVendu est signalé tronqué ; les éléments tarifaires cités restent visibles.
- Les effets de correction des honoraires peuvent être calculés sur les notes, mais pas sur les rangs sans les autres scores.
- Les écarts entre groupes sont descriptifs et ne permettent pas d’identifier une causalité ou une intention.
- Aucune preuve suffisante de manipulation intentionnelle n’est apportée par ce paquet.
