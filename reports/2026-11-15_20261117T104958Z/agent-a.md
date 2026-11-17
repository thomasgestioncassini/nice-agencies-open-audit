# Analyse initiale — IA A

Fournisseur : openai · modèle : gpt-6.1-sol · statut : **ok**
Empreinte du mandat : 82e0fec40442f9e2ab530af39492ad0a83e777c1e424867598daa9a65e8089c8 · empreinte de l’entrée : a50d17bc2bfe97c426c880115a7b811908ab3f6883d2cbf5afa6624296efcd9b
Coût : 0.24 $ (68189 jetons lus, 10364 écrits)

> Texte produit par l’IA, publié sans aucune modification ni relecture de l’éditeur.

## Résumé

Le paquet étaye une bonne cohérence arithmétique, mais pas une validation des données primaires ni de l'équité globale du classement. Les notes des deux agences de l'éditeur sont recalculées correctement ; le contrôle fourni annonce 552 notes et rangs conformes. Les principales réserves portent sur le conflit d'intérêts, l'avantage procuré par l'ancienneté juridique à une enseigne récente, les traitements hétérogènes des informations manquantes et plusieurs classifications à revoir. Des éléments contredisent néanmoins une hypothèse de favoritisme systématique : ImmoVendu semble privé à tort de 30 points d'honoraires, Gestion Cassini est classée 124e et les deux agences ont des honoraires moins bien notés que leurs voisines. Aucune manipulation intentionnelle n'est démontrée. Les conclusions restent limitées aux extraits, contrôles et simulations fournis.

## Constats

### A-1 · Conflit d'intérêts structurel entre l'éditeur et deux agences évaluées

Catégorie : conflit_interets · nature : fait_verifie · gravité : majeur · concerne l’éditeur : oui

La société éditrice évalue ses propres activités et leurs concurrentes. Ce cumul impose une transparence renforcée, une traçabilité des classifications et une vérification indépendante des données. Il constitue un risque d'impartialité, non une preuve de manipulation.

Preuves : classement.editeur : SARL GESTION CASSINI ; classement.agences_editeur : gestion-cassini et immovendu ; agences_editeur : même SIREN 400877866 ; rangs 124 et 2

Incertitude : Le paquet ne permet pas d'évaluer la visibilité de cette relation pour le lecteur ni l'existence d'une validation extérieure effective.

### A-2 · L'ancienneté juridique avantage fortement ImmoVendu sans mesurer son âge d'enseigne

Catégorie : anciennete · nature : fait_verifie · gravité : majeur · concerne l’éditeur : oui

Le scénario fourni chiffre un avantage de 4,29 points et 11 places pour ImmoVendu par rapport à un calcul depuis le lancement de l'enseigne. La date juridique n'est pas fausse : elle correspond à la société exploitante. La règle bénéficie aussi à des groupes concurrents et ne constitue donc pas une exception démontrée en faveur de l'éditeur. Il faut distinguer explicitement ancienneté de société, d'établissement et d'enseigne.

Preuves : immovendu.sources : date_creation_societe=1995-05-02 ; enseigne_depuis=2024 ; anc=100 ; tests_biais.publisher_specific.anciennete_depuis_enseigne : ImmoVendu 90,66 à 86,37 ; rang 2 à 13 ; V-10 : 43 groupes de même SIREN ; V-10b : date d'enseigne connue pour 1 agence sur 552

Incertitude : La date d'enseigne n'est connue qu'à l'année et le contrefactuel ne peut pas être appliqué équitablement aux concurrentes faute de données.

### A-3 · Les données primaires et les classifications d'avis ne sont pas certifiées

Catégorie : donnees · nature : non_verifiable · gravité : majeur · concerne l’éditeur : oui

La reproduction d'une note ne garantit ni l'exhaustivité des avis ni la justesse des profils, doublons, problèmes signalés ou partages entre agences. V-7 est un signal à examiner, pas la preuve que 182 partages sont erronés : les avis peuvent être reconnus par leur texte sans être présents sur toutes les fiches exportées. Les mêmes vérifications sont nécessaires pour l'éditeur et les concurrentes.

