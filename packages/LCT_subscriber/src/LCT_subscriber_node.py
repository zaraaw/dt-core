#!/usr/bin/env python3
import numpy as np
import rospy

from duckietown.dtros import DTROS, NodeType, TopicType, DTParam, ParamType
from duckietown_msgs.msg import (LanePose, Twist2DStamped, WheelsCmdStamped)#, FSMState)

class LCTsubscriberNode(DTROS):
    def __init__(self, node_name):

        super(LCTsubscriberNode, self).__init__(node_name=node_name, node_type=NodeType.PERCEPTION)

        # Initialize variables
        self.pose_msg = LanePose()
        self.current_pose_source = "lane_filter"

        #self.params["~d_thres"] = rospy.get_param("/veh_name/lane_controller_node/d_thres", None)
        #self.params["~d_offset"] = rospy.get_param("/veh_name/lane_controller_node/d_offset", None)
                                                   
        
        ################################################################### for getting v from car_cmd, copied from kinematics node
        # Get static parameters
        self._k = rospy.get_param("/schorsch/kinematics_node/k")
        # Get editable parameters
        self._gain = DTParam("/schorsch/kinematics_node/gain", param_type=ParamType.FLOAT, min_value=0.1, max_value=1.0)
        self._trim = DTParam("/schorsch/kinematics_node/trim", param_type=ParamType.FLOAT, min_value=0.1, max_value=1.0)
        self._limit = DTParam("/schorsch/kinematics_node/limit", param_type=ParamType.FLOAT, min_value=0.1, max_value=1.0)
        self._baseline = DTParam("/schorsch/kinematics_node/baseline", param_type=ParamType.FLOAT, min_value=0.05, max_value=0.2)
        self._radius = DTParam("/schorsch/kinematics_node/radius", param_type=ParamType.FLOAT, min_value=0.01, max_value=0.1)
        self._v_max = DTParam("/schorsch/kinematics_node/v_max", param_type=ParamType.FLOAT, min_value=0.01, max_value=2.0)
        self._omega_max = DTParam("/schorsch/kinematics_node/omega_max", param_type=ParamType.FLOAT, min_value=1.0, max_value=10.0)
        ############################################################################################################################
        
        # self.wheels_cmd_executed = WheelsCmdStamped()

        # self.vel_msg = Twist2DStamped()
        # self.current_vel_source = "kinematics"

        # Construct subscribers
        self.sub_lane_reading = rospy.Subscriber("~lane_pose", LanePose, self.lanepose_callback)
        
        #self.sub_wheels_cmd_executed = rospy.Subscriber("~wheels_cmd", WheelsCmdStamped, self.velocity_callback)

        self.sub_car_cmd = rospy.Subscriber("~car_cmd", Twist2DStamped, self.velocity_callback)           # runs but v stays the same

        # self.sub_velocity = rospy.Subscriber("~velocity", Twist2DStamped, self.velocity_callback)         # runs but v stays the same

        # self.sub_fsm_state = rospy.Subscriber(self._mode_topic, FSMState, self.fsm_state_cb)            # copied from car_cmd_switch_node

        self.log("Initialized!")
    
    """
    def fsm_state_cb(self, fsm_state_msg):
        #rospy.loginfo("Heard: %s", fsm_state_msg)

        global state
        state = fsm_state_msg.state
    """
    def lanepose_callback(self, msg_lane_pose):
        # call back for lane pose message
        #rospy.loginfo("Heard: %s", data)

        global d
        global phi
        global in_lane
        d = msg_lane_pose.d
        phi = msg_lane_pose.phi        
        in_lane = msg_lane_pose.in_lane


        #print(f"lane pose: {d},{phi},{in_lane}")
        
        # rospy.loginfo("%s",d)
        # rospy.loginfo("%s",phi)
        # rospy.loginfo("%s",in_lane)

        
    """
    def cbWheelsCmdExecuted(self, msg_wheels_cmd):
        #Callback that reports if the requested control action was executed.
        #Args:
        #    msg_wheels_cmd (:obj:`WheelsCmdStamped`): Executed wheel commands
        
        self.wheels_cmd_executed = msg_wheels_cmd
        rospy.loginfo("Heard: %s", msg_wheels_cmd)


    
    def velocity_callback(self, msg_car_cmd):
        # callback for velocity message

        global v
        v = msg_car_cmd.v                                                       # stays constant 0.189... (when moving or stationary)

        global v_bar
        v_bar = rospy.get_param("/woifi/lane_controller_node/v_bar")         #also constant at 0.19



        global gain
        gain = rospy.set_param("/schorsch/kinematics_node/gain", 0.5)
        gain = rospy.get_param("/woifi/kinematics_node/gain")

        print(f"{d},{phi},{v},{in_lane},{gain},{v_bar}")
        

        #rospy.loginfo("velocity: %s", v)
    """
    ################################################################### for getting v from car_cmd, copied from kinematics node
    def velocity_callback(self, msg_car_cmd):
        # A callback that reposponds to received `car_cmd` messages by calculating the
        # corresponding wheel commands, taking into account the robot geometry, gain and trim
        # factors, and the set limits. These wheel commands are then published for the motors to use.
        # The resulting linear and angular velocities are also calculated and published.
        # Args:
        #    msg_car_cmd (:obj:`Twist2DStamped`): desired car command
        

        # INVERSE KINEMATICS PART

        # trim the desired commands such that they are within the limits:
        # trim = rospy.get_param("/woifi/kinematics_node/trim")
        msg_car_cmd.v = self.trim(msg_car_cmd.v, low=-self._v_max.value, high=self._v_max.value)
        msg_car_cmd.omega = self.trim(
            msg_car_cmd.omega, low=-self._omega_max.value, high=self._omega_max.value
        )

        # assuming same motor constants k for both motors
        k_r = k_l = self._k

        # adjusting k by gain and trim
        k_r_inv = (self._gain.value + self._trim.value) / k_r
        k_l_inv = (self._gain.value - self._trim.value) / k_l

        omega_r = (msg_car_cmd.v + 0.5 * msg_car_cmd.omega * self._baseline.value) / self._radius.value
        omega_l = (msg_car_cmd.v - 0.5 * msg_car_cmd.omega * self._baseline.value) / self._radius.value

        # conversion from motor rotation rate to duty cycle
        # u_r = (gain + trim) (v + 0.5 * omega * b) / (r * k_r)
        u_r = omega_r * k_r_inv
        # u_l = (gain - trim) (v - 0.5 * omega * b) / (r * k_l)
        u_l = omega_l * k_l_inv

        # limiting output to limit, which is 1.0 for the duckiebot
        u_r_limited = self.trim(u_r, -self._limit.value, self._limit.value)
        u_l_limited = self.trim(u_l, -self._limit.value, self._limit.value)

        # Put the wheel commands in a message and publish
        #msg_wheels_cmd = WheelsCmdStamped()
        #msg_wheels_cmd.header.stamp = msg_car_cmd.header.stamp
        #msg_wheels_cmd.vel_right = u_r_limited
        #msg_wheels_cmd.vel_left = u_l_limited
        #self.pub_wheels_cmd.publish(msg_wheels_cmd)

        # FORWARD KINEMATICS PART

        # Conversion from motor duty to motor rotation rate #was using msg_wheels_cmd.vel_right & left previous
        omega_r = u_r_limited / k_r_inv
        omega_l = u_l_limited / k_l_inv

        # Compute linear and angular velocity of the platform
        v = (self._radius.value * omega_r + self._radius.value * omega_l) / 2.0
        omega = (self._radius.value * omega_r - self._radius.value * omega_l) / self._baseline.value

        global gain
        gain = rospy.get_param("/schorsch/kinematics_node/gain")

        # if state == 'LANE_FOLLOWING':
        print(f"{d},{phi},{in_lane},{v},{omega},{gain}")
    ############################################################################################################################
    """
    def velocity_callback(self, msg_wheels_cmd):
        # global v
        # vel_right = msg_wheels_cmd.vel_right
        # vel_left = msg_wheels_cmd.vel_left

        self.wheels_cmd_executed = msg_wheels_cmd
        vel_left =  self.wheels_cmd_executed.vel_left
        vel_right = self.wheels_cmd_executed.vel_right
        print(f"velocity cmd: {vel_left}, {vel_right}")

    def velocity_callback(self, msg_velocity):
        # callback for velocity message

        global v
        v = msg_velocity.v

        rospy.loginfo("velocity: %s", v)
    """ 


    @staticmethod
    def trim(value, low, high):
        """
        Trims a value to be between some bounds.
        Args:
            value: the value to be trimmed
            low: the minimum bound
            high: the maximum bound
        Returns:
            the trimmed value
        """
        return max(min(value, high), low)
    
    
          
if __name__ == "__main__":
    # Initialize the node
    LCT_subscriber_node = LCTsubscriberNode(node_name="LCTsubscriber")
    # Keep it spinning
    rospy.spin()
    
