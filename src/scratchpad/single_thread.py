import threading
import time
import os

def thread_function(name):
    print("Thread starting", name)
    for t in range(10):
        print(time.time())
        time.sleep(1)

    safeQuit()
    print("Thread finishing", name)


def safeQuit():
    print("Stopped motors")
    # sys.exit() # Doesn't stop main thread
    os._exit(0)


if __name__ == "__main__":
    print("start prog")


    x = threading.Thread(target=thread_function, args=(1,), daemon=True)
    x.start()
    t=input("Type any letter then press enter to quit")
    safeQuit()
