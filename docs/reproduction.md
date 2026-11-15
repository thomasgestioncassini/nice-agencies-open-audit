# Reproduire un audit

1. Cloner le dépôt (Python 3.10+ suffit, aucune installation).
2. `python3 -m auditor verify reports/<id>` : vérifie que le rapport et le relevé archivé n'ont pas été modifiés (empreintes SHA-256 du manifeste).
3. `python3 -m auditor run snapshots/<date>` : restaure le relevé, vérifie chaque empreinte, recalcule les 23 critères, les 6 piliers, les notes et les rangs, puis compare avec les valeurs publiées.
4. Comparer `report.json` et `calculations.csv` avec ceux du rapport publié : seuls l'identifiant, l'heure d'exécution et la version du code peuvent différer.

Pour écrire votre propre moteur, partez des fichiers de `snapshots/<date>/` (décompressés avec `gunzip`) et du texte de la méthode ; les règles que ce texte ne précise pas sont listées dans [interpretations.md](interpretations.md).

Les étapes que les exports ne permettent pas de refaire (lecture des textes d'avis, détection des doublons, lecture des sites, registre des entreprises) sont reprises telles quelles : elles relèvent de la dimension « données primaires ».
