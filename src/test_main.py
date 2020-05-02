from lib import robot_movement

# Testing environment dependent importing
import platform
if platform.system() == 'Windows':
    from lib import brickpi3_mock
    BP = brickpi3_mock.BrickPi3()
elif platform.system() == 'Linux':
    import brickpi3
    BP = brickpi3.BrickPi3()


from time import sleep

from Bluetin_Echo import Echo # https://github.com/MarkAHeywood/Bluetin_Python_Echo

# Define pin constants
TRIGGER_PIN_LEFT = 27
ECHO_PIN_LEFT = 17
TRIGGER_PIN_RIGHT = 22
ECHO_PIN_RIGHT = 23

# Initialise two sensors.
echo = [Echo(TRIGGER_PIN_LEFT, ECHO_PIN_LEFT)
        , Echo(TRIGGER_PIN_RIGHT, ECHO_PIN_RIGHT)]

def main():
    try:
        M = robot_movement.Movement(BP)
        BP.set_motor_limits(BP.PORT_B, 45, 900)
        BP.set_motor_limits(BP.PORT_C, 45, 900)
        
        BP.set_motor_dps(BP.PORT_B, 400)
        BP.set_motor_dps(BP.PORT_B, 400)
        while True:

            left_distance = echo[0].read('cm', 3)
            sleep(0.029) # 29 ms
            right_distance = echo[1].read('cm', 3)
            sleep(0.029) # 29 ms
            print('left: {}cm\tright: {}cm'.format(round(left_distance,1), round(right_distance,1)))

            if (left_distance > 5 and left_distance < 20):
                if (right_distance > 5 and right_distance < 20):
                    M.stop_both()
                    break
                    
            if (left_distance > 5 and left_distance < 20):
                M.rotate_right(90)
                M.wait_for_motors_to_stop()
                
            if (right_distance > 5 and right_distance < 20):
                M.rotate_left(90)
                M.wait_for_motors_to_stop()
                
    except KeyboardInterrupt:
        echo[0].stop()
        BP.reset_all()
        print("Measurement stopped by User")

if __name__ == '__main__':
    main()


#M.rotate_left(45)
#M.wait_for_motors_to_stop()
#M.rotate_right(45)
#M.wait_for_motors_to_stop()
