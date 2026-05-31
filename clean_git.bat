@echo off
title Re-initialisation Git - SkinScan AI
echo ============================================================
echo   RE-INITIALISATION DE GIT ET SUPPRESSION DE OUSSAMA
echo ============================================================
echo.

:: 1. Suppression du dossier .git actuel
if exist .git (
    echo [1/5] Suppression de l'ancien historique Git...
    rmdir /s /q .git
    echo ✅ Ancien historique supprime.
) else (
    echo [1/5] Aucun historique .git local detecte.
)
echo.

:: 2. Initialisation d'un nouveau depot Git
echo [2/5] Initialisation du nouveau depot Git...
git init
echo ✅ Depot Git local initialise.
echo.

:: 3. Configuration de l'auteur (Amine)
echo [3/5] Configuration de l'auteur (aminesaadaoui93)...
git config user.name "aminesaadaoui93"
:: Note: Remplacez l'email ci-dessous par votre email GitHub si necessaire
git config user.email "aminesaadaoui93@gmail.com"
echo ✅ Auteur configure : aminesaadaoui93
echo.

:: 4. Ajout des fichiers du projet
echo [4/5] Ajout de tous les fichiers du projet...
git add .
git commit -m "Initial commit - Skin Cancer Detection App"
echo ✅ Fichiers commits avec succes sous votre nom !
echo.

:: 5. Association avec votre depot GitHub
echo [5/5] Liaison avec votre depot GitHub distant...
git remote add origin https://github.com/aminesaadaoui93/SKIN_CANCER_APP.git
git branch -M main
echo ✅ Liaison etablie avec : https://github.com/aminesaadaoui93/SKIN_CANCER_APP.git
echo.

echo ============================================================
echo   PROCHAINE ETAPE : MISE A JOUR DE GITHUB
echo ============================================================
echo Pour ecraser l'historique sur GitHub et faire disparaitre
echo definitivement le nom de 'oussama' de vos contributeurs,
echo lancez la commande suivante dans votre terminal :
echo.
echo     git push -u origin main --force
echo.
echo ============================================================
pause
