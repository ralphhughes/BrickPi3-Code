# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

# import brickpi3
import math

# Global
#BP = brickpi3.BrickPi3()

# Constants
WHEEL_DIAMETER = 8.2 # CM
GEAR_RATIO = 12 / 20  # 12t:20t

def move_distance(distance):
    try:
        wheel_circumference = math.pi * WHEEL_DIAMETER
        num_wheel_revolutions = distance / wheel_circumference
        num_motor_revolutions = num_wheel_revolutions / GEAR_RATIO
        motor_degrees = 360 * num_motor_revolutions
        
        BP.set_motor_position_relative(BP.PORT_A & BP.PORT_D, motor_degrees)
        
    except KeyboardInterrupt:
        #BP.reset_all()
        print ("Bye")

if __name__ == "__main__":
    required_distance = int(input("Enter number of centimeters to move: "))
    move_distance(required_distance)
