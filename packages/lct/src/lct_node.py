#!/usr/bin/env python3
import numpy as np
import rospy
# import simple_function
import pandas as pd
import random
import LCT

from duckietown.dtros import DTROS, NodeType, TopicType, DTParam, ParamType
from duckietown_msgs.msg import (LanePose, Twist2DStamped, FSMState)

class LCTNode(DTROS):
    def __init__(self, node_name):

        super(LCTNode, self).__init__(node_name=node_name, node_type=NodeType.PERCEPTION)

        # Initialize variables
        self.pose_msg = LanePose()
        self.current_pose_source = "lane_filter"

        self._mode_topic = rospy.get_param("/schorsch/car_cmd_switch_node/mode_topic")

        # Construct subscribers
        self.sub_lane_reading = rospy.Subscriber("~lane_pose", LanePose, self.lanepose_callback)        # will instead subscribe to my publisher
        # self.sub_car_cmd = rospy.Subscriber("~car_cmd", Twist2DStamped, self.velocity_callback)         # wont use this

        self.sub_fsm_state = rospy.Subscriber(self._mode_topic, FSMState, self.fsm_state_cb)            # copied from car_cmd_switch_node
        

        self.log("Initialized!")

    def fsm_state_cb(self, fsm_state_msg):
        #rospy.loginfo("Heard: %s", fsm_state_msg)

        global state
        state = fsm_state_msg.state

           
    def lanepose_callback(self, msg_lane_pose):
        #rospy.loginfo("Heard: %s", data)

        global d                                                        # keep this bit outside the loop or no? or does it make a difference?
        global phi
        global in_lane

        d = round(msg_lane_pose.d, 2)
        phi = round(msg_lane_pose.phi, 2)
        in_lane = msg_lane_pose.in_lane

        global v
        v = rospy.get_param("/schorsch/kinematics_node/gain")               # using gain as a condition           

        global lct_out
        if state == "NORMAL_JOYSTICK_CONTROL":
            print(f"STATE: {state}")
        else:
            lct_out = LCT.runLCT().run_LCT(d, phi, v)
            print(f"LCT output: {lct_out}")
            if lct_out == None:                                             # keeps gain the same if no action selected from lct
                gain = rospy.get_param("/schorsch/kinematics_node/gain")
            else:
                gain = lct_out
            
            rospy.set_param("/schorsch/kinematics_node/gain", gain)
            
            print(f"conditions:{d},{phi},{v}")
            print(f"gain: {gain}")
            rospy.sleep(1) 

    """
    def velocity_callback(self, msg_car_cmd):
        # callback for velocity message

        global v         
        v = msg_car_cmd.v
    """
          
if __name__ == "__main__":
    # Initialize the node
    lct_node = LCTNode(node_name="lct_node")
    
    # Keep it spinning
    rospy.spin()
    
# add to master.launch
# <remap from="lct_node/car_cmd" to="lane_controller_node/car_cmd"/>