import RPi.GPIO as GPIO

ledGreenPin = 11
ledYellowPin = 32
buttonPin = 12


def setLedGreen(state):
    if state:
        GPIO.output(ledGreenPin, GPIO.HIGH)
    else:
        GPIO.output(ledGreenPin, GPIO.LOW)

def setLedYellow(state):
    if state:
        GPIO.output(ledYellowPin, GPIO.HIGH)
    else:
        GPIO.output(ledYellowPin, GPIO.LOW)

def getButtonState() -> bool:
    if GPIO.input(buttonPin)==GPIO.LOW: 
        return False
    else:
        return True
