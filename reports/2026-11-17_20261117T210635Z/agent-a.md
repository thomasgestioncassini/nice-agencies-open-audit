# Analyse initiale — IA A

Fournisseur : openai · modèle : gpt-6.1-sol · statut : **ok**
Empreinte du mandat : 82e0fec40442f9e2ab530af39492ad0a83e777c1e424867598daa9a65e8089c8 · empreinte de l’entrée : 98c621da3077c2ccf7714acda0d6778b448222d9bf5c46a90dc8f5e60a86b960
Coût : 0.1183 $ (15292 jetons lus, 8767 écrits)

> Texte produit par l’IA, publié sans aucune modification ni relecture de l’éditeur.

## Résumé

Le paquet permet de reproduire les deux notes de l’éditeur, mais pas de certifier indépendamment les 546 résultats ni les données primaires. Les réserves principales concernent le conflit d’intérêts, une notation différente de formulations identiques sur le payeur des honoraires, les 55,2 % d’avis au profil non précisé et plusieurs choix méthodologiques influençant fortement les rangs. Des éléments contredisent toutefois l’hypothèse d’une faveur systématique : l’exception d’ancienneté pénalise ImmoVendu, les avis non précisés désavantagent Gestion Cassini dans le scénario fourni, et renforcer certains piliers dégrade les positions de l’éditeur. Aucune manipulation intentionnelle n’est démontrée.

## Constats

### A-1 · Conflit d’intérêts structurel entre l’éditeur et deux agences classées

Catégorie : conflit_interets · nature : fait_verifie · gravité : majeur · concerne l’éditeur : oui

L’entité qui définit et applique le classement exploite deux participantes. Cela impose une vigilance renforcée, sans constituer en soi une preuve de manipulation. La mention « gel de l’éditeur » dans la version v5.6 n’est accompagnée d’aucune règle permettant d’en contrôler la portée.

Preuves : classement.editeur = SARL GESTION CASSINI ; agences_editeur = gestion-cassini et immovendu. ; Les deux sources d’agence portent le SIREN 400877866 et la raison sociale GESTION CASSINI. ; Rangs publiés : Gestion Cassini 131 ; ImmoVendu 12.

Incertitude : Les mécanismes de séparation éditoriale, de recours et de contrôle indépendant ne sont pas fournis.

### A-2 · Honoraires : traitement incohérent d’une même formulation sur le payeur

Catégorie : honoraires · nature : fait_verifie · gravité : majeur · concerne l’éditeur : oui

Gestion Cassini : Barème publié 30/30 confirmé ; Montants TTC 20/20 confirmé ; Payeur 0/30 impossible à juger définitivement sans définition opérationnelle ; Barème complet 20/20 confirmé pour les prix des prestations présentées, avec taux et minima explicites. ImmoVendu : Barème publié 30/30 confirmé ; Montants TTC 20/20 confirmé ; Payeur 30/30 impossible à juger définitivement pour la même raison ; Barème complet 20/20 confirmé dans le périmètre transactionnel visible, sous réserve de troncature. L’attribution différente des points de payeur n’est pas justifiée par les passages fournis. Une règle commune conduirait soit à ajouter 5,10 points à Gestion Cassini, soit à retirer 5,10 points à ImmoVendu, toutes choses égales par ailleurs. Les notes deviendraient respectivement 79,62 ou 82,48 ; les nouveaux rangs ne sont pas calculables ici.

Preuves : Les deux textes indiquent : « Honoraires à la charge du VENDEUR ou de l’ACQUEREUR en fonction du mandat de vente. » ; Gestion Cassini : Payeur indiqué = 0/30 ; ImmoVendu = 30/30, observations du 17/11/2026. ; Poids du pilier honoraires : 17 %.

Incertitude : Le critère ne précise pas s’il suffit de mentionner les deux payeurs possibles ou s’il faut identifier un payeur déterminé. Le texte ImmoVendu est signalé comme tronqué.

### A-3 · Plus de la moitié des avis comptés n’ont pas de profil précisé

Catégorie : donnees · nature : fait_verifie · gravité : majeur · concerne l’éditeur : oui

La pertinence transactionnelle d’environ 55,2 % des avis comptés reste indéterminée. Le classement dépend fortement de leur inclusion. Le scénario contredit une hypothèse de faveur uniforme à l’éditeur : leur inclusion désavantage nettement Gestion Cassini et améliore légèrement la note d’ImmoVendu tout en dégradant son rang relatif.

