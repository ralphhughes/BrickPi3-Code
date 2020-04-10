import sys,os
import curses
import math
import brickpi3

# Global
BP = brickpi3.BrickPi3()

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


def draw_menu(stdscr):
    k = 0
    cursor_x = 0
    cursor_y = 0

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

        if k == curses.KEY_DOWN:
            cursor_y = cursor_y - .1
        elif k == curses.KEY_UP:
            cursor_y = cursor_y + .1
        elif k == curses.KEY_RIGHT:
            cursor_x = cursor_x + .1
        elif k == curses.KEY_LEFT:
            cursor_x = cursor_x - .1

        # Clamp cursorx,y to range of (-1 to +1)
        cursor_x = max(-1, cursor_x)
        cursor_x = min(1, cursor_x)
        cursor_y = max(-1, cursor_y)
        cursor_y = min(1, cursor_y)

        left_motor, right_motor = steering(cursor_y, cursor_x)
        left_motor_dps = 960 * left_motor
        right_motor_dps = 960 * right_motor


        # Declaration of strings
        title = "Motor Controller using keyboard"[:width-1]
        subtitle = "Attach servomotors to BrickPi3 ports A and D, use arrow keys to control them"[:width-1]
        keystr = "Last key pressed: {}".format(k)[:width-1]
        statusbarstr = "Press 'q' to exit | STATUS BAR | Speed: {:.1f}, Turn: {:.1f}, LeftMotor: {:.1f}, RightMotor: {:.1f}".format(cursor_y, cursor_x, left_motor_dps, right_motor_dps)
        if k == 0:
            keystr = "No key press detected..."[:width-1]

        if abs(round(left_motor,1)) > 0.05:
            BP.set_motor_dps(BP.PORT_A, left_motor_dps)
        else:
            keystr=keystr + "left stopped"
            BP.set_motor_power(BP.PORT_A, -128)

        if abs(round(right_motor,1)) > 0.05:
            BP.set_motor_dps(BP.PORT_D, right_motor_dps)
        else:
            keystr = keystr + "right stopped"
            BP.set_motor_power(BP.PORT_D, -128)

        # Centering calculations
        start_x_title = int((width // 2) - (len(title) // 2) - len(title) % 2)
        start_x_subtitle = int((width // 2) - (len(subtitle) // 2) - len(subtitle) % 2)
        start_x_keystr = int((width // 2) - (len(keystr) // 2) - len(keystr) % 2)
        start_y = int((height // 2) - 2)

        # Rendering some text
        whstr = "Width: {}, Height: {}".format(width, height)
        stdscr.addstr(0, 0, whstr, curses.color_pair(1))

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

        # Wait for next input
        k = stdscr.getch()

def main():
    try:
        curses.wrapper(draw_menu)
        BP.set_motor_power(BP.PORT_A, -128)
        BP.set_motor_power(BP.PORT_D, -128)
    except KeyboardInterrupt:
        BP.reset_all()

if __name__ == "__main__":
    main()
