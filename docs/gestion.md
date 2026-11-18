# Comparateur gestion locative (méthode G1.2)

Depuis le 18/11/2026, le site publie aussi un comparateur des agences de gestion locative
(https://meilleure-agence-nice.fr/gestion-locative-nice/), avec sa propre méthode (G1.2) et son propre dossier de recalcul
(`/methode/gestion-locative/reproduction/`).

## Ce que fait l'auditeur

- **Archivage** : les quatre fichiers du dossier de recalcul et la page de méthode sont archivés avec chaque relevé
  (`gestion-parametres.json`, `gestion-agences.csv`, `gestion-avis.csv`, `gestion-criteres.csv`, `gestion-methode.html`),
  avec leur empreinte SHA-256. Ils sont facultatifs : les relevés antérieurs au 18/11/2026 ne les ont pas.
- **Recalcul indépendant** : `auditor/gestion.py`, écrit à partir de la rubrique « Formules » de la page de méthode et de
  `config/methodology-gestion-g12.json`. Il recalcule la moyenne de référence, les six piliers, la note, le groupe
  (évaluée, peu évaluée, données insuffisantes) et l'ordre de chaque agence, puis les compare aux valeurs publiées
  (piliers au dixième, note au centième). Résultat : statut `calculs_gestion` du rapport (conforme ou écarts), fichier
  `gestion-calculations.csv`, colonne « Gestion locative » du registre.

## Ce qu'il ne refait pas

Comme pour le classement vente, les étapes que les exports ne permettent pas de refaire sont reprises telles quelles :
qualification des avis (bailleur ou non, niveau de preuve, arbitrages et exclusions), dédoublonnage entre plateformes,
partage d'un avis entre agences, lecture des problèmes de service, lecture des sites et des barèmes. Les textes des avis
ne sont pas publiés. Une reproduction conforme prouve que les notes publiées découlent des données publiées selon les
formules publiées ; elle ne prouve pas que ces données sont exactes.

## Limites

- L'audit mensuel par deux IA (`audit-ia.yml`) porte aussi sur le comparateur depuis le 18/11/2026 (accord de l'éditeur) : mandat v2 (`config/mandate-v2.md`, mission 8), section « comparateur_gestion » du paquet (résultats publiés, recalcul déterministe, agences évaluées, premières agences peu évaluées, agence de l'éditeur). Surcoût estimé : environ 15 000 caractères de plus par appel.
- La méthode G1.2 a été relue par ChatGPT (dossiers v2 à v11, verdict favorable du 18/11/2026) ; aucune vérification
  humaine indépendante n'a été faite (décision de l'éditeur). Le dispositif reste administré par l'éditeur.
