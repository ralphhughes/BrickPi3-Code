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
WHEEL_TRACK_WIDTH = 15.00 # CM (nice round number, what are the chances!)

LEFT_MOTOR = BP.PORT_B
RIGHT_MOTOR = BP.PORT_C


def distance_to_motor_degrees(distance):
    wheel_circumference = math.pi * WHEEL_DIAMETER
    num_wheel_revolutions = distance / wheel_circumference
    num_motor_revolutions = num_wheel_revolutions / GEAR_RATIO
    motor_degrees = 360 * num_motor_revolutions
    return motor_degrees
    
    
def turn_left(angle):
    fraction_of_circle = angle / 360
    required_distance = fraction_of_circle * (math.pi * WHEEL_TRACK_WIDTH)
    motor_degrees = distance_to_motor_degrees(required_distance)
    BP.set_motor_power(LEFT_MOTOR, 0)
    BP.set_motor_position_relative(RIGHT_MOTOR, motor_degrees)
    
def turn_right(angle):
    fraction_of_circle = angle / 360
    required_distance = fraction_of_circle * (math.pi * WHEEL_TRACK_WIDTH)
    motor_degrees = distance_to_motor_degrees(required_distance)
    BP.set_motor_position_relative(LEFT_MOTOR, motor_degrees)
    BP.set_motor_power(RIGHT_MOTOR, 0)

def move_forward(distance):
    motor_degrees = distance_to_motor_degrees(distance)
    BP.set_motor_position_relative(LEFT_MOTOR, motor_degrees)
    BP.set_motor_position_relative(RIGHT_MOTOR, motor_degrees)

def move_backward(distance):
    motor_degrees = distance_to_motor_degrees(distance)
    BP.set_motor_position_relative(LEFT_MOTOR, -motor_degrees)
    BP.set_motor_position_relative(RIGHT_MOTOR, -motor_degrees)

def wait_for_motors_to_stop():
    while True:
        time.sleep(0.25)
        left_motor_dps = BP.get_motor_status(LEFT_MOTOR)[3]
        right_motor_dps = BP.get_motor_status(RIGHT_MOTOR)[3]
        if (left_motor_dps < 1 and right_motor_dps < 1):
            break
        
        
if __name__ == "__main__":
    BP.set_motor_limits(BP.PORT_B, 40, 600)
    BP.set_motor_limits(BP.PORT_C, 40, 600)
    required_distance = float(input("Enter number of centimeters to move: "))
    try:
        move_forward(required_distance)
        wait_for_motors_to_stop()
        turn_left(30)
        wait_for_motors_to_stop()
        turn_right(30)
        wait_for_motors_to_stop()
        move_backward(required_distance)
        wait_for_motors_to_stop()
        BP.reset_all()
    except KeyboardInterrupt:
        BP.reset_all()
        print ("Bye")
        