Preuves : resultats_deterministes.statuts.donnees_primaires : non_verifiees ; V-6 : 833 avis déclarés doublons ; textes non publiés ; ImmoVendu=20 et Gestion Cassini=0 ; V-7 : 182 discordances de partage ; les deux agences de l'éditeur sont concernées ; tests_biais.not_testable : part des avis exclus pour profil non identifié indisponible

Incertitude : Les textes d'avis et les décisions individuelles de classification ne figurent pas dans le paquet.

### A-4 · Les traitements de données manquantes rendent les notes partiellement non comparables

Catégorie : methode · nature : fait_verifie · gravité : majeur · concerne l’éditeur : oui

Une information non relevée peut conduire à une moyenne globale, une redistribution, une valeur de 50 ou une pénalité de 20. Ces conventions ne représentent pas le même niveau de performance ou d'incertitude. Le recours à des agrégats sans profil peut aussi réintroduire des avis hors vente et achat. Une analyse séparant performance observée et couverture documentaire est nécessaire.

Preuves : I-1 : plateforme incomplète intégrée par note globale, poids individuel fixe de 0,5, sans profil ni date ; I-6 : absence de relevé individuel entraînant redistribution des 15 % de régularité ; V-10d : ancienneté absente remplacée par 50 pour 14 agences ; baremes_relus : barème illisible fixé à 20/100 pour John Royce, LBI et Leggett ; effet_des_regles_vs_texte_initial.I-6 : 22 notes et 255 rangs changés ; déplacement maximal 37

Incertitude : La répartition complète des cas manquants et les effets isolés de chaque traitement ne sont pas fournis.

### A-5 · Le diagnostic documentaire global est en tension avec l'inventaire détaillé

Catégorie : methode · nature : fait_verifie · gravité : majeur · concerne l’éditeur : oui

Les étiquettes globales de conformité ne suffisent pas à trancher les contradictions citées. Il faut rattacher chaque citation et correction à une version du texte et du calcul. Les simulations concernent explicitement le texte initial : elles ne prouvent pas que tous ces écarts subsistent dans la documentation actuelle. L'ambiguïté I-6 porte sur un sous-critère et non sur un pilier entier.

Preuves : statuts : texte_documentation=complete ; texte_coherence=aucune_contradiction_repertoriee ; texte_historique=ecarts_anterieurs ; I-4 : « un même avis publié sur plusieurs plateformes ne compte qu'une fois » alors que la régularité compte les doublons ; I-7 : « rangées selon leur note exacte » alors que le classement utilise une note arrondie au centième ; effet_des_regles_vs_texte_initial.ensemble : 362 notes et 289 rangs changés ; déplacement maximal 37 ; 8 membres du top 10 conservés

Incertitude : Le texte public intégral et ses versions datées ne sont pas fournis ; certains champs documented_by suggèrent des précisions ou corrections déjà apportées.

### A-6 · Présence probable d'acteurs ou de spécialités insuffisamment comparables

Catégorie : donnees · nature : hypothese · gravité : majeur · concerne l’éditeur : non

Un marchand de biens opérant pour son compte, un chasseur, une agence résidentielle et un spécialiste des fonds de commerce ne répondent pas nécessairement aux mêmes besoins. L'absence d'un barème d'intermédiation peut être non applicable plutôt qu'une mauvaise transparence. Il faut vérifier l'éligibilité et segmenter les métiers avant de confirmer leur comparaison dans un classement unique.

Preuves : BS Invest : titre « Marchand de biens sur la Côte d'Azur » ; description d'achats et rénovations pour son groupe ; Cabinet Grimaz : « spécialisée en immobilier commercial et d'entreprise » ; Artemiz : chasseur immobilier et honoraires de recherche ; WIS : activités patrimoniales, immobilières et numériques ; PAP : page en échec, sans texte exploitable

Incertitude : Les activités juridiques exactes, cartes professionnelles et règles d'inclusion ne sont pas fournies. Le seul identifiant de PAP ne suffit pas à établir son activité.

### A-7 · Association forte entre volume d'avis et note globale

Catégorie : biais · nature : fait_verifie · gravité : majeur · concerne l’éditeur : oui

