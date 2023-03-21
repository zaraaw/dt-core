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
min_v = 1.0
stop_v = 1.25
low_v = 1.75
max_v = 3.25
# for v (car_cmd)
# min_v = 1
# stop_v = 1.25
# low_v = 1.75
# max_v = 0.19


min_d = -0.2
d1 = -0.1               
d2 = -0.04
d3 = 0       
d4 = 0.04
max_d = 0.3

min_phi = -1.3
phi1 = -1
phi2 = -0.1
phi3 = 0
phi4 = 0.2
max_phi = 1.3

#5 levels of gain
min_gain = 1.0
gain1 = 1.5
gain2 = 2.0
gain3 = 2.5
gain4 = 2.75
max_gain = 3.25



# fit_list = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ]
# fit_list = [16, 15, 14, 13, 12, 11, 10 ,9, 8, 7, 6, 5, 4, 3 ,2, 1]
# fit_list = [0.16, 0.15, 0.14, 0.13, 0.12, 0.11, 0.1, 0.09, 0.08, 0.07, 0.06, 0.05, 0.04, 0.03, 0.02, 0.01]

def sv_rule_pop():
    rules = 17
    sv_rule_pop = pd.DataFrame({
    "d_lower" : [min_d, min_d, d2, min_d, d4,  d2, min_d, min_d, d4, min_d, min_d, d1, d3, min_d, min_d,min_d, d1], 
    "d_upper" : [max_d, max_d, d3, d1, max_d,  d3, max_d, d1, max_d, max_d, max_d, d2, d4, max_d, max_d, max_d, d4], 
    "phi_lower" : [min_phi, min_phi, phi2, min_phi, phi4,  min_phi, phi2, min_phi, min_phi, min_phi, phi4, min_phi, min_phi, phi1, phi3, min_phi, phi1],
    "phi_upper" : [max_phi, max_phi, phi3, phi1, max_phi,  max_phi, phi3, max_phi, max_phi, phi1, max_phi, max_phi, max_phi, phi2, phi4, max_phi, phi4],
    "vel_lower" : [min_v, low_v, low_v, stop_v, stop_v,  min_v, min_v, min_v, min_v, min_v, min_v, min_v, min_v,min_v, min_v, stop_v, min_v],
    "vel_upper" : [stop_v, max_v, max_v,low_v, low_v,  max_v, max_v, max_v, max_v, max_v, max_v, max_v, max_v,  max_v, max_v, low_v, max_v],
    "act" : [gain4, gain4, max_gain, gain1, gain1, gain3, gain3, gain1, gain1, gain1, gain1, gain2, gain2, gain2, gain2, gain4, gain4],
    "fit" : [0.5] * rules,
    "in_match_set" : [0] * rules
    })
    return sv_rule_pop
#sv_rule_pop = sv_rule_pop()

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
fit = 1             # start w/ same initial fitness

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

