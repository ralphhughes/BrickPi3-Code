import brickpi3
import datetime
import socket
import time

from heliostat import motor_functions
from heliostat.sun_position import sunpos

MOTORS_ENABLED = True


def get_target():
    # Prompt for target azimuth and inclination
    str_target_azimuth = input("Enter compass bearing to target in degrees")
    if not str_target_azimuth:
        target_azimuth = 0
    else:
        target_azimuth = float(str_target_azimuth)

    str_target_elevation = input("Enter elevation to target in degrees (leave blank for horizontal")
    if not str_target_elevation:
        target_elevation = 0
    else:
        target_elevation = float(str_target_elevation)
    return target_azimuth, target_elevation


if __name__ == "__main__":

    print("Running on", socket.gethostname())
    BP = brickpi3.BrickPi3()
    try:
        BP.reset_all()
        INC_MOTOR = BP.PORT_A
        LIMIT_SWITCH = BP.PORT_3
        AZI_MOTOR = BP.PORT_D
        M = motor_functions.Movement(BP, INC_MOTOR, AZI_MOTOR, LIMIT_SWITCH)

        # Hardcoded location
        location = (53.31851, -3.81203)

        # Ask user for target direction
        target_azimuth, target_inclination = get_target()

        # Home the elevation axis using the limit switch
        print("Homing inclination axis...")
        if MOTORS_ENABLED:
            M.home_inclination_axis()


        # Prompt for current azimuth
        strAzimuth = input("Please enter current azimuth? (leave blank for due north)")
        if not strAzimuth:
            current_azimuth = 0
        else:
            current_azimuth = float(strAzimuth)


        while True:
            # Calculate azimuth & inclination of sun right now for the given lat/long
            now = datetime.datetime.now(datetime.timezone.utc)
            when = (now.year, now.month, now.day, now.hour, now.minute, now.second, 0)
            # Get the Sun's apparent location in the sky
            sun_azimuth, sun_inclination = sunpos(when, location, True)

            # Bisect the azimuth and inclination angle deltas to work out mirror azimuth and inclination
            mirror_azimuth = (target_azimuth + sun_azimuth) / 2
            mirror_inclination = (target_inclination + sun_inclination) / 2

            # Print everything I've been given or calculated
            print("-" * 34)
            print("Datetime now: ", datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S'))

            print("Target Azimuth: ", target_azimuth)
            print("Target Inclination: ", target_inclination)

            print("Sun Azimuth: ", sun_azimuth)
            print("Sun Inclination: ", sun_inclination)

            print("Mirror Azimuth: ", mirror_azimuth)
            print("Mirror Inclination: ", mirror_inclination)


            # Instruct motors to move to specified position
            if MOTORS_ENABLED:
                M.set_mirror_azimuth(current_azimuth, mirror_azimuth)
                M.set_mirror_inclination(mirror_inclination)
                M.wait_for_motors_to_stop()

                # We assume the mirror is at its destination now, so save the position for next time round the loop
                current_azimuth = mirror_azimuth

                # Float both motors
                BP.set_motor_power(INC_MOTOR, -128)
                BP.set_motor_power(AZI_MOTOR, -128)
            time.sleep(60 * 5)

    except KeyboardInterrupt:  # Stop the motors if user pressed Ctrl+C
        BP.reset_all()
