# Portée et limites de l'audit

Ce document dit, dimension par dimension, ce qu'un rapport de l'auditeur permet de conclure et ce qu'il ne permet pas.
Il répond à la troisième condition de la revue de ChatGPT du 17/11/2026 : aucun contrôle partiel ne doit être présenté
comme une validation du classement.

**Règle générale.** Chaque statut vaut pour la dimension qu'il nomme, et seulement pour le relevé audité. Aucun rapport,
ni aucun ensemble de rapports, ne constitue une certification du classement. Le dispositif est administré par
l'éditeur du classement, qui exploite deux agences classées (GOVERNANCE.md).

| Dimension | Ce qu'un statut favorable établit | Ce qu'il n'établit pas |
| --- | --- | --- |
| Calculs — reproduction | Les notes et les rangs publiés découlent des données publiées, selon les règles appliquées par le site, recalculés par un moteur distinct | Que les données sont exactes ; que des données falsifiées de façon cohérente avant l'export seraient détectées |
| Texte de la méthode | Chaque règle répertoriée (docs/interpretations.md) est décrite dans le texte archivé ; aucune contradiction répertoriée n'y subsiste | Une relecture complète du texte ; l'absence de contradictions non répertoriées |
| Dédoublonnage (V-14) | Les décisions de dédoublonnage publiées se retrouvent en refaisant la règle sur les empreintes anonymisées, agence par agence | Que les empreintes correspondent aux avis réellement publiés ; une correspondance avis par avis |
| Données primaires | Pour les agences tirées au sort et celles de l'éditeur : dates de société comparées au registre national, barèmes relus à la date de l'audit | Les avis sur les plateformes ; les agences non tirées ; l'état des pages à la date du relevé initial |
| Biais | Des écarts descriptifs entre catégories (volume d'avis, réseau, activités, outils, âge de la société) et l'effet de variantes de poids ou de règles | Une discrimination causale, ou son absence ; la justesse des poids |
| Audit des deux IA | Deux analyses séparées, puis la position de chacune sur les constats de l'autre, publiées sans modification | Un consensus ; l'exactitude de chaque constat ; une expertise juridique |
| Historique (V-13) | Pas d'ajout rétrodaté, de disparition ou de modification d'avis non expliqués entre deux relevés archivés | Ce qui a pu changer avant le premier relevé archivé |
| Tirage de l'échantillon | Un tirage fixé d'avance, sur un relevé engagé avant l'échéance, avec une balise drand vérifiée | Une preuve d'engagement indépendante de GitHub, administré par l'éditeur |

## Décisions qui ne reposent que sur l'éditeur

Les arbitrages des constats contestés (docs/arbitrages-phase-c.md) sont rendus par l'éditeur. Ils ne valent pas
validation indépendante, même lorsqu'ils sont défavorables à ses agences.

## Lecture des sites par une IA

Les points relevés sur les sites des agences (honoraires, mentions légales, information) sont lus par une IA du site
audité. Deux lectures de la même page peuvent différer (docs/v13c-2026-11-17.md). L'auditeur ne refait pas ces lectures
pour toutes les agences.

## Lacunes documentaires connues

- Les journaux GitHub des exécutions 44109196708 et 44109218926 ne sont pas disponibles (erreur BlobNotFound) : ce
  sont deux contrôles d'intégration interrompus par des envois successifs, à quelques secondes d'intervalle ; les mêmes
  commits ont été contrôlés par l'exécution suivante.
- L'archivage 44079915474 a échoué pour la même raison que les contrôles d'intégration du 17/11 (rapport canari sans
  manifeste) ; il a été relancé (44081234613).