L'écart de note globale entre les tiers extrêmes atteint 24,03 points. La méthode peut favoriser les acteurs établis ou disposant d'une collecte d'avis plus importante. Ce résultat n'établit pas un effet causal du seul volume, puisque les autres piliers diffèrent aussi.

Preuves : Poids du pilier Avis : 43 % ; Groupes de 184 agences : petit volume note=47,96 ; volume moyen=62,62 ; grand volume=71,99 ; Pilier Avis : 50,6 pour petit volume contre 81,6 pour grand volume ; Les grands volumes ont aussi une ancienneté moyenne de 75,7 contre 62,9 pour les petits volumes

Incertitude : Ces comparaisons descriptives ne contrôlent ni la qualité réelle, ni l'âge, ni la spécialité. Les groupes de volume des deux agences de l'éditeur ne sont pas indiqués.

### A-8 · Le critère de fraîcheur des annonces est presque toujours non applicable

Catégorie : methode · nature : fait_verifie · gravité : majeur · concerne l’éditeur : oui

Le critère est inapplicable dans 99,62 % des cas contrôlés et applicable à seulement deux agences. L'affichage de 23 critères surestime donc la couverture effective de cette dimension. Il faut préciser son dénominateur, la règle de retrait et le poids effectif des autres critères.

Preuves : V-9 : « Annonce publiée depuis moins de 30 jours » non applicable pour 524 agences sur 526 ; Les deux agences de l'éditeur : regles_valeurs_absentes=criteres_non_applicables:1 ; Méthode : 23 critères au total

Incertitude : Le paquet ne rattache pas explicitement le critère non applicable de chaque agence de l'éditeur à celui de V-9 et n'explique pas les 26 agences hors du dénominateur de 526.

### A-9 · Le zéro au critère du payeur d'ImmoVendu est contredit par le texte fourni

Catégorie : honoraires · nature : calcul_reproduit · gravité : majeur · concerne l’éditeur : oui

D'après le texte fourni, les critères Barème publié 30/30, Montants TTC 20/20 et Barème complet 20/20 sont confirmés ; Payeur indiqué 0/30 est contredit. La même formulation conditionnelle est acceptée chez une concurrente. Une correction isolée à 100/100 ajouterait 5,10 points à la note : 95,76 après arrondi. Le rang corrigé ne peut pas être calculé sans les autres notes. Cette erreur apparente désavantage l'éditeur.

Preuves : ImmoVendu : « Honoraires à la charge du VENDEUR ou de l’ACQUEREUR en fonction du mandat de vente » ; points payeur=0/30 ; Cabinet Immobilier Nice : « vendeur ou de l'acquéreur, selon les conditions du mandat » ; points payeur=30/30 ; ImmoVendu : barème publié=30 ; TTC=20 ; complet=20 ; pilier Honoraires=70 ; Poids Honoraires : 17 %

Incertitude : La relecture date du 17 novembre et la notation du 12 novembre ; aucune archive du texte au jour de la notation n'est fournie.

### A-10 · French Riviera Studios : présence explicite de TTC malgré un zéro publié

Catégorie : honoraires · nature : fait_verifie · gravité : mineur · concerne l’éditeur : non

Barème publié 30/30, Payeur indiqué 30/30 et Complet 20/20 sont confirmés pour la vente à taux uniforme. TTC 0/20 est contredit si le critère mesure l'affichage de montants TTC. Le texte contient toutefois des conversions incohérentes : avec une TVA de 20 %, 5 % HT donne 6 % TTC et 3 % HT donne 3,6 % TTC, non 7 % et 5 %. Il faut distinguer présence du TTC et exactitude du calcul. Accorder les 20 points ajouterait 3,40 points à la note globale.

Preuves : Points publiés : Barème=30 ; TTC=0 ; Payeur=30 ; Complet=20 ; Texte : « 5% HT [...] soit 7% TTC » et honoraires « à la charge du vendeur » ; Texte : recherche « 3% HT [...] soit 5 % TTC [...] TVA [...] à 20% »

Incertitude : La définition détaillée du critère TTC n'est pas jointe : présence de la mention ou exactitude des conversions. Dates de notation et relecture différentes.

### A-11 · Des extractions pauvres ne permettent pas de confirmer les barèmes, y compris chez l'éditeur

