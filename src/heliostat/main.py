import brickpi3
import datetime
import socket
import time
from configparser import ConfigParser
from heliostat import motor_functions
from heliostat.sun_position import sunpos

MOTORS_ENABLED = True


def get_float_from_user(message, default_value):
    str_user_input = input(message)
    if not str_user_input:
        my_float = default_value
    else:
        my_float = float(str_user_input)
    return my_float


if __name__ == "__main__":

    print("Running on", socket.gethostname())
    BP = brickpi3.BrickPi3()

    config = ConfigParser()
    config.read('heliostat.ini')
    if not config.has_section('main'):
        config.add_section("main")
    if not config.has_option('main', 'last_moved'):
        config.set('main', 'target_azimuth', '180.5')
        config.set('main', "target_inclination", "42.0")
        config.set('main', "mirror_azimuth", "0")
        config.set('main', "last_moved", "None")

    try:
        BP.reset_all()
        M = motor_functions.Movement(BP)

        # Hardcoded location
        location = (53.31851, -3.81203)

        # Ask user for target direction
        last_target_azimuth = config.get("main", "target_azimuth")
        target_azimuth = get_float_from_user("Enter target azimuth (default is " + last_target_azimuth + ")", last_target_azimuth)

        last_target_inclination = config.get("main", "target_inclination")
        target_inclination = get_float_from_user("Enter target inclination (default is " + last_target_inclination + ")", last_target_inclination)

        # Home the elevation axis using the limit switch
        print("Homing inclination axis...")
        if MOTORS_ENABLED:
            M.home_inclination_axis()

        # Prompt for current azimuth
        last_mirror_azimuth = config.get("main", "mirror_azimuth")
        current_azimuth = get_float_from_user("Enter mirror azimuth default is (" + last_mirror_azimuth + ")", last_mirror_azimuth)

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

                # Serialise in case of power loss
                config.set('main', 'mirror_azimuth', str(mirror_azimuth))
                config.set('main', 'mirror_inclination', str(mirror_inclination))
                config.set('main', 'target_azimuth', str(target_azimuth))
                config.set('main', 'target_inclination', str(target_inclination))
                config.set('main', 'last_moved', datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
                with open('heliostat.ini', 'w') as f:
                    config.write(f)

                # Float both motors
                M.float_motors()
            time.sleep(60)

    except KeyboardInterrupt:  # Stop the motors if user pressed Ctrl+C
        BP.reset_all()
