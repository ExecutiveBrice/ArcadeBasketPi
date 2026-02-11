# ArcadeBasketPi

Arcade basketball basket counter for Raspberry Pi 3 B+ with GPIO sensor input, reset button, LED and sound feedback, SQLite history, and Flask dashboard.

## Hardware wiring (BCM)
- `GPIO17` -> optical sensor output (`SENSOR_PIN`)
- `GPIO27` -> reset/start push button (`RESET_BUTTON_PIN`)
- `GPIO22` -> basket scored LED (`LED_SCORE_PIN`)
- `GPIO23` -> match active LED (`LED_MATCH_ACTIVE_PIN`)
- Use common GND and proper resistor/pull-up design for your sensor and button.

## Install on Raspberry Pi 3 B+
1. Copy project to Pi (example target path: `/opt/ArcadeBasketPi`).
2. Install system dependencies:
   ```bash
   sudo apt update
   sudo apt install -y python3 python3-venv python3-pip alsa-utils
   ```
3. Create virtual environment and install Python packages:
   ```bash
   cd /opt/ArcadeBasketPi
   python3 -m venv .venv
   source .venv/bin/activate
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
4. Add your sound file:
   ```bash
   mkdir -p static/sounds
   cp /path/to/your/bip.wav static/sounds/bip.wav
   ```

## Run manually
```bash
cd /opt/ArcadeBasketPi
source .venv/bin/activate
python3 main.py
```
Then open `http://<raspberry-pi-ip>:5000`.

## Enable auto-start with systemd
1. Copy service file:
   ```bash
   sudo cp systemd/basket-counter.service /etc/systemd/system/
   ```
2. If you use venv Python, edit `ExecStart` in `/etc/systemd/system/basket-counter.service` to:
   ```
   /opt/ArcadeBasketPi/.venv/bin/python /opt/ArcadeBasketPi/main.py
   ```
3. Enable and start:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable basket-counter.service
   sudo systemctl start basket-counter.service
   sudo systemctl status basket-counter.service
   ```

## Operational notes
- Sensor and button inputs are debounced in software (`config.py`).
- Button behavior: if idle, starts a match; if active, stores current match and starts a new one.
- Web buttons provide Start, Reset/New Match, and Stop.
- Match history is stored in `storage/arcade_basket.db`.
