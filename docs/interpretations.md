# Règles appliquées par le site et absentes du texte de la méthode

Le moteur de l'auditeur a d'abord été écrit à partir du seul texte public de la méthode (version 5 du 14/11/2026). Ce texte ne suffisait pas : premier essai, 552 notes sur 552 différentes. Les règles ci-dessous ont alors été établies en lisant le code publié par le site (/methode/reproduction/code/), sans le copier ni l'importer. Après leur ajout, le recalcul retrouve exactement les valeurs publiées.

Le moteur a donc été ajusté pour reproduire le calcul du site : la reproduction conforme ne vaut pas conformité au texte. Pour cette raison, chaque rapport publie deux statuts de calcul séparés (reproduction, conformité au texte) et mesure l'effet de chaque contradiction ou ambiguïté en recalculant le classement selon la lecture littérale du texte.

Classement des règles :

- **contradiction** : le site fait autre chose que ce que le texte affirme ;
- **texte ambigu** : le texte admet plusieurs lectures et le site en applique une ;
- **règle absente du texte** : le texte ne dit rien d'une règle qui change les notes ;
- **précision d'implémentation** : détail technique compatible avec le texte.

L'auditeur ne tranche pas et ne modifie aucune règle du classement.

## I-1 · Plateformes non relevées avis par avis — règle absente du texte

- Règle appliquée par le site : Quand une plateforme n'a pas été relevée en entier, ses avis comptent par sa note globale, chacun avec le poids fixe 0,5 (celui d'un avis de 3 ans), sans profil ni date.
- Texte : Le texte ne décrit pas ce cas.
- Source : avis.py : score(), AGG_AGE

## I-2 · Moyenne de Nice — règle absente du texte

- Règle appliquée par le site : Moyenne simple, sur toutes les agences listées dans agregats-plateformes.csv (classées ou non), de la note moyenne de chaque agence ; arrondie au millième (4,453 au 15/11/2026).
- Texte : Le texte dit seulement « la moyenne de Nice ».
- Source : build.py : _avis.M_REF

## I-3 · Fenêtre de la régularité — précision d'implémentation

- Règle appliquée par le site : Les 12 derniers mois calendaires, mois du relevé compris.
- Texte : Le texte dit « les 12 derniers mois ».
- Source : avis.py : months_back()

## I-4 · Dénominateur de la régularité — contradiction avec le texte

- Règle appliquée par le site : Nombre de mois actifs divisé par le nombre d'avis de vente ou d'achat des 12 derniers mois, borné entre 3 et 12. Ce nombre compte les doublons entre plateformes et les plateformes incomplètes.
- Texte : « Doublons retirés : un même avis publié sur plusieurs plateformes ne compte qu'une fois. » (section 3, règles de comptage du pilier Avis)
- Commentaire : Le texte annonce que les doublons sont retirés ; ils ne le sont pas pour ce sous-critère.
- Lecture littérale testée par l'auditeur : régularité calculée sur les avis retenus, doublons retirés
- Source : avis.py : score(), variable rec

## I-5 · Âge d'un avis — précision d'implémentation

- Règle appliquée par le site : Âge en mois de 30,44 jours ; le poids est divisé par deux tous les 36 mois, de façon continue.
- Texte : Le texte dit « il perd la moitié de son poids après 3 ans », sans préciser la forme continue.
- Source : avis.py : age_weight()

## I-6 · Régularité non vérifiable — texte ambigu

- Règle appliquée par le site : Si aucun avis n'a été relevé un par un, la régularité est retirée et son poids (15 %) est réparti sur la qualité et le volume.
- Texte : « Il n'y a plus de redistribution du poids d'un pilier manquant. » (section 10) — le texte parle d'un pilier ; ici, c'est un sous-critère.
- Commentaire : Le texte affirme qu'« il n'y a plus de redistribution du poids d'un pilier manquant » ; ici c'est un sous-critère dont le poids est redistribué.
- Lecture littérale testée par l'auditeur : régularité non relevée = valeur neutre 50, sans redistribution
- Source : avis.py : score(), variable total

## I-7 · Arrondis — contradiction avec le texte

- Règle appliquée par le site : Chaque sous-critère et chaque pilier sont arrondis au dixième ; la note est calculée à partir des piliers arrondis, puis arrondie au centième.
- Texte : « Les agences sont rangées selon leur note exacte. » (section 9)
- Commentaire : Le texte dit que les agences sont « rangées selon leur note exacte » : la note qui sert au rang est en réalité arrondie au centième.
- Lecture littérale testée par l'auditeur : aucun arrondi intermédiaire ; rang selon la note non arrondie
- Source : build.py : r['t'] ; avis.py, service.py : round(…, 1)

