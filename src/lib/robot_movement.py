#!/usr/bin/env python3
#encoding: windows-1252

import math
import time

class Movement():
    # Constants
    WHEEL_DIAMETER = 8.2 # CM
    GEAR_RATIO = 12 / 20  # 12t:20t
    WHEEL_TRACK_WIDTH = 15.00 # CM (nice round number, what are the chances!)
    LEFT_MOTOR = None
    RIGHT_MOTOR = None
    BP = None
    
    def __init__(self, BP):
        print("class init")
        self.LEFT_MOTOR = BP.PORT_B
        self.RIGHT_MOTOR = BP.PORT_C
        self.BP = BP
        
        
    def distance_to_motor_degrees(self, distance):
        wheel_circumference = math.pi * self.WHEEL_DIAMETER
        num_wheel_revolutions = distance / wheel_circumference
        num_motor_revolutions = num_wheel_revolutions / self.GEAR_RATIO
        motor_degrees = 360 * num_motor_revolutions
        print("    motor_degrees: {}".format(motor_degrees))
        return motor_degrees

    def rotate_left(self, angle):
        fraction_of_circle = angle / 360
        required_distance = fraction_of_circle * (math.pi * self.WHEEL_TRACK_WIDTH)
        motor_degrees = self.distance_to_motor_degrees(required_distance)
        self.BP.set_motor_position_relative(self.LEFT_MOTOR, -motor_degrees)
        self.BP.set_motor_position_relative(self.RIGHT_MOTOR, motor_degrees)

    def rotate_right(self, angle):
        fraction_of_circle = angle / 360
        required_distance = fraction_of_circle * (math.pi * self.WHEEL_TRACK_WIDTH)
        motor_degrees = self.distance_to_motor_degrees(required_distance)
        self.BP.set_motor_position_relative(self.LEFT_MOTOR, motor_degrees)
        self.BP.set_motor_position_relative(self.RIGHT_MOTOR, -motor_degrees)

    def turn_left(self, angle):
        fraction_of_circle = angle / 360
        required_distance = fraction_of_circle * (math.pi * 2 * self.WHEEL_TRACK_WIDTH)
        motor_degrees = self.distance_to_motor_degrees(required_distance)
        self.BP.set_motor_position_relative(self.LEFT_MOTOR, 0)
        self.BP.set_motor_position_relative(self.RIGHT_MOTOR, motor_degrees)

    def turn_right(self, angle):
        fraction_of_circle = angle / 360
        required_distance = fraction_of_circle * (math.pi * 2 * self.WHEEL_TRACK_WIDTH)
        motor_degrees = self.distance_to_motor_degrees(required_distance)
        self.BP.set_motor_position_relative(self.LEFT_MOTOR, motor_degrees)
        self.BP.set_motor_position_relative(self.RIGHT_MOTOR, 0)

    def move_forward(self, distance):
        motor_degrees = self.distance_to_motor_degrees(distance)
        self.BP.set_motor_position_relative(self.LEFT_MOTOR, motor_degrees)
        self.BP.set_motor_position_relative(self.RIGHT_MOTOR, motor_degrees)

    def move_backward(self, distance):
        motor_degrees = self.distance_to_motor_degrees(distance)
        self.BP.set_motor_position_relative(self.LEFT_MOTOR, -motor_degrees)
        self.BP.set_motor_position_relative(self.RIGHT_MOTOR, -motor_degrees)

    def wait_for_motors_to_stop(self):
        timeout_time_start = time.time() + 0.5
        while not self.is_moving(): 
            time.sleep(0.05)
            if time.time() > timeout_time_start:
                print("WARN: Timeout waiting for motors to start")
                break
        timeout_time_stop = time.time() + 10        
        while self.is_moving(): 
            time.sleep(0.1)
            if time.time() > timeout_time_stop:
                print("WARN: Timeout waiting for motors to stop")
                break

    def is_moving(self):
      return (self.BP.get_motor_status(self.LEFT_MOTOR)[3] != 0) or (self.BP.get_motor_status(self.RIGHT_MOTOR)[3] != 0)

    
if __name__ == "__main__":
    print("Class must be instantiated")