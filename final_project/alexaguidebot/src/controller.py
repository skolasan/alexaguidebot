#!/usr/bin/env python2.7
import rospy
import roslib
import actionlib
import sys
import numpy as np
import math
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from actionlib_msgs.msg import *
from geometry_msgs.msg import Point
from geometry_msgs.msg import PoseWithCovarianceStamped
from alexaguidebot.srv import Command
from alexaguidebot.srv import CommandRequest
from alexaguidebot.srv import CommandResponse

zone1x=1.9478963962
zone1y=7.05327463996

zone2x=2.84276238302
zone2y=9.12342601152

zone3x=6.3316227806
zone3y=0.857146775507

location_names=["zone1","zone2","zone3"]
location_x_position=[zone1x,zone2x,zone3x]
location_y_position=[zone1y,zone2y,zone3y]

roslib.load_manifest('alexaguidebot')

def getDistance(x1,y1,x2,y2):
    return math.pow(x2-x1,2)+math.pow(y2-y1,2)

def poseDataCallBack(data):
    x=data.pose.pose.position.x;
    y=data.pose.pose.position.y;

    min_d = sys.maxint
    min_i = 0
    for i in range(len(location_names)):
        d=getDistance(x,y,location_x_position[i],location_y_position[i])
        if d<min_d:
            min_d=d
            min_i=i
    global current_location;
    current_location = location_names[i]

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
        print "Navigate called: "+req.location
        if(req.location=="zone 1"):
            moveToGoal(zone1x,zone1y)
            return CommandResponse(True,"Success")

    elif req.command == req.LOCATE:
        print "Locate called"
        global current_location
        return CommandResponse(True,current_location)

    else:
        print "Others called: "+str(req.command)
        return CommandResponse(True,"False")


current_location="Unknown"
def main(args):
    rospy.init_node('controller', anonymous=True)
    command_srv = rospy.Service("voice_commands",Command,handle_command)
    rospy.Subscriber("/amcl_pose",PoseWithCovarianceStamped,poseDataCallBack)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
        rospy.shutdown();

if __name__ == '__main__':
    main(sys.argv)
