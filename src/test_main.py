from lib import robot_movement

# Testing environment dependent importing
import platform
if platform.system() == 'Windows':
    from lib import brickpi3_mock
    BP = brickpi3_mock.BrickPi3()
elif platform.system() == 'Linux':
    import brickpi3
    BP = brickpi3.BrickPi3()


# Testing robot_movement wrapper class   
M = robot_movement.Movement(BP)
M.rotate_left(45)
M.wait_for_motors_to_stop()
M.rotate_right(45)
M.wait_for_motors_to_stop()
