#!/usr/bin/env python

import time
import brickpi3

BP = brickpi3.BrickPi3()

myPort = BP.PORT_B
try:
    BP.reset_motor_encoder(myPort)
    BP.set_motor_limits(myPort, 0, 0)
    BP.set_motor_power(myPort, 100)
    print("PWM\tSpeed(DPS)\tSpeed(RPM)")
    for pwr in range(100, -100, -5):
        try:
            BP.set_motor_power(myPort, pwr)
            time.sleep(5)
            status = BP.get_motor_status(myPort)
            print("{0}%\t{1}\t{2}".format(status[1], status[3], round(status[3] / 6,1)))
        except IOError as error:
            print(error)

        time.sleep(0.02)

    BP.reset_all()
except KeyboardInterrupt:
    BP.reset_all()
