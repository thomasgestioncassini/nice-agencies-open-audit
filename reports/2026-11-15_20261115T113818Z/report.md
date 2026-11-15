# Rapport d’audit 2026-11-15_20261115T113818Z

Classement audité : https://meilleure-agence-nice.fr · relevé du 2026-11-15 · méthode v5 du 14/11/2026
Exécuté le 2026-11-15T11:38:18+00:00 (UTC) · code de l’auditeur 9d96f53bbb497047297fa20b39e6a71a6b87ffa0

> Ce dispositif est administré par SARL GESTION CASSINI, éditrice du classement et exploitante de deux agences classées. Il n’est pas une certification indépendante. Voir GOVERNANCE.md.

## Statuts

- **Exactitude des calculs** : CONFORME — toutes les notes, tous les piliers et tous les rangs recalculés sont identiques aux valeurs publiées
- **Vérification des données primaires** : NON VÉRIFIÉES — les données d’entrée (avis, pages des sites, registre) n’ont pas été recontrôlées à leur source
- **Analyse des biais** : NON ÉVALUÉ — aucune analyse de biais n’a été menée dans ce rapport

## Exactitude des calculs

- Agences examinées : 552
- Notes conformes : 552 · divergentes : 0 · à une frontière d’arrondi : 0
- Rangs divergents : 0
- Moyenne de Nice recalculée : 4.453
- Valeurs anormales listées dans anomalies.json : 0

Le recalcul utilise les données élémentaires publiées, jamais les notes finales. Il prouve que l’arithmétique du site est conforme à ses règles ; il ne prouve pas que ces données sont exactes.

## Contrôles de cohérence des données publiées

- [mineur] V-4b · avis notés sous 1/5, minimum habituel d’une échelle à étoiles : ils entrent tels quels dans la moyenne ; échelle d’Opinion System à vérifier à la source (19)
- [info] V-6 · avis déclarés doublons par le site (non vérifiable à partir des exports : les textes ne sont pas publiés) (833)
- [mineur] V-7 · avis déclarés partagés entre k agences, mais présents sur un autre nombre de fiches dans l’export (le partage est détecté sur le texte, que l’export ne contient pas) (182)
- [majeur] V-9 · critère « Annonce publiée depuis moins de 30 jours » non applicable pour 524 agences sur 526 : la méthode le compte parmi les 23 critères, mais il ne pèse presque nulle part (524)
- [mineur] V-11 · sources-agences.csv absent : identifiants stables, dates d’observation et URL des preuves indisponibles pour ce relevé
- [info] I-6 · agences dont la régularité est retirée et son poids redistribué (règle I-6) (22)

## Règles appliquées par le site mais absentes du texte de la méthode

Le texte public ne suffisait pas à reproduire les notes. Ces règles ont été établies en lisant le code publié par le site (docs/interpretations.md) :

- I-1 · Plateformes non relevées avis par avis
- I-2 · Moyenne de Nice
- I-3 · Fenêtre de la régularité
- I-4 · Dénominateur de la régularité — **écart avec le texte publié**
- I-5 · Âge d'un avis
- I-6 · Régularité non vérifiable — **écart avec le texte publié**
- I-7 · Arrondis — **écart avec le texte publié**
- I-8 · Réponses aux avis négatifs
- I-9 · Problèmes signalés
- I-10 · Ancienneté
- I-11 · Départage des égalités — **écart avec le texte publié**
- I-12 · Ordre des opérations de l'ancienneté

## Agences retenues pour les contrôles à la source (phase C)

Graine : fdc0fe70d95c9c89ac443a94520a578964fd34ae0892828db5cee06a2111d83a · règle 1.0

- editeur : 2
- tirage_aleatoire : 20
- voisine_de_gestion-cassini : 10
- voisine_de_immovendu : 6

## Limites

- Le recalcul reprend tels quels les résultats d’étapes que les exports ne permettent pas de refaire : profil de l’auteur et problème signalé (lus par une IA du site), détection des doublons et des avis partagés (faite sur les textes, non publiés), points attribués en lisant les sites des agences, date de création des sociétés.
- Les données primaires (avis sur les plateformes, pages des sites, registre des entreprises) ne sont pas recontrôlées à leur source dans ce rapport.
- Le moteur a été écrit par Claude (Anthropic), qui a aussi écrit le code de production du site. Il a été rédigé à partir du texte de la méthode, puis complété en lisant le code publié (docs/interpretations.md). Un tiers peut écrire et exécuter son propre moteur à partir des mêmes fichiers archivés.
- Le dépôt, ses workflows et son financement sont contrôlés par SARL GESTION CASSINI (GOVERNANCE.md).
