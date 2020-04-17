#!/usr/bin/env python

import time
import brickpi3

BP = brickpi3.BrickPi3()
BP.reset_all()

try:
    desiredSpeed = 165 * 6
    BP.reset_motor_encoder(BP.PORT_C)
    BP.set_motor_limits(BP.PORT_C, 0, 0)
    BP.set_motor_dps(BP.PORT_C, desiredSpeed)
    atSteadyState = False
    while True:
        try:
            status = BP.get_motor_status(BP.PORT_C)
            print("flags: {0}\tpwr: {1}\t enc: {2}\tdps: {3}".format(status[0], status[1], status[2], status[3]))
            if (atSteadyState == False and status[3] == desiredSpeed):
                atSteadyState = True
            if (atSteadyState == True and status[3] < 170 * 3):
                BP.set_motor_power(BP.PORT_C, -128) # float
                break
        except IOError as error:
            print(error)

        time.sleep(0.02)

except KeyboardInterrupt:
    BP.reset_all()
