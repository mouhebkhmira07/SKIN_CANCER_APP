import os
import shutil
import stat
import subprocess
import time

DATABASE = 'skin_cancer.db'
UPLOAD_FOLDER = 'static/uploads'

def remove_readonly(func, path, excinfo):
    """Force remove read-only attribute to allow deletion on Windows."""
    try:
        os.chmod(path, stat.S_IWRITE)
        func(path)
    except Exception as e:
        print(f"   ⚠️ Impossible de modifier les permissions de {path} : {e}")

def run_git_cleanup():
    print("=" * 60)
    print("   FORCE-RESET DU DEPOT GIT - SKINSCAN AI")
    print("=" * 60)
    
    # 1. Quitter proprement ou alerter si un dossier .git existe
    git_dir = '.git'
    if os.path.exists(git_dir):
        print("[1/5] Suppression forcee de l'ancien historique Git...")
        # Essayer de supprimer récursivement en enlevant le mode lecture seule
        try:
            shutil.rmtree(git_dir, onerror=remove_readonly)
            time.sleep(1) # Attendre que le système libère le dossier
            if not os.path.exists(git_dir):
                print("   ✅ Ancien historique Git (.git) supprime avec succes.")
            else:
                print("   ❌ Echec de la suppression automatique de .git. Veuillez fermer VS Code et relancer.")
                return
        except Exception as e:
            print(f"   ❌ Erreur lors de la suppression de .git : {e}")
            return
    else:
        print("[1/5] Aucun dossier .git local detecte. Pret a initialiser.")

    # 2. Initialisation Git
    print("\n[2/5] Initialisation du nouveau depot Git...")
    try:
        subprocess.run(["git", "init"], check=True)
        print("   ✅ Nouveau depot Git initialise.")
    except Exception as e:
        print(f"   ❌ Erreur lors de 'git init' : {e}")
        return

    # 3. Configuration de l'auteur (Amine)
    print("\n[3/5] Configuration de l'auteur de confiance...")
    username = "aminesaadaoui93"
    email = "aminesaadaoui93@gmail.com"  # Votre adresse e-mail GitHub primaire
    
    try:
        subprocess.run(["git", "config", "user.name", username], check=True)
        subprocess.run(["git", "config", "user.email", email], check=True)
        print(f"   ✅ Auteur configure : {username} <{email}>")
    except Exception as e:
        print(f"   ❌ Erreur de configuration de l'auteur : {e}")
        return

    # 4. Commit initial
    print("\n[4/5] Ajout des fichiers et creation du commit...")
    try:
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", "Initial commit - Skin Cancer Detection App"], check=True)
        print("   ✅ Commit cree avec succes sous votre nom !")
    except Exception as e:
        print(f"   ❌ Erreur lors du commit : {e}")
        return

    # 5. Liaison GitHub et Force-Push
    print("\n[5/5] Liaison avec GitHub et envoi force...")
    repo_url = "https://github.com/aminesaadaoui93/SKIN_CANCER_APP.git"
    try:
        subprocess.run(["git", "remote", "add", "origin", repo_url], check=True)
        subprocess.run(["git", "branch", "-M", "main"], check=True)
        print("   🚀 Lancement de l'envoi force vers GitHub...")
        
        # Lancer le force-push
        push_res = subprocess.run(["git", "push", "-u", "origin", "main", "--force"], check=True)
        if push_res.returncode == 0:
            print("\n" + "=" * 60)
            print("🎉 SUCCES TOTAL !")
            print("Le depot GitHub a ete entierement mis a jour.")
            print("Oussama a ete supprime et vous etes le seul auteur !")
            print("=" * 60)
        else:
            print("❌ Echec du push. Verifiez votre connexion ou vos identifiants.")
    except Exception as e:
        print(f"\n❌ Une erreur est survenue lors de la liaison ou du push : {e}")
        print("Veuillez executer manuellement dans votre console :")
        print("   git push -u origin main --force")

if __name__ == "__main__":
    run_git_cleanup()
