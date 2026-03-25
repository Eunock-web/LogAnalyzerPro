# 📊 LogAnalyzer Pro

**LogAnalyzer Pro** est un outil d'administration système conçu en Python. Il automatise l'analyse, le reporting et l'archivage sécurisé des fichiers de logs de manière modulaire.

---

## 🚀 Fonctionnalités principales

* **Analyse Filtrée :** Extraction intelligente des logs par niveau (`INFO`, `WARN`, `ERROR`).
* **Statistiques Avancées :** Calcul automatique du **Top 5** des messages d'erreurs les plus fréquents via `collections.Counter`.
* **Reporting JSON :** Génération de rapports structurés incluant des métadonnées système (Utilisateur, OS, Date de génération).
* **Gestion de l'Espace Disque :** Vérification préventive de l'espace disponible via `subprocess`.
* **Archivage & Nettoyage :** Compression des logs traités en format `.tar.gz` et gestion de la rétention des anciens rapports.

---

## 📁 Structure du Projet

Le projet respecte une architecture modulaire pour une maintenance simplifiée :

* **`main.py`** : Point d'entrée unique et chef d'orchestre du pipeline de données.
* **`analyzer.py`** : Gestion des arguments CLI (`argparse`) et moteur de scan des fichiers `.log`.
* **`rapport.py`** : Module dédié à la mise en forme des données et à l'écriture du fichier JSON.
* **`archiver.py`** : Fonctions système (compression `tarfile`, suppression de fichiers, surveillance disque).

---

## 🛠 Installation et Utilisation

### Exécution manuelle
Lancez le script depuis le terminal en précisant le dossier source :
```bash
python3 main.py --source /chemin/vers/logs --niveau ERROR
 
---
Commande CRON: 
    - On ouvre la liste des tâches cron avec "crontab -e"

    - 0 3 * * 0 /usr/bin/python3 /home/user/LogAnalyzer/main.py --source /home/user/logs --niveau ALL