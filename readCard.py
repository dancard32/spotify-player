import RPi.GPIO as GPIO             # Python module to read RFID tags
from mfrc522 import SimpleMFRC522   # Allows RPi to interface with GPIO
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
reader = SimpleMFRC522()
while True:
    try:
        print("Waiting for you to scan an RFID sticker/card")
        id = reader.read()[0] # Takes the first value of the tuple
        print("The ID for this card is:", id)

    finally:
        GPIO.cleanup()
