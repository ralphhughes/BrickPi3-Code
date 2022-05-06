# Standalone test for using BrickPi to move\rotate a certain distance\angle

import math
import time
from lib import robot_movement
import platform
if platform.system() == 'Windows':
    from lib import brickpi3_mock
    BP = brickpi3_mock.BrickPi3()
elif platform.system() == 'Linux':
    import brickpi3
    BP = brickpi3.BrickPi3()


LEFT_MOTOR = BP.PORT_B
RIGHT_MOTOR = BP.PORT_C
M = robot_movement.Movement(BP, LEFT_MOTOR, RIGHT_MOTOR)


if __name__ == "__main__":
    BP.set_motor_limits(BP.PORT_B, 45, 900)
    BP.set_motor_limits(BP.PORT_C, 45, 900)
    required_distance = float(input("Enter number of centimeters to move: "))
    try:
        print("Move forward")
        M.move_forward(required_distance)
        M.wait_for_motors_to_stop()
        M.drive_in_circle(True, 30, 300)
        time.sleep(15)
        M.stop_both()
        print("Reset")
        BP.reset_all()
    except KeyboardInterrupt:
        BP.reset_all()
        print ("Bye")
        
