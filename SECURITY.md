# Sécurité

- Aucun accès en écriture au site audité, aucun secret du site.
- Les fichiers téléchargés sont des données : taille limitée (50 Mo), encodage vérifié, colonnes vérifiées. Aucun script du site audité n'est exécuté (le recalcul.py publié par le site n'est jamais lancé).
- Bibliothèque standard de Python uniquement en phase B : aucune dépendance tierce à verrouiller.
- Workflows : permissions minimales (`contents: read`), aucun secret en phase B.
- Clés d'API (phase C) : secrets GitHub du dépôt, plafond de dépense par fournisseur, arrêt des appels au-delà.

Vulnérabilité : ouvrez une issue sans détail exploitable, ou écrivez via le formulaire de contact de meilleure-agence-nice.fr.
