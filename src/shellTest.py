#!/usr/bin/env python3
#encoding: windows-1252
import subprocess


def start(executable_file):
    return subprocess.Popen(
        executable_file,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )


def read(process):
    return process.stdout.readline().decode("utf-8").strip()


def write(process, message):
    process.stdin.write(f"{message.strip()}\n".encode("utf-8"))
    process.stdin.flush()


def terminate(process):
    process.stdin.close()
    process.terminate()
    process.wait(timeout=0.2)

sshCmd = 'plink -ssh rpi-robot2 "cd /home/pi/BrickPi3-Code/src; python3 motor_move_distance.py'
process = start(sshCmd)
try:
    while True:
        print(read(process))
        myStr = input("")
        write(process, myStr)
        
except KeyboardInterrupt:
    terminate(process)