Catégorie : honoraires · nature : non_verifiable · gravité : mineur · concerne l’éditeur : oui

Gestion Cassini : TTC 20/20 confirmé quant à la mention de TVA ; Barème publié 30/30, Payeur 0/30 et Complet 20/20 impossibles à juger. Cap Sud, Étude Lotte et Immo Terrasse : chacun des quatre critères est impossible à juger sur le seul texte fourni. Les liens ou titres ne suffisent pas à valider le contenu du document. Il serait inéquitable de transformer ces lacunes d'extraction en erreurs certaines pour les seules agences de l'éditeur.

Preuves : Gestion Cassini : texte « Honoraires TVA incluse au taux de 20 % », sans taux ni tranches ; points 30/20/0/20 ; Cap Sud : texte « Tarifs », sans barème lisible ; points 30/20/30/20 ; Étude Lotte : « Télécharger nos honoraires » ; points 30/20/0/20 ; Immo Terrasse : « Ouvrir le PDF dans un nouvel onglet » ; points 30/20/30/20

Incertitude : Images, documents intégrés et PDF liés ne sont pas restitués dans le texte. L'absence dans l'extraction ne prouve pas l'absence sur la page.

### A-12 · Plusieurs barèmes textuels confirment les notes, avec quelques limites d'interprétation

Catégorie : honoraires · nature : fait_verifie · gravité : mineur · concerne l’éditeur : non

Riviera Real Estate, Hestia, Cabinet Immobilier Nice et Richer : les quatre critères publiés sont confirmés pour le périmètre de transaction décrit. Chez Cabinet Immobilier Nice, le payeur est confirmé comme pouvant être vendeur ou acquéreur selon mandat, sans identifier un payeur unique pour toutes les ventes. Artemiz : Barème 30/30, TTC 20/20 et Complet 20/20 confirmés ; Payeur 30/30 impossible à confirmer strictement faute de désignation explicite de la personne redevable. Une règle identique sur l'explicitation du payeur doit être appliquée à tous.

Preuves : Riviera Real Estate : taux de vente TTC, minimum de 6 000 €, aucun payeur explicite pour la vente ; points 30/20/0/20 ; Hestia : taux 6 % jusqu'à 1 000 000 €, 5 % au-delà, TTC à la charge du vendeur ; points 30/20/30/20 ; Cabinet Immobilier Nice : tranches jusqu'à 100 000 €, 200 000 €, 1 000 000 € et au-delà ; points 30/20/30/20 ; Richer : quatre tranches continues de vente, TTC, pas de payeur explicite de vente ; points 30/20/0/20 ; Artemiz : grille de 7 500 € à 2,30 %, titre Honoraires TTC ; points 30/20/30/20

Incertitude : Pour Artemiz, le payeur est déduit de la relation de chasse pour l'acquéreur plutôt que nommé explicitement. Le périmètre retenu est celui de la vente ou recherche, pas celui de la location.

### A-13 · Des bornes de prix fragilisent les points accordés pour la complétude

Catégorie : honoraires · nature : fait_verifie · gravité : mineur · concerne l’éditeur : non

Agence du Port et Tosca : Barème 30/30, TTC 20/20 et Payeur 0/30 confirmés dans les textes de vente ; Complet 20/20 contredit par les bornes littérales, notamment 100 000 € et 100 001 € chez Tosca. Maison Quatre : Barème 30/30, TTC 0/20 et Payeur 0/30 confirmés pour la vente ; Complet 20/20 contredit littéralement à 500 001 €. Les mentions TTC et locataire de location ne corrigent pas ces absences en vente. Resid'Immo : Barème 30/30, TTC 0/20 et Payeur 0/30 confirmés pour la vente ; Complet 20/20 impossible à confirmer à cause de la première tranche ambiguë, avec en outre une lacune littérale à 250 001 €. Une vérification visuelle doit précéder toute correction définitive.

Preuves : Agence du Port : dernière tranche « Supérieur à 500 001 € » après une tranche finissant à 500 000 € ; Tosca : « inférieurs à 100 000€ » puis « supérieurs à 100 001€ » ; Maison Quatre : dernière tranche « > 500 001 € » après 500 000 € ; Resid'Immo : première ligne « 70 000 € 12 % » sans borne basse ; dernière tranche « > 250 001 € »

