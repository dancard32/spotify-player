import RPi.GPIO as GPIO # Allows RPi to interface with GPIO
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def forward_button(channel):
    """
    forward_button GPIO callback function for testing
    
    Attributes:
        channel (BOARD): Inhereted from GPIO.setmode(GPIO.BOARD)
    """

    print("Pushed Button")
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
""" RPi set-up to allow button pushing """
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

# GPIO setup on PIN 11 to test button functionality
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(11, GPIO.RISING, callback=forward_button)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
while True:
    pass
GPIO.cleanup()

    