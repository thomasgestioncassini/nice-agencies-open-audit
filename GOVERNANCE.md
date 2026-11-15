# Gouvernance et limites d'indépendance

**Ce dispositif n'est pas institutionnellement indépendant.** Sans tiers extérieur, SARL GESTION CASSINI, qui édite le classement et exploite deux agences classées, garde des droits administratifs sur toute l'infrastructure. Le dispositif ne peut pas l'empêcher d'intervenir : il vise à rendre toute intervention visible.

| Droit | Détenteur | Ce qui rend une intervention visible |
| --- | --- | --- |
| Propriété du dépôt, droits d'administration | compte GitHub thomasgestioncassini (gérant de SARL GESTION CASSINI) | historique Git public ; copies (forks) faites par des tiers |
| Modification du code, des workflows, du mandat et des règles (config/) | même compte | chaque modification est un commit public daté ; les rapports indiquent la version du code et des règles utilisées |
| Identité de signature (phase D) | identité de workflow GitHub, sans clé conservée (Sigstore) | journal public de transparence Rekor |
| Financement des API d'IA (phase C) | SARL GESTION CASSINI | plafonds publiés ; une coupure produit un rapport « IA indisponible » |
| Arrêt du système, retrait d'un rapport | même compte, techniquement possible | surveillance externe (phase D) ; inscriptions Rekor ; copies tierces |
| Développement | Claude (Anthropic), outil utilisé par l'éditeur, qui a aussi écrit le code de production du site | moteur rédigé à partir du texte public de la méthode ; règles tirées du code listées dans docs/interpretations.md |

Interventions techniquement possibles pour l'administrateur et non encore détectables par un tiers : supprimer des exécutions GitHub Actions (et donc des journaux d'engagement), réécrire l'historique Git, retirer un relevé archivé avant qu'un tiers en ait fait une copie. Un horodatage et une conservation hors du dépôt sont prévus en phase D.

Ce que GitHub, les empreintes, les signatures ou l'usage de deux IA **ne garantissent pas** : l'impossibilité pour l'administrateur de modifier l'infrastructure, ni la justesse des conclusions. Une signature prouve l'intégrité d'un fichier et son origine technique, rien de plus.

Amélioration possible : confier un droit d'administration ou une copie miroir à un tiers extérieur.
