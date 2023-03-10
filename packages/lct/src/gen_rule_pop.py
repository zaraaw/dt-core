"""
Code for automatically generating the rule population for the LCT
"""
#%%
import numpy as np
import pandas as pd
from statistics import mean
import os

#%%
min_v = 0.25
stop_v = 0.5
low_v = 1
max_v = 2

min_d = -0.5
d1 = -0.4               
d2 = -0.2
d3 = 0.2               
d4 = 0.4
max_d = 0.5 

min_phi = -2
phi1 = -1.6
phi2 = -0.8
phi3 = 0.8
phi4 = 1.6
max_phi = 2

#fit_list = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ]
fit_list = [16, 15, 14, 13, 12, 11, 10 ,9, 8, 7, 6, 5, 4, 3 ,2, 1]
fit_list = [0.16, 0.15, 0.14, 0.13, 0.12, 0.11, 0.1, 0.09, 0.08, 0.07, 0.06, 0.05, 0.04, 0.03, 0.02, 0.01]

def sv_rule_pop():
    sv_rule_pop = pd.DataFrame({
    "d_lower" : [min_d, d2, min_d, d4, min_d, d2, min_d, min_d, d4, min_d, min_d, d1, d3, min_d, min_d,min_d], 
    "d_upper" : [max_d, d3, d1, max_d, max_d, d3, max_d, d1, max_d, max_d, max_d, d2, d4, max_d, max_d, max_d], 
    "phi_lower" : [min_phi, phi2, min_phi, phi4, min_phi, min_phi, phi2, min_phi, min_phi, min_phi, phi4, min_phi, min_phi, phi1, phi3, min_phi],
    "phi_upper" : [max_phi, phi3, phi1, max_phi, max_phi, max_phi, phi3, max_phi, max_phi, phi1, max_phi, max_phi, max_phi, phi2, phi4, max_phi],
    "vel_lower" : [min_v, low_v, stop_v, stop_v, low_v, min_v, min_v, min_v, min_v, min_v, min_v, min_v, min_v,min_v, min_v, stop_v],
    "vel_upper" : [stop_v, max_v,low_v, low_v, max_v, max_v, max_v, max_v, max_v, max_v, max_v, max_v, max_v,  max_v, max_v, low_v],
    "act" : [1.8, 2, 1, 1, 1.5, 1.5, 1.5, 0.5, 0.5, 0.5, 0.5, 1.0, 1.0, 1.0, 1.0, 1.8],
    "fit" : fit_list,
    "in_match_set" : [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    })
    return sv_rule_pop
#sv_rule_pop = sv_rule_pop()
#%%

# conditions

v_step = 0.25
v_range = np.arange(min_v, max_v+v_step, v_step)

d_step = 0.1                      # step > std dev from baseline
d_range = np.arange(min_d, max_d+d_step, d_step) 

phi_step = 0.4
phi_range = np.arange(min_phi, max_phi+phi_step, phi_step) 

# action
gain_rng = np.arange(0.1, 1.0, 0.1)


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

