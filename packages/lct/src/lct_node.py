#!/usr/bin/env python3
import numpy as np
import rospy

from duckietown.dtros import DTROS, NodeType, TopicType, DTParam, ParamType
from duckietown_msgs.msg import (LanePose)

class LCTNode(DTROS):
    def __init__(self, node_name):

        super(LCTNode, self).__init__(node_name=node_name, node_type=NodeType.PERCEPTION)

        # Initialize variables
        self.pose_msg = LanePose()
        self.current_pose_source = "lane_filter"

        # Construct subscribers
        self.sub_lane_reading = rospy.Subscriber("~lane_pose", LanePose, self.callback)
        self.log("Initialized!")
           
    def callback(self,data):
        #rospy.loginfo("Heard: %s", data)

        global d
        global phi
        global in_lane

        d = data.d
        phi = data.phi
        in_lane = data.in_lane
        
        rospy.loginfo("%s",d)
        rospy.loginfo("%s",phi)
        rospy.loginfo("%s",in_lane)
          
if __name__ == "__main__":
    # Initialize the node
    lct_node = LCTNode(node_name="lct_node")
    
   
    # Keep it spinning
    rospy.spin()
    
