# Rapport d’audit 2026-11-15_20261117T093932Z

Classement audité : https://meilleure-agence-nice.fr · relevé du 2026-11-15 · méthode v5 du 14/11/2026
Exécuté le 2026-11-17T09:39:32+00:00 (UTC) · code de l’auditeur 1c903b42624dc03171b25fd57997f09807d892dd

> Ce dispositif est administré par SARL GESTION CASSINI, éditrice du classement et exploitante de deux agences classées. Il n’est pas une certification indépendante. Voir GOVERNANCE.md.

## Statuts

- **Calculs — reproduction des notes publiées** : CONFORME
- **Texte de la méthode — règles de calcul décrites** : PARTIELLEMENT — des règles appliquées ne sont pas décrites, ou contredites, dans le texte archivé
- **Texte de la méthode — contradictions répertoriées encore présentes** : OUI — le texte affirme encore une règle contraire au calcul
- **Texte de la méthode — écarts dans les versions archivées antérieures** : AUCUN dans les versions archivées antérieures
- **Vérification des données primaires** : NON VÉRIFIÉES — les données d’entrée (avis, pages des sites, registre) n’ont pas été recontrôlées à leur source
- **Analyse des biais** : NON ÉVALUÉ — aucune analyse de biais n’a été menée dans ce rapport

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
- [mineur] V-11 · sources-agences.csv absent : identifiants stables, dates d’observation et URL des preuves indisponibles pour ce relevé
- [info] I-6 · agences dont la régularité est retirée et son poids redistribué (règle I-6) (22)

## Conformité au texte de la méthode

Le texte public ne suffisait pas à reproduire les notes. Les règles suivantes ont été établies en lisant le code publié par le site (docs/interpretations.md) :

- I-1 · Plateformes non relevées avis par avis — règle absente du texte
- I-2 · Moyenne de Nice — règle absente du texte
- I-3 · Fenêtre de la régularité — précision d’implémentation
- I-4 · Dénominateur de la régularité — contradiction avec le texte
- I-5 · Âge d'un avis — précision d’implémentation
- I-6 · Régularité non vérifiable — texte ambigu
- I-7 · Arrondis — contradiction avec le texte
- I-8 · Réponses aux avis négatifs — règle absente du texte
- I-9 · Problèmes signalés — précision d’implémentation
- I-10 · Ancienneté — règle absente du texte
- I-11 · Départage des égalités — texte ambigu
- I-12 · Ordre des opérations de l'ancienneté — précision d’implémentation

Effet des règles retenues par le site par rapport à la lecture littérale du texte initial (v5 du 14/11/2026). Ce tableau reste publié même quand le texte décrit la règle : il montre ce que ce choix change (diagnostic seulement, les notes officielles ne changent pas) :

| Règle | Notes changées | Rangs changés | Déplacement max | Top 10 inchangé | ImmoVendu | Gestion Cassini |
| --- | --- | --- | --- | --- | --- | --- |
| I-4 | 8 | 49 | 17 | 8/10 | 2 → 2 | 124 → 125 |
| I-6 | 22 | 255 | 37 | 10/10 | 2 → 2 | 124 → 122 |
| I-7 | 357 | 67 | 3 | 10/10 | 2 → 2 | 124 → 124 |
| I-11 | 0 | 6 | 1 | 10/10 | 2 → 2 | 124 → 124 |
| ensemble | 362 | 289 | 37 | 8/10 | 2 → 2 | 124 → 123 |

## Agences retenues pour les contrôles à la source (phase C)

Ce relevé n’est pas celui engagé pour le tirage (relevé engagé : 2026-11-15_121239).

## Limites

- Le recalcul reprend tels quels les résultats d’étapes que les exports ne permettent pas de refaire : profil de l’auteur et problème signalé (lus par une IA du site), détection des doublons et des avis partagés (faite sur les textes, non publiés), points attribués en lisant les sites des agences, date de création des sociétés.
- Les données primaires (avis sur les plateformes, pages des sites, registre des entreprises) ne sont pas recontrôlées à leur source dans ce rapport.
- Le moteur a été écrit par Claude (Anthropic), qui a aussi écrit le code de production du site. Il a été rédigé à partir du texte de la méthode, puis complété en lisant le code publié (docs/interpretations.md). Un tiers peut écrire et exécuter son propre moteur à partir des mêmes fichiers archivés.
- Le dépôt, ses workflows et son financement sont contrôlés par SARL GESTION CASSINI (GOVERNANCE.md).