Preuves : tests_biais.avis_non_precises : 18 264 avis non précisés, tous comptés, sur 33 064 avis comptés ; part publiée 0,552. ; Scénario d’exclusion : 526 rangs changés, déplacement médian 26, maximum 252, 6 membres du top 10 conservés. ; Gestion Cassini : rang 131 vers 62, note 74,52 vers 79,24 ; ImmoVendu : rang 12 vers 9, note 87,58 vers 87,50.

Incertitude : Un profil non précisé n’est pas nécessairement un profil hors vente ou achat. L’exclusion systématique n’est donc pas une correction démontrée.

### A-4 · Régularité : les doublons interviennent malgré une promesse générale de retrait

Catégorie : methode · nature : fait_verifie · gravité : majeur · concerne l’éditeur : oui

Le dossier révèle au minimum une tension entre la règle générale et l’exception appliquée à ce sous-critère. Le traitement doit être explicité comme une exception et justifié. Son effet est limité sur les notes directement modifiées, mais se propage à 58 rangs.

Preuves : Règle I-4 : le dénominateur de régularité compte les doublons entre plateformes et les plateformes incomplètes. ; Citation fournie : « un même avis publié sur plusieurs plateformes ne compte qu’une fois ». ; Variante I-4 : 8 notes et 58 rangs changés, déplacement maximal 19 ; ImmoVendu 12 vers 13 ; Gestion Cassini reste 131.

Incertitude : Le paquet comporte aussi une formulation précisant que la régularité « les compte tous » ; la page publique intégrale n’est pas fournie.

### A-5 · Régularité manquante : redistribution influente et non équivalente à une valeur neutre

Catégorie : methode · nature : fait_verifie · gravité : majeur · concerne l’éditeur : oui

Deux agences ne sont pas évaluées avec la même composition effective du pilier Avis selon la disponibilité du détail. La variante modifie environ 38,5 % des rangs. Elle n’établit pas que la neutralisation à 50 serait meilleure, mais montre que la gestion des valeurs absentes est déterminante.

Preuves : I-6 : en l’absence de relevé avis par avis, les 15 % de régularité sont reportés sur qualité et volume. ; Variante valeur neutre 50 : 21 notes changées, 210 rangs changés, déplacement maximal 34. ; Gestion Cassini : 131 vers 129 ; ImmoVendu reste 12.

Incertitude : L’interdiction citée vise la redistribution d’un pilier manquant, tandis que la règle concerne un sous-critère : ce n’est pas une contradiction littérale certaine.

### A-6 · Les plateformes incomplètes bénéficient d’un traitement différent des avis détaillés

Catégorie : methode · nature : fait_verifie · gravité : majeur · concerne l’éditeur : non

Cette substitution empêche d’appliquer individuellement les mêmes filtres et pondérations qu’aux avis détaillés. Selon l’âge réel et les profils, elle peut avantager ou désavantager une agence. L’absence de ventilation interdit de quantifier ce biais ou de l’attribuer à l’éditeur.

Preuves : I-1 : chaque avis d’une plateforme non relevée en entier est représenté par sa note globale avec un poids fixe 0,5. ; Ce traitement n’utilise ni profil ni date ; le poids correspond à celui d’un avis de trois ans. ; I-1 est étiqueté non_documente, mais comporte également un champ documented_by.

Incertitude : Le nombre de plateformes et d’avis soumis à cette règle, leurs agences et leur effet propre ne sont pas fournis.

### A-7 · Les statuts globaux de conformité documentaire sont trop catégoriques

Catégorie : methode · nature : fait_verifie · gravité : majeur · concerne l’éditeur : oui

Le paquet ne distingue pas assez clairement les écarts historiques résolus des écarts encore présents. Il serait excessif de qualifier toutes les variantes de corrections nécessaires ; il serait tout aussi excessif d’accepter sans réserve le statut de cohérence totale. La variante d’ensemble touche environ 46,5 % des rangs, sans changer la composition du top 10.

Preuves : statuts : texte_documentation = complete ; texte_coherence = aucune_contradiction_repertoriee. ; La liste des règles contient pourtant des éléments étiquetés non_documente, contradiction et ambiguite, notamment I-4, I-6, I-7 et I-11. ; Variante d’ensemble : 359 notes et 254 rangs changés ; Gestion Cassini 131 vers 129 ; ImmoVendu 12 vers 13.

