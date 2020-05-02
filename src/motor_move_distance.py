# Standalone test for using BrickPi to move\rotate a certain distance\angle

import math
import time
import platform
if platform.system() == 'Windows':
    from lib import brickpi3_mock
    BP = brickpi3_mock.BrickPi3()
elif platform.system() == 'Linux':
    import brickpi3
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
    print("    motor_degrees: {}".format(motor_degrees))
    return motor_degrees
    
def rotate_left(angle):
    fraction_of_circle = angle / 360
    required_distance = fraction_of_circle * (math.pi * WHEEL_TRACK_WIDTH)
    motor_degrees = distance_to_motor_degrees(required_distance)
    BP.set_motor_position_relative(LEFT_MOTOR, -motor_degrees)
    BP.set_motor_position_relative(RIGHT_MOTOR, motor_degrees)
    
def rotate_right(angle):
    fraction_of_circle = angle / 360
    required_distance = fraction_of_circle * (math.pi * WHEEL_TRACK_WIDTH)
    motor_degrees = distance_to_motor_degrees(required_distance)
    BP.set_motor_position_relative(LEFT_MOTOR, motor_degrees)
    BP.set_motor_position_relative(RIGHT_MOTOR, -motor_degrees)
    
def turn_left(angle):
    fraction_of_circle = angle / 360
    required_distance = fraction_of_circle * (math.pi * 2 * WHEEL_TRACK_WIDTH)
    motor_degrees = distance_to_motor_degrees(required_distance)
    BP.set_motor_position_relative(LEFT_MOTOR, 0)
    BP.set_motor_position_relative(RIGHT_MOTOR, motor_degrees)
    
def turn_right(angle):
    fraction_of_circle = angle / 360
    required_distance = fraction_of_circle * (math.pi * 2 * WHEEL_TRACK_WIDTH)
    motor_degrees = distance_to_motor_degrees(required_distance)
    BP.set_motor_position_relative(LEFT_MOTOR, motor_degrees)
    BP.set_motor_position_relative(RIGHT_MOTOR, 0)

def move_forward(distance):
    motor_degrees = distance_to_motor_degrees(distance)
    BP.set_motor_position_relative(LEFT_MOTOR, motor_degrees)
    BP.set_motor_position_relative(RIGHT_MOTOR, motor_degrees)

def move_backward(distance):
    motor_degrees = distance_to_motor_degrees(distance)
    BP.set_motor_position_relative(LEFT_MOTOR, -motor_degrees)
    BP.set_motor_position_relative(RIGHT_MOTOR, -motor_degrees)

def is_moving():
  return (BP.get_motor_status(LEFT_MOTOR)[3] != 0) or (BP.get_motor_status(RIGHT_MOTOR)[3] != 0)


if __name__ == "__main__":
    BP.set_motor_limits(BP.PORT_B, 45, 900)
    BP.set_motor_limits(BP.PORT_C, 45, 900)
    required_distance = float(input("Enter number of centimeters to move: "))
    try:
        print("Move forward")
        move_forward(required_distance)
        while not is_moving(): time.sleep(0.05)
        while is_moving(): time.sleep(0.1)

        print("Turn left")
        rotate_left(45)
        while not is_moving(): time.sleep(0.05)
        while is_moving(): time.sleep(0.1)

        print("Turn right")
        rotate_right(45)
        while not is_moving(): time.sleep(0.05)
        while is_moving(): time.sleep(0.1)

        print("Move backwards")
        move_backward(required_distance)
        while not is_moving(): time.sleep(0.05)
        while is_moving(): time.sleep(0.1)

        print("Reset")
        BP.reset_all()
    except KeyboardInterrupt:
        BP.reset_all()
        print ("Bye")
        
