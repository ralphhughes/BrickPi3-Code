import socket, sys, brickpi3, time
import random
from heliostat import motor_functions



def home_inc_motor():
    M.home_inclination_axis()

    #  Test inclination axis
    M.set_mirror_inclination(-10)
    M.wait_for_motors_to_stop()
    time.sleep(5)
    for i in range(0, 100, 10):
        print("angle", i)
        M.set_mirror_inclination(i)
        M.wait_for_motors_to_stop()
        time.sleep(10)


def test_azi_motor():
    #  Test azimuth axis
    startingAngle = 90
    BP.reset_motor_encoder(AZI_MOTOR)
    M.set_mirror_azimuth(90, 315)
    M.wait_for_motors_to_stop()
    M.set_mirror_azimuth(315, 0)
    M.wait_for_motors_to_stop()

def azi_simulation():
    for i in range(1,20):
        current_angle = random.randint(0,360)
        target_angle = random.randint(0,360)
        angle_to_move = ((((target_angle - current_angle) % 360) + 540) % 360) - 180
        print(f'{current_angle}\t{target_angle}\t{angle_to_move}')

if __name__ == "__main__":

    print("Running on", socket.gethostname())

    try:
        BP = brickpi3.BrickPi3()
        BP.reset_all()
        INC_MOTOR = BP.PORT_A
        LIMIT_SWITCH = BP.PORT_3
        AZI_MOTOR = BP.PORT_D
        M = motor_functions.Movement(BP, INC_MOTOR, AZI_MOTOR, LIMIT_SWITCH)
        # home_inc_motor()
        test_azi_motor()
        # azi_simulation()

        # Float both motors
        BP.set_motor_power(INC_MOTOR, -128)
        BP.set_motor_power(AZI_MOTOR, -128)
    except KeyboardInterrupt: # Stop the motors if user pressed Ctrl+C
        BP.reset_all()
