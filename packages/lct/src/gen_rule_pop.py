"""
Code for automatically generating the rule population for the LCT
"""
#%%
import numpy as np
import pandas as pd
from statistics import mean
import os

#%%
# for gain
min_v = 0.5
v1 = 1.25
v2 = 1.5
max_v = 2.0

min_d = 0
d1 = 0.075
d2 = 0.1   
max_d = 0.3

min_phi = 0
phi1 = 0.75
phi2 = 1.0
max_phi = 1.5

min_gain = 0.5
gain1 = 1.25
gain2 = 1.5
max_gain = 2.0


def sv_rule_pop():
    rules = 8
    sv_rule_pop = pd.DataFrame({
    "d_lower" : [min_d, min_d, d2, d1, d2, min_d, min_d, min_d],
    "d_upper" : [max_d, d1, max_d, d2, max_d, max_d, max_d, d1],
    "phi_lower" : [min_phi, min_phi, phi2, phi1, min_phi, min_phi, phi2, min_phi ],
    "phi_upper" : [max_phi, phi1, max_phi, phi2, max_phi, phi1, max_phi, max_phi ],
    "vel_lower" : [min_v, min_v, v2, min_v, v1, v2, v2,  min_v],
    "vel_upper" : [v1, max_v, max_v, v1, v2, max_v, max_v, v1],
    "act" : [gain2, max_gain, min_gain, gain1, min_gain, gain2, min_v, gain2],
    "fit" : [0.5] * rules,
    "in_match_set" : [0] * rules
    })
    return sv_rule_pop
# sv_rule_pop = sv_rule_pop()

#%%

# conditions

v_step = 0.25
v_range = np.arange(min_v, max_v+v_step, v_step)

d_step = 0.05                     # step > std dev from baseline
d_range = np.arange(min_d, max_d+d_step, d_step) 

phi_step = 0.15
phi_range = np.arange(min_phi, max_phi+phi_step, phi_step) 

# action
gain_step = 0.25
gain_rng = np.arange(min_gain, max_gain, gain_step)


# fitness 
fit = 0.5             # start w/ same initial fitness

rule_pop = pd.DataFrame(columns=["d_lower", "d_upper", "phi_lower", "phi_upper", "vel_lower", "vel_upper", "act", "fit", "in_match_set"])

# print(rule_pop)
    
def random_sample( arr: np.array, size: int = 1):
    return round(arr[np.random.choice(len(arr), size=size, replace=False)][0], 2) #indexing here to get a number not an array

def makerow():
    d_lower = random_sample(d_range)
    d_upper = random_sample(np.arange(d_lower, max_d+d_step, d_step))

    phi_lower = random_sample(phi_range)
    phi_upper = random_sample(np.arange(phi_lower, max_phi+phi_step, phi_step))

    vel_lower = random_sample(v_range)
    vel_upper = random_sample(np.arange(vel_lower, max_v+v_step, v_step))

    act = random_sample(gain_rng)

    next_row = pd.DataFrame({
                "d_lower" : -d_lower, 
                "d_upper" : d_upper, 
                "phi_lower" : phi_lower, 
                "phi_upper" : phi_upper,
                "vel_lower" : vel_lower,
                "vel_upper" : vel_upper, 
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
    

#rule_pop = make_rule_pop(5)
#print(rule_pop)

# os.makedirs("LCT/rule_pop", exist_ok=True)
# rule_pop.to_csv("LCT/rule_pop/rule_pop.csv"

