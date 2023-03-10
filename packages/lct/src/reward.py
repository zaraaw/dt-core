"""
The reward function to be called by the LCT 
"""


class Reward:
    def __init__(self) -> None:
        self.low_v = 1
        self.max_v = 2
        self.stop_v = 0.5
        
        self.d1 = -0.4               
        self.d2 = -0.15
        self.d3 = 0.15               
        self.d4 = 0.4

        self.phi1 = -1.6
        self.phi2 = -0.6
        self.phi3 = 0.6
        self.phi4 = 1.6

    def calc_reward(self, d, phi, v):
        if 0 <= v <= self.stop_v:
            print("punished for crashing")
            reward = 0.001 # worst 
        elif self.low_v <= v <= self.max_v and (d <= self.d1 or d >= self.d4) and (self.phi2 <= phi <= self.phi3):
            print("rewarded for going straight - d & phi and fast speed ")
            reward = 20
        elif v < self.low_v and (d <= self.d1 or d >= self.d4) and (phi <= self.phi1 or phi >= self.phi4):
            print("punished for bad deviation - d & phi and slow speed ")
            reward = 0.005

        elif self.low_v < v <= self.max_v:
            print("rewarded for fast speed")
            reward = 10 # good
            
        elif self.d2 <= d <= self.d3:
            print("rewarded for going straight - d")
            reward = 10
        elif self.phi2 <= phi <= self.phi3:
            print("rewarded for going straight - phi")
            reward = 10
        
        elif d <= self.d1 or d >= self.d4:
            print("punished for bad deviation - d")
            reward = 0.01
        elif phi <= self.phi1 or phi >= self.phi4:
            print("punished for bad deviation - phi")
            reward = 0.01

        elif self.d1 < d < self.d2 or self.d3 < d < self.d4:
            print("punished for okay deviation - d")
            reward = 0.1
        elif self.phi1 < d < self.phi2 or self.phi3 < d < self.phi4:
            print("punished for okay deviation - phi")
            reward = 0.1
        

        elif self.stop_v < v < self.low_v:
            print("punished for slow speed")
            reward = 0.1 # bad 
        
        
        return reward
        
        