## I-8 · Réponses aux avis négatifs — règle absente du texte

- Règle appliquée par le site : Avis Google de vente ou d'achat à 3 étoiles ou moins, doublons compris, dont la présence ou l'absence de réponse a été relevée.
- Texte : Le texte ne précise ni le périmètre exact ni le traitement des avis dont la réponse n'est pas relevée.
- Source : service.py : reply_part()

## I-9 · Problèmes signalés — précision d'implémentation

- Règle appliquée par le site : Part des avis uniques (doublons retirés) dont le texte a été lu par l'IA.
- Texte : Conforme au texte.
- Source : service.py : text_part()

## I-10 · Ancienneté — règle absente du texte

- Règle appliquée par le site : Années et mois écoulés depuis la date de création (le jour est ignoré ; juin si le mois est inconnu), divisés par 20, × 100, arrondis au dixième.
- Texte : Le texte dit « de 0 à 20 ans, proportionnel ».
- Source : build.py : anc_points()

## I-11 · Départage des égalités — texte ambigu

- Règle appliquée par le site : À note égale (au centième), passe devant l'agence qui a le plus d'avis au total sur les plateformes, avis de locataires, de bailleurs et de syndic compris ; puis l'ordre interne de la base.
- Texte : « À note égale, celle qui a le plus d'avis passe devant. » (section 9) — sans dire lesquels.
- Commentaire : Le texte dit « celle qui a le plus d'avis », sans préciser lesquels. L'auditeur utilise l'identifiant stable en dernier recours.
- Lecture littérale testée par l'auditeur : départage par le nombre d'avis comptés (vente et achat)
- Source : build.py : order()

## I-12 · Ordre des opérations de l'ancienneté — précision d'implémentation

- Règle appliquée par le site : Années ÷ 20 × 100 (et non 100 × années ÷ 20) : l'ordre décide du dernier chiffre pour 2 agences dont la valeur tombe exactement sur une demi-unité d'arrondi.
- Texte : Sans effet de fond (0,1 point d'ancienneté, soit 0,005 point de note).
- Source : build.py : anc_points()

## I-13 · Reconnaissance des doublons et des avis partagés — règle absente du texte

- Règle appliquée par le site : deux avis de plateformes différentes sont un même avis s'ils comptent chacun au moins 5 mots (de plus de 2 lettres) et que leurs mots communs représentent au moins 70 % de leurs mots réunis, ou 90 % des mots du plus court ; sinon (avis sans texte), s'ils ont la même note à un demi-point près, le même prénom d'auteur, des initiales compatibles et des dates à 45 jours au plus. La copie conservée est celle d'Opinion System, puis d'Immodvisor, puis de Google. Un avis est partagé entre agences quand les 120 premiers caractères de son texte (s'il en compte au moins 60) se retrouvent sur les fiches de plusieurs agences classées.
- Texte : le retrait des doublons et le partage des avis entre agences sont annoncés (section 3), sans dire comment un doublon est reconnu.
- Contrôle : V-14 refait ce dédoublonnage avec l'implémentation de l'auditeur (auditor/dedupcheck.py), sur le paquet de données anonymisées publié par le site (texte et auteur remplacés par des empreintes salées), et compare les nombres agence par agence aux fichiers de reproduction.
- Source : avis.py : same_review(), unique_reviews(), text_key() ; build.py : SHARED

## I-14 · Méthode v6 : pilier = moyenne de ses critères pondérée par leurs poids — précision d'implémentation

- Règle appliquée par le site : pilier Avis = (30,1 × qualité + 7,6 × volume + 5,9 × régularité) ÷ 43,6 ; pilier Service = (4,8 × réponses + 15,1 × problèmes) ÷ 19,9, ou les seuls problèmes quand le critère « réponse aux avis négatifs » est retiré (relevé Google complet sans avis négatif) ; avis Google non relevés un par un : réponse = 50. Arrondi au dixième.
- Texte : le texte v6 donne le poids de chaque critère dans la note (sections 3 et 4), sans écrire la formule du pilier.
- Effet de l'ordre des opérations : calculer avec des parts arrondies au lieu des poids change le dixième d'une agence sur 545 au relevé du 17/11/2026 (frontière d'arrondi).
- Critères de maximum 0 (confidentialité, HTTPS, estimation en ligne) : affichés pour information, hors de la note ; ils ne sont pas contrôlés par V-8 ni V-13c.
- Source : avis.py : score() ; service.py (méthode v6)
