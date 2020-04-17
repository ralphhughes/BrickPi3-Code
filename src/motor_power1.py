#!/usr/bin/env python

import time
import brickpi3

BP = brickpi3.BrickPi3()

try:
    BP.reset_motor_encoder(BP.PORT_C) # set encoder to 0
    BP.set_motor_limits(BP.PORT_B, 25, 0) # 25% max power for B
    BP.set_motor_power(BP.PORT_C, -128) # float C
    while True:
        try:
            status = BP.get_motor_status(BP.PORT_B)
            print(status)

            posC = BP.get_motor_encoder(BP.PORT_C)
            # print(posC)
            if (posC > -100 and posC < 100):
                BP.set_motor_power(BP.PORT_B, posC)
        except IOError as error:
            print(error)

        time.sleep(0.02)

except KeyboardInterrupt:
    BP.reset_all()
