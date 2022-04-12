import RPi.GPIO as GPIO

def forward_button(channel):
    print("Pushed Button")
    
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(11, GPIO.RISING, callback=forward_button)

while True:
    pass
GPIO.cleanup()

    