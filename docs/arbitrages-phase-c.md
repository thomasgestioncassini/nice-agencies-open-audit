# Arbitrages de la phase C (17 novembre 2026)

Ce document répond, point par point, aux constats que les deux IA n'ont pas confirmés ensemble ou qu'elles ont
renvoyés à un contrôle humain, et aux quatre priorités de la revue de ChatGPT sur la phase C.

**Qui arbitre.** Les décisions ci-dessous sont prises par SARL GESTION CASSINI, éditrice du classement et exploitante
de deux agences classées (Gestion Cassini et ImmoVendu). Elle est donc partie intéressée : ces arbitrages ne valent pas
validation indépendante. Les constats des IA restent publiés tels quels dans les rapports ; rien n'y est modifié ni
retiré. Aucun consensus entre les deux IA n'a été recherché.

Rapports concernés : `reports/2026-11-15_20261117T105659Z` (premier audit complet),
`reports/2026-11-17_20261117T121921Z` (audit du relevé v5.2) et `reports/2026-11-17_20261117T150158Z` (audit du
relevé final du 17/11 : v5.4 et barèmes relus).

## Priorités de la revue ChatGPT

### Priorité 1 — Erreurs de notation des honoraires

| Point | Décision | Preuve | Effet |
| --- | --- | --- | --- |
| Formule « vendeur ou acquéreur selon le mandat » notée tantôt 0, tantôt 30 | Règle précisée pour toutes les agences : la formule remplit le critère « payeur indiqué » (méthode v5.2) | 179 barèmes relus ; chaque décision archivée avec la phrase citée (`data/rectifications/payeur-2026-11-17.json` du site) | 38 agences gagnent le critère, dont ImmoVendu (2ᵉ → 1ʳᵉ) ; Gestion Cassini inchangée sur ce critère |
| Gestion Cassini : 50 points de barème non visibles dans le texte de la page | Points maintenus | Le barème était publié en images (lues par la relecture d'images commune à toutes les agences). La page a été republiée en texte le 17/11 : taux TTC par type de bien et minimums. L'observation d'origine (12/11, images) ne peut pas être reprouvée en texte | Aucun |
| Gestion Cassini : la page republiée le 17/11 indique désormais le payeur avec la même phrase qu'ImmoVendu, mais garde 0/30 (relevé du 12/11, relu le 17/11 au matin avant la republication) ; constat jugé le plus grave par l'IA B dans l'audit `2026-11-17_20261117T150158Z` | Pas d'application immédiate, décidée par l'éditeur alors que la méthode permet à toute agence de demander une relecture de son site : l'éditeur renonce à cette faculté pour sa propre agence le jour de l'audit | Dates de lecture publiées (`criteres-sites.csv`) | Critère gagné à la prochaine lecture trimestrielle, comme pour toute agence ; environ +5,1 points, environ 68ᵉ au lieu de 129ᵉ |
| French Riviera Studios : 0/20 en « Montants TTC » malgré des taux TTC affichés | Erreur corrigée par la relecture commune ci-dessous | Constat confirmé par l'IA A ; barème relu le 17/11 | Montants TTC 20/20 ; 353ᵉ → 318ᵉ |
| 72 barèmes « illisibles » (20/100) dont John Royce et LBI, alors qu'un barème de même type a été lu pour Gestion Cassini | Relecture, avec une seule règle, des 61 barèmes illisibles dont l'adresse est connue et de celui de French Riviera Studios (les 11 autres n'ont pas d'adresse de barème enregistrée) | Règle : si la relecture lit un barème de vente, la grille relue remplace l'ancienne ; sinon rien ne change. Journal : `data/rectifications/baremes-2026-11-17.json` du site | 4 barèmes deviennent lisibles (Nice Carré d'Or 315ᵉ → 154ᵉ, Immobilière Prestige 273ᵉ → 150ᵉ, PHT Real Estate 371ᵉ → 284ᵉ, French Riviera Studios) ; 58 restent illisibles, dont John Royce et LBI, sans perte ; aucune baisse ; agences de l'éditeur inchangées |

### Priorité 2 — Ancienneté d'ImmoVendu

Décision (méthode v5.2) : l'ancienneté reste comptée depuis la création de la société, pour toutes les agences. Motif
publié : la société est l'entité responsable (carte professionnelle, garantie, assurance). Conséquence assumée et
publiée : ImmoVendu, enseigne lancée en 2024 par une société créée en 1995, hérite de l'ancienneté de la société. Le
scénario « ancienneté depuis l'enseigne » est publié à chaque audit comme simulation (ImmoVendu 3ᵉ au lieu de 1ʳᵉ).
Limite connue (V-10b) : la date de lancement d'enseigne n'est relevée que pour ImmoVendu ; la même simulation ne peut pas
être faite pour les autres agences.

### Priorité 3 — Périmètre et critère presque inapplicable

