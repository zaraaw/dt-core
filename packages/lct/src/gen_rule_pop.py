"""
Code for automatically generating the rule population for the LCT
"""
#%%
import numpy as np
import pandas as pd
from statistics import mean
import os

# conditions
min_v = 0.1           # fix when got better v message
max_v = 1
v_step = 0.1
v_range = np.arange(min_v, max_v+v_step, v_step)            #check what all these should be

min_d = -0.15
max_d = 0.22
d_step = 0.05
d_range = np.arange(min_d, max_d+d_step, d_step) 

min_phi = -1.36
max_phi = 0.4
phi_step = 0.03
phi_range = np.arange(min_phi, max_phi+phi_step, phi_step) 

good_phi_rng = np.arange(-0.8, -0.3+phi_step, phi_step)
ok_phi_rng = np.arange(-1.2, -0.1+phi_step, phi_step)

# action
gain_rng = np.arange(0.1, 1.0, 0.1)


# fitness 
fit = 1             # start w/ same initial fitness

rule_pop = pd.DataFrame(columns=["vel_lower", "vel_upper", "phi_lower", "phi_upper", "d_lower", "d_upper", "act", "fit", "in_match_set"])

# print(rule_pop)
    
def random_sample( arr: np.array, size: int = 1):
    return round(arr[np.random.choice(len(arr), size=size, replace=False)][0], 2) #indexing here to get a number not an array

def makerow():
    vel_lower = random_sample(v_range)
    vel_upper = random_sample(np.arange(vel_lower, max_v+v_step, v_step))

    d_lower = random_sample(d_range)
    d_upper = random_sample(np.arange(d_lower, max_d+d_step, d_step))

    phi_lower = random_sample(phi_range)
    phi_upper = random_sample(np.arange(phi_lower, max_phi+phi_step, phi_step))
    
    act = random_sample(gain_rng)

    next_row = pd.DataFrame({"vel_lower" : vel_lower,
                "vel_upper" : vel_upper, 
                "phi_lower" : phi_lower, 
                "phi_upper" : phi_upper, 
                "d_lower" : -d_lower, 
                "d_upper" : d_upper, 
                "act" : act, 
                "fit" : fit, 
                "in_match_set":0}, index=[0])
    return next_row

# print(makerow())



def make_rule_pop(rules):
    temp = pd.DataFrame(columns=["vel_lower", "vel_upper", "phi_lower", "phi_upper", "d_lower", "d_upper", "act", "fit", "in_match_set"])
    for i in range (rules):
        next_row = makerow()
        temp = pd.concat([next_row, temp[:]]).reset_index(drop=True)
    return temp
    
