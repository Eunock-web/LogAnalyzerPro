# LogAnalyzer Pro

**LogAnalyzer Pro** est un outil d'administration système conçu en Python. Il automatise l'analyse, le reporting et l'archivage sécurisé des fichiers de logs de manière modulaire.

---

## 1. Description du projet et objectif

LogAnalyzer Pro permet d'analyser des fichiers de logs applicatifs, de générer des rapports structurés au format JSON, d'archiver les fichiers traités et de nettoyer automatiquement les anciens rapports. Il est planifiable via Cron et respecte les contraintes d'un environnement DevOps.

## 2. Prérequis et installation

- Python 3.x
- Aucune dépendance externe (bibliothèque standard uniquement)

## 3. Utilisation : exemples de commandes

```bash
python3 main.py --source /chemin/vers/logs_test --niveau ERROR
```

- `--source` : chemin vers le dossier contenant les fichiers logs (obligatoire)
- `--niveau` : niveau de filtrage parmi ERROR, WARN, INFO, ALL (défaut : ALL)

## 4. Description de chaque module et son rôle

- **main.py** : Point d'entrée principal, orchestre l'exécution des modules, gestion des erreurs.
- **analyzer.py** : Ingestion et analyse des logs, filtrage, statistiques, top 5 erreurs, métadonnées. (Mouwafic BADAROU)
- **rapport.py** : Génération du rapport JSON structuré, gestion des chemins, métadonnées. (Eunock AIHOUNHIN)
- **archiver.py** : Archivage des logs, suppression des anciens rapports, vérification espace disque. (Wesley OKWUDIAFOR)
- **main.py** : Orchestration, gestion des erreurs, exécution planifiée. (Andy ATOHOUN)

## 5. Ligne Cron complète

Pour exécuter LogAnalyzer Pro tous les dimanches à 03h00 :

```
0 3 * * 0 /usr/bin/python3 /chemin/vers/LogAnalyzerPro/main.py --source /chemin/vers/logs_test --niveau ALL
```

- `0 3 * * 0` : tous les dimanches à 03h00
- `/usr/bin/python3` : chemin vers l’interpréteur Python
- `/chemin/vers/LogAnalyzerPro/main.py` : chemin absolu du script principal
- `--source` : dossier des logs à analyser
- `--niveau` : niveau de criticité à filtrer

## 6. Répartition des tâches

- **Mouwafic BADAROU** : Module 1 (analyzer.py)
- **Eunock AIHOUNHIN** : Module 2 (rapport.py)
- **Wesley OKWUDIAFOR** : Module 3 (archiver.py)
- **Andy ATOHOUN** : Module 4 (main.py)

---

## 📁 Structure du Projet

```
LogAnalyzerPro/
├── main.py
├── analyzer.py
├── rapport.py
├── archiver.py
├── logs_test/
│   ├── app1.log
│   ├── app2.log
│   └── app3.log
├── rapports/
├── backups/
└── README.md
```
