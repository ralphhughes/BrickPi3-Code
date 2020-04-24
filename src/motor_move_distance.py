# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

import brickpi3
import math
import time

# Global
BP = brickpi3.BrickPi3()

# Constants
WHEEL_DIAMETER = 8.2 # CM
GEAR_RATIO = 12 / 20  # 12t:20t

def move_distance(distance):
    try:
        print("Moving {} cm...".format(distance))
        wheel_circumference = math.pi * WHEEL_DIAMETER
        num_wheel_revolutions = distance / wheel_circumference
        print("Wheel revolutions: {}".format(num_wheel_revolutions))

        num_motor_revolutions = num_wheel_revolutions / GEAR_RATIO
        motor_degrees = 360 * num_motor_revolutions
        print("Motor degrees: {}".format(motor_degrees))
        BP.set_motor_position_relative(BP.PORT_B, motor_degrees)
        time.sleep(5)
        BP.set_motor_power(BP.PORT_B, -128)
    except KeyboardInterrupt:
        BP.reset_all()
        print ("Bye")

if __name__ == "__main__":
    BP.set_motor_limits(BP.PORT_B, 0, 600)
    required_distance = int(input("Enter number of centimeters to move: "))
    move_distance(required_distance)
