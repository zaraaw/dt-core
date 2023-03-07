#!/usr/bin/env python3
import numpy as np
import rospy

from duckietown.dtros import DTROS, NodeType, TopicType, DTParam, ParamType
from duckietown_msgs.msg import (LanePose, Twist2DStamped)

class LCTsubscriberNode(DTROS):
    def __init__(self, node_name):

        super(LCTsubscriberNode, self).__init__(node_name=node_name, node_type=NodeType.PERCEPTION)

        # Initialize variables
        self.pose_msg = LanePose()
        self.current_pose_source = "lane_filter"

        # self.vel_msg = Twist2DStamped()
        # self.current_vel_source = "kinematics"

        # contruct publisher


        # Construct subscribers
        self.sub_lane_reading = rospy.Subscriber("~lane_pose", LanePose, self.lanepose_callback)

        self.sub_car_cmd = rospy.Subscriber("~car_cmd", Twist2DStamped, self.velocity_callback)

        # self.sub_velocity = rospy.Subscriber("~velocity", Twist2DStamped, self.velocity_callback)

        self.log("Initialized!")
    
          
    def lanepose_callback(self, msg_lane_pose):
        # call back for lane pose message
        #rospy.loginfo("Heard: %s", data)

        global d
        global phi
        global in_lane

        d = msg_lane_pose.d
        phi = msg_lane_pose.phi
        in_lane = msg_lane_pose.in_lane
        
        #rospy.loginfo("%s",d)
        #rospy.loginfo("%s",phi)
        #rospy.loginfo("%s",in_lane)
    
    """
    def velocity_callback(self, msg_velocity):
        # callback for velocity message

        global v
        v = msg_velocity.v

        rospy.loginfo("velocity: %s", v)
    
    """
    def velocity_callback(self, msg_car_cmd):
        # callback for velocity message

        global v
        v = msg_car_cmd.v               # i dont like this v -- it doesnt change from 0.189... when moving or stationary

        global gain
        
        rospy.set_param("/schorsch/kinematics_node/gain", 0.5)

        gain = rospy.get_param("/schorsch/kinematics_node/gain")

        print(f"{d},{phi},{v},{in_lane}, gain: {gain}")
        

        #rospy.loginfo("velocity: %s", v)
    """
    def printlog(self, d, phi, v):
        print(f"IN NEW METHOD:{d},{phi},{v}, {in_lane}")
        # prob need to add smthn in master.launch so it's run
    """
    
          
if __name__ == "__main__":
    # Initialize the node
    LCT_subscriber_node = LCTsubscriberNode(node_name="LCTsubscriber")
    # Keep it spinning
    rospy.spin()
    