Incertitude : Des symboles ou éléments de mise en page peuvent avoir été perdus dans l'extraction. Les conventions sur les prix avec centimes ne sont pas définies.

### A-14 · Les zéros tirés de pages d'accueil ne prouvent pas une absence sur tout le site

Catégorie : honoraires · nature : non_verifiable · gravité : mineur · concerne l’éditeur : non

Agence Californie, BS Invest et Cabinet Grimaz : chacun des quatre zéros est impossible à juger globalement à partir d'une page tronquée. Alliance Riviera et WIS : les quatre zéros sont compatibles avec l'absence de ces informations sur la page fournie, mais impossibles à confirmer à l'échelle de tout le site. PAP : les quatre critères sont impossibles à juger ; un échec HTTP ne confirme aucun zéro. L'applicabilité du barème à BS Invest doit d'abord être vérifiée.

Preuves : Les six agences ont quatre critères à zéro ; Agence Californie, BS Invest et Cabinet Grimaz : text_truncated=true ; Alliance Riviera : site en cours de refonte, texte sans barème ; WIS : page d'accueil sans grille tarifaire ; PAP : status=echec ; error=HTTPError

Incertitude : Aucune exploration exhaustive du site ou archive du 12 novembre n'est fournie.

### A-15 · Les PDF non lus ou mal décodés ne permettent pas de contrôler les critères d'honoraires

Catégorie : honoraires · nature : non_verifiable · gravité : mineur · concerne l’éditeur : non

Pour chacune des quatorze agences listées, chacun des quatre critères publiés — Barème publié, Montants TTC, Payeur indiqué et Barème complet — est impossible à juger d'après le contenu fourni. Cela vaut aussi bien pour les points positifs que pour les zéros, notamment ceux de Maison K. Le statut technique « lu » ne signifie pas que le document a été compris.

Preuves : Douze entrées baremes_relus portent status=pdf_non_lu ; Maison K : status=lu mais texte commençant par %PDF-1.3, suivi de flux compressés ; Vizcaya : status=lu mais texte commençant par %PDF-1.4, suivi de structures PDF et flux compressés

Incertitude : Les documents ne sont pas disponibles sous une forme textuelle ou visuelle exploitable dans le paquet.

### A-16 · Le forfait de 20 pour barème illisible mesure une limite d'outil plutôt que la transparence réelle

Catégorie : honoraires · nature : non_verifiable · gravité : mineur · concerne l’éditeur : non

Le forfait publié de 20/100 est impossible à valider comme appréciation de la transparence. Aucun des quatre critères usuels ne peut être jugé individuellement sur ces extraits, et leurs points ne sont pas publiés séparément pour ces agences. L'écart entre 20 et 100 représente 13,60 points de note globale ; ce chiffre mesure une amplitude possible, pas une correction justifiée.

Preuves : Les trois agences : « Barème trouvé mais illisible par notre outil : 20 sur 100 (valeur fixe) » ; John Royce et LBI : texte sans grille tarifaire ; Leggett : extrait tronqué avant la section Honoraires

Incertitude : Ni le document tarifaire ni son rendu visuel ne sont fournis.

### A-17 · La valeur dite neutre d'ancienneté n'est pas neutre pour chaque agence

Catégorie : anciennete · nature : calcul_reproduit · gravité : mineur · concerne l’éditeur : non

La valeur 50 apporte 2,50 points à la note, équivalant à une société de dix ans dans une échelle linéaire sur vingt ans. Elle avantage une société réellement plus jeune et désavantage une société plus ancienne, jusqu'à 2,50 points de note dans chaque sens. Les 14 cas représentent 2,54 % des 552 agences. L'absence de SIREN pour Riviera Real Estate et Alliance Riviera ne démontre pas une erreur de date.

Preuves : V-10d : 14 dates absentes remplacées par 50 ; Poids Ancienneté : 5 % ; Groupes de sociétés : 164 de moins de 10 ans et 374 de 10 ans ou plus, soit 538 dates disponibles

