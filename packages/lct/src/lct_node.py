#!/usr/bin/env python3
import numpy as np
import rospy
# import LCT 

from duckietown.dtros import DTROS, NodeType, TopicType, DTParam, ParamType
from duckietown_msgs.msg import (LanePose, Twist2DStamped)

class LCTNode(DTROS):
    def __init__(self, node_name):

        super(LCTNode, self).__init__(node_name=node_name, node_type=NodeType.PERCEPTION)

        # Initialize variables
        self.pose_msg = LanePose()
        self.current_pose_source = "lane_filter"

        # config file?



        # Construct subscribers
        self.sub_lane_reading = rospy.Subscriber("~lane_pose", LanePose, self.lanepose_callback)
        self.sub_car_cmd = rospy.Subscriber("~car_cmd", Twist2DStamped, self.velocity_callback)



        self.log("Initialized!")
           
    def lanepose_callback(self, msg_lane_pose):
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
    
    def velocity_callback(self, msg_car_cmd):
        # callback for velocity message

        global v
        v = msg_car_cmd.v

        rospy.loginfo("%s",d)
        rospy.loginfo("%s",phi)
        rospy.loginfo("%s",in_lane)

        rospy.loginfo("velocity: %s", v)

    """
    def runLCT(self, d, phi, v):
        cons = LCT.Constants()
        cons.setConstants()
        
        LCT.runLCT().run_LCT(d, phi, v)
    """           

          
if __name__ == "__main__":
    # Initialize the node
    lct_node = LCTNode(node_name="lct_node")
    
   
    # Keep it spinning
    rospy.spin()
    
# add to master.launch
# <remap from="lct_node/car_cmd" to="lane_controller_node/car_cmd"/>
