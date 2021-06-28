import random
from pprint import pprint
import math
from copy import deepcopy
import time
import traceback

import numpy as np

from simulated_annealing import *
from constraints import *
from utils import *
from evaluation import *

def move_all_demand_constraint(result, input_data):
    updated_result = deepcopy(result)
    for d in range(input_data['length_of_schedule']):
        sum_day, sum_afternoon, sum_night = 0, 0, 0
        for e in range(input_data['number_of_employees']):
            if updated_result[e][d] == 'D': sum_day += 1
            elif updated_result[e][d] == 'A': sum_afternoon += 1
            elif updated_result[e][d] == 'N': sum_night += 1

        if sum_day >= input_data['temporal_requirements_matrix'][0][d]: pass
        else: updated_result[random.randint(0, input_data['number_of_employees']-1)][d] = 'D'
        if sum_afternoon >= input_data['temporal_requirements_matrix'][1][d]: pass
        else: updated_result[random.randint(0, input_data['number_of_employees']-1)][d] = 'A'
        if input_data['number_of_shifts'] > 2 :
            if sum_night >= input_data['temporal_requirements_matrix'][2][d]: pass
            else: updated_result[random.randint(0, input_data['number_of_employees']-1)][d] = 'N'
    return updated_result

def move_day_demand_constraint(result, input_data):
    updated_result = deepcopy(result)
    for d in range(input_data['length_of_schedule']):
        sum_day = 0
        for e in range(input_data['number_of_employees']):
            if updated_result[e][d] == 'D': sum_day += 1
        if sum_day >= input_data['temporal_requirements_matrix'][0][d]: pass
        else: 
            updated_result[random.randint(0, input_data['number_of_employees']-1)][d] = 'D'
            break
    return updated_result

def move_afternoon_demand_constraint(result, input_data):
    updated_result = deepcopy(result)
    for d in range(input_data['length_of_schedule']):
        sum_afternoon = 0
        for e in range(input_data['number_of_employees']):
            if updated_result[e][d] == 'A': sum_afternoon += 1
        if sum_afternoon >= input_data['temporal_requirements_matrix'][0][d]: pass
        else: 
            updated_result[random.randint(0, input_data['number_of_employees']-1)][d] = 'A'
            break
    return updated_result

def move_night_demand_constraint(result, input_data):
    updated_result = deepcopy(result)
    if input_data['number_of_shifts'] < 3 : return updated_result
    for d in range(input_data['length_of_schedule']):
        sum_night = 0
        for e in range(input_data['number_of_employees']):
            if updated_result[e][d] == 'N': sum_night += 1
        if sum_night >= input_data['temporal_requirements_matrix'][0][d]: pass
        else: 
            updated_result[random.randint(0, input_data['number_of_employees']-1)][d] = 'N'
            break
    return updated_result

def move_all_day_off_constraint(result, input_data):
    updated_result = deepcopy(result)
    code = input_data['shift_name'] + ['-']
    for e in range(input_data['number_of_employees']):
        count_dayoff = 0
        for d in range(input_data['length_of_schedule']):
            if updated_result[e][d] == '-': count_dayoff += 1
        if count_dayoff >= input_data['min_days_off']: pass
        else: updated_result[e][random.randint(0, input_data['length_of_schedule']-1)] = '-'
        if count_dayoff <= input_data['max_days_off']: pass
        else: updated_result[e][random.randint(0, input_data['length_of_schedule']-1)] = random.choice(list(set(code) - set('-')))            
    return updated_result

def move_min_day_off_constraint(result, input_data):
    updated_result = deepcopy(result)
    code = input_data['shift_name'] + ['-']
    for e in range(input_data['number_of_employees']):
        count_dayoff = 0
        for d in range(input_data['length_of_schedule']):
            if updated_result[e][d] == '-': count_dayoff += 1
        if count_dayoff >= input_data['min_days_off']: pass
        else: 
            updated_result[e][random.randint(0, input_data['length_of_schedule']-1)] = '-'
            break
    return updated_result

def move_max_day_off_constraint(result, input_data):
    updated_result = deepcopy(result)
    code = input_data['shift_name'] + ['-']
    for e in range(input_data['number_of_employees']):
        count_dayoff = 0
        for d in range(input_data['length_of_schedule']):
            if updated_result[e][d] == '-': count_dayoff += 1
        if count_dayoff <= input_data['max_days_off']: pass
        else: 
            updated_result[e][random.randint(0, input_data['length_of_schedule']-1)] = random.choice(list(set(code) - set('-')))
            break
        
    return updated_result

def move_all_length_work_blocks_constraint(result, input_data):
    updated_result = deepcopy(result)
    code = input_data['shift_name'] + ['-']
    for e in range(input_data['number_of_employees']):
        count_consecutive = 0
        min_flag, max_flag = False, False
        for d in range(input_data['length_of_schedule'] - 1):
            if updated_result[e][d] != '-' and updated_result[e][d+1] != '-': 
                count_consecutive += 1
                if count_consecutive >= input_data['min_length_work_blocks'] - 1:
                    min_flag = True
                    if count_consecutive <= input_data['max_length_work_blocks'] - 1:
                        max_flag = True
            else:  count_consecutive = 0
                
        if min_flag: pass
        else: 
            count_concecutive = 0
            for d in range(input_data['length_of_schedule']):
                if updated_result[e][d] == '-' and count_concecutive <= input_data['max_length_work_blocks'] - 1: 
                    updated_result[e][d] = random.choice(list(set(code) - set('-')))
                count_concecutive += 1
        if max_flag: pass
        else: updated_result[e][random.randint(0, input_data['length_of_schedule']-1)] = '-'
                
    return updated_result 

