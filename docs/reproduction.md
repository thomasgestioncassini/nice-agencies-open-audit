# Reproduire un audit

1. Cloner le dépôt (Python 3.10+ suffit, aucune installation).
2. `python3 -m auditor verify reports/<id>` : vérifie que le rapport et le relevé archivé n'ont pas été modifiés (empreintes SHA-256 du manifeste).
3. `python3 -m auditor run snapshots/<date>` : restaure le relevé, vérifie chaque empreinte, recalcule les 23 critères, les 6 piliers, les notes et les rangs, puis compare avec les valeurs publiées.
4. Comparer `report.json` et `calculations.csv` avec ceux du rapport publié : seuls l'identifiant, l'heure d'exécution et la version du code peuvent différer.

Pour écrire votre propre moteur, partez des fichiers de `snapshots/<date>/` (décompressés avec `gunzip`) et du texte de la méthode ; les règles que ce texte ne précise pas sont listées dans [interpretations.md](interpretations.md).

Les étapes que les exports ne permettent pas de refaire (lecture des textes d'avis, détection des doublons, lecture des sites, registre des entreprises) sont reprises telles quelles : elles relèvent de la dimension « données primaires ».

## Tirage des agences contrôlées à la source

L'archivage fixe l'échéance du tirage : le premier 06:00 UTC qui suit (`draw_planned` dans le manifeste du relevé). La valeur aléatoire publique drand de ce tour (chaîne quicknet) est enregistrée dans `snapshots/<date>/draw.json`. Relancer l'archivage ou le tirage ne permet pas d'en obtenir une autre. Sans balise valide, aucun échantillon n'est publié.

Contrôles faits : numéro de tour, chaîne, valeur aléatoire égale au SHA-256 de la signature. Non fait à ce stade : la vérification cryptographique de la signature BLS (bibliothèque spécialisée nécessaire, prévue en phase D). Vous pouvez la faire avec le client officiel drand à partir de `draw.json`.
