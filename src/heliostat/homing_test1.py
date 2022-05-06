import socket, sys, time, brickpi3

print("Running on", socket.gethostname())

try:
    BP = brickpi3.BrickPi3()
    BP.reset_all()
    INC_MOTOR = BP.PORT_A
    LIMIT_SWITCH = BP.PORT_3
    AZI_MOTOR = BP.PORT_D

    BP.set_sensor_type(LIMIT_SWITCH, BP.SENSOR_TYPE.TOUCH)
    time.sleep(0.1) # gives time for sensor to be configured


    BP.set_motor_power(INC_MOTOR, 20) # Winch in at 20% power
    is_pressed = 0
    while is_pressed == 0:
        try:
            is_pressed = BP.get_sensor(LIMIT_SWITCH)
        except brickpi3.SensorError as error:
            print(error)

        time.sleep(0.02)
    BP.set_motor_power(INC_MOTOR, 0) # stop motor
    BP.reset_motor_encoder(INC_MOTOR) # Set this position as "0" on the motors encoder
    BP.set_motor_position_relative(INC_MOTOR, -300) # 1500 degrees of motor is approx 90 degrees of mirror (50:3 reduction)

except KeyboardInterrupt: # Stop the motors if user pressed Ctrl+C
    BP.reset_all()

sys.exit()