Incertitude : La rubrique d’effets vise le texte initial et plusieurs champs documented_by peuvent refléter des corrections ultérieures.

### A-8 · L’ancienneté d’enseigne ne peut pas être comparée équitablement entre concurrentes

Catégorie : anciennete · nature : fait_verifie · gravité : majeur · concerne l’éditeur : oui

La création de la société et celle de l’enseigne ne mesurent pas la même chose. Le dispositif ne permet pas de savoir si certaines concurrentes récentes bénéficient d’une société ancienne. Cette lacune ne démontre pas un avantage indu d’ImmoVendu : son exception va au contraire dans un sens défavorable.

Preuves : V-10b : année de lancement d’enseigne relevée pour une seule agence sur 546, ImmoVendu, en 2024. ; V-10 : 43 groupes de sociétés partagées sont recensés. ; V-10f : Gestion Cassini utilise 1995-05-02 ; ImmoVendu 2024-05-01 pour le même SIREN.

Incertitude : Aucune date d’enseigne concurrente n’est disponible pour rechercher des cas comparables.

### A-9 · La classification des avis et des critères ne peut pas être validée sur les données primaires

Catégorie : donnees · nature : non_verifiable · gravité : majeur · concerne l’éditeur : oui

Il est impossible de contrôler les catégories vente/achat, les profils non précisés, les problèmes signalés ou les erreurs de lecture de l’IA. La reproductibilité d’un calcul sur des catégories publiées ne valide pas ces catégories. Les barèmes fournis permettent néanmoins de relever l’incohérence particulière décrite en A-2.

Preuves : statuts.donnees_primaires = non_verifiees. ; echantillon = null. ; I-9 : le critère des problèmes signalés repose sur les textes lus par l’IA. ; Les textes individuels d’avis ne figurent pas dans le paquet.

Incertitude : Aucun taux d’erreur de classification ne peut être estimé.

### A-10 · Les positions sont sensibles aux choix de pondération, sans faveur uniforme à l’éditeur

Catégorie : biais · nature : fait_verifie · gravité : majeur · concerne l’éditeur : oui

Les rangs ne doivent pas être présentés comme indépendants des préférences méthodologiques. ImmoVendu profite relativement de davantage de poids aux avis et à l’information, mais souffre de davantage de poids à la confiance et à l’ancienneté. Gestion Cassini bénéficie de l’ancienneté. Ces effets opposés ne soutiennent pas une faveur systématique à toutes les agences de l’éditeur.

Preuves : Sans ancienneté : 537 rangs changés, déplacement médian 13, maximum 49 ; Gestion Cassini 131 vers 150 ; ImmoVendu 12 vers 6. ; avis_plus20 : 492 rangs changés ; ImmoVendu 12 vers 10 ; avis_moins20 : ImmoVendu vers 16. ; conf_plus20 : ImmoVendu 12 vers 16 ; conf_moins20 : vers 9. ; info_plus20 : Gestion Cassini 131 vers 128 et ImmoVendu 12 vers 10.

Incertitude : Ces scénarios sont fournis, non réexécutés ; ils ne déterminent pas une pondération objectivement correcte.

### A-11 · Le scénario d’ancienneté depuis l’enseigne est difficile à réconcilier avec la règle publiée

Catégorie : calcul · nature : calcul_reproduit · gravité : mineur · concerne l’éditeur : oui

Avec juin 2024 comme date de remplacement et novembre 2026 comme mois de calcul, l’ancienneté serait de 29 mois, soit 12,1 points après arrondi. À autres piliers inchangés, la note serait 87,56, non 87,67. Le résultat annoncé doit donc être expliqué par les paramètres exacts du scénario ; son gain de rang ne peut être retenu comme vérifié.

Preuves : Date effective actuelle : 2024-05-01 ; ancienneté actuelle 12,5 ; note 87,58. ; I-10 : lorsque seul l’an est connu, juin est utilisé ; enseigne_depuis = 2024. ; publisher_specific.anciennete_depuis_enseigne : note 87,67 et rang 11.

Incertitude : La date effectivement injectée dans le scénario et son code ne sont pas fournis.

### A-12 · Arrondis : la note de classement n’est pas une note non arrondie

Catégorie : calcul · nature : fait_verifie · gravité : mineur · concerne l’éditeur : oui

