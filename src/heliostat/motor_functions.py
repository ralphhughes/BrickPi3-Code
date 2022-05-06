import time

import brickpi3


class Movement:
    # Constants for current robot
    INC_MOTOR = None
    INC_SPEED = 350
    AZI_MOTOR = None
    AZI_SPEED = 200
    LIMIT_SWITCH = None
    BP = None
    WHEEL_DIA = 43 # mm
    BASE_DIA = 225 # mm

    def __init__(self, bp, inc_motor, azi_motor, limit_switch):
        # print("class init")
        self.INC_MOTOR = inc_motor
        self.AZI_MOTOR = azi_motor
        self.LIMIT_SWITCH = limit_switch
        self.BP = bp

    def home_inclination_axis(self):
        """

        """
        self.BP.set_sensor_type(self.LIMIT_SWITCH, self.BP.SENSOR_TYPE.TOUCH)
        time.sleep(0.1)  # gives time for sensor to be configured


        self.BP.set_motor_power(self.INC_MOTOR, 20)     # Winch in at 20% power
        is_pressed = 0
        while is_pressed == 0:
            try:
                is_pressed = self.BP.get_sensor(self.LIMIT_SWITCH)
            except brickpi3.SensorError as error:
                print(error)

            time.sleep(0.02)

        self.BP.set_motor_power(self.INC_MOTOR, 0)      # Stop the motor
        self.BP.reset_motor_encoder(self.INC_MOTOR)     # Set this position as "0" on the motors encoder
        self.BP.set_motor_limits(self.INC_MOTOR, 0, self.INC_SPEED)     # Remove the power limit and set speed limit for future moves

    def set_mirror_inclination(self, inc_angle):
        if 0 <= inc_angle < 90:
            # 1500 degrees of motor is approx 90 degrees of mirror (50:3 reduction)
            motor_degrees = -(90-inc_angle) * (50/3)
            self.BP.set_motor_position(self.INC_MOTOR, motor_degrees)

    def set_mirror_azimuth(self, target_bearing):
        #  1 degree of motor rotates the base (360/68.8)=5.23ish degrees
        self.BP.set_motor_limits(self.AZI_MOTOR, 0, self.AZI_SPEED)
        motor_degrees_per_base_degree = (self.BASE_DIA / self.WHEEL_DIA)
        self.BP.set_motor_position(self.AZI_MOTOR, target_bearing * motor_degrees_per_base_degree)

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
      return (self.BP.get_motor_status(self.INC_MOTOR)[3] != 0) or (self.BP.get_motor_status(self.AZI_MOTOR)[3] != 0)
