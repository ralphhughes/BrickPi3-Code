# Import necessary libraries.
from time import sleep

from Bluetin_Echo import Echo # https://github.com/MarkAHeywood/Bluetin_Python_Echo

# Define pin constants
TRIGGER_PIN_1 = 27
ECHO_PIN_1 = 17
TRIGGER_PIN_2 = 22
ECHO_PIN_2 = 23

# Initialise two sensors.
echo = [Echo(TRIGGER_PIN_1, ECHO_PIN_1)
        , Echo(TRIGGER_PIN_2, ECHO_PIN_2)]

def main():
    sleep(0.1)
    for counter in range(1, 6):
        result1 = echo[0].read('cm', 3)
        result2 = echo[1].read('cm', 3)
        print('C1: {}cm\tC2: {}cm'.format(round(result2,2), round(result1,2)))

    echo[0].stop()

if __name__ == '__main__':
    main()
