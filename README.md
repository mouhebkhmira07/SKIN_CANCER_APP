# Skin Cancer Detection App (SkinScan AI)
A Flask-based web application for AI-assisted skin lesion classification with patient history tracking and a medical dashboard.

## Overview
This project lets medical staff upload dermatoscopic images, run an AI prediction (Benign vs Malignant), and store the full result history in SQLite.

The app includes:
- Secure login flow for clinical use
- Real-time dashboard statistics
- AI-assisted prediction workflow
- Per-patient report pages with confidence score
- Historical patient list with image previews

## Feature Showcases
### 1) Medical Login Portal
- Route: `/login`
- Role-gated entry point for authorized users
- Flash messages for authentication feedback

### 2) Diagnostic Dashboard
- Route: `/dashboard`
- Displays:
  - Total analyses
  - Malignant cases
  - Benign cases
- Includes visual distribution/progress widgets

### 3) New AI Analysis Workflow
- Route: `/predict`
- Supports:
  - Drag-and-drop image upload
  - Patient metadata capture (name, age)
  - Client-side preview before submission
  - Prediction using a VGG16-based model checkpoint

### 4) Detailed Result Report
- Route: `/result/<report_id>`
- Shows:
  - AI verdict (Benign/Malignant)
  - Confidence percentage
  - Uploaded lesion image
  - Print-friendly report action

### 5) Patient History Database View
- Route: `/patients`
- Chronological list of all analyses
- Quick navigation to individual report detail pages

## Tech Stack
- Python + Flask
- TensorFlow / Keras
- Pillow + NumPy
- SQLite (local embedded database)
- HTML/CSS + Font Awesome

## Project Structure
- `app.py` — main Flask app, routes, DB initialization, prediction pipeline
- `templates/` — UI pages (`login`, `dashboard`, `predict`, `result`, `patients`)
- `static/style.css` — global styling
- `static/uploads/` — uploaded lesion images
- `requirements.txt` — Python dependencies

## Getting Started
### 1) Clone
```bash
git clone https://github.com/mouhebkhmira07/SKIN_CANCER_APP.git
cd SKIN_CANCER_APP
```

### 2) Create and activate a virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3) Install dependencies
```bash
pip install -r requirements.txt
```

### 4) Add model checkpoint
`app.py` expects this file:
- `model/vgg16_malignant_vs_bengin.h5`

Create the folder and place your trained model there:
```bash
mkdir -p model
# copy your model to:
# model/vgg16_malignant_vs_bengin.h5
```

### 5) Run the app
```bash
python app.py
```
Then open `http://127.0.0.1:5000`.

## Default Login
On startup, the app seeds a default account:
- Username: `admin`
- Password: `admin123`

Change this immediately for real deployments.

## Notes
- The application is intended for educational/research support and not as a standalone medical diagnosis system.
- For production, disable Flask debug mode and move credentials/secrets to environment variables.
