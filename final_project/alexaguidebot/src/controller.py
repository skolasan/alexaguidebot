#!/usr/bin/env python2.7
import rospy
import roslib
import actionlib
import sys
import numpy as np
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from actionlib_msgs.msg import *
from geometry_msgs.msg import Point
from alexaguidebot.srv import Command
from alexaguidebot.srv import CommandRequest
from alexaguidebot.srv import CommandResponse

zone1x=1.9478963962
zone1y=7.05327463996

zone2x=2.84276238302
zone2y=9.12342601152

zone3x=6.3316227806
zone3y=0.857146775507


roslib.load_manifest('alexaguidebot')

def moveToGoal(xGoal,yGoal):

    #define a client for to send goal requests to the move_base server through a SimpleActionClient
    ac = actionlib.SimpleActionClient("move_base", MoveBaseAction)
    
    #wait for the action server to come up
    while(not ac.wait_for_server(rospy.Duration.from_sec(5.0))):
        rospy.loginfo("Waiting for the move_base action server to come up")
    
    
    goal = MoveBaseGoal()
    
    #set up the frame parameters
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    
    # moving towards the goal*/
    
    goal.target_pose.pose.position =  Point(xGoal,yGoal,0)
    goal.target_pose.pose.orientation.x = 0.0
    goal.target_pose.pose.orientation.y = 0.0
    goal.target_pose.pose.orientation.z = 0.0
    goal.target_pose.pose.orientation.w = 1.0
    
    rospy.loginfo("Sending goal location ...")
    ac.send_goal(goal)
    
    ac.wait_for_result(rospy.Duration(60))
    
    if(ac.get_state() ==  GoalStatus.SUCCEEDED):
        rospy.loginfo("You have reached the destination")
        return True
    
    else:
        rospy.loginfo("The robot failed to reach the destination")
        return False

def handle_command(req):
    error=""
    if req.command == req.NAVIGATE:
        print "Navigate called"
        if(req.location=="zone1"):
            moveToGoal(zone1x,zone1y)
    else:
        print "Others called: "+str(req.command)
    return CommandResponse(True,"Success")


def main(args):
    rospy.init_node('controller', anonymous=True)
    command_srv = rospy.Service("voice_commands",Command,handle_command)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
        rospy.shutdown();

if __name__ == '__main__':
    main(sys.argv)
