import os
import time
import tarfile
import shutil
import subprocess
import argparse
from datetime import datetime


def verifier_espace_disque(source):
    """
    Vérifie l'espace disque disponible dans le dossier source.
    Retourne True si l'espace est suffisant, False sinon.
    """
    print("==> Vérification de l'espace disque...")

    # Affiche le résumé lisible (df -h) dans le terminal
    resultat = subprocess.run(["df", "-h", source], capture_output=True, text=True)
    print(resultat.stdout)

    # Récupère l'espace libre en MB
    stat = shutil.disk_usage(source)
    espace_libre_mb = stat.free / (1024 * 1024)
    print(f"    Espace libre : {espace_libre_mb:.1f} MB")

    if espace_libre_mb < 50:
        print("    ATTENTION : Moins de 50 MB disponibles.")
        return False

    print("    Espace suffisant.")
    return True

def archiver_logs(source, dest):
    """
    Crée une archive backup_YYYY-MM-DD.tar.gz directement dans dest
    avec tous les fichiers .log trouvés dans source.
    Retourne le chemin de l'archive créée, ou None si aucun .log trouvé.
    """
    print("\n==> Recherche des fichiers .log à archiver...")

    # Lister tous les fichiers .log dans le dossier source
    fichiers_log = []
    for fichier in os.listdir(source):
        if fichier.endswith(".log"):
            chemin = os.path.join(source, fichier)
            fichiers_log.append(chemin)

    if not fichiers_log:
        print("    Aucun fichier .log trouvé.")
        return None

    print(f"    {len(fichiers_log)} fichier(s) .log trouvé(s).")

    # Construire le nom et chemin de l'archive directement dans dest
    date_du_jour = datetime.now().strftime("%Y-%m-%d")
    nom_archive  = f"backup_{date_du_jour}.tar.gz"

    os.makedirs(dest, exist_ok=True)
    chemin_archive = os.path.join(dest, nom_archive)

    # Créer l'archive directement dans dest (plus de passage par source)
    print(f"    Création de l'archive : {chemin_archive}")
    with tarfile.open(chemin_archive, "w:gz") as archive:
        for chemin in fichiers_log:
            archive.add(chemin, arcname=os.path.basename(chemin))
            print(f"      + {os.path.basename(chemin)}")

    print(f"    Archive créée : {chemin_archive}")
    return chemin_archive


def supprimer_json_anciens(source, retention):
    """
    Supprime les fichiers .json dans source dont l'âge
    dépasse le nombre de jours défini par retention.
    Retourne le nombre de fichiers supprimés.
    """
    print(f"\n==> Suppression des fichiers .json de plus de {retention} jours...")

    maintenant         = time.time()
    limite_en_secondes = retention * 24 * 60 * 60
    fichiers_supprimes = 0

    for fichier in os.listdir(source):
        if fichier.endswith(".json"):
            chemin = os.path.join(source, fichier)

            date_modif      = os.path.getmtime(chemin)
            age_en_secondes = maintenant - date_modif

            if age_en_secondes > limite_en_secondes:
                os.remove(chemin)
                age_jours = age_en_secondes / (24 * 60 * 60)
                print(f"    Supprimé : {fichier} (âge : {age_jours:.0f} jours)")
                fichiers_supprimes += 1

    if fichiers_supprimes == 0:
        print("    Aucun fichier JSON à supprimer.")

    return fichiers_supprimes


# Orchestration d'archivage te nettoyage
def main():
    """
    Point d'entrée du module.
    Lit les arguments, puis appelle les fonctions dans l'ordre.
    """
    parser = argparse.ArgumentParser(description="Module d'archivage et nettoyage")
    parser.add_argument("--source",    required=True,        help="Dossier source contenant les .log et .json")
    parser.add_argument("--dest",      required=True,        help="Dossier de destination pour l'archive")
    parser.add_argument("--retention", type=int, default=30, help="Jours avant suppression des JSON (défaut: 30)")
    args = parser.parse_args()

    # Étape 1 : vérifier l'espace disque
    espace_ok = verifier_espace_disque(args.source)
    if not espace_ok:
        print("\nEspace insuffisant. Archivage annulé.")
        return

    # Étape 2 : archiver les .log directement dans dest
    archiver_logs(args.source, args.dest)

    # Étape 3 : supprimer les .json trop anciens
    supprimer_json_anciens(args.source, args.retention)

    print("\n==> Module terminé.")
