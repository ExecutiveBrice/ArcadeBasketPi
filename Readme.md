# 🏀 Basket Counter – Raspberry Pi

Système autonome de comptage de paniers de basket utilisant un **capteur optique**,  
un **Raspberry Pi B 1.2**, des **GPIO**, et une **interface web locale**.

Conçu pour un **usage club** : robuste, simple, sans écran/clavier, utilisable par tous.

---

## ✨ Fonctionnalités

- 🏀 Comptage automatique des paniers (capteur optique)
- 🔴 Bouton physique de reset / démarrage de match
- 💡 LEDs de retour visuel (panier / match en cours)
- 🔊 Signal sonore à chaque panier
- ⏱️ Chronomètre automatique
- 🌐 Interface web locale (Flask)
- 🏆 Historique des matchs (SQLite)
- 🔁 Redémarrage automatique au boot (systemd)

---

## 🧠 Architecture


---

## 🧰 Matériel requis

- Raspberry Pi **Model B rev 1.2**
- Carte SD (≥ 8 Go, qualité recommandée)
- Alimentation 5V / 2A
- Capteur optique (sortie **3.3 V max**)
- 1 bouton poussoir (NO)
- 2 LEDs
- 2 résistances 220–330 Ω (LEDs)
- Câbles Dupont
- Haut-parleur ou enceinte (jack ou HDMI)

---

## 🔌 Schéma GPIO (BCM)

| Fonction | GPIO BCM | Type |
|-------|----------|------|
| Capteur optique | GPIO 17 | Entrée |
| Bouton RESET | GPIO 27 | Entrée |
| LED Panier | GPIO 22 | Sortie |
| LED Match | GPIO 23 | Sortie |
| GND | GND | Masse |

⚠️ **Ne jamais injecter du 5V sur un GPIO**

---

## 🖥️ Installation logicielle

```bash
sudo apt update
sudo apt install python3 python3-pip python3-rpi.gpio aplay
pip3 install flask
```

▶️ Lancement manuel
python3 main.py

Interface web :
http://IP_DU_RASPBERRY:5000

🔁 Lancement automatique au démarrage
sudo cp systemd/basket-counter.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable basket-counter
sudo systemctl start basket-counter

🧪 Mode test sans matériel

Désactiver l'option de DockerDesktop : Use containerd for pulling and storing images
-Permet l'usage des images ARMv7
docker run --rm --privileged multiarch/qemu-user-static --reset -p yes

docker compose up -d


---

# 🔌 Schéma de branchement (texte + ASCII)

## 🧠 Principe général
- Toutes les masses (**GND**) doivent être communes
- LEDs **avec résistance en série**
- Bouton relié à la masse (pull-up interne)
- Capteur optique **3.3V max**

---

## 🧩 Schéma logique

      Raspberry Pi B 1.2 (GPIO BCM)

  +--------------------------------+
  |                                |
  |  GPIO17 <---- Capteur optique  |
  |                                |
  |  GPIO27 <---- Bouton RESET ----┐
  |                                │
  |  GPIO22 ----> LED Panier --[R]-┘
  |                                |
  |  GPIO23 ----> LED Match  --[R]-┐
  |                                │
  |  GND --------------------------┘
  |                                |
  +--------------------------------+

  
`[R] = résistance 220–330 Ω`

---

## 🔊 Son

- Jack audio du Raspberry
- Ou HDMI → écran
- Son joué via `aplay`
