# Rapport d’audit 2026-11-15_20261117T160724Z

Classement audité : https://meilleure-agence-nice.fr · relevé du 2026-11-15 · méthode v5.4 du 17/11/2026 (poids et calcul de la v5 du 14/11/2026 ; 22 critères depuis la v5.3 ; texte des doublons décrit en v5.4)
Exécuté le 2026-11-17T16:07:24+00:00 (UTC) · code de l’auditeur 9d9ed61e61c5c489f8da3c13fbecc0e4d54d2f70

> Ce dispositif est administré par SARL GESTION CASSINI, éditrice du classement et exploitante de deux agences classées. Il n’est pas une certification indépendante. Voir GOVERNANCE.md.

## Statuts

- **Calculs — reproduction des notes publiées** : CONFORME
- **Texte de la méthode — règles de calcul décrites** : PARTIELLEMENT — des règles appliquées ne sont pas décrites, ou contredites, dans le texte archivé
- **Texte de la méthode — contradictions répertoriées encore présentes** : AUCUNE parmi celles répertoriées (contrôle par phrases, pas une relecture complète du texte)
- **Texte de la méthode — écarts dans les versions archivées antérieures** : OUI — le calcul appliqué contredisait ou dépassait le texte publié dans au moins une version archivée antérieure ; ces écarts restent publiés ci-dessous
- **Vérification des données primaires** : NON VÉRIFIÉES — les données d’entrée (avis, pages des sites, registre) n’ont pas été recontrôlées à leur source
- **Analyse des biais** : NON ÉVALUÉ — aucune analyse de biais n’a été menée dans ce rapport
- **Dédoublonnage des avis — refait indépendamment sur les données anonymisées** : NON VÉRIFIÉ — données anonymisées absentes de ce relevé

Une reproduction conforme prouve que les notes publiées découlent des données publiées selon les règles appliquées par le site. Elle ne prouve ni que ces règles sont celles du texte publié, ni que les données sont exactes à leur source : si des données étaient falsifiées de façon cohérente avant leur export, le recalcul resterait conforme. Seuls les contrôles à la source (phase C) et la comparaison entre relevés (V-13) peuvent le révéler.

## Exactitude des calculs

- Agences examinées : 552
- Notes conformes : 552 · divergentes : 0 · à une frontière d’arrondi : 0
- Rangs divergents : 0
- Moyenne de Nice recalculée : 4.453
- Valeurs anormales listées dans anomalies.json : 0

Le recalcul utilise les données élémentaires publiées, jamais les notes finales. Il prouve que l’arithmétique du site est conforme à ses règles ; il ne prouve pas que ces données sont exactes.

## Contrôles de cohérence des données publiées

- [mineur] V-4b · avis notés sous 1/5, minimum habituel d’une échelle à étoiles : ils entrent tels quels dans la moyenne ; échelle d’Opinion System à vérifier à la source (19)
- [info] V-12a · toutes les plateformes relevées en entier dont le nombre d’avis relevés diffère, même d’un avis, du nombre affiché (les deux nombres viennent des exports du site) (8)
- [info] V-12 · nombre d’avis relevés un par un cohérent avec le nombre affiché par la plateforme pour les 532 plateformes relevées en entier (écart toléré : 10 % ou 2 avis) (0)
- [info] V-6 · avis déclarés doublons par le site (non vérifiable à partir des exports : les textes ne sont pas publiés) (833)
- [mineur] V-7 · avis déclarés partagés entre k agences, mais présents sur un autre nombre de fiches dans l’export (le partage est détecté sur le texte, que l’export ne contient pas) (182)
- [majeur] V-9 · critère « Annonce publiée depuis moins de 30 jours » non applicable pour 524 agences sur 526 : la méthode le compte parmi les 23 critères, mais il ne pèse presque nulle part (524)
- [info] V-10 · agences exploitées par une même société (même SIREN) : même date d’ancienneté (43)
- [majeur] V-10b · date de lancement d’enseigne relevée pour seulement 1 agence(s) sur 552 : la comparaison « enseigne récente, société ancienne » ne peut pas être faite pour les concurrentes à partir des exports (1)
- [info] V-10c · ancienneté saisie à la main (rachat déclaré prouvé) (0)
- [info] V-10e · ancienneté fixée par une exception déclarée par l’éditeur (publiée dans la méthode ; à vérifier : elle doit être défavorable à l’agence concernée) (0)
- [info] V-10f · sociétés partagées dont les agences ont des dates d’ancienneté différentes (expliquées par une saisie manuelle ou une exception déclarée, sauf mention contraire) (0)
- [info] V-10d · date de création de la société non relevée (valeur neutre 50) (14)
- [info] V-13a · avis apparus depuis le relevé précédent avec une date antérieure de plus d’un mois, sur une plateforme déjà relevée en entier (0)
- [info] V-13b · avis disparus depuis le relevé précédent, chez des agences toujours classées (0)
- [info] V-13e · agences retirées du classement depuis le relevé précédent (leurs avis sortent avec elles) (0)
- [info] V-13d · avis déjà relevés dont la note, le profil, le problème signalé ou les drapeaux de comptage ont changé depuis le relevé précédent (0)
- [info] I-6 · agences dont la régularité est retirée et son poids redistribué (règle I-6) (22)

