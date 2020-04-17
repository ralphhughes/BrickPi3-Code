#!/usr/bin/env python

import time
import brickpi3

def testAtPower(myPort, pwr):
    BP.set_motor_power(myPort, pwr) # Set desired motor power
    time.sleep(2) # Wait 2 seconds for rpm to stabilise
    avgDPS = 0
    for i in range(0,10):
        status = BP.get_motor_status(myPort)
        time.sleep(0.2)
        avgDPS = avgDPS + status[3]

    avgDPS = avgDPS / 10
    print("{0}%\t{1}\t{2}".format(status[1], round(avgDPS,1), round(avgDPS / 6,1)))




BP = brickpi3.BrickPi3()
BP.reset_all()

myPort = BP.PORT_B
try:
    BP.reset_motor_encoder(myPort)
    BP.set_motor_limits(myPort, 0, 0)
    print("PWM\tDPS\tRPM")

    # Test forwards
    pwr = 100
    while pwr >= 0:
        try:
            testAtPower(myPort, pwr)
            pwr -= 5
        except IOError as error:
            print(error)

    # Test reverse
    pwr = -100
    while pwr <= 0:
        try:
           testAtPower(myPort, pwr)
           pwr += 5
        except IOError as error:
            print(error)


    BP.reset_all()
except KeyboardInterrupt:
    BP.reset_all()