La formulation peut laisser croire à un classement sur une précision supérieure à celle réellement utilisée. L’effet est faible par agence mais non nul, y compris à la frontière du top 10. Les deux rangs de l’éditeur restent inchangés dans ce test.

Preuves : I-7 : sous-critères et piliers arrondis au dixième, puis note au centième. ; Citation : « Les agences sont rangées selon leur note exacte. » ; Variante sans arrondis intermédiaires : 353 notes et 78 rangs changés, déplacement maximal 2 ; 9 membres du top 10 conservés.

Incertitude : Le sens donné à « exacte » dans la page complète n’est pas disponible ; le paquet contient aussi une mention explicite de l’arrondi au centième.

### A-13 · Des notes inférieures à 1/5 sont effectivement comptées

Catégorie : donnees · nature : fait_verifie · gravité : mineur · concerne l’éditeur : non

Ces valeurs peuvent être légitimes sur une échelle commençant à zéro ou révéler une conversion incorrecte. Leur prise en compte peut peser sur les concurrentes concernées. Il ne faut ni les corriger automatiquement à 1 ni les traiter comme des erreurs établies sans vérifier la source.

Preuves : V-4b : 19 avis sous 1/5, dont 9 comptés. ; Le contrôle demande de vérifier l’échelle d’Opinion System.

Incertitude : L’échelle originale et les neuf enregistrements comptés ne sont pas fournis.

### A-14 · Avis partagés et doublons : conformité procédurale non équivalente à validation du contenu

Catégorie : donnees · nature : non_verifiable · gravité : mineur · concerne l’éditeur : oui

Le résultat V-14 constitue un élément favorable à la reproductibilité de la procédure, pas une validation indépendante de chaque doublon. Les seuils peuvent produire de faux rapprochements ou manquer des doublons. Les 186 écarts de partage ne démontrent pas à eux seuls un mauvais comptage, puisque leur détection dépend de textes absents des exports.

Preuves : V-6 : 834 avis déclarés doublons ; Gestion Cassini 0, ImmoVendu 21. ; V-7 : 186 cas d’écart entre le partage déclaré et la présence dans les fiches exportées ; les deux agences de l’éditeur figurent dans la liste. ; V-14 : aucune différence annoncée lors du dédoublonnage refait. ; I-13 décrit des seuils lexicaux, une règle de rapprochement sans texte et une priorité Opinion System, Immodvisor, puis Google.

Incertitude : Les textes nécessaires pour vérifier les rapprochements ne sont pas dans le paquet.

### A-15 · Les réponses aux avis négatifs sont évaluées sur un sous-ensemble observé

Catégorie : methode · nature : fait_verifie · gravité : mineur · concerne l’éditeur : non

Un taux de réponse calculé sur les seuls cas documentés peut différer du taux réel si les cas manquants ne sont pas aléatoires. Il faut publier le nombre de cas observés et manquants. Rien ne permet ici d’attribuer ce risque plus particulièrement à l’éditeur.

Preuves : I-8 : seuls les avis Google de vente ou achat à trois étoiles ou moins sont retenus. ; Les doublons sont compris. ; Seuls les avis dont la présence ou l’absence de réponse a été relevée entrent dans le calcul.

Incertitude : Les taux de couverture par agence et les effets sur les notes ne sont pas fournis.

### A-16 · Les comparaisons de groupes montrent des associations, pas des effets causaux

Catégorie : biais · nature : fait_verifie · gravité : mineur · concerne l’éditeur : oui

Le classement est associé au volume d’avis, à l’appartenance à un réseau et à la présence numérique. Cela peut refléter les critères retenus, des ressources différentes ou des différences de service. L’écart de 19,73 points entre l’éditeur et l’ensemble ne prouve pas un favoritisme. L’absence des voisines annoncées empêche une comparaison locale plus pertinente ; le champ not_testable vide ne rend pas cette comparaison disponible.

Preuves : Grand volume d’avis : note moyenne 72,66 ; petit volume : 48,05, soit 24,61 points d’écart. ; Réseaux : 72,38 ; indépendantes : 59,75, soit 12,63 points d’écart. ; Avec estimation en ligne : 69,15 ; sans : 53,95, soit 15,20 points d’écart. ; Éditeur : n = 2, moyenne 81,05 ; toutes agences : 61,32 ; voisines_editeur : n = 0.

Incertitude : Les groupes ne sont pas appariés et leurs facteurs explicatifs se recouvrent ; les données individuelles ne sont pas fournies.

