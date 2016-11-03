#!/usr/bin/env python2.7
import sys
import time
import rospy
import roslib
import thread as _thread
from rc_create.srv import Control
from rc_create.srv import ControlResponse
roslib.load_manifest('rc_create')

def handle_rc_command(req):
    if req.command == req.MOVE_FORWARD:
        print "Move forward called"
    else:
        print "Others called: "+str(req.command)
    return ControlResponse(True,"Success")

def main(args):
    rospy.init_node('rc_create_driver_python', anonymous=True)
    rc_command_srv = rospy.Service("rc_commands",Control,handle_rc_command)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
        rospy.shutdown();

if __name__ == '__main__':
    main(sys.argv)
