#!/usr/bin/env python3
# Code lock for Raspberry Pi & Franzboard
# 
import RPi.GPIO as GPIO
import sys
import time

LED1 = 18
LED2 = 23
LED3 = 24
LED4 = 25

BUT1 = 22
BUT2 = 27
BUT3 = 17

FALSE = 0
WAIT = -1
TRUE = 1
code = [BUT1, BUT2, BUT3, BUT2]
keys = []
passed = 0

def keyPressed(channel):
    global passed
    passed = WAIT
    print('Pressed key %s' % channel)
    keys.append(channel)
    if (len(keys) == len(code)):
        if keys == code:
            passed = TRUE
            print('*** Open ***')
        else:
            passed = FALSE
            print('Wrong code')
        keys.clear()

def blinkShort():
    GPIO.output([LED1, LED2, LED3, LED4], GPIO.HIGH)
    time.sleep(0.01)
    GPIO.output([LED1, LED2, LED3, LED4], GPIO.LOW)
    time.sleep(1)

def showWait():
    GPIO.output([LED1, LED2, LED3, LED4], GPIO.HIGH)
    time.sleep(1)

def blinkOpen():
    for i in range(5):
        for led in [LED1, LED2, LED3, LED4]:
            GPIO.output(led, GPIO.HIGH)
            time.sleep(.1)
            GPIO.output(led, GPIO.LOW)
            time.sleep(.1)

def main():
    global passed
    GPIO.setmode(GPIO.BCM)
    GPIO.setup([LED1, LED2, LED3, LED4], GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup([BUT1, BUT2, BUT3], GPIO.IN)
    GPIO.add_event_detect(BUT1, GPIO.FALLING, callback=keyPressed, bouncetime = 200)
    GPIO.add_event_detect(BUT2, GPIO.FALLING, callback=keyPressed, bouncetime = 200)
    GPIO.add_event_detect(BUT3, GPIO.FALLING, callback=keyPressed, bouncetime = 200)

    print('Code %s' % code)

    timeout = 10
    while True:
        try:
            if passed == TRUE:
                passed = FALSE 
                blinkOpen()
                print('*** Closing ***')
            elif passed == WAIT:
                if timeout >= 0:
                    print('Wait %d' % timeout)
                    showWait()
                    timeout -= 1
                else:
                    passed = FALSE
                    timeout = 5 
                    keys.clear() 
                    print('Timeout expired')
            else:
                blinkShort()

        except KeyboardInterrupt:
            GPIO.cleanup([LED1, LED2, LED3, LED4])
            sys.exit()


if  __name__ == '__main__':
     main()


