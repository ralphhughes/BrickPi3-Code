import sys,os
import curses
import math
import brickpi3

# Global
BP = brickpi3.BrickPi3()

def center_text(text, scr_width):
    start_x = int((scr_width // 2) - (len(text) // 2) - len(text) % 2)
    if start_x < 0:
        start_x = 0
    return start_x

def draw_menu(stdscr):
    k = 0
    current_motor = 1
    current_power = 0

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
            current_power -= 5
        elif k == curses.KEY_UP:
            current_power += 5
        elif k == curses.KEY_RIGHT:
            current_motor += 1
        elif k == curses.KEY_LEFT:
            current_motor -= 1
        elif k == 32: # Spacebar
            BP.reset_all()
            current_power = 0

        current_power = max(-100, current_power)
        current_power = min(100, current_power)
        current_motor = max(1, current_motor)
        current_motor = min(4, current_motor)


        # Declaration of strings
        title = "Motor Controller"[:width-1]
        subtitle = "subtitle"[:width-1]
        keystr = "current_motor: {}, current_power: {}".format(current_motor, current_power)
        statusbarstr = "Battery Voltage: {:.3f}".format(BP.get_voltage_battery())

        if current_motor == 1:
            BP.set_motor_power(BP.PORT_A, current_power)
        elif current_motor == 2:
            BP.set_motor_power(BP.PORT_B, current_power)
        elif current_motor == 3:
            BP.set_motor_power(BP.PORT_C, current_power)
        elif current_motor == 4:
            BP.set_motor_power(BP.PORT_D, current_power)



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

        # Wait for next input
        k = stdscr.getch()

def main():
    try:
        curses.wrapper(draw_menu)
        BP.set_motor_power(BP.PORT_A, -128)
        BP.set_motor_power(BP.PORT_B, -128)
        BP.set_motor_power(BP.PORT_C, -128)
        BP.set_motor_power(BP.PORT_D, -128)
    except KeyboardInterrupt:
        BP.reset_all()

if __name__ == "__main__":
    main()
