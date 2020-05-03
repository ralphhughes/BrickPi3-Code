#!/usr/bin/env python3
#encoding: windows-1252

import math
import time


"""
Wrapper round brickpi3 class to provide higher level functions
"""
class Movement():
    # Constants for current robot
    WHEEL_DIAMETER = 8.2 # CM
    GEAR_RATIO = 12 / 20  # 12t:20t
    WHEEL_TRACK_WIDTH = 15.00 # CM (nice round number, what are the chances!)
    LEFT_MOTOR = None
    RIGHT_MOTOR = None
    BP = None
    
    def __init__(self, BP, left_motor, right_motor):
        # print("class init")
        self.LEFT_MOTOR = left_motor
        self.RIGHT_MOTOR = right_motor
        self.BP = BP
        
    def drive_in_circle(self, isRightHand, radius, speed):
        """
        Sets motor speeds to drive in an un-ending circle with specified radius
        Note: radius is measured to the inner driving wheel, not the further out one.
        Note: ratio(WheelSpeed1:WheelSpeed2) = ratio(CircleRadius:(CircleRadius+TrackWidth))
        """

        if radius == 0:
            outer_wheel_speed = speed
            inner_wheel_speed = 0
        elif radius > 0:
            fraction = radius / (radius + self.WHEEL_TRACK_WIDTH)
            outer_wheel_speed = speed
            inner_wheel_speed = outer_wheel_speed * fraction

        if isRightHand:
            self.BP.set_motor_dps(self.LEFT_MOTOR, outer_wheel_speed)
            self.BP.set_motor_dps(self.RIGHT_MOTOR, inner_wheel_speed)
        else:
            self.BP.set_motor_dps(self.LEFT_MOTOR, inner_wheel_speed)
            self.BP.set_motor_dps(self.RIGHT_MOTOR, outer_wheel_speed)

    def _distance_to_motor_degrees(self, distance):
        wheel_circumference = math.pi * self.WHEEL_DIAMETER
        num_wheel_revolutions = distance / wheel_circumference
        num_motor_revolutions = num_wheel_revolutions / self.GEAR_RATIO
        motor_degrees = 360 * num_motor_revolutions
        # print("    motor_degrees: {}".format(motor_degrees))
        return motor_degrees

    def rotate_left(self, angle):
        """
        Rotates the robot on the spot by the angle in degrees by rotating one
        motor forward and the other backward by an equal amount.
        """
        fraction_of_circle = angle / 360
        required_distance = fraction_of_circle * (math.pi * self.WHEEL_TRACK_WIDTH)
        motor_degrees = self._distance_to_motor_degrees(required_distance)
        self.BP.set_motor_position_relative(self.LEFT_MOTOR, motor_degrees)
        self.BP.set_motor_position_relative(self.RIGHT_MOTOR, -motor_degrees)

    def rotate_right(self, angle):
        """
        Rotates the robot on the spot by the angle in degrees by rotating one
        motor forward and the other backward by an equal amount.
        """
        fraction_of_circle = angle / 360
        required_distance = fraction_of_circle * (math.pi * self.WHEEL_TRACK_WIDTH)
        motor_degrees = self._distance_to_motor_degrees(required_distance)
        self.BP.set_motor_position_relative(self.LEFT_MOTOR, -motor_degrees)
        self.BP.set_motor_position_relative(self.RIGHT_MOTOR, motor_degrees)

    def turn_left(self, angle):
        """
        Turns the robot by stopping one wheel and driving the wheel on the opposite side
        by a certain amount.
        """
        fraction_of_circle = angle / 360
        required_distance = fraction_of_circle * (math.pi * 2 * self.WHEEL_TRACK_WIDTH)
        motor_degrees = self._distance_to_motor_degrees(required_distance)
        self.BP.set_motor_position_relative(self.LEFT_MOTOR, 0)
        self.BP.set_motor_position_relative(self.RIGHT_MOTOR, motor_degrees)

    def turn_right(self, angle):
        """
        Turns the robot by stopping one wheel and driving the wheel on the opposite side
        by a certain amount.
        """
        fraction_of_circle = angle / 360
        required_distance = fraction_of_circle * (math.pi * 2 * self.WHEEL_TRACK_WIDTH)
        motor_degrees = self._distance_to_motor_degrees(required_distance)
        self.BP.set_motor_position_relative(self.LEFT_MOTOR, motor_degrees)
        self.BP.set_motor_position_relative(self.RIGHT_MOTOR, 0)

    def move_forward(self, distance):
        motor_degrees = self._distance_to_motor_degrees(distance)
        self.BP.set_motor_position_relative(self.LEFT_MOTOR, motor_degrees)
        self.BP.set_motor_position_relative(self.RIGHT_MOTOR, motor_degrees)

    def move_backward(self, distance):
        motor_degrees = self._distance_to_motor_degrees(distance)
        self.BP.set_motor_position_relative(self.LEFT_MOTOR, -motor_degrees)
        self.BP.set_motor_position_relative(self.RIGHT_MOTOR, -motor_degrees)

    def stop_both(self):
        self.BP.set_motor_position_relative(self.LEFT_MOTOR, 0)
        self.BP.set_motor_position_relative(self.RIGHT_MOTOR, 0)


    def wait_for_motors_to_stop(self, timeout_seconds = 10):
        """
        This function pauses (time.sleep) until the motors have stopped moving. This
        is useful for blocking execution until the motors have rotated to a specified
        angle.

        Note: Includes timeouts, so only designed for use with turn_left\right,
        rotate_left\right functions, move_forward or move_backward functions.
        """
        timeout_time_to_start = time.time() + 0.5
        while not self.is_moving(): 
            time.sleep(0.05)
            if time.time() > timeout_time_to_start:
                print("WARN: Timeout waiting for motors to start")
                break
        timeout_time_to_stop = time.time() + timeout_seconds
        while self.is_moving(): 
            time.sleep(0.1)
            if time.time() > timeout_time_to_stop:
                print("WARN: Timeout waiting for motors to stop")
                break

    def is_moving(self):
      return (self.BP.get_motor_status(self.LEFT_MOTOR)[3] != 0) or (self.BP.get_motor_status(self.RIGHT_MOTOR)[3] != 0)

    
if __name__ == "__main__":
    print("Class must be instantiated")