from hardware.gpio import init_gpio, cleanup
from hardware.capteur import on_panier
from hardware.bouton import on_reset
from app import app
import RPi.GPIO as GPIO
from config import GPIO_CAPTEUR, GPIO_RESET


def main():
    try:
        app.run(host="0.0.0.0", port=5000)
    finally:
        cleanup()


if __name__ == "__main__":
    main()