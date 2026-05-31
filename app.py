import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, flash, g
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "medical_key_2026"

# ============================================================
# 1. DATABASE SQLITE (aucune installation nécessaire)
# ============================================================
DATABASE = 'skin_cancer.db'

def get_db():
    """Retourne la connexion SQLite pour la requête actuelle."""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row  # Accès par nom de colonne (comme un dict)
    return db

@app.teardown_appcontext
def close_connection(exception):
    """Ferme la connexion SQLite à la fin de chaque requête."""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    """Crée les tables si elles n'existent pas et ajoute l'admin par défaut, puis nettoie les données d'ammareoussama."""
    with app.app_context():
        db = get_db()
        db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id       INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        """)
        db.execute("""
            CREATE TABLE IF NOT EXISTS patients (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                name        TEXT,
                age         INTEGER,
                result      TEXT,
                confidence  REAL,
                image_path  TEXT,
                date_added  TEXT
            )
        """)
        # Créer ou réinitialiser l'utilisateur admin par défaut (garantit la connexion avec admin / admin123)
        db.execute("INSERT OR REPLACE INTO users (id, username, password) VALUES (1, 'admin', 'admin123')")
        
        # Nettoyage des données associées à 'ammareoussama' ou 'oussama' ou 'ammar'
        try:
            keywords = ['ammareoussama', 'oussama', 'ammar']
            deleted_patients = 0
            deleted_users = 0
            deleted_images = []
            
            for kw in keywords:
                # Récupérer les chemins d'images des patients correspondants pour suppression physique
                rows = db.execute("SELECT image_path FROM patients WHERE name LIKE ?", (f"%{kw}%",)).fetchall()
                for r in rows:
                    img_name = r['image_path']
                    if img_name:
                        filepath = os.path.join(UPLOAD_FOLDER, img_name)
                        if os.path.exists(filepath):
                            try:
                                os.remove(filepath)
                                deleted_images.append(img_name)
                            except Exception as e:
                                print(f"⚠️ Erreur lors de la suppression de l'image {img_name}: {e}")
                
                # Supprimer les patients correspondants
                cursor = db.execute("DELETE FROM patients WHERE name LIKE ?", (f"%{kw}%",))
                deleted_patients += cursor.rowcount
                
                # Supprimer les utilisateurs correspondants
                cursor = db.execute("DELETE FROM users WHERE username LIKE ?", (f"%{kw}%",))
                deleted_users += cursor.rowcount
                
            db.commit()
            if deleted_patients > 0 or deleted_users > 0 or deleted_images:
                print(f"🧹 NETTOYAGE EFFECTUÉ :")
                print(f"   - {deleted_patients} patient(s) supprimé(s)")
                print(f"   - {deleted_users} utilisateur(s) supprimé(s)")
                print(f"   - Images supprimées : {', '.join(deleted_images) if deleted_images else 'Aucune'}")
        except Exception as e:
            print(f"⚠️ Erreur lors du nettoyage de la base de données : {e}")
            
        print("✅ Base de données SQLite initialisée avec succès.")

# ============================================================
# 2. Dossier d'uploads
# ============================================================
UPLOAD_FOLDER = 'static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# ============================================================
# 3. Chargement du modèle IA
# ============================================================
MODEL_PATH = 'model/vgg16_malignant_vs_bengin.h5'
try:
    model = load_model(MODEL_PATH)
    print("✅ Modèle IA chargé avec succès.")
except Exception as e:
    model = None
    print(f"⚠️  ATTENTION: Le modèle n'a pas pu être chargé. {e}")

# ============================================================
# ROUTES
# ============================================================

@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'loggedin' in session:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        user = request.form['username']
        pwd  = request.form['password']
        db = get_db()
        account = db.execute(
            "SELECT * FROM users WHERE username=? AND password=?", (user, pwd)
        ).fetchone()
        if account:
            session['loggedin'] = True
            session['username'] = account['username']
            return redirect(url_for('dashboard'))
        else:
            flash("Identifiants incorrects !", "danger")
    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    db = get_db()
    total   = db.execute("SELECT COUNT(*) FROM patients").fetchone()[0]
    m_count = db.execute("SELECT COUNT(*) FROM patients WHERE result='Malignant'").fetchone()[0]
    b_count = db.execute("SELECT COUNT(*) FROM patients WHERE result='Benign'").fetchone()[0]
    return render_template('dashboard.html', total=total, m_count=m_count, b_count=b_count)


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        file   = request.files.get('file')
        p_name = request.form.get('patient_name', 'Inconnu')
        p_age  = request.form.get('patient_age', None)

        if not file or file.filename == '':
            flash("Veuillez sélectionner une image.", "warning")
            return render_template('predict.html')

        if not model:
            flash("Le modèle IA n'est pas disponible.", "danger")
            return render_template('predict.html')

        # Sauvegarde de l'image
        filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # Prédiction IA
        img      = Image.open(filepath).convert('RGB').resize((224, 224))
        x        = np.array(img, dtype='float32') / 255.0
        x        = np.expand_dims(x, axis=0)
        pred_raw = model.predict(x)[0][0]
        res      = "Malignant" if pred_raw > 0.5 else "Benign"
        conf     = float(pred_raw * 100) if pred_raw > 0.5 else float((1 - pred_raw) * 100)

        # Enregistrement en base de données
        db = get_db()
        cursor = db.execute(
            "INSERT INTO patients (name, age, result, confidence, image_path, date_added) VALUES (?,?,?,?,?,?)",
            (p_name, p_age, res, round(conf, 2), filename, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        )
        db.commit()
        last_id = cursor.lastrowid
        return redirect(url_for('result', report_id=last_id))

    return render_template('predict.html')


@app.route('/result/<int:report_id>')
def result(report_id):
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    db = get_db()
    report = db.execute("SELECT * FROM patients WHERE id=?", (report_id,)).fetchone()
    if not report:
        flash("Rapport introuvable.", "warning")
        return redirect(url_for('patients'))
    return render_template('result.html', report=report)


@app.route('/patients')
def patients():
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    db = get_db()
    all_patients = db.execute("SELECT * FROM patients ORDER BY date_added DESC").fetchall()
    return render_template('patients.html', patients=all_patients)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


# ============================================================
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
