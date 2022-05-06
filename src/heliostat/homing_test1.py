import socket, sys, brickpi3, time

from heliostat import motor_functions

if __name__ == "__main__":

    print("Running on", socket.gethostname())

    try:
        BP = brickpi3.BrickPi3()
        BP.reset_all()
        INC_MOTOR = BP.PORT_A
        LIMIT_SWITCH = BP.PORT_3
        AZI_MOTOR = BP.PORT_D
        M = motor_functions.Movement(BP, INC_MOTOR, AZI_MOTOR, LIMIT_SWITCH)
        M.home_inclination_axis()

        #  Test inclination axis
        M.set_mirror_inclination(1)
        M.wait_for_motors_to_stop()
        M.set_mirror_inclination(70)
        M.wait_for_motors_to_stop()

        #  Test azimuth axis
        BP.reset_motor_encoder(AZI_MOTOR)
        M.set_mirror_azimuth(45)
        M.wait_for_motors_to_stop()
        M.set_mirror_azimuth(0)
        M.wait_for_motors_to_stop()

        # Float both motors
        BP.set_motor_power(INC_MOTOR, -128)
        BP.set_motor_power(AZI_MOTOR, -128)
    except KeyboardInterrupt: # Stop the motors if user pressed Ctrl+C
        BP.reset_all()



