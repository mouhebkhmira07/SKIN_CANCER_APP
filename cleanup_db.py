import sqlite3
import os

DATABASE = 'skin_cancer.db'
UPLOAD_FOLDER = 'static/uploads'

def cleanup():
    print("=" * 60)
    print("   PROCÉDURE DE NETTOYAGE DE LA BASE DE DONNÉES SKIN CANCER")
    print("=" * 60)
    
    if not os.path.exists(DATABASE):
        print(f"❌ Erreur : Le fichier de base de données '{DATABASE}' n'existe pas.")
        return

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    keywords = ['ammareoussama', 'oussama', 'ammar']
    deleted_patients = 0
    deleted_users = 0
    deleted_images = []

    try:
        for kw in keywords:
            # 1. Traitement des Patients
            patients = cursor.execute(
                "SELECT id, name, image_path FROM patients WHERE name LIKE ?", 
                (f"%{kw}%",)
            ).fetchall()
            
            for p in patients:
                pid = p['id']
                pname = p['name']
                img_name = p['image_path']
                
                print(f"🔍 Patient trouvé : ID {pid} | Nom: '{pname}'")
                
                # Suppression de l'image
                if img_name:
                    filepath = os.path.join(UPLOAD_FOLDER, img_name)
                    if os.path.exists(filepath):
                        try:
                            os.remove(filepath)
                            deleted_images.append(img_name)
                            print(f"   🗑️ Image supprimée : {img_name}")
                        except Exception as e:
                            print(f"   ⚠️ Impossible de supprimer l'image {img_name}: {e}")
                    else:
                        print(f"   ℹ️ Fichier image introuvable sur le disque : {img_name}")
                
                # Suppression du record
                cursor.execute("DELETE FROM patients WHERE id = ?", (pid,))
                deleted_patients += 1

            # 2. Traitement des Utilisateurs
            users = cursor.execute(
                "SELECT id, username FROM users WHERE username LIKE ?", 
                (f"%{kw}%",)
            ).fetchall()
            
            for u in users:
                uid = u['id']
                username = u['username']
                print(f"🔍 Utilisateur trouvé : ID {uid} | Nom: '{username}'")
                
                cursor.execute("DELETE FROM users WHERE id = ?", (uid,))
                deleted_users += 1

        conn.commit()
        
        print("-" * 60)
        print("📊 BILAN DU NETTOYAGE :")
        print(f"   - Patients supprimés : {deleted_patients}")
        print(f"   - Utilisateurs supprimés : {deleted_users}")
        print(f"   - Images supprimées du disque : {len(deleted_images)}")
        if deleted_images:
            for img in deleted_images:
                print(f"     * {img}")
        print("=" * 60)
        print("✅ Nettoyage terminé avec succès !")
        
    except Exception as e:
        conn.rollback()
        print(f"❌ Une erreur est survenue lors du nettoyage : {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    cleanup()
