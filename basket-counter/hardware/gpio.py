import RPi.GPIO as GPIO
from config import (
    GPIO_CAPTEUR,
    GPIO_RESET,
    GPIO_LED_PANIER,
    GPIO_LED_MATCH
)

def init_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    # Entrées
    GPIO.setup(GPIO_CAPTEUR, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(GPIO_RESET, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # Sorties
    GPIO.setup(GPIO_LED_PANIER, GPIO.OUT)
    GPIO.setup(GPIO_LED_MATCH, GPIO.OUT)

    # État initial
    GPIO.output(GPIO_LED_PANIER, GPIO.LOW)
    GPIO.output(GPIO_LED_MATCH, GPIO.LOW)

    print("✅ GPIO initialisés")

def cleanup():
    GPIO.cleanup()
    print("🧹 GPIO nettoyés")
