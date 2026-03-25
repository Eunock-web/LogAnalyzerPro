#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import analyzer
import archiver
import rapport

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGS_DIR = os.path.join(BASE_DIR, "logs_test")
RAPPORT_DIR = os.path.join(BASE_DIR, "rapports")


def setup_test_env():

    os.makedirs(LOGS_DIR, exist_ok=True)
    with open(os.path.join(LOGS_DIR, "app1.log"), "w", encoding="utf-8") as f:
        f.write("2024-04-01 08:22:30 ERROR Échec de la connexion\n")
        f.write("2024-04-01 08:22:30 WARN Le serveur est bientôt plein\n")
        f.write("2024-04-01 08:22:30 INFO Envoi d'email à tous les utilisateurs\n")


if __name__ == "__main__":
    print(f"Initialisation du LogAnalyzer dans : {BASE_DIR}")

    try:
        setup_test_env()
        # la fonction et_arguments
        args = analyzer.get_arguments()
        # La fonction de vérification de l'espace disque
        espace = archiver.verifier_espace_disque(BASE_DIR)
        if(espace):
            # La fonction d'analyse
            stats = analyzer.analyser_logs(args.source, args.niveau)
            # La fonction de génération de rapport
            print(rapport.generate_file(stats, args.source))
            # La fonction d'archivage
            archiver.archiver_logs(args.source, args.dest)
            # La fonction de nettoyage
            archiver.supprimer_json_anciens(args.source, )
        else:
            print("Erreur: Espace insuffisant sur le disque")
            sys.exit(1)

    except Exception as e:
        print(f"Erreur: {e}")