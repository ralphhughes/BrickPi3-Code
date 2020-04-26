#!/usr/bin/env python3
#encoding: windows-1252

class Movement():
    # Constants
    WHEEL_DIAMETER = 8.2 # CM
    GEAR_RATIO = 12 / 20  # 12t:20t
    WHEEL_TRACK_WIDTH = 15.00 # CM (nice round number, what are the chances!)

    LEFT_MOTOR = BP.PORT_B
    RIGHT_MOTOR = BP.PORT_C
    def __init__(self):
        print("class init")
        
    def distance_to_motor_degrees(self, distance):
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

