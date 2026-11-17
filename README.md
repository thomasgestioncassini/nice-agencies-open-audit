# nice-agencies-open-audit

Auditeur ouvert du classement des agences immobilières de Nice publié sur [meilleure-agence-nice.fr](https://meilleure-agence-nice.fr).

> **Ce dispositif n'est pas une certification indépendante.** Il est administré par SARL GESTION CASSINI, éditrice du classement et exploitante de deux agences classées (Gestion Cassini et ImmoVendu). Ce qu'il apporte : un code ouvert, des calculs reproductibles par n'importe qui et des rapports publics, y compris défavorables. Voir [GOVERNANCE.md](GOVERNANCE.md) et [CONFLICTS.md](CONFLICTS.md).

## État du projet

| Phase | Contenu | État |
| --- | --- | --- |
| B | Recalcul indépendant, sans IA, archivage des relevés, tests | développée, en cours de validation |
| C | Deux IA d'audit (OpenAI, Google Gemini), contrôles à la source | non commencée |
| D | Exécution hebdomadaire, signatures, registre, surveillance externe | non commencée |
| E | Affichage sur le site | non commencée |

## Trois dimensions, six statuts

Chaque rapport donne un statut séparé pour :

1. **les calculs et le texte de la méthode** :
   - *reproduction* : les notes publiées découlent-elles des données publiées, selon les règles que le site applique ?
   - *règles décrites* : le texte archivé avec le relevé décrit-il chaque règle appliquée ?
   - *contradictions encore présentes* : le texte affirme-t-il encore une règle contraire au calcul ? (contrôle par phrases répertoriées, pas une relecture complète)
   - *écarts antérieurs* : une version archivée antérieure du texte contredisait-elle le calcul ? Ces écarts restent publiés même après correction du texte. L'effet de chaque écart sur les notes et les rangs est mesuré.
2. **la vérification des données primaires** : les données d'entrée sont-elles exactes à leur source (plateformes d'avis, sites des agences, registre des entreprises) ?
3. **l'analyse des biais** : la méthode avantage-t-elle certaines agences, dont celles de l'éditeur ?

Une reproduction conforme ne dit rien des autres statuts. En particulier, des données falsifiées de façon cohérente avant leur export ne se voient pas au recalcul : seuls les contrôles à la source et la comparaison entre relevés successifs peuvent les révéler (tests `CoordinatedForgery`).

## Reproduire un audit (sans clé d'API, sans réseau)

Python 3.10 ou plus récent, bibliothèque standard uniquement.

```
git clone https://github.com/thomasgestioncassini/nice-agencies-open-audit
cd nice-agencies-open-audit
python3 -m auditor run snapshots/<date>        # recalcule un relevé archivé, écrit reports/<id>/
python3 -m auditor verify reports/<id>         # vérifie les empreintes du rapport et du relevé
python3 -m auditor draw snapshots/<date>       # balise drand du tour fixé à l'archivage (réseau)
python3 -m unittest -v                         # tests, dont les altérations volontaires
```

Pour archiver le relevé publié en ce moment : `python3 -m auditor fetch` (seule commande qui utilise le réseau).

Détails : [docs/reproduction.md](docs/reproduction.md). Règles que le texte de la méthode ne précise pas : [docs/interpretations.md](docs/interpretations.md). Arbitrages de la phase C (constats contestés, priorités de la revue ChatGPT) : [docs/arbitrages-phase-c.md](docs/arbitrages-phase-c.md). Ce que l’audit établit et n’établit pas : [docs/portee-et-limites.md](docs/portee-et-limites.md).

## Contenu

- `auditor/` : téléchargement et archivage, contrôles de cohérence, recalcul, comparaison, échantillonnage, rapport.
- `config/` : méthode v5 recopiée du texte public, règles de l'auditeur (tolérances, échantillonnage), règles établies par lecture du code.
- `snapshots/<date>/` : relevés archivés (gzip) avec empreintes SHA-256, URL et heure UTC de téléchargement.
- `reports/<id>/` : rapports (`report.json`, `report.md`, `calculations.csv`, `anomalies.json`, `manifest.json`).
- `tests/` : tests automatisés.

## Signaler une erreur

Ouvrez une issue sur ce dépôt. Une contestation ne modifie jamais une note : l'auditeur peut seulement publier une recommandation de correction.
