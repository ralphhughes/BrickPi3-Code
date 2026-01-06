import sys,os
import curses
import math
import brickpi3

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
LA_MAX_POS = 6400 # Degrees at full extension
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

def center_text(text, scr_width):
    start_x = int((scr_width // 2) - (len(text) // 2) - len(text) % 2)
    if start_x < 0:
        start_x = 0
    return start_x

def draw_menu(stdscr):
    global la_target
    k = 0
    current_turn = 0
    current_speed = 0

    # Clear and refresh the screen for a blank canvas
    stdscr.clear()
    stdscr.refresh()

    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)


    # Loop where k is the last character pressed
    while (k != ord('q')):

        # Initialization
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        stdscr.nodelay(True)
        stdscr.timeout(50)   # 50 ms loop period (~20 Hz)

        # Which key was pressed
        if k == curses.KEY_DOWN:
            current_speed = current_speed - (1 / NUM_STEPS_SPEED)
        elif k == curses.KEY_UP:
            current_speed = current_speed + (1 / NUM_STEPS_SPEED)
        elif k == curses.KEY_RIGHT:
            current_turn = current_turn - (1 / NUM_STEPS_TURN)
        elif k == curses.KEY_LEFT:
            current_turn = current_turn + (1 / NUM_STEPS_TURN)
        elif k == 32: # Spacebar
            current_turn = 0
            current_speed = 0
            la_target = None
            BP.set_motor_power(LA_MOTOR_PORT, 0)
        elif k == ord('e'):
            la_target = LA_MAX_POS
        elif k == ord('r'):
            la_target = LA_MIN_POS


        # Clamp cursor x,y to range of (-1 to +1)
        current_turn = max(-1, current_turn)
        current_turn = min(1, current_turn)
        current_speed = max(-1, current_speed)
        current_speed = min(1, current_speed)

        left_motor, right_motor = steering(current_speed, current_turn)
        left_motor_dps = MAX_WHEEL_SPEED * 6 * left_motor
        right_motor_dps = MAX_WHEEL_SPEED * 6 * right_motor


        # Declaration of strings
        title = "Motor Controller"[:width-1]
        subtitle = "A: Left, D: Right, B: Linear Actuator (E/R/S)"[:width-1]
        #keystr = "Speed: {}%, Turn: {}%, LeftMotor: {:.1f}, RightMotor: {:.1f}".format(round(current_speed * 100, 0), round(current_turn * 100, 0), left_motor_dps, right_motor_dps)
        la_pos = BP.get_motor_encoder(LA_MOTOR_PORT)
        keystr = (
            f"Speed: {round(current_speed*100,0)}%, "
            f"Turn: {round(current_turn*100,0)}%, "
            f"LA Pos: {int(la_pos)}"
        )
        statusbarstr = "Battery Voltage: {:.3f}".format(BP.get_voltage_battery())

        if abs(round(left_motor,1)) >= (1 / NUM_STEPS_SPEED):
            BP.set_motor_dps(BP.PORT_A, left_motor_dps)
        else:
            BP.set_motor_power(BP.PORT_A, 0)

        if abs(round(right_motor,1)) >= (1 / NUM_STEPS_SPEED):
            BP.set_motor_dps(BP.PORT_D, right_motor_dps)
        else:
            BP.set_motor_power(BP.PORT_D, 0)


        # Read encoder every loop
        la_pos = BP.get_motor_encoder(LA_MOTOR_PORT)

        # Hard stop: limit switch
        try:
            if BP.get_sensor(LA_LIMIT_SENSOR):
                BP.set_motor_power(LA_MOTOR_PORT, 0)
                BP.offset_motor_encoder(LA_MOTOR_PORT, la_pos)
                la_target = None
        except brickpi3.SensorError:
            pass

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


        # Centering calculations
        start_x_title = center_text(title, width)
        start_x_subtitle = center_text(subtitle, width)
        start_x_keystr = center_text(keystr, width)
        start_y = 0


        # Render status bar
        stdscr.attron(curses.color_pair(3))
        stdscr.addstr(height-1, 0, statusbarstr)
        stdscr.addstr(height-1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
        stdscr.attroff(curses.color_pair(3))

        # Turning on attributes for title
        stdscr.attron(curses.color_pair(2))
        stdscr.attron(curses.A_BOLD)

        # Rendering title
        stdscr.addstr(start_y, start_x_title, title)

        # Turning off attributes for title
        stdscr.attroff(curses.color_pair(2))
        stdscr.attroff(curses.A_BOLD)

        # Print rest of text
        stdscr.addstr(start_y + 1, start_x_subtitle, subtitle)
        stdscr.addstr(start_y + 3, (width // 2) - 2, '-' * 4)
        stdscr.addstr(start_y + 5, start_x_keystr, keystr)



        # Refresh the screen
        stdscr.refresh()

        # Check if any key pressed
        k = stdscr.getch()

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

    # Extend actuator slightly so as to release the limit switch
    BP.set_motor_position(LA_MOTOR_PORT, 90)

def main():
    try:
        BP.set_sensor_type(LA_LIMIT_SENSOR, BP.SENSOR_TYPE.TOUCH)
        home_linear_actuator()

        curses.wrapper(draw_menu)
        BP.set_motor_power(BP.PORT_A, -128)
        BP.set_motor_power(BP.PORT_D, -128)
    except KeyboardInterrupt:
        BP.reset_all()
    finally:
        BP.reset_all()

if __name__ == "__main__":
    main()
