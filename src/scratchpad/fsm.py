#!/usr/bin/env python3
#encoding: windows-1252
import brickpi3
import math
import time

# Global
BP = brickpi3.BrickPi3()

# Constants
WHEEL_DIAMETER = 8.2 # CM
GEAR_RATIO = 12 / 20  # 12t:20t
WHEEL_TRACK_WIDTH = 15.00 # CM (nice round number, what are the chances!)

LEFT_MOTOR = BP.PORT_B
RIGHT_MOTOR = BP.PORT_C

def mowing():
    print("mowing")
    
def turnLeft():
    print("left")
    
def turnRight():
    print("right")
    
def quitting():
    print("quitting")
    quit()
    
currentState = 0

states = {
    0: mowing,
    1: turnLeft,
    2: turnRight,
    3: quitting
}


if __name__ == "__main__":
    func = states.get(currentState)
    func()


