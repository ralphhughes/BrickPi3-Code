# Mock class for running code on windows

# Made by coping the original from:
# https://www.dexterindustries.com/BrickPi/
# https://github.com/DexterInd/BrickPi3
#
# Copyright (c) 2017 Dexter Industries
# Released under the MIT license (http://choosealicense.com/licenses/mit/).
# For more information see https://github.com/DexterInd/BrickPi3/blob/master/LICENSE.md
#
# Python drivers for the BrickPi3




class Enumeration(object):
    def __init__(self, names):  # or *names, with no .split()
        number = 0
        for line, name in enumerate(names.split('\n')):
            if name.find(",") >= 0:
                # strip out the spaces
                while(name.find(" ") != -1):
                    name = name[:name.find(" ")] + name[(name.find(" ") + 1):]

                # strip out the commas
                while(name.find(",") != -1):
                    name = name[:name.find(",")] + name[(name.find(",") + 1):]

                # if the value was specified
                if(name.find("=") != -1):
                    number = int(float(name[(name.find("=") + 1):]))
                    name = name[:name.find("=")]

                # optionally print to confirm that it's working correctly
                #print "%40s has a value of %d" % (name, number)

                setattr(self, name, number)
                number = number + 1


class FirmwareVersionError(Exception):
    """Exception raised if the BrickPi3 firmware needs to be updated"""


class SensorError(Exception):
    """Exception raised if a sensor is not yet configured when trying to read it with get_sensor"""


def set_address(address, id):
    print("mock: set_address")


