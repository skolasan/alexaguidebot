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
from std_msgs.msg import String
from geometry_msgs.msg import Twist, Vector3
import math
from std_srvs.srv import Empty
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
    global pub
    global velocities
    if req.command == req.MOVE_FORWARD:
        velocities = Twist(Vector3(0.2,0,0), Vector3(0,0,0.0))
        print "Move forward called"
    elif req.command == req.MOVE_BACKWARD:
        velocities = Twist(Vector3(-0.2,0,0), Vector3(0,0,0.0))
    elif req.command == req.MOVE_LEFT:
        velocities = Twist(Vector3(0,0,0), Vector3(0,0,0.8))
    elif req.command == req.MOVE_RIGHT:
        velocities = Twist(Vector3(0,0,0), Vector3(0.0,0,-0.8))
    elif req.command == req.STOP:
        velocities = Twist(Vector3(0,0,0), Vector3(0,0,0.0))
    else:
        print "Others called: "+str(req.command)
    return ControlResponse(True,"Success")
    


current_command=-1
connection=None
port= "/dev/ttyUSB0"
pub=None
velocities = None
def main(args):
    global pub
    global connection
    global velocities
    error1=""
    rospy.init_node('rc_create_driver_python', anonymous=True)
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
    #rospy.init_node('turtle_controller', anonymous=True)
    rate = rospy.Rate(40) # 10hz
    rc_command_srv = rospy.Service("rc_commands",Control,handle_rc_command)
    while not rospy.is_shutdown() :
        if velocities is not None:
            pub.publish(velocities)
        try:
            rate.sleep()
        except KeyboardInterrupt:
            print("Shutting down")
            rospy.shutdown();


if __name__ == '__main__':
    main(sys.argv)
