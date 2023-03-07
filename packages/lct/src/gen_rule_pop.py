"""
Code for automatically generating the rule population for the LCT
"""
#%%
import numpy as np
import pandas as pd
from statistics import mean

# conditions
min_v = 0
max_v = 5
v_step = 0.1
v_range = np.arange(min_v, max_v+v_step, v_step)            #check what all these should be

slow_v_rng = np.arange(min_v, 2)
mid_v_rng = np.arange(2, 3.5)
fast_rng = np.arange(3.5,5)

min_d = -1.5
max_d = 1.5

d_step = 0.1
d_range = np.arange(min_d, max_d+d_step, d_step) 


min_phi = -1.5
max_phi = 1.5
phi_step = 0.1
phi_range = np.arange(min_phi, max_phi+phi_step, phi_step) 

# for deciding action
inc = 0.1
good_low = -0.8
good_up = 0.8
good_phi_rng = np.arange(good_low, good_up+inc, inc)
ok_low = -1.2
ok_up = 1.2
ok_phi_rng = np.arange(ok_low, ok_up+inc, inc)

# using same boundaries for d & phi for now
good_d_rng = np.arange(good_low, good_up+inc, inc)
ok_d_rng = np.arange(ok_low, ok_up+inc, inc)
# (bad d range == d range)

# action
gain_step = 0.1
# am i using this?#########
low_gain_rng = np.arange(0.1, 0.3, gain_step)
med_gain_rng = np.arange(0.3, 0.7, gain_step)
high_gain_rng = np.arange(0.7, 1.0, gain_step)
gain_rng = np.arange(0.1, 1.1, 0.1)
###########################

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
    """
    # work on this
    ############################################################
    # if straight, high gain
    if mean((d_lower, d_upper)) in good_d_rng: #and mean((phi_lower, phi_upper)) in good_phi_rng:
        act = random_sample(high_gain_rng)
        print(f"mean: {mean((d_lower, d_upper))}")
    # if going med and straight, med  gain
    elif mean((d_lower, d_upper)) in ok_d_rng: #and mean((phi_lower, phi_upper)) in ok_phi_rng:
        act = random_sample(med_gain_rng)
    # if going squinty, low gain
    elif mean((d_lower, d_upper)) in d_range: #or mean((phi_lower, phi_upper)) in phi_range:
        act = random_sample(low_gain_rng)
    # add more
    # elif 
        # act = 
    # to cover incase if missed a case
    else:
        act = 0.5
    #############################################################
    #act = "placeholder"
    """
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
    for i in range (rules):
        next_row = makerow()
        placeholder = pd.concat([next_row, rule_pop[:]]).reset_index(drop=True)
    return placeholder
    
