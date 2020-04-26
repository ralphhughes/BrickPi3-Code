# This file seems to be run by the green 'Run' button in NetBeans
# So lets make it deploy the actual code I want to run on the Pi and then run it remotely.
# Requires SSH public\private key pair to have been setup and working ok
import inspect
import os
from os import path, popen
from subprocess import Popen, PIPE

FILE_TO_UPLOAD = "motor_move_distance.py"
REMOTE_FOLDER = "/home/pi/BrickPi3-Code/src"
PUTTY_SAVED_SESSION = "rpi-robot2"

## shell out, prompt
def shell(args, input=''):
    ''' uses subprocess pipes to call out to the shell.

    args:  args to the command
    input:  stdin

    returns stdout, stderr
    '''
    p = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate(input=input)
    return stdout, stderr

def main():
    thisScript = os.path.realpath(__file__)
    print("Running " + thisScript)
    
    folderContainingMe = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    print("From folder: " + folderContainingMe)
    
    localFile = folderContainingMe + os.path.sep + FILE_TO_UPLOAD
    print("To upload and run this file: " + localFile)
    cmd = 'pscp "%s" %s:%s' % (FILE_TO_UPLOAD, PUTTY_SAVED_SESSION, REMOTE_FOLDER)
    print(popen(cmd).read())
    
    
    print("Running the new remote file: " + REMOTE_FOLDER + "/" + FILE_TO_UPLOAD)
#    shell('plink -ssh rpi-robot2 "cd ' + REMOTE_FOLDER + '; python3 ' + FILE_TO_UPLOAD + '"')
    os.system('start /wait plink -ssh rpi-robot2 "cd ' + REMOTE_FOLDER + '; python3 ' + FILE_TO_UPLOAD + '"')   
    print ("Done.")
        
    
if __name__ == "__main__":
    main()