### A-17 · La référence « moyenne de Nice » dépend d’un périmètre et d’une moyenne spécifiques

Catégorie : methode · nature : fait_verifie · gravité : mineur · concerne l’éditeur : non

Cette référence n’est ni une moyenne de tous les avis ni nécessairement celle des seules 546 agences classées. Les petites et grandes agences y ont le même poids au stade décrit. Ce choix peut être défendable, mais doit être explicite ; la valeur 4,453 ne peut pas être recalculée ici.

Preuves : I-2 : moyenne simple des notes moyennes par agence dans agregats-plateformes.csv, agences classées ou non. ; Valeur de référence : 4,453 ; règle mentionnant le 15/11/2026, relevé général daté du 17/11/2026.

Incertitude : Le fichier de calcul et la liste des agences hors classement ne sont pas fournis.

### A-18 · Le départage des égalités utilise des avis hors du périmètre transactionnel

Catégorie : methode · nature : fait_verifie · gravité : mineur · concerne l’éditeur : oui

Un volume hors vente et achat peut influencer un classement présenté comme transactionnel, mais seulement à égalité au centième. L’effet observé est faible. L’auditeur utilise un identifiant stable en dernier recours, contrairement à l’ordre interne de production ; aucune divergence de rang n’est néanmoins annoncée dans le contrôle global.

Preuves : I-11 : départage par tous les avis des plateformes, locataires, bailleurs et syndic compris, puis ordre interne. ; Variante limitée aux avis vente/achat : aucune note changée, 4 rangs changés d’une place. ; Les deux agences de l’éditeur et le top 10 restent inchangés.

Incertitude : Les agences effectivement départagées ne sont pas identifiées.

### A-19 · Une ancienneté absente est remplacée par un équivalent de dix ans

Catégorie : anciennete · nature : calcul_reproduit · gravité : mineur · concerne l’éditeur : non

La valeur 50 correspond à dix ans et apporte 2,50 points de note. Par rapport à l’ancienneté réelle sur l’échelle 0–100, elle peut créer un avantage ou un désavantage allant jusqu’à 2,50 points. Elle est neutre au milieu de l’échelle, pas nécessairement par rapport à la population, dont l’ancienneté moyenne publiée vaut 68,6.

Preuves : V-10d : 15 dates de société absentes, remplacées par 50 points. ; Pilier ancienneté : poids 5 %, progression de 0 à 100 sur vingt ans.

Incertitude : Les dates réelles sont inconnues ; aucun effet de rang spécifique n’est fourni.

### A-20 · Les écarts de nombres d’avis restent dans la tolérance annoncée

Catégorie : donnees · nature : fait_verifie · gravité : info · concerne l’éditeur : non

Il n’y a pas de contradiction entre les 11 écarts exacts et le contrôle de tolérance favorable. L’écart le plus visible cité, 11 avis chez Orpi Agerim, représente environ 8,7 % des 126 déclarés. Les causes, notamment le décalage de collecte, ne sont pas établies.

Preuves : V-12a : 11 plateformes présentent un écart, généralement d’un avis. ; Winter Google : 438 relevés contre 437 déclarés. ; Orpi Agerim Google : 115 relevés contre 126 déclarés. ; V-12 : aucun dépassement de la tolérance de 10 % ou deux avis sur 525 plateformes relevées en entier.

Incertitude : Les deux nombres comparés viennent des exports du site, pas d’une vérification indépendante des plateformes.

### A-21 · Les dates du registre concordent et l’exception ImmoVendu est défavorable

Catégorie : anciennete · nature : calcul_reproduit · gravité : info · concerne l’éditeur : oui

Il n’existe pas d’écart de création de société à expliquer dans les deux lignes du registre. L’écart porte sur la date choisie pour noter ImmoVendu. Par rapport à l’application de l’ancienneté de la société, l’exception retire 87,5 points de pilier, soit 4,375 points de note avant arrondi. Sans cette exception et à autres piliers inchangés, ImmoVendu aurait 91,96. Le rang correspondant n’est pas connu.

Preuves : registre_entreprises : date publiée et date du registre identiques, 1995-05-02, pour les deux fiches du SIREN 400877866. ; Ancienneté notée : Gestion Cassini 100 ; ImmoVendu 12,5. ; V-10e : exception_editeur_depot_de_marque ; V-10f : date effective ImmoVendu 2024-05-01.

