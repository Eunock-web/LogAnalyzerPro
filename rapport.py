#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import platform
import sys
from pathlib import Path
from datetime import datetime

def generate_file(statistique, dossier_source):
    """
    Génère un rapport structuré au format JSON selon un format specifique.
    """
    try:
        #  Gestion des dates et horodatage
        now = datetime.now()
        date_nom_fichier = now.strftime("%Y-%m-%d") # Pour le nom du fichier 
        date_complete = now.strftime("%Y-%m-%d %H:%M:%S") # Pour les métadonnées 

        # Construction des chemins absolus (Contrainte : utilisation de __file__) 
        # On récupère le dossier où se trouve le script actuel
        base_dir = Path(__file__).resolve().parent
        
        # Creation du  dossier 'rapports/' 
        dossier_rapports = base_dir / "rapports"
        dossier_rapports.mkdir(exist_ok=True) # Crée le dossier s'il n'existe pas

        nom_fichier = f"rapport_{date_nom_fichier}.json"
        chemin_final = dossier_rapports / nom_fichier

        #  Préparation des métadonnées et statistiques
        # Note : os.getlogin() ou os.environ.get('USER') pour l'utilisateur 
        utilisateur = os.environ.get('USER') or os.environ.get('USERNAME') or "unknown"
        systeme = platform.system() # Utilise la bibliothèque platform -

        # structure JSON du rapport
        data = {
            "metadata": {
                "date": date_complete,
                "utilisateur": utilisateur,
                "os": systeme,
                "source": os.path.abspath(dossier_source)
            },
            "statistiques": {
                "total_lignes": statistique.get('total_lignes', 0),
                "par_niveau": statistique.get('par_niveau', {}),
                "top5_erreurs": statistique.get('top5_erreurs', [])
            },
            "fichiers_traites": statistique.get('fichiers_traites', [])
        }

        #  Écriture dans le fichier 
        chemin_final.write_text(json.dumps(data, indent=4, ensure_ascii=False), encoding="utf-8")

        return f"Fichier {nom_fichier} créé avec succès dans {dossier_rapports}"

    except Exception as e:
        print(f"Erreur lors de la génération du rapport : {e}")
        sys.exit(1) 

# Exemple d'utilisation pour tes tests
if __name__ == "__main__":
    # Simulation de l'objet statistique provenant du Module 1
    stats_demo = {
        "total_lignes": 100,
        "par_niveau": {"ERROR": 10, "WARN": 20, "INFO": 70},
        "top5_erreurs": ["Timeout", "Auth Error", "Disk Full"],
        "fichiers_traites": ["logs_test/app1.log", "logs_test/app2.log"]
    }
    print(generate_file(stats_demo, "./logs_test"))