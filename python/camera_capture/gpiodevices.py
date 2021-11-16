import RPi.GPIO as GPIO

ledGreenPin = 11
ledYellowPin = 32
buttonPin = 12

def setup():
    GPIO.setmode(GPIO.BOARD)      # use PHYSICAL GPIO Numbering
    GPIO.setup(ledGreenPin, GPIO.OUT)   # set ledPin to OUTPUT mode
    GPIO.setup(ledYellowPin, GPIO.OUT)   # set ledPin to OUTPUT mode
    GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # set buttonPin to PULL UP INPUT mode

def reset():
    setLedGreen(False)
    setLedYellow(False)
    GPIO.cleanup()                    # Release GPIO resource

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
    if GPIO.input(buttonPin)==GPIO.HIGH: 
        return False
    else:
        return True