def move_min_length_work_blocks_constraint(result, input_data):
    updated_result = deepcopy(result)
    code = input_data['shift_name'] + ['-']
    
    for e in range(input_data['number_of_employees']):
        count_consecutive = 0
        min_flag, max_flag = False, False
        for d in range(input_data['length_of_schedule'] - 1):
            if updated_result[e][d] != '-' and updated_result[e][d+1] != '-': 
                count_consecutive += 1
                if count_consecutive >= input_data['min_length_work_blocks'] - 1:
                    min_flag = True
                    if count_consecutive <= input_data['max_length_work_blocks'] - 1:
                        max_flag = True
            else:  count_consecutive = 0
            
        if min_flag: pass
        else: 
            count_concecutive = 0
            for d in range(input_data['length_of_schedule']):
                if updated_result[e][d] == '-' and count_concecutive <= input_data['max_length_work_blocks'] - 1: 
                    updated_result[e][d] = random.choice(list(set(code) - set('-')))
                    return updated_result
                count_concecutive += 1
    return updated_result

def move_max_length_work_blocks_constraint(result, input_data):
    updated_result = deepcopy(result)
    code = input_data['shift_name'] + ['-']
    
    for e in range(input_data['number_of_employees']):
        count_consecutive = 0
        min_flag, max_flag = False, False
        for d in range(input_data['length_of_schedule'] - 1):
            if updated_result[e][d] != '-' and updated_result[e][d+1] != '-': 
                count_consecutive += 1
                if count_consecutive >= input_data['min_length_work_blocks'] - 1:
                    min_flag = True
                    if count_consecutive <= input_data['max_length_work_blocks'] - 1:
                        max_flag = True
            else:  count_consecutive = 0
            
        if min_flag: pass
        else: 
            count_concecutive = 0
            for d in range(input_data['length_of_schedule']):
                if updated_result[e][d] == '-' and count_concecutive <= input_data['max_length_work_blocks'] - 1: 
                    pass
                count_concecutive += 1
        if max_flag: pass
        else: 
            updated_result[e][random.randint(0, input_data['length_of_schedule']-1)] = '-'
            return updated_result
        
    return updated_result

def move_all_0_forbidden_constraint2(result, input_data):
    updated_result = deepcopy(result)
    code = input_data['shift_name'] + ['-']
    if input_data['not_allowed_shift_sequences_2'] == []: return updated_result
    if input_data['not_allowed_shift_sequences_2'] != []:
        for e in range(input_data['number_of_employees']):
            for d in range(input_data['length_of_schedule'] - 1):
                for f in input_data['not_allowed_shift_sequences_2']:
                    if updated_result[e][d] == f[0] and updated_result[e][d+1] == f[1]:
                        for c in code:
                            if [f[0], c] not in input_data['not_allowed_shift_sequences_2']:
                                updated_result[e][d+1] = c
                                break
        return updated_result
    
def move_all_1_forbidden_constraint2(result, input_data):
    updated_result = deepcopy(result)
    code = input_data['shift_name'] + ['-']
    if input_data['not_allowed_shift_sequences_2'] == []: return updated_result
    if input_data['not_allowed_shift_sequences_2'] != []:
        for e in range(input_data['number_of_employees']):
            for d in range(input_data['length_of_schedule'] - 1):
                for f in input_data['not_allowed_shift_sequences_2']:
                    if updated_result[e][d] == f[0] and updated_result[e][d+1] == f[1]:
                        for c in code:
                            if [c, f[1]] not in input_data['not_allowed_shift_sequences_2']:
                                updated_result[e][d] = c
                                break
        return updated_result
    
def move_0_forbidden_constraint2(result, input_data):
    updated_result = deepcopy(result)
    code = input_data['shift_name'] + ['-']
    move_flage = False
    if input_data['not_allowed_shift_sequences_2'] == []: return updated_result
    if input_data['not_allowed_shift_sequences_2'] != []:
        for e in range(input_data['number_of_employees']):
            for d in range(input_data['length_of_schedule'] - 1):
                for f in input_data['not_allowed_shift_sequences_2']:
                    if updated_result[e][d] == f[0] and updated_result[e][d+1] == f[1]:
                        for c in code:
                            if [f[0], c] not in input_data['not_allowed_shift_sequences_2']:
                                updated_result[e][d+1] = c
                                return updated_result
        return updated_result
    
