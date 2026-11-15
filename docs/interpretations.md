# Règles appliquées par le site et absentes du texte de la méthode

Le moteur de l'auditeur a d'abord été écrit à partir du seul texte public de la méthode (version 5 du 14/11/2026). Ce texte ne suffisait pas : premier essai, 552 notes sur 552 différentes. Les règles ci-dessous ont alors été établies en lisant le code publié par le site (/methode/reproduction/code/), sans le copier ni l'importer. Après leur ajout, le recalcul retrouve exactement les valeurs publiées.

Celles marquées **écart** contredisent ou dépassent le texte publié : le site devrait soit corriger son texte, soit corriger son calcul. L'auditeur ne tranche pas et n'en modifie aucune.

## I-1 · Plateformes non relevées avis par avis

- Règle appliquée : Quand une plateforme n'a pas été relevée en entier, ses avis comptent par sa note globale, chacun avec le poids fixe 0,5 (celui d'un avis de 3 ans), sans profil ni date.
- Ce que dit le texte : Le texte ne décrit pas ce cas.
- Source : avis.py : score(), AGG_AGE

## I-2 · Moyenne de Nice

- Règle appliquée : Moyenne simple, sur toutes les agences listées dans agregats-plateformes.csv (classées ou non), de la note moyenne de chaque agence ; arrondie au millième (4,453 au 15/11/2026).
- Ce que dit le texte : Le texte dit seulement « la moyenne de Nice ».
- Source : build.py : _avis.M_REF

## I-3 · Fenêtre de la régularité

- Règle appliquée : Les 12 derniers mois calendaires, mois du relevé compris.
- Ce que dit le texte : Le texte dit « les 12 derniers mois ».
- Source : avis.py : months_back()

## I-4 · Dénominateur de la régularité — écart

- Règle appliquée : Nombre de mois actifs divisé par le nombre d'avis de vente ou d'achat des 12 derniers mois, borné entre 3 et 12. Ce nombre compte les doublons entre plateformes et les plateformes incomplètes.
- Ce que dit le texte : Le texte annonce que les doublons sont retirés ; ils ne le sont pas pour ce sous-critère.
- Source : avis.py : score(), variable rec

## I-5 · Âge d'un avis

- Règle appliquée : Âge en mois de 30,44 jours ; le poids est divisé par deux tous les 36 mois, de façon continue.
- Ce que dit le texte : Le texte dit « il perd la moitié de son poids après 3 ans », sans préciser la forme continue.
- Source : avis.py : age_weight()

## I-6 · Régularité non vérifiable — écart

- Règle appliquée : Si aucun avis n'a été relevé un par un, la régularité est retirée et son poids (15 %) est réparti sur la qualité et le volume.
- Ce que dit le texte : Le texte affirme qu'« il n'y a plus de redistribution du poids d'un pilier manquant » ; ici c'est un sous-critère dont le poids est redistribué.
- Source : avis.py : score(), variable total

## I-7 · Arrondis — écart

- Règle appliquée : Chaque sous-critère et chaque pilier sont arrondis au dixième ; la note est calculée à partir des piliers arrondis, puis arrondie au centième.
- Ce que dit le texte : Le texte dit que les agences sont « rangées selon leur note exacte » : la note qui sert au rang est en réalité arrondie au centième.
- Source : build.py : r['t'] ; avis.py, service.py : round(…, 1)

## I-8 · Réponses aux avis négatifs

- Règle appliquée : Avis Google de vente ou d'achat à 3 étoiles ou moins, doublons compris, dont la présence ou l'absence de réponse a été relevée.
- Ce que dit le texte : Le texte ne précise ni le périmètre exact ni le traitement des avis dont la réponse n'est pas relevée.
- Source : service.py : reply_part()

## I-9 · Problèmes signalés

- Règle appliquée : Part des avis uniques (doublons retirés) dont le texte a été lu par l'IA.
- Ce que dit le texte : Conforme au texte.
- Source : service.py : text_part()

## I-10 · Ancienneté

- Règle appliquée : Années et mois écoulés depuis la date de création (le jour est ignoré ; juin si le mois est inconnu), divisés par 20, × 100, arrondis au dixième.
- Ce que dit le texte : Le texte dit « de 0 à 20 ans, proportionnel ».
- Source : build.py : anc_points()

## I-11 · Départage des égalités — écart

- Règle appliquée : À note égale (au centième), passe devant l'agence qui a le plus d'avis au total sur les plateformes, avis de locataires, de bailleurs et de syndic compris ; puis l'ordre interne de la base.
- Ce que dit le texte : Le texte dit « celle qui a le plus d'avis », sans préciser lesquels. L'auditeur utilise l'identifiant stable en dernier recours.
- Source : build.py : order()

## I-12 · Ordre des opérations de l'ancienneté

- Règle appliquée : Années ÷ 20 × 100 (et non 100 × années ÷ 20) : l'ordre décide du dernier chiffre pour 2 agences dont la valeur tombe exactement sur une demi-unité d'arrondi.
- Ce que dit le texte : Sans effet de fond (0,1 point d'ancienneté, soit 0,005 point de note).
- Source : build.py : anc_points()
