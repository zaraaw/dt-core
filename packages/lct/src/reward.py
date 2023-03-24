"""
The reward function to be called by the LCT 
"""
import gen_rule_pop as r

class Reward:
    def __init__(self) -> None:                         # i think this is redundant
        self.low_v = r.v2                          # just use r. value in the method
        self.max_v = r.max_v
        self.stop_v = r.v1
        
        
        self.d1 = r.d1             
        self.d2 = r.d2
        

        self.phi1 = r.phi1
        self.phi2 = r.phi2
        
    
    def calc_reward(self, d, phi, v):                       # for gain as v 

        if v < self.low_v and (self.d2 <= d) and (self.phi2 <= phi):
            print("punished for bad deviation - d & phi and slow speed ")
            reward = 0.01

        elif (self.d2 <= d) and (self.phi2 <= phi):
            print("punished for bad deviation - d & phi")
            reward = 0.1
        

        elif self.low_v < v <= self.max_v and (d <= self.d1) and (phi <= self.phi1):
            print("rewarded for going straight - d & phi and fast speed ")
            reward = 1

        elif (d <= self.d1) and (phi <= self.phi1):
            print("rewarded for going straight - d & phi")
            reward = 0.9
        
        elif (self.d2 <= d):
            print("punished for bad deviation - d")
            reward = 0.2
        elif (self.phi2 <= phi):
            print("punished for bad deviation - phi")
            reward = 0.2

        elif (self.d1 < d < self.d2):
            print("punished for okay deviation - d")
            reward = 0.3
        elif (self.phi1 < phi < self.phi2):
            print("punished for okay deviation - phi")
            reward = 0.3

        elif (self.stop_v < v < self.low_v):
            print("punished for slow speed")
            reward = 0.4
        
        elif (self.low_v < v <= self.max_v):
            print("rewarded for fast speed")
            reward = 0.8
            
        elif (d <= self.d1):
            print("rewarded for going straight - d")
            reward = 0.7
        elif (phi <= self.phi1):
            print("rewarded for going straight - phi")
            reward = 0.7 
        
        return reward   
    