- Périmètre (méthode v5.3) : sont retirés les établissements dont l'activité présentée au client n'est pas la vente pour
  le compte de propriétaires : 4 chasseurs immobiliers, 1 marchand de biens, 1 site d'annonces entre particuliers,
  2 bailleurs sociaux, 1 espace de vente de promoteur. Le code d'activité au registre ne suffit pas : 6 agences
  enregistrées comme marchands de biens restent classées, leur site montrant qu'elles vendent pour des propriétaires.
  Repérage publié (`data/perimetre/` sur la branche `perimetre` du site). Effet : Gestion Cassini 131ᵉ → 129ᵉ ;
  ImmoVendu inchangée.
- Critère « annonce publiée depuis moins de 30 jours » : retiré (v5.3). Il n'était mesurable que pour 2 agences sur 528.
  Effet : 2 notes modifiées, aucune pour les agences de l'éditeur.

### Priorité 4 — Preuves à la source et tests de biais

- Extraits courts et datés des barèmes, lecture des PDF : en place depuis le 17/11 (`auditor/sitecheck.py`).
- Dédoublonnage des avis : refait par l'auditeur avec sa propre implémentation (V-14, règle I-13) sur le paquet de
  données anonymisées publié par le site. Résultat au relevé v5.4 : conforme pour les 463 agences ayant des avis relevés
  un par un. La règle, absente du texte, y est décrite depuis la v5.4.
- Catégories ajoutées aux tests de biais : réseau / indépendante (liste de l'auditeur fixée avant résultats,
  `config/networks.json`), vente seule / mixte (colonne `activites` publiée depuis la v5.4), estimation en ligne.
- Avis sans profil précisé : aucun n'est exclu ; ils font 55 % des avis comptés. Leur retrait est publié comme simulation.
- Métadonnées des fournisseurs (identifiant de réponse, motif d'arrêt) : archivées depuis le 17/11.

## Constats renvoyés à un contrôle humain

| Constat | Arbitrage |
| --- | --- |
| B-1 (premier audit) · Six barèmes notés en contradiction avec le texte relu | Voir priorité 1 : deux erreurs confirmées et corrigées (ImmoVendu payeur en v5.2 ; French Riviera Studios TTC) ; les autres cas dépendaient d'images ou de PDF : relecture commune des barèmes illisibles. John Royce et LBI restent illisibles pour l'outil : l'écart de traitement avec Gestion Cassini n'est donc pas résolu, et reste ouvert |
| B-4 (premier audit) et B-6 (second) · Biais lié au volume d'avis | Pas de décision à ce jour. L'IA A conteste le caractère causal ; l'association reste publiée dans chaque rapport. Constat ouvert |
| B-6 (premier audit) et B-7 (second) · Critère « annonce de moins de 30 jours » | Critère retiré (v5.3) |
| B-8 (premier audit) · Erreurs de périmètre | Règle de périmètre fixée et appliquée (v5.3) |
| B-1 (second audit) · 70 points d'honoraires de Gestion Cassini | Voir priorité 1 : points maintenus, barème en images puis republié en texte |
| B-4 (second audit) · Redistribution de la régularité manquante (I-6) | Pas de changement. Règle décrite dans le texte depuis la v5.1 ; l'IA A conteste le constat. Son effet reste publié (variante I-6) |
| B-4 (audit final) · Écarts entre le texte et le code (359 notes, 282 rangs) | Pas de changement. Ces chiffres mesurent l'effet des règles par rapport au texte INITIAL de la méthode ; le texte actuel les décrit toutes (statut « texte : règles décrites = oui »). L'IA A le conteste pour cette raison. Les écarts passés restent publiés |
| B-6 (audit final) · Biais liés au volume d'avis, aux réseaux et aux outils numériques | Pas de décision à ce jour. Écarts descriptifs exacts (+24,7, +12,9, +15,4 points), non ajustés ; l'IA A conteste leur lecture causale. Constat ouvert |
| B-8 (audit final) · Payeur de Gestion Cassini 0/30 pour la phrase notée 30/30 chez ImmoVendu | Voir priorité 1 : écart dû à la date de lecture (12/11 contre republication du 17/11) ; l'éditeur n'utilise pas la relecture sur demande pour sa propre agence. Sur « barème complet », l'IA A juge qu'un taux unique avec minimum couvre tous les prix |

## Autres constats confirmés par les deux IA

| Constat | Suite |
| --- | --- |
| A-5 / B-3 · Points modifiés sans nouvelle date de lecture (38 agences) | Corrigé : date et adresse de la relecture publiées critère par critère ; V-13c n'a plus d'écart |
| A-10 / B-12 · Dédoublonnage non vérifiable | Corrigé : contrôle V-14 |
| A-11 / B-10 · Mentions légales d'ImmoVendu incohérentes (forme sociale, numéro RCS, validité de carte) alors que le pilier vaut 100 | Signalé à l'éditeur pour correction de son site. Question de méthode ouverte : le critère compte la présence des mentions, pas leur exactitude |
| A-9 / B-13 · 19 avis notés sous 1/5 | Ouvert : échelle d'Opinion System à vérifier à la source |