## Conformité au texte de la méthode

Le texte public ne suffisait pas à reproduire les notes. Les règles suivantes ont été établies en lisant le code publié par le site (docs/interpretations.md) :

- I-1 · Plateformes non relevées avis par avis — désormais décrite dans le texte archivé (à l’origine : règle absente du texte)
- I-2 · Moyenne de Nice — désormais décrite dans le texte archivé (à l’origine : règle absente du texte)
- I-3 · Fenêtre de la régularité — désormais décrite dans le texte archivé (à l’origine : précision d’implémentation)
- I-4 · Dénominateur de la régularité — désormais décrite dans le texte archivé (à l’origine : contradiction avec le texte)
- I-5 · Âge d'un avis — désormais décrite dans le texte archivé (à l’origine : précision d’implémentation)
- I-6 · Régularité non vérifiable — désormais décrite dans le texte archivé (à l’origine : texte ambigu)
- I-7 · Arrondis — désormais décrite dans le texte archivé (à l’origine : contradiction avec le texte)
- I-8 · Réponses aux avis négatifs — désormais décrite dans le texte archivé (à l’origine : règle absente du texte)
- I-9 · Problèmes signalés — précision d’implémentation
- I-10 · Ancienneté — désormais décrite dans le texte archivé (à l’origine : règle absente du texte)
- I-11 · Départage des égalités — désormais décrite dans le texte archivé (à l’origine : texte ambigu)
- I-12 · Ordre des opérations de l'ancienneté — précision d’implémentation
- I-13 · Reconnaissance des doublons et des avis partagés — règle absente du texte

**Écarts dans les versions antérieures du texte (conservés) :**

- relevé 2026-11-15 : contradictions I-4, I-7 ; ambiguïtés I-6, I-11

Compléter le texte après coup est une révision de la méthode publiée : elle ne rend pas conformes les relevés publiés avant elle.

Effet des règles retenues par le site par rapport à la lecture littérale du texte initial (v5 du 14/11/2026). Ce tableau reste publié même quand le texte décrit la règle : il montre ce que ce choix change (diagnostic seulement, les notes officielles ne changent pas) :

| Règle | Notes changées | Rangs changés | Déplacement max | Top 10 inchangé | ImmoVendu | Gestion Cassini |
| --- | --- | --- | --- | --- | --- | --- |
| I-4 | 8 | 49 | 17 | 8/10 | 2 → 2 | 124 → 125 |
| I-6 | 22 | 255 | 37 | 10/10 | 2 → 2 | 124 → 122 |
| I-7 | 357 | 67 | 3 | 10/10 | 2 → 2 | 124 → 124 |
| I-11 | 0 | 6 | 1 | 10/10 | 2 → 2 | 124 → 124 |
| ensemble | 362 | 289 | 37 | 8/10 | 2 → 2 | 124 → 123 |

## Agences retenues pour les contrôles à la source (phase C)

Graine : 308601a341a56c8acc947e53882a2c4defa3298d921756af1bc76af20f92432b · règle 1.0 · tour drand 34030612 (signature BLS de la balise vérifiée avec la clé publique du réseau drand)

- anciennete_comparable : 110
- editeur : 2
- tirage_aleatoire : 20
- voisine_de_gestion-cassini : 10
- voisine_de_immovendu : 6

## Limites

- Le recalcul reprend tels quels les résultats d’étapes que les exports ne permettent pas de refaire : profil de l’auteur et problème signalé (lus par une IA du site), points attribués en lisant les sites des agences, date de création des sociétés. Le dédoublonnage est refait (V-14), mais sur des empreintes produites par le site : il ne prouve pas que ces empreintes correspondent aux avis réellement publiés sur les plateformes.
- Un statut « conforme » vaut pour la dimension qu’il nomme, jamais pour le classement entier. Ce rapport n’est pas une certification du classement (docs/portee-et-limites.md).
- Les écarts entre catégories d’agences (tests de biais) sont descriptifs et non ajustés : ils ne prouvent ni une discrimination, ni son absence.
- Les arbitrages des constats contestés sont rendus par l’éditeur, partie intéressée (docs/arbitrages-phase-c.md) : ils ne valent pas validation indépendante.
- Les données primaires (avis sur les plateformes, pages des sites, registre des entreprises) ne sont pas recontrôlées à leur source dans ce rapport.
- Le moteur a été écrit par Claude (Anthropic), qui a aussi écrit le code de production du site. Il a été rédigé à partir du texte de la méthode, puis complété en lisant le code publié (docs/interpretations.md). Un tiers peut écrire et exécuter son propre moteur à partir des mêmes fichiers archivés.
- Le dépôt, ses workflows et son financement sont contrôlés par SARL GESTION CASSINI (GOVERNANCE.md).
