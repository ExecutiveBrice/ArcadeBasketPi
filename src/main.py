from hardware.gpio import init_gpio, cleanup
from hardware.capteur import on_panier
from hardware.bouton import on_reset
from app import app
import RPi.GPIO as GPIO
from config import GPIO_CAPTEUR, GPIO_RESET


def main():
#     init_gpio()
#
#
# GPIO.add_event_detect(GPIO_CAPTEUR, GPIO.RISING, callback=on_panier)
# GPIO.add_event_detect(GPIO_RESET, GPIO.FALLING, callback=on_reset, bouncetime=200)

    try:
        app.run(host="0.0.0.0", port=5000)
    finally:
        cleanup()


if __name__ == "__main__":
    main()