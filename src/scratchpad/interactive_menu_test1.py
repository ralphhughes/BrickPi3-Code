

def print_menu():
    print("1: Set current location (lat\\long)")
    print("2: Calibrate current azimuth\\inclination")
    print("3: Set target position")
    print("4: manual move")
    print("q: quit")


while True:
    print_menu()
    strInput = input()
    if strInput == 'q':
        raise SystemExit
