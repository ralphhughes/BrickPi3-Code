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
import tempfile

FILE_TO_RUN = "src/test_main.py"
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

def deploy():
    folderContainingMe = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    
    print("Recursively copying this local folder:")
    print(folderContainingMe)
    print("to the remote folder:")
    print(REMOTE_FOLDER)
    print("via SCP, overwriting anything in remote folder.")
    cmd = 'pscp -r -p "%s" %s:%s' % (folderContainingMe, PUTTY_SAVED_SESSION, REMOTE_FOLDER)
    print("DEBUG: " + cmd)
    print(popen(cmd).read())
    
def remote_run():
    remoteFile = REMOTE_FOLDER + FILE_TO_RUN
    print("Running the new remote file: " + remoteFile)
    
    #tempFile = tempfile.gettempdir() + os.path.sep + "putty_cmd.txt" # Not using .TemporaryFile() as I want to view it after program has completed
    #f= open(tempFile,"w+")
    #f.write("python3 " + remoteFile)
    #f.close()
    #sshCmd = "start putty -load rpi-robot2 -m " + tempFile

    sshCmd = 'start plink -ssh rpi-robot2 -t "python3 ' + remoteFile + '"'
    print("DEBUG: " + sshCmd)
    print(popen(sshCmd).read())

    sshCmd = 'plink -ssh rpi-robot2 "python3 ' + REMOTE_FOLDER + 'src/stop_motors.py"'
    print("DEBUG: " + sshCmd)
    print(popen(sshCmd).read())


if __name__ == "__main__":
    deploy()
    remote_run()
