# This file seems to be run by the green 'Run' button in NetBeans
# So lets make it deploy the actual code I want to run on the Pi and then run it remotely.
# Requires SSH public\private key pair to have been setup and working ok
import inspect
import os
#import sys
#import subprocess
#from os import path
from os import popen
from subprocess import Popen
from subprocess import PIPE


#FILE_TO_UPLOAD = "test_main.py"
REMOTE_FOLDER = "/home/pi/BrickPi3-Code/"
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
    #thisScript = os.path.realpath(__file__)
    #print("Running " + thisScript)
    
    folderContainingMe = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    #print("From folder: " + folderContainingMe)
    
    
    print("Recursively copying this local folder:")
    print(folderContainingMe)
    print("to the remote folder:")
    print(REMOTE_FOLDER)
    print("via SCP, overwriting anything in remote folder.")
    cmd = 'pscp -r -p "%s" %s:%s' % (folderContainingMe, PUTTY_SAVED_SESSION, REMOTE_FOLDER)
    print("DEBUG: " + cmd)
    print(popen(cmd).read())
    
    
    #print("Running the new remote file: " + REMOTE_FOLDER + "/" + FILE_TO_UPLOAD)
    #sshCmd = 'start plink -ssh rpi-robot2 "cd ' + REMOTE_FOLDER + '; python3 ' + FILE_TO_UPLOAD + '"'
#    shell(sshCmd)
#    os.system('start /wait ' + sshCmd)  
    #subprocess.Popen(sshCmd, shell=True)
    #print ("Done.")
        
    
if __name__ == "__main__":
    main()
