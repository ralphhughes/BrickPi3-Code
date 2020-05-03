print("Stopping motors and resetting BrickPi3...")
import brickpi3
BP = brickpi3.BrickPi3()
BP.reset_all()
print("Done")