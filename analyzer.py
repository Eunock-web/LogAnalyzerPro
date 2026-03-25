#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import glob, argparse, os, platform
from collections import Counter
from typing import TypedDict

class RapportResultats(TypedDict):
    total_lignes: int
    par_niveau: dict[str, int]
    top5_erreurs: list[tuple[str, int]]
    fichier_traites: list[str]
    

def analyser_logs(dossier_source:str, filtre_niveau:str) -> RapportResultats:
  """
    Analyse les fichiers .log d'un répertoire pour extraire des statistiques de niveau.

    Args:
        dossier_source: Nom du sous-dossier contenant les fichiers logs.
        filtre_niveau: Niveau de log à afficher en console (ERROR, WARN, INFO ou ALL).

    Returns:
        RapportResultats: Dictionnaire contenant le total de lignes, le décompte par 
        niveau, le top 5 des messages d'erreur et la liste des fichiers traités.
  """
  base_dir = os.path.dirname(os.path.abspath(__file__))
  chemin_complet = os.path.join(base_dir, dossier_source, "*.log")

  fichier_trouves:list[str] = glob.glob(chemin_complet)

  total_lignes:int = 0

  compteurs:dict[str, int] = {
    "ERROR": 0,
    "WARN": 0,
    "INFO": 0
  }

  toutes_erreurs:list[str] = []

  for fichier in fichier_trouves:
    with open(fichier, "r", encoding="utf-8") as fichier_courant:
      
      for ligne in fichier_courant:
        
        total_lignes += 1
          
        if "ERROR" in ligne:
          
          compteurs["ERROR"] += 1
          parties = ligne.split(" ", 3)
          if len(parties) == 4:
            toutes_erreurs.append(parties[-1].strip())
            
        elif "WARN" in ligne:
          compteurs["WARN"] += 1
        elif "INFO" in ligne:
          compteurs["INFO"] += 1
        
        if filtre_niveau in ligne or filtre_niveau == "ALL":
          print(ligne.strip())
          
          
  top5_erreurs = Counter(toutes_erreurs).most_common(5)

  # Affichage structuré des résultats
  print("\n=== RÉSUMÉ D'ANALYSE ===")
  print(f"Total de lignes analysées : {total_lignes}")
  print("Comptage par niveau :")
  for niveau, nombre in compteurs.items():
    print(f"  - {niveau}: {nombre}")

  print("Top 5 des messages ERROR les plus fréquents :")
  if top5_erreurs:
    for i, (msg, cnt) in enumerate(top5_erreurs, start=1):
      print(f"  {i}. {msg} ({cnt})")
  else:
    print("  Aucun message d'erreur trouvé")

  os_detecte = platform.system()
  utilisateur = os.environ.get("USER") or os.environ.get("USERNAME") or "Inconnu"
  print(f"Machine: {os_detecte} | Lancé par: {utilisateur}")
  
  resultats:RapportResultats = {
    "total_lignes": total_lignes,
    "par_niveau": compteurs,
    "top5_erreurs": top5_erreurs,
    "fichier_traites": fichier_trouves
  }
  
  return resultats


def get_arguments():
  parser = argparse.ArgumentParser(description="Flemme")
  
  parser.add_argument("--source", required=True, help="Ah gars pourtant c'est simple")
  parser.add_argument("--niveau", default="ALL", choices=['ERROR', 'WARN', 'INFO', 'ALL'], help="Chef toi aussi")
  parser.add_argument('--dest', required=True, help="Tout est dans le nom wallah")

  args = parser.parse_args()

  return args


if __name__ == "__main__":
  
  args = get_arguments()
  analyser_logs(args.source, args.niveau)