Incertitude : L'ancienneté réelle des 14 agences n'est pas connue.

### A-18 · Les conventions d'agrégation et de périmètre doivent être explicitées et testées

Catégorie : methode · nature : fait_verifie · gravité : mineur · concerne l’éditeur : oui

La « moyenne de Nice » donne le même poids à chaque agence, pas à chaque avis, et dépend d'un univers plus large que les 552 classées. Le taux de réponse porte sur un sous-échantillon observé ; il ne décrit pas nécessairement tous les avis négatifs. Le départage utilise des activités hors du périmètre vente/achat. L'ordre interne n'est pas identique au dernier recours par identifiant stable utilisé par l'auditeur, même si aucun écart de rang n'est annoncé dans cette exécution.

Preuves : I-2 : moyenne simple des moyennes d'agences, classées ou non ; M_REF=4,453 ; I-8 : réponses aux seuls avis Google vente/achat à trois étoiles ou moins, doublons compris et réponse relevée ; I-11 : départage par tous les avis, locataires, bailleurs et syndic compris ; puis ordre interne ; I-11 : variante vente/achat change 6 rangs, aucune note, sans effet sur les rangs de l'éditeur

Incertitude : Le texte public intégral n'est pas fourni ; certains éléments peuvent avoir été documentés depuis les écarts initiaux.

### A-19 · Des notes d'avis inférieures à une étoile appellent une validation de l'échelle

Catégorie : donnees · nature : fait_verifie · gravité : mineur · concerne l’éditeur : non

Dix-neuf valeurs sont signalées, dont neuf comptées. Elles pourraient provenir d'une échelle valide incluant zéro ou d'une conversion incorrecte. Il ne faut ni les accepter sans vérification ni les remonter arbitrairement à une étoile. L'incidence sur le classement reste inconnue.

Preuves : V-4b : count=19 ; counted=9 ; dix agences listées ; V-4b : valeurs sous 1/5 intégrées telles quelles ; échelle Opinion System à vérifier

Incertitude : Les valeurs individuelles, l'échelle source et leur effet sur les scores ne sont pas fournis.

### A-20 · Les écarts de compteurs d'avis sont réels mais compatibles avec le contrôle tolérant

Catégorie : donnees · nature : fait_verifie · gravité : mineur · concerne l’éditeur : non

Le contrôle exact et le contrôle avec tolérance ne se contredisent pas. L'écart maximal est de quatre avis, soit environ 4,7 % des 85 annoncés. Des décalages de collecte peuvent l'expliquer, sans que cela soit établi. Aucun impact de note n'est quantifié.

Preuves : V-12a : huit plateformes avec différence de compteur ; Century 21 à Cimiez Lafage Google : 89 relevés contre 85 déclarés ; Les sept autres différences de V-12a sont d'un avis ; V-12 : aucun écart au-delà du seuil toléré sur 532 plateformes entièrement relevées

Incertitude : Les dates exactes des deux compteurs et les données des plateformes sources ne sont pas jointes.

### A-21 · Les avantages de l'éditeur sont contrebalancés par des désavantages mesurables

Catégorie : biais · nature : calcul_reproduit · gravité : info · concerne l’éditeur : oui

Face aux voisines, l'écart d'honoraires coûte environ 2,65 points de note moyenne à l'éditeur ; l'information et l'ancienneté lui apportent environ 1,10 et 1,26 point. Le solde de tous les piliers est proche des 2,45 points de note moyenne observés. Face à l'ensemble, les honoraires de l'éditeur sont au contraire supérieurs de 20,3 points de pilier. Le référentiel de comparaison change donc sensiblement l'interprétation.

Preuves : Groupes éditeur/voisines : Honoraires 70 contre 85,6 ; Information 100 contre 86,2 ; Ancienneté 100 contre 74,9 ; Autres écarts de piliers éditeur/voisines : Avis +1,2 ; Service +4,3 ; Confiance +13,8 ; Notes moyennes : éditeur=82,59 ; voisines=80,14 ; toutes=60,86 ; Gestion Cassini : Confiance=50 ; ImmoVendu=100

Incertitude : Les moyennes de piliers sont arrondies, les deux agences de l'éditeur sont très différentes et les voisines sont sélectionnées par leur rang.

