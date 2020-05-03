import keyboard  # using module keyboard
while True:  # making a loop
    try:  # used try so that if user pressed other than the given key error will not be shown
        if keyboard.is_pressed('q'):  # if key 'q' is pressed
            print('You Pressed Q!')
            break  # finishing the loop
    except:
        print("You pressed something other than Q!")
        break  # if user pressed a key other than the given key the loop will break