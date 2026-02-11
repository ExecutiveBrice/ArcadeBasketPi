"""Application configuration for ArcadeBasketPi."""

from pathlib import Path

# Absolute project directory.
BASE_DIR = Path(__file__).resolve().parent

# GPIO pin mapping (BCM numbering).
SENSOR_PIN = 17
RESET_BUTTON_PIN = 27
LED_SCORE_PIN = 22
LED_MATCH_ACTIVE_PIN = 23

# GPIO behavior.
GPIO_MODE = "BCM"
SENSOR_PULL_UP_DOWN = "PUD_UP"
BUTTON_PULL_UP_DOWN = "PUD_UP"
SENSOR_EDGE = "FALLING"
BUTTON_EDGE = "FALLING"
DEBOUNCE_SENSOR_MS = 120
DEBOUNCE_BUTTON_MS = 250

# Feedback behavior.
SCORE_LED_PULSE_SECONDS = 0.15
SOUND_FILE = BASE_DIR / "static" / "sounds" / "bip.wav"

# Storage.
DB_PATH = BASE_DIR / "storage" / "arcade_basket.db"
SCHEMA_PATH = BASE_DIR / "storage" / "schema.sql"
HISTORY_LIMIT = 20

# Web server.
HOST = "0.0.0.0"
PORT = 5000
DEBUG = False

# Polling / loop timing.
MAIN_LOOP_SLEEP_SECONDS = 1.0
