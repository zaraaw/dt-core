"""
This is the code for the LCT

"""
#%% 
# import libraries
import random
import copy
import math
import pandas as pd
pd.options.mode.chained_assignment = None           #silence pandas warnings
from gen_rule_pop import *
from reward import * 

# CONFIG FILE
# Configuration file (setting the variables used later)

# Parameters for LCT
###### fitness update
algo_select =  'roulette_wheel'     # 'roulette_wheel' or 'winner_takes_all'     
beta = 0.125                          # choose value
#min_v = 3                          # choose a min value
#max_v = 5                           # check max value (assuming the ROS node would give the vel in m/s)
#stop_v = 1.5                        # the speed below which would be considered stopped/crashed
reward = 0                          # initial value of reward
###### action selection
selected_rule = -1
best_fitness = 0

###### apply action
act = 1.0                            # setting initial gain
last_rule = pd.Series(dtype='float64')             # inital last_rule is empty Series

# rule_pop = make_rule_pop(500)
# rule_pop = pd.read_csv("LCT/rule_pop/rule_pop_test.csv")
rule_pop = sv_rule_pop()

# The constants class saves the variables set in the 'Configuration file' as global constants
class Constants:
    # def __init__(self):
        # self.setConstants()
    def __str__(self) -> str:                       # not sure what the -> str does but came up in autofill
        return "This is the constants class"
    def setConstants(self):
        #### LCT parameters
        self.rule_pop = rule_pop
        ## fitness update
        self.algo_select = algo_select
        self.beta = beta
        #self.min_v = min_v
        #self.max_v = max_v
        #self.stop_v = stop_v
        self.reward = reward

        ## action selection
        self.last_rule = last_rule
        self.selected_rule = selected_rule
        self.best_fitness = best_fitness
        
        ## apply action
        self.act = act

        self.counter = 0            # for debugging testing large rule pops

        # tbc
