#!/bin/bash


PROJECT_NAME="basket-counter"


echo "Création du projet $PROJECT_NAME..."


# Dossier racine
mkdir -p $PROJECT_NAME
cd $PROJECT_NAME || exit 1


# Fichiers racine
touch app.py main.py config.py requirements.txt README.md


# Dossiers principaux
mkdir -p hardware core storage templates static sounds systemd


# Hardware
touch hardware/gpio.py
touch hardware/capteur.py
touch hardware/bouton.py
touch hardware/leds.py
touch hardware/son.py


# Core
touch core/state.py
touch core/timer.py
touch core/scorer.py


# Storage
touch storage/db.py
touch storage/schema.sql


# Web
touch templates/index.html
touch static/style.css


# Systemd
touch systemd/basket-counter.service


# Son (placeholder)
touch sounds/bip.wav


echo "✅ Arborescence créée avec succès"
echo
tree .. 2>/dev/null || find . -type f