### A-22 · ImmoVendu reste deuxième sous les variations modérées de poids, mais pas sans ancienneté

Catégorie : biais · nature : fait_verifie · gravité : info · concerne l’éditeur : oui

Le rang élevé d'ImmoVendu ne dépend pas d'un réglage très fin des poids testés. En revanche, le choix même d'inclure l'ancienneté bénéficie aux deux agences : sans elle, elles perdent respectivement quatre et vingt places. Les nombreuses permutations générales montrent une sensibilité des rangs fins, sans établir un favoritisme ciblé.

Preuves : Douze scénarios de variation de poids de plus ou moins 20 % : ImmoVendu reste rang 2 ; Gestion Cassini : rangs 119 à 130 dans ces douze scénarios ; Sans ancienneté : ImmoVendu rang 6 et Gestion Cassini rang 144 ; 546 rangs changés ; déplacement médian 13 ; Variantes I-4/I-6/I-7/I-11 réunies : ImmoVendu rang 2 ; Gestion Cassini rang 123

Incertitude : Les sorties de simulations sont fournies, mais les matrices complètes et scripts exécutables ne le sont pas. La suppression d'un pilier n'est pas équivalente à sa variation modérée.

### A-23 · Les dates du registre concordent, sans certifier l'histoire des enseignes

Catégorie : anciennete · nature : fait_verifie · gravité : info · concerne l’éditeur : oui

Aucun écart entre date publiée et date du registre n'est signalé dans les 146 comparaisons, soit 26,45 % des 552 agences, avec plusieurs lignes correspondant à une même société. Les écarts avec les récits commerciaux peuvent refléter une reprise, une histoire familiale ou une enseigne antérieure : ils ne démontrent pas une fausse date juridique. Les récits de longévité des concurrentes doivent être traités avec les mêmes exigences de preuve que celui d'ImmoVendu.

Preuves : registre_entreprises.counts : 146 conformes ; 2 SIREN non publiés ; Gestion Cassini et ImmoVendu : dates publiée et registre identiques, 1995-05-02 ; Agence Californie : registre 1989 ; site évoquant un héritage familial depuis 1956 ; Cabinet Grimaz : registre 1992 ; site évoquant 1960 ; Richer : registre 2013 ; site évoquant 1976

Incertitude : Les réponses API originales ne sont pas incluses et les URL et empreintes ne constituent pas une consultation indépendante. Les continuités d'activité ou reprises ne sont pas documentées.

### A-24 · Les deux notes de l'éditeur sont arithmétiquement reproduites

Catégorie : calcul · nature : calcul_reproduit · gravité : info · concerne l’éditeur : oui

Les poids et les notes détaillées disponibles sont cohérents. Les nombres de critères totalisent également 23. La conformité déterministe générale annoncée est un argument favorable, mais ne valide ni les observations initiales ni les choix normatifs du classement.

Preuves : Poids : 43+16+17+11+8+5=100 ; Gestion Cassini : 76,7×0,43+69,6×0,16+70×0,17+50×0,11+100×0,08+100×0,05=74,517, arrondi à 74,52 ; ImmoVendu : 94,5×0,43+88,3×0,16+70×0,17+100×0,11+100×0,08+100×0,05=90,663, arrondi à 90,66 ; recalcul fourni : 552 notes conformes ; 0 divergente ; 0 rang divergent ; 0 frontière d'arrondi

Incertitude : Seules les deux sommes pondérées sont directement reproduites ici. Les 552 notes, sous-critères et rangs ne peuvent pas être recalculés indépendamment sans la base complète.

### A-25 · Traçabilité et contrôles historiques favorables, mais portée limitée

Catégorie : methode · nature : declaration_site · gravité : info · concerne l’éditeur : oui

L'engagement d'un instantané, la graine publique, les empreintes et l'inclusion de concurrentes sont des éléments favorables à la reproductibilité. Le sous-ensemble élargi n'est toutefois pas un échantillon aléatoire simple : on ne peut pas extrapoler un taux d'erreur global à partir de ses relectures. L'absence de changements détectés contredit une hypothèse d'altérations entre ces deux relevés seulement ; elle ne certifie pas les périodes antérieures.