cons = Constants()
cons.setConstants()
#%%
# LCT CLASS
# LCT class contains the functions for updating fitness, action selection, and applying the action
# based on c code for implementing LCT 
class LCT:
    def __str__(self) -> str:
        return "This is the LCT class"
    #def __init__(self): 
        #cons = Constants()
        #cons.setConstants()
    def updatefitness(self, d, phi, v):
        #cons = Constants()
        #cons.setConstants()
        #print("Running fitness update")
        if cons.last_rule.empty:
            #print("No action was selected last instance")
            for i, rule in cons.rule_pop.iterrows():                # iterate through each rule 
                    #print(f"rule {i}")
                    # print(rule["in_match_set"])
                    rule["in_match_set"] = 0                        # reset in_match_set to false
                    # print(rule["in_match_set"])
        else:
            # cons.reward = 0
            cons.reward = Reward().calc_reward(d, phi, v)
                        
            for i, rule in cons.rule_pop.iterrows():             # iterate through each rule 
                if cons.rule_pop["in_match_set"][i] == 1:                   # if the value of in_match_set is True
                    if cons.rule_pop["act"][i] == cons.last_rule["act"]: 
                        #print(f"Rule {i} has been updated")
                        cons.rule_pop["fit"][i] = cons.rule_pop["fit"][i] + (beta * (cons.reward - cons.rule_pop["fit"][i]))
                        cons.rule_pop["in_match_set"][i] = 0
                    else:
                        #print(f"The action of the current rule (Rule {i}) does not equal the action of the last rule")
                        cons.rule_pop["in_match_set"][i] = 0
        #for getting out cumulative reward
        #print(f"Reward given: {cons.reward}")
        return cons.reward
                    
    def actionselection(self, d, phi, v):
        #cons = Constants()
        #cons.setConstants()
        if algo_select == 'winner_takes_all':
            for i, rule in cons.rule_pop.iterrows():             # iterate through each rule
                #print(f"Current Rule: {i}")
                rule_vel_match = rule["vel_lower"] <= v <= rule["vel_upper"]        # true if velocity in range
                #print(f'vel_lower: {rule["vel_lower"]}, vel_upper{rule["vel_upper"]}')
                rule_d_match = rule["d_lower"] <= d <= rule["d_upper"]              # true if d in range
                rule_phi_match = rule["phi_lower"] <= phi <= rule["phi_upper"]      # true if phi in range
                rule_match = rule_vel_match and rule_d_match and rule_phi_match

                if rule_match:
                    cons.rule_pop["in_match_set"][i] = 1
                    #print(f"best fit: {cons.best_fitness}, rule fit :{cons.rule_pop['fit'][i]}")
                    #print(cons.best_fitness < cons.rule_pop["fit"][i])
                    # print("best fit < rule fit")
                    
                    # print(f"Matched rule: {i}")
                    # print(f'match set:{rule["in_match_set"]}')
                    # cons.counter += 1
                    if cons.best_fitness <= cons.rule_pop["fit"][i]:         # this doesnt work 
                        
                        cons.selected_rule = i
                        cons.best_fitness = cons.rule_pop["fit"][i]
                        #print(f"best fitness: {cons.best_fitness}")
        
        elif algo_select == "roulette_wheel":
            acc_weight_list = [] 
            fitness_sum = 0
            fitness_values = []
            match_pop = []
            for i, rule in cons.rule_pop.iterrows():
                #print(f"Current Rule: {i}")
                rule_vel_match = rule["vel_lower"] <= v <= rule["vel_upper"]        # true if velocity in range
                rule_d_match = rule["d_lower"] <= d <= rule["d_upper"]              # true if d in range
                rule_phi_match = rule["phi_lower"] <= phi <= rule["phi_upper"]      # true if phi in range
                #print(f"MATCHES - v: {rule_vel_match}, d: {rule_d_match}, phi: {rule_phi_match}")
                #print(f'phi low: {rule["phi_lower"]}, phi up: {rule["phi_upper"]}')
                
                rule_match = rule_vel_match and rule_d_match and rule_phi_match

                if rule_match:                                                      # make a list of the fitnesses of the matching rules
                    #print(f"MATCH: Rule {i}")
                    cons.rule_pop["in_match_set"][i] = 1
                    #fitness_sum += rule["fit"]
                    #acc_weight_list.append(fitness_sum)
                    fitness_values.append(cons.rule_pop["fit"][i])
                    match_pop.append(i)
                    #print(f"fitness sum: {fitness_sum} & weight list: {acc_weight_list} & fitness values: {fitness_values}")
                else:
                    #acc_weight_list.append(fitness_sum)
                    pass
                  
            #print(f"matched rules: {match_pop}")
            total = sum(fitness_values) 
            norm_fitness_values = [x/total for x in fitness_values]
            cumulative_fitness = []
            start = 0
            for norm_value in norm_fitness_values:
                start += norm_value
                cumulative_fitness.append(start)

            #print(f"norm fitness values: {norm_fitness_values}, cumulative fitness: {cumulative_fitness}")

            match_pop_size = len(match_pop)
            for j in range(match_pop_size):

                random_number = random.uniform(0,1)
                #print(f"random number: {random_number}")
                for score in cumulative_fitness:
                    if(random_number <= score):

                        cons.selected_rule = match_pop[cumulative_fitness.index(score)]
                        cons.best_fitness = cons.rule_pop["fit"][cumulative_fitness.index(score)]
                        #print(f"Rule {i} has been selected")                        # only 1 should be selected here 
                        break

        #print(f"Best fitness is {cons.best_fitness} and the selected rule is {cons.selected_rule}")    
        return cons.best_fitness, cons.selected_rule 
                    
    def applyaction(self, d, phi, v):
        #cons = Constants()
        #cons.setConstants()
        if cons.selected_rule == -1:                             # no rule selected so nothing's done
            #print("No rule selected")
            cons.last_rule = pd.Series(dtype="float64")          # create empty series
        else:            
            #print(f"Selected rule: {cons.selected_rule}, gain from selected rule: {cons.rule_pop['act'][cons.selected_rule]}, current gain: {cons.act}")           # apply the action of the selected rule
            cons.act = cons.rule_pop["act"][cons.selected_rule]    # get action
            cons.last_rule = cons.rule_pop.iloc[cons.selected_rule]#.astype("float64")  # set current rule to last rule
            cons.counter += 1
        #return cons.gain   

# run LCT class
# class for running the LCT (runs the methods in the LCT class, add timing here?)
class runLCT:
    def __init__(self):
        #print("Initialize LCT algorithm")
        #...
    
        #self.run_LCT()
        pass

    def run_LCT(self, d, phi, v):
        rwd = LCT().updatefitness(d, phi, v)
        #LCT().updatefitness(d, phi, v)
        LCT().actionselection(d, phi, v)
        LCT().applyaction(d, phi, v)
        return float(cons.act), rwd
    

# for testing
print(cons.rule_pop)
reward_lst = []
for x in range(10):
    print(f"------------------- ITER {x} -------------------")
    out = runLCT().run_LCT(0.04, -0.55, 0.8)
    reward_lst.append(cons.reward)
    #print(cons.rule_pop)
    

# cons.rule_pop.iloc[114]
print("------------------- END -------------------")
print(f"Sum of rewards given: {sum(reward_lst)}")
print(cons.rule_pop)