class BrickPi3(object):
    PORT_1 = 0x01
    PORT_2 = 0x02
    PORT_3 = 0x04
    PORT_4 = 0x08

    PORT_A = 0x01
    PORT_B = 0x02
    PORT_C = 0x04
    PORT_D = 0x08

    MOTOR_FLOAT = -128

    SensorType = [0, 0, 0, 0]
    I2CInBytes = [0, 0, 0, 0]

    SENSOR_TYPE = Enumeration("""
        NONE = 1,
        I2C,
        CUSTOM,

        TOUCH,
        NXT_TOUCH,
        EV3_TOUCH,

        NXT_LIGHT_ON,
        NXT_LIGHT_OFF,

        NXT_COLOR_RED,
        NXT_COLOR_GREEN,
        NXT_COLOR_BLUE,
        NXT_COLOR_FULL,
        NXT_COLOR_OFF,

        NXT_ULTRASONIC,

        EV3_GYRO_ABS,
        EV3_GYRO_DPS,
        EV3_GYRO_ABS_DPS,

        EV3_COLOR_REFLECTED,
        EV3_COLOR_AMBIENT,
        EV3_COLOR_COLOR,
        EV3_COLOR_RAW_REFLECTED,
        EV3_COLOR_COLOR_COMPONENTS,

        EV3_ULTRASONIC_CM,
        EV3_ULTRASONIC_INCHES,
        EV3_ULTRASONIC_LISTEN,

        EV3_INFRARED_PROXIMITY,
        EV3_INFRARED_SEEK,
        EV3_INFRARED_REMOTE,
    """)

    SENSOR_STATE = Enumeration("""
        VALID_DATA,
        NOT_CONFIGURED,
        CONFIGURING,
        NO_DATA,
        I2C_ERROR,
    """)

    SENSOR_CUSTOM = Enumeration("""
        PIN1_9V,
        PIN5_OUT,
        PIN5_STATE,
        PIN6_OUT,
        PIN6_STATE,
        PIN1_ADC,
        PIN6_ADC,
    """)

    
    MOTOR_STATUS_FLAG = Enumeration("""
        LOW_VOLTAGE_FLOAT,
        OVERLOADED,
    """)

    MOTOR_STATUS_FLAG.LOW_VOLTAGE_FLOAT = 0x01 # If the motors are floating due to low battery voltage
    MOTOR_STATUS_FLAG.OVERLOADED        = 0x02 # If the motors aren't close to the target (applies to position control and dps speed control).

    
    def __init__(self, addr = 1, detect = True): # Configure for the BrickPi. Optionally set the address (default to 1). Optionally disable detection (default to detect).
        """
        Do any necessary configuration, and optionally detect the BrickPi3

        Optionally specify the SPI address as something other than 1
        Optionally disable the detection of the BrickPi3 hardware. This can be used for debugging and testing when the BrickPi3 would otherwise not pass the detection tests.
        """

        if addr < 1 or addr > 255:
            raise IOError("error: SPI address must be in the range of 1 to 255")
            return

        self.SPI_Address = addr
    
    def spi_transfer_array(self, data_out):
        """
        Conduct a SPI transaction

        Keyword arguments:
        data_out -- a list of bytes to send. The length of the list will determine how many bytes are transferred.

        Returns a list of the bytes read.
        """
        return False


    def spi_read_16(self, MessageType):
        """
        Read a 16-bit value over SPI

        Keyword arguments:
        MessageType -- the SPI message type

        Returns:
        value
        """
        reply = False
        if(reply[3] == 0xA5):
            return int((reply[4] << 8) | reply[5])
        raise IOError("No SPI response")
        return

    def spi_write_16(self, MessageType, Value):
        """
        Send a 16-bit value over SPI

        Keyword arguments:
        MessageType -- the SPI message type
        Value -- the value to be sent
        """
        outArray = False

    def spi_write_24(self, MessageType, Value):
        """
        Send a 24-bit value over SPI

        Keyword arguments:
        MessageType -- the SPI message type
        Value -- the value to be sent
        """
        outArray = False

    def spi_read_32(self, MessageType):
        """
        Read a 32-bit value over SPI

        Keyword arguments:
        MessageType -- the SPI message type

        Returns :
        value
        """
        
        return False

    def spi_write_32(self, MessageType, Value):
       return False

    def get_manufacturer(self):
        return False

    def get_board(self):
        return False

    def get_version_hardware(self):
        return False

    def get_version_firmware(self):
        return False

    def get_id(self):
        return False

    def set_led(self, value):
        """
        Control the onboard LED

        Keyword arguments:
        value -- the value (in percent) to set the LED brightness to. -1 returns control of the LED to the firmware.
        """
        print("set_led")

    def get_voltage_3v3(self):
        """
        Get the 3.3v circuit voltage

        Returns:
        3.3v circuit voltage
        """
        return False

    def get_voltage_5v(self):
        """
        Get the 5v circuit voltage

        Returns:
        5v circuit voltage
        """
        return False

    def get_voltage_9v(self):
        """
        Get the 9v circuit voltage

        Returns:
        9v circuit voltage
        """
        return False

    def get_voltage_battery(self):
        """
        Get the battery voltage

        Returns:
        battery voltage
        """
        return False

    def set_sensor_type(self, port, type, params = 0):
        """
        Set the sensor type

        Keyword arguments:
        port -- The sensor port(s). PORT_1, PORT_2, PORT_3, and/or PORT_4.
        type -- The sensor type
        params = 0 -- the parameters needed for some sensor types.

        params is used for the following sensor types:
            CUSTOM -- a 16-bit integer used to configure the hardware.
            I2C -- a list of settings:
                params[0] -- Settings/flags
                params[1] -- target Speed in microseconds (0-255). Realistically the speed will vary.
                if SENSOR_I2C_SETTINGS_SAME flag set in I2C Settings:
                    params[2] -- Delay in microseconds between transactions.
                    params[3] -- Address
                    params[4] -- List of bytes to write
                    params[5] -- Number of bytes to read
        """
        print("set_sensor_type")

    def transact_i2c(self, port, Address, OutArray, InBytes):
        """
        Conduct an I2C transaction

        Keyword arguments:
        port -- The sensor port (one at a time). PORT_1, PORT_2, PORT_3, or PORT_4.
        Address -- The I2C address for the device. Bits 1-7, not 0-6.
        OutArray -- A list of bytes to write to the device
        InBytes -- The number of bytes to read from the device
        """
        print("transact_i2c")

    def get_sensor(self, port):
        """
        Read a sensor value

        Keyword arguments:
        port -- The sensor port (one at a time). PORT_1, PORT_2, PORT_3, or PORT_4.

        Returns the value(s) for the specified sensor.
            The following sensor types each return a single value:
                NONE ----------------------- 0
                TOUCH ---------------------- 0 or 1 (released or pressed)
                NXT_TOUCH ------------------ 0 or 1 (released or pressed)
                EV3_TOUCH ------------------ 0 or 1 (released or pressed)
                NXT_ULTRASONIC ------------- distance in CM
                NXT_LIGHT_ON  -------------- reflected light
                NXT_LIGHT_OFF -------------- ambient light
                NXT_COLOR_RED -------------- red reflected light
                NXT_COLOR_GREEN ------------ green reflected light
                NXT_COLOR_BLUE ------------- blue reflected light
                NXT_COLOR_OFF -------------- ambient light
                EV3_GYRO_ABS --------------- absolute rotation position in degrees
                EV3_GYRO_DPS --------------- rotation rate in degrees per second
                EV3_COLOR_REFLECTED -------- red reflected light
                EV3_COLOR_AMBIENT ---------- ambient light
                EV3_COLOR_COLOR ------------ detected color
                EV3_ULTRASONIC_CM ---------- distance in CM
                EV3_ULTRASONIC_INCHES ------ distance in inches
                EV3_ULTRASONIC_LISTEN ------ 0 or 1 (no other ultrasonic sensors or another ultrasonic sensor detected)
                EV3_INFRARED_PROXIMITY ----- distance 0-100%

            The following sensor types each return a list of values
                CUSTOM --------------------- Pin 1 ADC (5v scale from 0 to 4095), Pin 6 ADC (3.3v scale from 0 to 4095), Pin 5 digital, Pin 6 digital
                I2C ------------------------ the I2C bytes read
                NXT_COLOR_FULL ------------- detected color, red light reflected, green light reflected, blue light reflected, ambient light
                EV3_GYRO_ABS_DPS ----------- absolute rotation position in degrees, rotation rate in degrees per second
                EV3_COLOR_RAW_REFLECTED ---- red reflected light, unknown value (maybe a raw ambient value?)
                EV3_COLOR_COLOR_COMPONENTS - red reflected light, green reflected light, blue reflected light, unknown value (maybe a raw value?)
                EV3_INFRARED_SEEK ---------- a list for each of the four channels. For each channel heading (-25 to 25), distance (-128 or 0 to 100)
                EV3_INFRARED_REMOTE -------- a list for each of the four channels. For each channel red up, red down, blue up, blue down, boadcast

        """
        return False

    def set_motor_power(self, port, power):
        """
        Set the motor power in percent

        Keyword arguments:
        port -- The Motor port(s). PORT_A, PORT_B, PORT_C, and/or PORT_D.
        power -- The power from -100 to 100, or -128 for float
        """
        print("set_motor_power")

    def set_motor_position(self, port, position):
        """
        Set the motor target position in degrees

        Keyword arguments:
        port -- The motor port(s). PORT_A, PORT_B, PORT_C, and/or PORT_D.
        position -- The target position
        """
        position = int(position)
        print("set_motor_position")

    def set_motor_position_relative(self, port, degrees):
        """
        Set the relative motor target position in degrees. Current position plus the specified degrees.

        Keyword arguments:
        port -- The motor port(s). PORT_A, PORT_B, PORT_C, and/or PORT_D.
        degrees -- The relative target position in degrees
        """
        print("set_motor_position_relative")

    def set_motor_position_kp(self, port, kp = 25):
        """
        Set the motor target position KP constant

        If you set kp higher, the motor will be more responsive to errors in position, at the cost of perhaps overshooting and oscillating.
        kd slows down the motor as it approaches the target, and helps to prevent overshoot.
        In general, if you increase kp, you should also increase kd to keep the motor from overshooting and oscillating.

        Keyword arguments:
        port -- The motor port(s). PORT_A, PORT_B, PORT_C, and/or PORT_D.
        kp -- The KP constant (default 25)
        """
        

    def set_motor_position_kd(self, port, kd = 70):
        """
        Set the motor target position KD constant

        If you set kp higher, the motor will be more responsive to errors in position, at the cost of perhaps overshooting and oscillating.
        kd slows down the motor as it approaches the target, and helps to prevent overshoot.
        In general, if you increase kp, you should also increase kd to keep the motor from overshooting and oscillating.

        Keyword arguments:
        port -- The motor port(s). PORT_A, PORT_B, PORT_C, and/or PORT_D.
        kd -- The KD constant (default 70)
        """
        

    def set_motor_dps(self, port, dps):
        """
        Set the motor target speed in degrees per second

        Keyword arguments:
        port -- The motor port(s). PORT_A, PORT_B, PORT_C, and/or PORT_D.
        dps -- The target speed in degrees per second
        """
        dps = int(dps)
        print("set_motor_dps")

    def set_motor_limits(self, port, power = 0, dps = 0):
        """
        Set the motor speed limit

        Keyword arguments:
        port -- The motor port(s). PORT_A, PORT_B, PORT_C, and/or PORT_D.
        power -- The power limit in percent (0 to 100), with 0 being no limit (100)
        dps -- The speed limit in degrees per second, with 0 being no limit
        """
        print("set_motor_limits")

    def get_motor_status(self, port):
        """
        Read a motor status

        Keyword arguments:
        port -- The motor port (one at a time). PORT_A, PORT_B, PORT_C, or PORT_D.

        Returns a list:
            flags -- 8-bits of bit-flags that indicate motor status:
                bit 0 -- LOW_VOLTAGE_FLOAT - The motors are automatically disabled because the battery voltage is too low
                bit 1 -- OVERLOADED - The motors aren't close to the target (applies to position control and dps speed control).
            power -- the raw PWM power in percent (-100 to 100)
            encoder -- The encoder position
            dps -- The current speed in Degrees Per Second
        """
        return False

    def get_motor_encoder(self, port):
        """
        Read a motor encoder in degrees

        Keyword arguments:
        port -- The motor port (one at a time). PORT_A, PORT_B, PORT_C, or PORT_D.

        Returns the encoder position in degrees
        """
        return False

    def offset_motor_encoder(self, port, position):
        """
        Offset a motor encoder

        Keyword arguments:
        port -- The motor port(s). PORT_A, PORT_B, PORT_C, and/or PORT_D.
        offset -- The encoder offset

        You can zero the encoder by offsetting it by the current position
        """
        position = int(position)
        

    def reset_motor_encoder(self, port):
        """
        Reset motor encoder(s) to 0

        Keyword arguments:
        port -- The motor port(s). PORT_A, PORT_B, PORT_C, and/or PORT_D.
        """
        

    def reset_all(self):
        """
        Reset the BrickPi. Set all the sensors' type to NONE, set the motors to float, and motors' limits and constants to default, and return control of the LED to the firmware.
        """
        