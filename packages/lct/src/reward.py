"""
The reward function to be called by the LCT 
"""
import gen_rule_pop as r

class Reward:
    def __init__(self) -> None:                         # i think this is redundant
        self.low_v = r.low_v                            # just use r. value in the method
        self.max_v = r.max_v
        self.stop_v = r.stop_v
        
        self.d1 = r.d1             
        self.d2 = r.d2
        self.d3 = r.d3          
        self.d4 = r.d4

        self.phi1 = r.phi1
        self.phi2 = r.phi2
        self.phi3 = r.phi3
        self.phi4 = r.phi4
    
    def calc_reward(self, d, phi, v):                       # for gain as v 

        if v < self.low_v and (d <= self.d1 or d >= self.d4) and (phi <= self.phi1 or phi >= self.phi4):
            print("punished for bad deviation - d & phi and slow speed ")
            reward = 0.01

        elif (d <= self.d1 or d >= self.d4) and (phi <= self.phi1 or phi >= self.phi4):
            print("punished for bad deviation - d & phi")
            reward = 0.1
        

        elif self.low_v < v <= self.max_v and (d <= self.d1 or d <= self.d4) and (self.phi2 <= phi <= self.phi3):
            print("rewarded for going straight - d & phi and fast speed ")
            reward = 1

        elif (self.d2 <= d <= self.d3) and (self.phi2 <= phi <= self.phi3):
            print("rewarded for going straight - d & phi")
            reward = 0.9
        
        elif d <= self.d1 or d >= self.d4:
            print("punished for bad deviation - d")
            reward = 0.2
        elif phi <= self.phi1 or phi >= self.phi4:
            print("punished for bad deviation - phi")
            reward = 0.2

        elif self.d1 < d < self.d2 or self.d3 < d < self.d4:
            print("punished for okay deviation - d")
            reward = 0.3
        elif self.phi1 < d < self.phi2 or self.phi3 < d < self.phi4:
            print("punished for okay deviation - phi")
            reward = 0.3

        elif self.stop_v < v < self.low_v:
            print("punished for slow speed")
            reward = 0.4
        
        elif self.low_v < v <= self.max_v:
            print("rewarded for fast speed")
            reward = 0.8
            
        elif self.d2 <= d <= self.d3:
            print("rewarded for going straight - d")
            reward = 0.7
        elif self.phi2 <= phi <= self.phi3:
            print("rewarded for going straight - phi")
            reward = 0.7 
        
        return reward   
   