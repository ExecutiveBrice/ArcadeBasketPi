#!/bin/bash

set -e

PROJECT_DIR="/home/ArcadeBasketPi"

cd $PROJECT_DIR

echo "🐍 Création environnement virtuel..."
python3 -m venv venv

echo "⚡ Activation venv..."
source venv/bin/activate

echo "📦 Installation requirements..."
pip install --upgrade pip
pip install -r requirements.txt

echo "🗄️ Initialisation base SQLite..."
python - <<EOF
from storage.db import init_db
init_db()
print("Base initialisée ✅")
EOF

echo "🔊 Test audio (optionnel)"
if [ -f sounds/bip.wav ]; then
    aplay sounds/bip.wav || true
fi

echo "✅ Installation terminée"
echo
echo "Pour lancer manuellement :"
echo "cd $PROJECT_DIR"
echo "source venv/bin/activate"
echo "python main.py"
