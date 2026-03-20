#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from pathlib import Path
from datetime import datetime, timedelta
import random

def generate_test_logs(directory="logs_test"):
    # Création du dossier de test s'il n'existe pas [cite: 46]
    path = Path(__file__).resolve().parent / directory
    path.mkdir(exist_ok=True)
    
    # Configuration des logs
    levels = ["INFO", "WARN", "ERROR"]
    messages = {
        "INFO": ["Connexion établie", "Nettoyage terminé", "Utilisateur connecté", "Requête reçue"],
        "WARN": ["Utilisation CPU élevée (>85%)", "Temps de réponse lent", "Mémoire saturée", "Tentative échouée"],
        "ERROR": ["Échec de la connexion au serveur LDAP", "Base de données inaccessible", "Erreur 500 sur /api/data", "Segmentation fault"]
    }

    # Génération de 3 fichiers de test [cite: 46]
    for i in range(1, 4):
        filename = path / f"app{i}.log"
        lines = []
        base_time = datetime.now() - timedelta(hours=24) # Logs sur les dernières 24h

        # Chaque fichier doit avoir au moins 20 lignes 
        for j in range(25):
            lvl = random.choice(levels)
            msg = random.choice(messages[lvl])
            # Format impératif : YYYY-MM-DD HH:MM:SS NIVEAU Message 
            timestamp = (base_time + timedelta(minutes=j*10)).strftime("%Y-%m-%d %H:%M:%S")
            lines.append(f"{timestamp} {lvl} {msg}")

        filename.write_text("\n".join(lines), encoding="utf-8")
        print(f"Fichier créé : {filename} ({len(lines)} lignes)")

if __name__ == "__main__":
    generate_test_logs()