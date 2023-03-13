import RPi.GPIO as GPIO

class ControlCenter():
    def __init__(self, luces=4, agua=27) -> None:
        GPIO.setmode(GPIO.BCM)
        self.luces=luces
        self.agua=agua
        GPIO.setup(self.luces, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(self.agua, GPIO.OUT, initial=GPIO.HIGH)
        self.luces_on = False
        self.agua_on= False
    
    def toggle_luces(self):
        if self.luces_on == False:
            GPIO.output(self.luces, GPIO.LOW)
            self.luces_on = True
        else:
            GPIO.output(self.luces, GPIO.HIGH)
            self.luces_on = False
    
    def toggle_agua(self):
        if self.agua_on == False:
            GPIO.output(self.agua, GPIO.LOW)
            print("on")
            self.agua_on = True
        else:
            GPIO.output(self.agua, GPIO.HIGH)
            print("off")
            self.agua_on = False