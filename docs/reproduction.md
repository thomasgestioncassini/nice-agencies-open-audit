# Reproduire un audit

1. Cloner le dépôt (Python 3.10+ suffit, aucune installation).
2. `python3 -m auditor verify reports/<id>` : vérifie que le rapport et le relevé archivé n'ont pas été modifiés (empreintes SHA-256 du manifeste).
3. `python3 -m auditor run snapshots/<date>` : restaure le relevé, vérifie chaque empreinte, recalcule les 23 critères, les 6 piliers, les notes et les rangs, puis compare avec les valeurs publiées.
4. Comparer `report.json` et `calculations.csv` avec ceux du rapport publié : seuls l'identifiant, l'heure d'exécution et la version du code peuvent différer.

Pour écrire votre propre moteur, partez des fichiers de `snapshots/<date>/` (décompressés avec `gunzip`) et du texte de la méthode ; les règles que ce texte ne précise pas sont listées dans [interpretations.md](interpretations.md).

Les étapes que les exports ne permettent pas de refaire (lecture des textes d'avis, détection des doublons, lecture des sites, registre des entreprises) sont reprises telles quelles : elles relèvent de la dimension « données primaires ».

## Tirage des agences contrôlées à la source

1. **Échéance fixe par relevé**, connue d'avance : le premier mardi à 06:00 UTC après la date du relevé (`draw_planned` dans le manifeste). Elle ne dépend ni de l'heure d'archivage ni du moment où le tirage est lancé.
2. **Relevé engagé, prouvé hors du dépôt** : à l'archivage, l'empreinte SHA-256 du manifeste est écrite dans le journal de l'exécution GitHub Actions (`archive_run` dans le manifeste). Au tirage, `auditor/commitment.py` interroge l'API de GitHub pour chaque relevé de la date : exécution de ce dépôt et du workflow d'archivage, réussie, terminée avant l'échéance selon l'horodatage de GitHub, et journal contenant l'empreinte exacte du manifeste. Un relevé sans cette preuve n'est jamais retenu. Parmi les relevés prouvés, le relevé engagé est celui dont l'archivage s'est terminé en dernier (heure de GitHub, jamais celle écrite dans le manifeste). Les preuves de tous les candidats sont conservées dans `draw.json`. Les données peuvent changer avant l'échéance, mais l'aléa est alors inconnu ; après l'échéance, aucun relevé nouveau ne peut être prouvé antérieur. L'administrateur peut supprimer une exécution : le relevé correspondant devient alors inadmissible, ce qui peut empêcher un tirage mais pas en choisir un autre.
3. **Aléa public** : la balise drand (chaîne quicknet, League of Entropy) du tour correspondant à l'échéance, enregistrée dans `draw.json`. Sa signature BLS est vérifiée avec la clé publique du réseau, épinglée dans `auditor/drandverify.py` et contrôlée sur une balise réelle. Bibliothèque : `pip install --require-hashes --no-deps -r requirements-tirage.txt`.
4. **Sans balise authentique, aucun tirage.** Il n'existe pas de valeur de secours.

Limites restantes : l'administrateur du dépôt peut supprimer des exécutions GitHub Actions ou réécrire l'historique, et modifier `config/audit-policy.json`. Chaque rapport publie l'empreinte des fichiers de `config/` ; un horodatage extérieur des engagements est prévu en phase D.