Preuves : echantillon : committed_snapshot=2026-11-15_121239 ; seed, round drand et URL d'engagement publiés ; echantillon : bls_reverified=true ; bls_signature_verified_at_draw=true ; Échantillon mêlant tirage aléatoire, voisines, ancienneté comparable et agences de l'éditeur ; V-13a, V-13b et V-13d : aucun ajout ancien, aucune disparition et aucune modification détectés entre les relevés

Incertitude : La signature, l'antériorité de l'engagement et le tirage ne sont pas vérifiés extérieurement ici. La période historique contrôlée et sa couverture ne sont pas précisées.

## Points favorables au classement

- Les deux notes détaillées de l'éditeur sont reproduites exactement après arrondi ; le contrôle fourni annonce la conformité des 552 notes et rangs.
- Les 146 comparaisons de dates juridiques fournies concordent avec les données du registre rapportées.
- ImmoVendu reste deuxième dans les douze variations modérées de poids et dans la combinaison des variantes de règles documentaires.
- Plusieurs barèmes concurrents confirment les points publiés ; aucune indulgence systématique envers l'éditeur n'est démontrée.
- Le zéro du payeur d'ImmoVendu paraît au contraire le désavantager de 5,10 points de note globale.
- Les honoraires des deux agences de l'éditeur sont moins bien notés que ceux de leurs voisines ; Gestion Cassini n'occupe que le rang 124.
- Le paquet présente des mécanismes de traçabilité et aucun changement d'avis n'est détecté dans la comparaison historique fournie.

## Points défavorables au classement

- L'éditeur évalue ses deux propres agences et leurs concurrentes, sans validation extérieure démontrée des données primaires.
- L'ancienneté de société attribue le maximum à ImmoVendu malgré une enseigne lancée en 2024 ; le scénario spécifique change son rang de 2 à 13.
- Les informations manquantes sont traitées selon des conventions hétérogènes, susceptibles de déplacer sensiblement les rangs.
- Les classifications de profils, doublons et partages ne sont pas auditables à partir des seuls exports fournis.
- Des critères d'honoraires paraissent mal classés ou insuffisamment justifiés, et plusieurs documents n'ont pas été effectivement lus.
- Le volume d'avis est fortement associé à la note, tandis que les métiers et modèles d'activité ne sont pas suffisamment segmentés.
- Le critère de fraîcheur des annonces est presque partout non applicable.
- Les statuts synthétiques de conformité documentaire ne sont pas suffisamment réconciliés avec les écarts détaillés et leurs versions.

## Instructions suspectes repérées dans les données


## Limites

- Audit limité au paquet : aucune consultation indépendante des sites, du registre, des plateformes d'avis, du dépôt ou du service drand n'a été effectuée.
- Les résultats de contrôle et contrefactuels fournis ont été examinés comme données ; ils ne sont pas assimilés à une exécution indépendante.
- La base complète des 552 agences, les avis textuels, les décisions individuelles de classification et le texte public intégral versionné sont absents.
- Les barèmes ont été notés le 12 novembre et relus le 17 novembre 2026 : un changement intervenu entre les deux dates peut expliquer certaines différences.
- Les extractions textuelles peuvent omettre images, tableaux, documents intégrés ou symboles ; un contenu absent d'un extrait n'est pas nécessairement absent du site.
- Les dates du registre concernent les sociétés, pas les enseignes ; l'ancienneté d'enseigne n'est disponible que pour ImmoVendu.
- Les comparaisons de groupes sont descriptives et ne prouvent pas de causalité ; les voisines sont sélectionnées à partir du classement lui-même.
- Les effets de corrections isolées ne doivent pas être additionnés mécaniquement ; aucun rang corrigé d'honoraires ne peut être établi sans toutes les notes.
- Les textes légaux et commerciaux cités ne prouvent ni l'exactitude juridique de leurs affirmations ni la validité actuelle des autorisations professionnelles.
- Aucune instruction d'audit suspecte n'a été identifiée ; les invitations commerciales et commandes ordinaires d'interface ne sont pas traitées comme des consignes adressées à l'auditeur.
