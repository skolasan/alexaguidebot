#!/usr/bin/env python2.7
import sys
import time
import rospy
import roslib
import thread as _thread
from rc_create.srv import Control
from rc_create.srv import ControlRequest
from rc_create.srv import ControlResponse
try:
    import serial
except ImportError:
    print("Import error Please install pyserial.")
    raise

roslib.load_manifest('rc_create')

# sendCommandASCII takes a string of whitespace-separated, ASCII-encoded base 10 values to send
def sendCommandASCII(command,error):
    cmd = ""
    for v in command.split():
        cmd += chr(int(v))

    return sendCommandRaw(cmd,error)

# sendCommandRaw takes a string interpreted as a byte array
def sendCommandRaw(command,error):
    global connection

    try:
        if connection is not None:
            connection.write(command)
            return True
        else:
            error="Not Connected!"
            print "Not Connected!"
            return False
    except serial.SerialException:
        error="Lost Connection"
        print "Lost Connection"
        connection = None
        return False

def handle_rc_command(req):
    error=""
    if req.command == req.MOVE_FORWARD:
        sendCommandASCII("137 127 255 0 0",error)
        print "Move forward called"
    elif req.command == req.MOVE_BACKWARD:
        sendCommandASCII("137 128 0 0 0",error)
    elif req.command == req.MOVE_LEFT:
        sendCommandASCII("137 0 0 255 255",error)
    elif req.command == req.MOVE_RIGHT:
        sendCommandASCII("137 0 0 0 1",error)
    elif req.command == req.STOP:
        sendCommandASCII("137 0 0 0 0",error)
    else:
        print "Others called: "+str(req.command)
    return ControlResponse(True,"Success")


current_command=-1
connection=None
port= "/dev/ttyUSB0"

def main(args):
    global connection
    error1=""
    rospy.init_node('rc_create_driver_python', anonymous=True)
    rc_command_srv = rospy.Service("rc_commands",Control,handle_rc_command)
    try:
        connection = serial.Serial(port, baudrate=115200, timeout=1)
        #send a OI open
        if sendCommandASCII("128",error1) == False:
            raise Exception("Unable to send the OI start command-->Check connection")
        if sendCommandASCII("132",error1) == False:
            raise Exception("Unable to put the Roomba to Full mode -- > Check connection")
    except Exception as e:
        print("Couldn't connect to "+port+" check if it exists error : "+str(e))

    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
        rospy.shutdown();

if __name__ == '__main__':
    main(sys.argv)
