from lib import robot_movement
import time
import os
import random
import threading
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
MOTORS_ENABLED = False

from Bluetin_Echo import Echo # https://github.com/MarkAHeywood/Bluetin_Python_Echo
# Define pin constants
TRIGGER_PIN_LEFT = 27
ECHO_PIN_LEFT = 17
TRIGGER_PIN_RIGHT = 22
ECHO_PIN_RIGHT = 23
# Initialise two HC-SR04 sensors on Pi GPIO pins.
echo = [Echo(TRIGGER_PIN_LEFT, ECHO_PIN_LEFT)
    , Echo(TRIGGER_PIN_RIGHT, ECHO_PIN_RIGHT)]

# Initialise NXT ultrasonic on BrickPi3 sensor port
BP.set_sensor_type(BP.PORT_1, BP.SENSOR_TYPE.NXT_ULTRASONIC)



def safeQuit():
    echo[0].stop()
    echo[1].stop()
    print("Both sonars stopped")
    BP.set_motor_dps(LEFT_MOTOR, 0)
    BP.set_motor_dps(RIGHT_MOTOR, 0)
    BP.reset_all()
    print("Both motors stopped")
    time.sleep(3)
    os._exit(0)

def main(name):
    last_nxt_read_time = time.time()
    try:
        if MOTORS_ENABLED:
            BP.set_motor_limits(LEFT_MOTOR, 45)
            BP.set_motor_limits(RIGHT_MOTOR, 45)
            BP.set_motor_dps(LEFT_MOTOR, 200)
            BP.set_motor_dps(RIGHT_MOTOR, 200)

        left_distance = 0
        center_distance = 0
        right_distance = 0
        while True:
            if left_distance != 255:
                left_distance = (left_distance + echo[0].read('cm')) / 2
            else:
                left_distance = echo[0].read('cm')

            time.sleep(0.2)
            if right_distance != 255:
                right_distance = (right_distance + echo[1].read('cm')) / 2
            else:
                right_distance = echo[1].read('cm')

            try:
                if (time.time() - last_nxt_read_time) > 0.2:
                    center_distance = BP.get_sensor(BP.PORT_1)
            except brickpi3.SensorError:
                print("ERROR: Can't read NXT ultrasonic sensor!")
                center_distance = 256
            time.sleep(0.2) # 0.029

            # Bluetin_Echo uses '0' as 'OutOfRange', BrickPi3 uses 255
            if left_distance == 0 or left_distance > 255:
                left_distance = 255
            if right_distance == 0 or right_distance > 255:
                right_distance = 255


            # Default action
            action = 'forward'
            
            if left_distance < 20 or right_distance < 20:
                if left_distance < right_distance:
                    action='right'
                else:
                    action='left'

            if center_distance < 20:
                action='reverse'

            print('left: {}cm\tcenter: {}cm\tright: {}cm\taction: {}'.format(
                int(left_distance), int(center_distance), int(right_distance), action)
            )

            if MOTORS_ENABLED:
                if action == 'forward':
                    BP.set_motor_dps(LEFT_MOTOR, 3 * min(left_distance,right_distance,center_distance))
                    BP.set_motor_dps(RIGHT_MOTOR, 3 * min(left_distance,right_distance,center_distance))
                elif action == 'reverse':
                    M.move_backward(30)
                    M.wait_for_motors_to_stop()
                    if random.choice([True, False]):
                        M.rotate_left(90)
                        M.wait_for_motors_to_stop()
                    else:
                        M.rotate_right(90)
                        M.wait_for_motors_to_stop()
                elif action == 'right':
                    M.rotate_right(90)
                    M.wait_for_motors_to_stop()
                elif action == 'left':
                    M.rotate_left(90)
                    M.wait_for_motors_to_stop()

    except KeyboardInterrupt:
        safeQuit()
        
if __name__ == '__main__':
    x = threading.Thread(target=main, args=(1,), daemon=True)
    x.start()
    try:
        t=input("Type any letter then press enter to quit")
    except KeyboardInterrupt:
        safeQuit()
    safeQuit()