Incertitude : La réponse API et son empreinte sont rapportées dans le paquet sans nouvelle interrogation ; la preuve du dépôt de marque n’est pas fournie.

### A-22 · Les deux notes de l’éditeur sont reproduites ; les autres contrôles favorables restent rapportés

Catégorie : calcul · nature : calcul_reproduit · gravité : info · concerne l’éditeur : oui

Les deux notes disponibles sont arithmétiquement cohérentes avec les piliers et poids annoncés. Les contrôles historiques ne signalent ni apparition rétrodatée, ni disparition, ni modification d’avis, ni retrait d’agence entre les deux relevés considérés. Ces éléments sont favorables, mais ne prouvent ni l’exactitude initiale des données ni la qualité des classifications.

Preuves : Somme des poids : 43 + 16 + 17 + 11 + 8 + 5 = 100 ; somme des critères : 3 + 2 + 4 + 7 + 5 + 1 = 22. ; Gestion Cassini : 76,7×0,43 + 69,6×0,16 + 70×0,17 + 50×0,11 + 100×0,08 + 100×0,05 = 74,517, soit 74,52. ; ImmoVendu : 94,6×0,43 + 88,3×0,16 + 100×0,17 + 65×0,11 + 100×0,08 + 12,5×0,05 = 87,581, soit 87,58. ; Rapport fourni : 546 notes conformes, aucune divergence de rang ni frontière d’arrondi ; V-13a, V-13b, V-13d et V-13e sans anomalie.

Incertitude : Les 544 autres lignes et les fichiers historiques ne sont pas fournis ; leur conformité ne peut pas être réexécutée dans cet audit.

## Points favorables au classement

- Les deux notes de l’éditeur sont reproduites exactement après arrondi ; les poids totalisent 100 % et les critères 22.
- Le rapport déterministe annonce 546 notes et tous les rangs conformes, sans cas frontière d’arrondi.
- L’exception d’ancienneté d’ImmoVendu est défavorable de 4,375 points avant arrondi par rapport à l’âge de la société.
- Les tests ne montrent pas d’avantage uniforme à l’éditeur : davantage de confiance ou d’ancienneté pénalise ImmoVendu, et supprimer l’ancienneté pénalise Gestion Cassini.
- Les contrôles fournis ne signalent pas de modification historique suspecte ; les écarts de nombres d’avis restent dans la tolérance annoncée.
- La variante cumulée du texte initial conserve les dix membres du top 10.

## Points défavorables au classement

- L’éditeur est également l’exploitant de deux agences classées, sans garanties d’indépendance vérifiables dans le paquet.
- Une formulation identique sur le payeur reçoit 0/30 et 30/30 : l’écart représente 5,10 points de note et n’est pas justifié par les textes fournis.
- Les avis au profil non précisé représentent 55,2 % des avis comptés ; leur exclusion modifie 526 rangs.
- Les règles de régularité, d’agrégation et de traitement des données manquantes créent des évaluations différentes selon la disponibilité des données.
- Le statut documentaire global favorable est difficile à concilier avec la coexistence d’écarts historiques, de formulations contradictoires et de champs signalant des corrections.
- Les données primaires, les dates d’enseigne concurrentes et les comparaisons avec les voisines de l’éditeur manquent.

## Instructions suspectes repérées dans les données


## Limites

- Audit limité au paquet fourni, sans navigation ni consultation indépendante des sites, plateformes, registres ou fichiers de calcul.
- Les recalculs directs concernent les deux agences disposant de leurs six piliers ; les résultats sur 546 agences et les scénarios sont des résultats rapportés, non réexécutés.
- La méthode publique intégrale et son historique versionné ne sont pas fournis : certains écarts peuvent avoir été résolus sans que le paquet le distingue clairement.
- Les textes individuels d’avis, leurs classifications et un échantillon de contrôle sont absents ; aucun taux d’erreur ne peut être estimé.
- Le texte du barème ImmoVendu est signalé comme tronqué ; les confirmations portent sur les passages visibles et ne constituent pas un avis de conformité juridique.
- Les résultats contrefactuels décrivent des sensibilités, pas des corrections nécessairement préférables ; leurs effets ne sont pas additionnables.
- Aucun nouveau rang n’est déduit d’une correction de note sans disposer des autres notes individuelles.
- Aucune preuve suffisante ne permet de conclure à une manipulation intentionnelle.
