#!/usr/bin/env python2.7
import sys
import time
import rospy
import roslib
import cv2
import numpy as np
import thread as _thread
from rc_create.srv import Control
from rc_create.srv import ControlRequest
roslib.load_manifest('rc_create')

class KeyCodes:
    ESCAPE=27
    UP=65362
    DOWN=65364
    RIGHT=65363
    LEFT=65361
    SPACE=32
    P=112
    S=115


def getkeypress():
    import tty,termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def call_control_service(keycode):
    rospy.wait_for_service("rc_commands")
    try:
        control_srv = rospy.ServiceProxy("rc_commands",Control)
        if keycode==KeyCodes.UP:
            print "Calling Up Service"
            control_srv(ControlRequest.MOVE_FORWARD)
        elif keycode==KeyCodes.DOWN:
            control_srv(ControlRequest.MOVE_BACKWARD)
        elif keycode==KeyCodes.LEFT:
            control_srv(ControlRequest.MOVE_LEFT)
        elif keycode==KeyCodes.RIGHT:
            control_srv(ControlRequest.MOVE_RIGHT)
        elif keycode==KeyCodes.SPACE:
            control_srv(ControlRequest.STOP)
        elif keycode==KeyCodes.P:
            control_srv(ControlRequest.PLAY_SONG)
        elif keycode==KeyCodes.S:
            control_srv(ControlRequest.STOP_SONG)

    except rospy.ServiceException, e:
        print "Service call failed: %s" % e

# Normal terminal has wierd formatting for arrow keys
# Use openCV's high gui support
size = 200, 200, 1
m = np.zeros(size, dtype=np.uint8)
text = "Odroid Controller\n \
    UP-Move Forward\n \
    DOWN-Move Backward\n \
    LEFT-Turn Left\n \
    RIGHT-Turn Right\n \
    P-Play Song\n \
    ESC-Exit\n"

y0, dy = 50, 20
for i, line in enumerate(text.split('\n')):
    y = y0 + i*dy
    print line
    cv2.putText(m, line, (0, y), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,255,255))

cv2.namedWindow("rc controller", cv2.WINDOW_AUTOSIZE )
cv2.imshow("rc controller",m)
while True:
    key = cv2.waitKey();
    print "got" + str(key)
    if key == KeyCodes.ESCAPE:
        cv2.destroyAllWindows()
        break
    else:
        call_control_service(key)
    time.sleep(0.2)
