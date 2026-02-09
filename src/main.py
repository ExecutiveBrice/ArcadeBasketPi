from hardware.gpio import cleanup
from app import app

def main():
    try:
        app.run(host="0.0.0.0", port=5000)
    finally:
        cleanup()


if __name__ == "__main__":
    main()