def move_1_forbidden_constraint2(result, input_data):
    updated_result = deepcopy(result)
    code = input_data['shift_name'] + ['-']
    if input_data['not_allowed_shift_sequences_2'] == []: return updated_result
    if input_data['not_allowed_shift_sequences_2'] != []:
        for e in range(input_data['number_of_employees']):
            for d in range(input_data['length_of_schedule'] - 1):
                for f in input_data['not_allowed_shift_sequences_2']:
                    if updated_result[e][d] == f[0] and updated_result[e][d+1] == f[1]: 
                        for c in code:
                            if [c, f[1]] not in input_data['not_allowed_shift_sequences_2']:
                                updated_result[e][d] = c
                                return updated_result
        return updated_result
    
def move_all_0_forbidden_constraint3(result, input_data):
    updated_result = deepcopy(result)
    code = input_data['shift_name'] + ['-']
    if input_data['not_allowed_shift_sequences_3'] == []: return updated_result
    if input_data['not_allowed_shift_sequences_3'] != []:
        for e in range(input_data['number_of_employees']):
            for d in range(input_data['length_of_schedule'] - 2):
                for f in input_data['not_allowed_shift_sequences_3']:
                    if result[e][d] == f[0] and result[e][d+1] == f[1]                                             and result[e][d+2] == f[2]: 
                        for c in code:
                            if [c, f[1], f[2]] not in input_data['not_allowed_shift_sequences_3']:
                                updated_result[e][d] = c
                                break
                            
        return updated_result
    
def move_0_forbidden_constraint3(result, input_data):
    updated_result = deepcopy(result)
    code = input_data['shift_name'] + ['-']
    if input_data['not_allowed_shift_sequences_3'] == []: return updated_result
    if input_data['not_allowed_shift_sequences_3'] != []:
        for e in range(input_data['number_of_employees']):
            for d in range(input_data['length_of_schedule'] - 2):
                for f in input_data['not_allowed_shift_sequences_3']:
                    if result[e][d] == f[0] and result[e][d+1] == f[1]                                             and result[e][d+2] == f[2]: 
                        for c in code:
                            if [c, f[1], f[2]] not in input_data['not_allowed_shift_sequences_3']:
                                updated_result[e][d] = c
                                return updated_result
                            
        return updated_result
    
def move_all_1_forbidden_constraint3(result, input_data):
    updated_result = deepcopy(result)
    code = input_data['shift_name'] + ['-']
    if input_data['not_allowed_shift_sequences_3'] == []: return updated_result
    if input_data['not_allowed_shift_sequences_3'] != []:
        for e in range(input_data['number_of_employees']):
            for d in range(input_data['length_of_schedule'] - 2):
                for f in input_data['not_allowed_shift_sequences_3']:
                    if result[e][d] == f[0] and result[e][d+1] == f[1]                                             and result[e][d+2] == f[2]: 
                        for c in code:
                            if [f[0], c, f[2]] not in input_data['not_allowed_shift_sequences_3']:
                                updated_result[e][d] = c
                                break
                            
        return updated_result
    
def move_all_2_forbidden_constraint3(result, input_data):
    updated_result = deepcopy(result)
    code = input_data['shift_name'] + ['-']
    if input_data['not_allowed_shift_sequences_3'] == []: return updated_result
    if input_data['not_allowed_shift_sequences_3'] != []:
        for e in range(input_data['number_of_employees']):
            for d in range(input_data['length_of_schedule'] - 2):
                for f in input_data['not_allowed_shift_sequences_3']:
                    if result[e][d] == f[0] and result[e][d+1] == f[1]                                             and result[e][d+2] == f[2]: 
                        for c in code:
                            if [f[0], f[1], c] not in input_data['not_allowed_shift_sequences_3']:
                                updated_result[e][d] = c
                                break
                            
        return updated_result
    
def move_1_forbidden_constraint3(result, input_data):
    updated_result = deepcopy(result)
    code = input_data['shift_name'] + ['-']
    if input_data['not_allowed_shift_sequences_3'] == []: return updated_result
    if input_data['not_allowed_shift_sequences_3'] != []:
        for e in range(input_data['number_of_employees']):
            for d in range(input_data['length_of_schedule'] - 2):
                for f in input_data['not_allowed_shift_sequences_3']:
                    if result[e][d] == f[0] and result[e][d+1] == f[1]                                             and result[e][d+2] == f[2]: 
                        for c in code:
                            if [f[0], c, f[2]] not in input_data['not_allowed_shift_sequences_3']:
                                updated_result[e][d] = c
                                return updated_result
                            
        return updated_result
    
def move_2_forbidden_constraint3(result, input_data):
    updated_result = deepcopy(result)
    code = input_data['shift_name'] + ['-']
    if input_data['not_allowed_shift_sequences_3'] == []: return updated_result
    if input_data['not_allowed_shift_sequences_3'] != []:
        for e in range(input_data['number_of_employees']):
            for d in range(input_data['length_of_schedule'] - 2):
                for f in input_data['not_allowed_shift_sequences_3']:
                    if result[e][d] == f[0] and result[e][d+1] == f[1]                                             and result[e][d+2] == f[2]: 
                        for c in code:
                            if [f[0], f[1], c] not in input_data['not_allowed_shift_sequences_3']:
                                updated_result[e][d] = c
                                return updated_result
                            
        return updated_result
    
