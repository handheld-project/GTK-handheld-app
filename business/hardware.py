import RPi.GPIO as GPIO
from time import sleep

class MyButton:
    def __init__(self, pin):
        self.pin = pin
        self.callback = None
        # Set up GPIO for the button
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


    def set_callback (self , call_back_function) :
        self.callback = call_back_function
        GPIO.add_event_detect(self.pin, GPIO.FALLING, callback= self.callback , bouncetime=300)

    def reset_callback (self) :
        GPIO.remove_event_detect(self.pin)

    def reset_all_callback (self) :
        list_pin = [16 ,17 , 23, 24 ,25 ,27 ]
        for pin in list_pin :
             GPIO.remove_event_detect(pin)