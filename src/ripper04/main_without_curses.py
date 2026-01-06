import sys,os
import termios
import tty
import select
import math
import brickpi3
import time

# Global
BP = brickpi3.BrickPi3()

# Constants
MAX_WHEEL_SPEED = 160 # RPM
NUM_STEPS_SPEED = 10  # Number of keypresses between stopped and max_wheel_speed
NUM_STEPS_TURN = 10 # Number of keypresses between straight ahead and full left or right

# Linear actuator configuration
LA_MOTOR_PORT = BP.PORT_B
LA_LIMIT_SENSOR = BP.PORT_4

LA_MIN_POS = 0
LA_MAX_POS = 7500 # Degrees at full extension would in theory be 9360 but we lose some to the limit switch
LA_SPEED_DPS = 400



# Actuator state
la_target = None   # None = idle, otherwise target encoder position



def steering(x, y):
    # convert to polar
    r = math.hypot(x, y)
    t = math.atan2(y, x)

    # rotate by 45 degrees
    t += math.pi / 4

    # back to cartesian
    left = r * math.cos(t)
    right = r * math.sin(t)

    # rescale the new coords
    left = left * math.sqrt(2)
    right = right * math.sqrt(2)

    # clamp to -1/+1
    left = max(-1, min(left, 1))
    right = max(-1, min(right, 1))

    return left, right

def control_loop():
    global la_target
    k = 0
    current_turn = 0
    current_speed = 0


    # Loop where k is the last character pressed
    while (k != 'q'):

        # Which key was pressed
        if k == 's':
            current_speed = current_speed - (1 / NUM_STEPS_SPEED)
        elif k == 'w':
            current_speed = current_speed + (1 / NUM_STEPS_SPEED)
        elif k == 'd':
            current_turn = current_turn - (1 / NUM_STEPS_TURN)
        elif k == 'a':
            current_turn = current_turn + (1 / NUM_STEPS_TURN)
        elif k == ' ': # Spacebar
            current_turn = 0
            current_speed = 0
            la_target = None
            BP.set_motor_power(LA_MOTOR_PORT, 0)
        elif k == 'e':
            la_target = LA_MAX_POS
        elif k == 'r':
            la_target = LA_MIN_POS


        # Clamp cursor x,y to range of (-1 to +1)
        current_turn = max(-1, current_turn)
        current_turn = min(1, current_turn)
        current_speed = max(-1, current_speed)
        current_speed = min(1, current_speed)

        left_motor, right_motor = steering(current_speed, current_turn)
        left_motor_dps = MAX_WHEEL_SPEED * 6 * left_motor # DPS = RPM * 360 deg/60s = 6 * RPM
        right_motor_dps = MAX_WHEEL_SPEED * 6 * right_motor

        # Linear actuator logic
        la_pos = update_linear_actuator()


        write_at(1, 1, f"Speed: {round(current_speed*100):.1f}%   ")
        write_at(2, 1, f"Turn:  {round(current_turn*100):.1f}%   ")
        write_at(3, 1, f"Left:  {left_motor_dps:.1f} dps   ")
        write_at(4, 1, f"Right: {right_motor_dps:.1f} dps   ")
        write_at(5, 1, f"LA pos: {int(la_pos):6d}   ")
        write_at(6, 1, f"Target: {la_target}   ")
        write_at(7, 1, f"Batt:  {BP.get_voltage_battery():5.3f} V   ")


        if abs(round(left_motor,1)) >= (1 / NUM_STEPS_SPEED):
            BP.set_motor_dps(BP.PORT_A, left_motor_dps)
        else:
            BP.set_motor_power(BP.PORT_A, 0)

        if abs(round(right_motor,1)) >= (1 / NUM_STEPS_SPEED):
            BP.set_motor_dps(BP.PORT_D, right_motor_dps)
        else:
            BP.set_motor_power(BP.PORT_D, 0)



        # Check if any key pressed
        k = read_key()


def update_linear_actuator():
    global la_target

    # Read encoder every loop
    la_pos = BP.get_motor_encoder(LA_MOTOR_PORT)

    # Hard stop: limit switch
    try:
        if BP.get_sensor(LA_LIMIT_SENSOR):
            BP.set_motor_power(LA_MOTOR_PORT, 0)
            BP.offset_motor_encoder(LA_MOTOR_PORT, la_pos)
            la_target = None
        return la_pos
    except brickpi3.SensorError:
        pass

    if la_target is None:
        return la_pos

    # Soft limits
    if la_pos <= LA_MIN_POS and la_target == LA_MIN_POS:
        BP.set_motor_power(LA_MOTOR_PORT, 0)
        la_target = None

    elif la_pos >= LA_MAX_POS and la_target == LA_MAX_POS:
        BP.set_motor_power(LA_MOTOR_PORT, 0)
        la_target = None

    # Motion control
    if la_target is not None:
        error = la_target - la_pos

        if abs(error) < 5:
            BP.set_motor_power(LA_MOTOR_PORT, 0)
            la_target = None
        else:
            direction = 1 if error > 0 else -1
            BP.set_motor_dps(LA_MOTOR_PORT, direction * LA_SPEED_DPS)


    return la_pos

def home_linear_actuator():
    # Drive actuator towards retract until limit switch is hit
    BP.set_motor_dps(LA_MOTOR_PORT, -LA_SPEED_DPS)

    while True:
        try:
            if BP.get_sensor(LA_LIMIT_SENSOR):
                break
        except brickpi3.SensorError:
            pass

    BP.set_motor_power(LA_MOTOR_PORT, 0)

    # Zero encoder at home
    BP.offset_motor_encoder(
        LA_MOTOR_PORT,
        BP.get_motor_encoder(LA_MOTOR_PORT)
    )
    time.sleep(0.5)

    # Extend actuator slightly so as to release the limit switch
    BP.set_motor_position(LA_MOTOR_PORT, 360)
    time.sleep(2)
    BP.set_motor_power(LA_MOTOR_PORT, 0)

def hide_cursor():
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()

def show_cursor():
    sys.stdout.write("\033[?25h")
    sys.stdout.flush()

def write_at(row, col, text):
    sys.stdout.write(f"\033[{row};{col}H{text}")
    sys.stdout.flush()

def get_key():
    if select.select([sys.stdin], [], [], 0)[0]:
        return sys.stdin.read(1)
    return None

def read_key():
    c = get_key()
    if c is None:
        return None

    if c == '\x1b':  # escape
        if get_key() == '[':
            return get_key()  # A, B, C, D etc
        return None

    return c


def main():
    try:
        stdin_fd = sys.stdin.fileno()
        old_term_settings = termios.tcgetattr(stdin_fd)
        tty.setcbreak(stdin_fd)
        hide_cursor()
        print(chr(27) + "[2J") # Clear screen

        BP.set_sensor_type(LA_LIMIT_SENSOR, BP.SENSOR_TYPE.TOUCH)
        home_linear_actuator()

        print("\n" * 8)   # reserve 8 lines for status output
        print("WASD keys to move, spacebar to stop all motors, E/R to extend/retract linear actuator, Q to quit.")

        control_loop()

        BP.set_motor_power(BP.PORT_A, -128)
        BP.set_motor_power(BP.PORT_D, -128)
    except KeyboardInterrupt:
        BP.reset_all()
    finally:
        BP.reset_all()
        termios.tcsetattr(stdin_fd, termios.TCSADRAIN, old_term_settings)
        show_cursor()
        sys.stdout.flush()
        print()   # move cursor to clean line


if __name__ == "__main__":
    main()
